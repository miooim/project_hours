"""app.py


main application
"""
import os
import config

from tornado.options import options
from tornado import ioloop, web
from urls import url_handlers

app = web.Application( url_handlers,
                      static_path=os.path.join(os.path.dirname(__file__),  '..'),
                      autoreload=True
)

if __name__ == '__main__':
    print('application running on http://localhost:{}/'.format(options.app_port))
    app.listen(options.app_port, xheaders=True)
    ioloop = ioloop.IOLoop.instance()
    ioloop.start()
