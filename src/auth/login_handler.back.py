__author__ = 'davidl'
from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from tornado.options import options

class LoginHandler(BaseHandler):
    def user_permissions(self, user):
        """
        Get a list of actions the user can perform
        :param user: a mongo user document
        :return:
        """

        return []

    def post(self):
        """
        Post action is used for login
        Expecting username password in request body
        :return:
        """
        body = loads(self.request.body.decode("utf-8"))
        try:
            username = body['username']
            password = body['password']

        except:
            self.write({'status': -2,
                        'error': 'User or password are missing',
                        'user': None,
                        'debug': ''})
            return

        self.set_cookie(options.auth_cookie_name, username)
        self.write({'status': 0,
                    'error': '',
                    'user': username,
                    'debug': ''})


    def put(self):
        self.write(dumps({'status': 0}))
        self.clear_cookie(options.auth_cookie_name)

