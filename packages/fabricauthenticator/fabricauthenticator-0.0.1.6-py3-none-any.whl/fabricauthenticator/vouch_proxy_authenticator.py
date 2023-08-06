#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author Komal Thareja (kthare10@renci.org)
import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from tornado import gen, web
from traitlets import Unicode
from ldap3 import Connection, Server, ALL
import jwt
import json
import requests


JUPYTERHUB_COU = os.getenv('FABRIC_COU_JUPYTERHUB', 'CO:COU:Jupyterhub:members:active')
CILOGON_JWKS_URL = os.getenv('CILOGON_JWKS_URL')


class VouchProxyLoginHandler(BaseHandler):
    isMemberOf = 'isMemberOf'

    async def get(self):
        user_name = self.request.headers.get(self.authenticator.user_header_name, "")
        if user_name == "":
            self.log.error("Missing User Name")
            raise web.HTTPError(401)

        id_token = self.request.headers.get(self.authenticator.id_token_header_name, "")
        if id_token == "":
            self.log.error("Missing Identity Token")
            raise web.HTTPError(401)

        if not self.verify_id_token(id_token=id_token):
            raise web.HTTPError(403, "Signature has expired")

        refresh_token = self.request.headers.get(self.authenticator.refresh_token_header_name, "")
        #if refresh_token == "":
        #    self.log.error("Missing Refresh Token")
        #    raise web.HTTPError(401)

        cookie = self.request.headers.get(self.authenticator.cookie_header_name, "")
        if cookie == "":
            self.log.error("Missing Vouch Cookie")
            raise web.HTTPError(401)

        if not self.is_in_allowed_cou(user_name):
            self.log.warn("FABRIC user {} is not in {}".format(user_name, JUPYTERHUB_COU))
            raise web.HTTPError(403, "Access not allowed")

        userdict = {"name": user_name}
        userdict["auth_state"] = auth_state = {}
        auth_state['id_token'] = id_token
        auth_state['refresh_token'] = refresh_token
        auth_state['cookie'] = cookie
        await self.auth_to_user(authenticated=userdict)

        user = self.user_from_username(user_name)
        self.set_login_cookie(user)
        next_url = self.get_next_url(user)
        self.redirect(next_url)

    def is_in_allowed_cou(self, username):
        """ Checks if user is in Comanage JUPYTERHUB COU.

            Args:
                username: i.e. ePPN

            Returns:
                Boolean value: True if username has attribute of JUPYTERHUB_COU, False otherwise
        """
        attributelist = self.get_ldap_attributes(username)
        if attributelist:
            self.log.debug("attributelist acquired.")
            if attributelist[self.isMemberOf]:
                for attribute in attributelist[self.isMemberOf]:
                    if attribute == JUPYTERHUB_COU:
                        return True
        return False

    @staticmethod
    def get_ldap_attributes(username):
        """ Get the ldap attributes from Fabric CILogon instance.

            Args:
                username: i.e. ePPN

            Returns:
                The attributes list
        """
        server = Server(os.getenv('LDAP_HOST', ''), use_ssl=True, get_info=ALL)
        ldap_user = os.getenv('LDAP_USER', '')
        ldap_password = os.getenv('LDAP_PASSWORD', '')
        ldap_search_base = os.getenv('LDAP_SEARCH_BASE', '')
        ldap_search_filter = '(mail=' + username + ')'
        conn = Connection(server, ldap_user, ldap_password, auto_bind=True)
        profile_found = conn.search(ldap_search_base,
                                    ldap_search_filter,
                                    attributes=[
                                        'isMemberOf',
                                    ])
        if profile_found:
            attributes = conn.entries[0]
        else:
            attributes = []
        conn.unbind()
        return attributes

    def verify_id_token(self, id_token):
        """
        verify signature and expiration date

        @param id_token: identity token
        """
        try:
            response = requests.get(CILOGON_JWKS_URL)
            if response.status_code != 200:
                return
            jwks = response.json()
            public_keys = {}
            for jwk in jwks['keys']:
                kid = jwk['kid']
                public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

            kid = jwt.get_unverified_header(id_token)['kid']
            key = public_keys[kid]

            options = {'verify_aud': False}
            claims = jwt.decode(id_token, key=key, verify=True, algorithms=['RS256'], options=options)
            self.log.debug("Decoded Identity Token %s", json.dumps(claims))
            return True
        except Exception as ex:
            self.log.error(ex)

        return False


class VouchProxyAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the X-Vouch-User HTTP header.
    """
    user_header_name = Unicode(
        default_value='X-Vouch-User',
        config=True,
        help="""HTTP header to inspect for the authenticated User.""")

    id_token_header_name = Unicode(
        default_value='X-Vouch-IdP-IdToken',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Identity Token.""")

    refresh_token_header_name = Unicode(
        default_value='X-Vouch-IdP-RefreshToken',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Refresh Token.""")

    cookie_header_name = Unicode(
        default_value='Cookie',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Refresh Token.""")

    def get_handlers(self, app):
        return [
            (r'/login', VouchProxyLoginHandler),
        ]

    async def pre_spawn_start(self, user, spawner):
        """ Populate credentials to spawned notebook environment
        """
        auth_state = await user.get_auth_state()
        self.log.debug("pre_spawn_start: {}".format(user.name))
        self.log.debug("pre_spawn_start: {}".format(auth_state))
        if not auth_state:
            self.log.debug("No Auth State found for user: {}".format(user.name))
            return
        spawner.environment['CILOGON_ID_TOKEN'] \
            = auth_state.get('id_token', '')
        spawner.environment['CILOGON_REFRESH_TOKEN'] \
            = auth_state.get('refresh_token', '')
        spawner.environment['VOUCH_COOKIE'] \
            = auth_state.get('cookie', '')

    async def refresh_user(self, user, handler=None):
        """ Force refresh of auth prior to spawn
        (based on setting c.Authenticator.refresh_pre_spawn = True)
        to ensure that user get a new refresh token.
        """
        self.log.debug("[refresh_user] always trigger refresh authentication")
        await handler.stop_single_user(user, user.spawner.name)
        handler.clear_cookie("jupyterhub-hub-login")
        handler.clear_cookie("jupyterhub-session-id")
        handler.redirect('/hub/logout')
        return True

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class VouchProxyLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    user_header_name = Unicode(
        default_value='X-Vouch-User',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    id_token_header_name = Unicode(
        default_value='X-Vouch-IdP-IdToken',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Identity Token.""")

    refresh_token_header_name = Unicode(
        default_value='X-Vouch-IdP-RefreshToken',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Refresh Token.""")

    cookie_header_name = Unicode(
        default_value='Cookie',
        config=True,
        help="""HTTP header to inspect for the authenticated user's Refresh Token.""")

    def get_handlers(self, app):
        return [
            (r'/login', VouchProxyLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()