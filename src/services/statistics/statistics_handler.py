import pprint

__author__ = 'davidl'

from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from drivers.statistics import Statistics
from tornado.options import options


class StatisticsHandler(BaseHandler):
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
        function = self.get_argument('function', None)
        month = int(self.get_argument('month', None))
        year = int(self.get_argument('year', None))
        group = self.get_argument('group', None)
        username = self.get_current_user()


        if username is None:
            self.write(dumps({
                'status': -10,
                'error': 'No user name!!!',
                'debug': 'Probably not logged in',
                'data': ''
            }))
            return

        if function == 'month_statistics':
            result = Statistics.month_statistics(month, year, username)
            if result:
                status = 0
                error = ''
                debug = ''
                data = result
            else:
                status = 10
                error = ''
                debug = 'No results found for this month'
                data = None
        elif function == 'half_year_statistics':
            result = Statistics.half_year_statistics(month, year, username)
            if result:
                status = 0
                error = ''
                debug = ''
                data = result
            else:
                status = 10
                error = ''
                debug = 'No results found for this month'
                data = None

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

        # result = ProjectsManager.save_projects(body, user=self.get_current_user())
        # if result is True:
        #     status = 0
        #     error = ''
        #     debug = ''
        #     data = True

        self.write(dumps({
            'status': status,
            'error': error,
            'debug': debug,
            'data': data
        }))
