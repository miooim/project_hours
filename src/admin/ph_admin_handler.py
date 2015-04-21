__author__ = 'davidl'

from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from admin.drivers.projects import ProjectsManager
from tornado.options import options


class ProjectHoursAdminHandler(BaseHandler):
    """
    Project hours admin handler
    """
    def initialize(self):
        pass

    def get(self):
        """
        get implementation
        :return:
        :rtype:
        """
        status = 0
        error = ''
        debug = ''
        data = None

        result = ProjectsManager.load_projects()
        if result:
            data = result
        else:
            data = None
            status = -10
            error = "Can't find projects in database"
            debug = "Could be OK if database is new or cleaned up"

        self.write(dumps({
            'status': status,
            'error': error,
            'debug': debug,
            'data': data
        }))

    def put(self):
        """
        put implementation
        :return:
        :rtype:
        """
        status = -10
        error = 'Save failed for some reason'
        debug = 'Have no idea why this would happen, check mongod!'
        data = None

        body = loads(self.request.body.decode("utf-8"))

        result = ProjectsManager.save_projects(body, user=self.get_current_user())
        if result is True:
            status = 0
            error = ''
            debug = ''
            data = True

        self.write(dumps({
            'status': status,
            'error': error,
            'debug': debug,
            'data': data
        }))
