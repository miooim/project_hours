import datetime
import pprint

__author__ = 'davidl'

from src.base_handler import BaseHandler
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from src.project_hours.driver.mongo_driver import ProjectHoursMongoDriver
from analysis import Analysis

class AnalysisHandler(BaseHandler):
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

        d_from = self.get_argument('from', None)
        d_to = self.get_argument('to', None)
        function = self.get_argument('function', None)
        if function == 'by_day':
            if d_from and d_to:
                data = Analysis.get_results_by_day(datetime.datetime.strptime(d_from, '%d %b %Y'),
                                            datetime.datetime.strptime(d_to, '%d %b %Y'))
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
        elif function == 'by_project':
            if d_from and d_to:
                data = Analysis.get_results_by_project(datetime.datetime.strptime(d_from, '%d %b %Y'),
                                            datetime.datetime.strptime(d_to, '%d %b %Y'))
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

