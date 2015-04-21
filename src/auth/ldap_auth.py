__author__ = 'davidl'

import os
import ldap3
from tornado.options import options
from ldap3 import Server, Connection

from utils import get_logger, get_mongodb_connection


class LdapAuth(object):
    """
    Authentication with LDAP/Active Directory
    """

    def __init__(self):
        self.connection = get_mongodb_connection()
        self._db = self.connection[options.auth_db]
        self.logger = get_logger('auth')


    def auth_user(self, username, password):
        """
        Authenticate a user with username password
        :param username:
        :param password:
        :return:
        {
            status:0 = ok,  any other number indicating an error
            error:'describe the error to the user'
            debug:'debug information to be used during development'
            data: True/False : True valid username password, False - user name password ok
        }
        """
        status = 0
        error = ''
        debug = ''
        data = True


        server = Server(options.active_directory_server)
        connection = Connection(server, user=options.active_directory_username,
                                password=options.active_directory_password,
                                auto_bind=ldap3.AUTO_BIND_NO_TLS, authentication=ldap3.AUTH_SIMPLE)
        with connection:
            if not connection.search(options.active_directory_search_def, '(sAMAccountName={})'.format(username),
                                     ldap3.SEARCH_SCOPE_WHOLE_SUBTREE, attributes=ldap3.ALL_ATTRIBUTES):
                debug = 'Error Connecting to active directory server'
                status = -2
                data = False
            else:
                try:
                    c2 = Connection(server, user=connection.response[0]['dn'], password=password,
                                    auto_bind=ldap3.AUTO_BIND_NO_TLS,
                                    authentication=ldap3.AUTH_SIMPLE)
                except ldap3.core.exceptions.LDAPBindError as e:
                    debug = str(e)
                    data = False
                    status = -1
                    error = 'Wrong username/password'

        return {'status': status,
                'error': error,
                'debug': debug,
                'data': data}

    def user_permission(self, username, action):
        """
        Checks if user has permission to do certain action
        :param username:
        :param action:
        :return: a dictionary with the following format
         {
            status: 0 = ok,  any other number indicating an error
            error:'describe the error to the user'
            debug:'debug information to be used during development'
            data: True/False : True user has permission for action, False - user has no permission for action
        }
        """
        raise NotImplementedError('user_permission must be implemented')