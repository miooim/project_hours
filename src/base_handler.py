
from tornado import web
from tornado.options import options

class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_cookie(options.auth_cookie_name)

    def has_permission(self, user, action):
        return True