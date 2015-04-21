"""mock_auth.py

An auth driver when you are not connected to the network
"""
from src.utils import get_logger


class MockAuth(object):
    """
    Authentication with LDAP/Active Directory
    """

    def __init__(self):
        self.logger =  get_logger('auth')

    def auth_user(self, username, password):
        """
        Authenticate a user with username password
        :param username:
        :param password:
        :return: all login will succeed

        """
        status = 0
        error = ''
        debug = ''
        data = True

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
        status = 0
        error = ''
        debug = ''
        data = []
        return {'status': status,
                'error': error,
                'debug': debug,
                'data': data}