from src.base_handler import BaseHandler
from tornado.options import options

class HomeHandler(BaseHandler):
    def get(self):
        self.render('web/index.html', auth_cookie_name=options.auth_cookie_name)
