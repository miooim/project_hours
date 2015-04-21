import datetime
import pprint

__author__ = 'davidl'

from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from src.project_hours.driver.mongo_driver import ProjectHoursMongoDriver
from src.admin.drivers.projects import ProjectsManager

class ProjectHoursHandler(BaseHandler):
    """

    """
    def initialize(self):
        """

        :param db: pymongo database instance
        :param dut_configuration_manager:
        :param logger:
        """
        # self.tse_setup_driver = tse_setup_driver
        # self.logger = logger
        pass

    def get(self):
        """
        Get implementation
        :return:
        :rtype:
        """
        status = 0
        error = ''
        debug = ''

        month = self.get_argument('month', None)
        year = self.get_argument('year', None)
        group = self.get_argument('group', None)
        username = self.get_current_user()

        if group:
            data = ProjectsManager.load_projects()
            if data is None:
                status = -10
                error = 'No projects found, ask admin for assistance'
                debug = 'Probably system is new...'
                data = None
            else:
                status = 0
                error = ''
                debug = ''
                data = data
            self.write(dumps({
                'status': status,
                'error': error,
                'debug': debug,
                'data': data
            }))
            return

        if (month is None) or (year is None):
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
        else:
            if  (0 < int(month) < 13) is False:
                status = -20
                error = 'Wrong month input parameter {} should be 1 <= month <= 12'.format(month)
                debug = 'Check web API'
                self.write(dumps({
                    'status': status,
                    'error': error,
                    'debug': debug,
                    'data': None
                }))
                return

        if username is None:
            status = -10
            error = 'Probably not logged in...'
            debug = ''
            data = None
            self.write(dumps({
                'status': status,
                'error': error,
                'debug': debug,
                'data': data
            }))
            return
        else:
            data = ProjectHoursMongoDriver.get_month_data(month, year, user=username)
            self.write(dumps({
                'status': status,
                'error': error,
                'debug': debug,
                'data': data
            }))
            return

    def put(self):
        """
        Put implementation
        :return:
        """
        status = -10
        error = 'No save success'
        debug = 'Have no idea why this would happen, check mongod!'
        data = None

        body = loads(self.request.body.decode("utf-8"))
        month = self.get_argument('month', None)
        year = self.get_argument('year', None)
        username = self.get_current_user()

        # print("Got:", month, year, username)
        # pprint.pprint(body)
        if month and year and username:
            data = ProjectHoursMongoDriver.save(month, year, username, body)
            if data:
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