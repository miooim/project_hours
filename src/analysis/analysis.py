import pprint

__author__ = 'davidl'

import pymongo
from tornado.options import options


class Analysis(object):
    """
    Authentication with LDAP/Active Directory
    """

    def __init__(self, logger):
        """
        Class constructor
        :param logger: a logging instance
        :type logger: AteLogger
        """
        self.__logger = logger

    @staticmethod
    def __get_results_by_day(date_from, date_to):
        """
        Retrieves results from database using filter...
        :param date_from: date from
        :type date_from: datetime.datetime
        :param date_to: date to
        :type date_to: datetime.datetime
        :return: results list
        :rtype: list
        """
        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name][options.mongod_name]

        pipeline = [
            {
                '$match': {
                    'month': {'$gte': date_from.month, '$lte': date_to.month},
                    'year': {'$gte': date_from.year, '$lte': date_to.year}
                },
            },
            {
                '$sort': {'month': 1}
            }
        ]
        result = collection.aggregate(pipeline)
        days = []
        if result['result']:
            for month in result['result']:
                for day in month['days']:
                    if month['year'] == date_from.year:
                        if month['month'] == date_from.month:
                            if day['number'] < date_from.day:
                                continue
                    if month['year'] == date_to.year:
                        if month['month'] == date_to.month:
                            if day['number'] > date_to.day:
                                continue

                    day['month'] = month['month']
                    day['year'] = month['year']
                    day['user'] = month['user']
                    day.pop('project', None)

                    days.append(day)
        return days

    @staticmethod
    def get_results_by_day(date_from, date_to):
        """
        Retrieves results from database using filter...
        :param date_from: date from
        :type date_from: datetime.datetime
        :param date_to: date to
        :type date_to: datetime.datetime
        :return: results list
        :rtype: list
        """
        result = Analysis.__get_results_by_day(date_from, date_to)
        days = []
        for item in result:
            if item['total'] != 0:
                item.pop('projects', None)
                item.pop('no_work', None)
                days.append(item)
        return days

    @staticmethod
    def get_results_by_project(date_from, date_to):
        """
        Retrieves results from database using filter...
        :param date_from: date from
        :type date_from: datetime.datetime
        :param date_to: date to
        :type date_to: datetime.datetime
        :return: results list
        :rtype: list
        """
        result = Analysis.__get_results_by_day(date_from, date_to)
        projects = {}
        for item in result:
            for project in item['projects']:
                if project['name']['name'] in projects:
                    projects[project['name']['name']] += project['hours']
                else:
                    projects[project['name']['name']] = project['hours']

        prj_list = []
        for key, value in projects.items():
            prj_list.append({
                'project': key,
                'total': value
            })

        return prj_list
