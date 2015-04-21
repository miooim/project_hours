__author__ = 'davidl'

from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from src.utils import get_logger, get_mongodb_connection, get_driver
from tornado.options import options


class LoginHandler(BaseHandler):
    def initialize(self):
        self.connection = get_mongodb_connection()
        self._db = self.connection[options.auth_db]
        self.logger = get_logger('auth')
        self.auth_driver = get_driver(options.auth_driver)

    def user_permissions(self, user):
        """
        Get a list of actions the user can perform
        :param user: a mongo user document
        :return:
        """
        try:
            user_groups = user['groups']
        except:
            return []
        groups = self._db['groups'].find({'_id': {'$in': user_groups}})
        print(groups)
        ret = []
        for g in groups:
            for action in g['actions']:
                ret.append(action)

        return ret

    def get(self):
        username = self.get_current_user()
        if not username:
            self.write(dumps({
                'status': -1,
                'error': 'user is not logged in',
                'debug': '',
                'data': []
            }))
            return
        user = self._db['users'].find_one({'username': username})
        print(user)
        perms = self.user_permissions(user)

        self.write(dumps({
            'status': 0,
            'error': '',
            'debug': '',
            'data': perms
        }))


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
        auth = self.auth_driver.auth_user(username, password)
        print (auth)
        if auth['data']:
            user = self._db['users'].find_one({'username': username})
            if not user:
                oid = ObjectId()
                self._db['users'].insert({'_id': str(oid), 'username': username, 'groups': [], 'is_new': True})
                user = self._db['users'].find_one({'_id': username})
            self.set_cookie(options.auth_cookie_name, username)
            auth['permission'] = self.user_permissions(user)
            self.write(dumps(auth))
            self.finish()
        else:
            self.write(dumps(auth))
            self.finish()

    def put(self):
        self.write(dumps({'status': 0}))
        self.clear_cookie(options.auth_cookie_name)


