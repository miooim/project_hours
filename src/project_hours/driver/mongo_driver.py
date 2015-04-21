import datetime
import pprint

__author__ = 'michaell'

import pymongo
from tornado.options import options


class ProjectHoursMongoDriver(object):
    """
    Project hours mongo driver implementation
    """
    @staticmethod
    def get_month_data(month, year, user):
        """
        Get results from database
        :param month: month
        :type month: int
        :param year: year
        :type year: int
        :param user: user name
        :type user: str
        :return: result dictionary
        :rtype: dict
        """
        query = {
            "$query": {
                'month': int(month),
                'year': int(year),
                'user': user
            }
        }
        # print(options.mongodb, options.mongod_name, options.mongod_name)
        # pprint.pprint(query)
        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name][options.mongod_name]
        return collection.find_one(query)

    @staticmethod
    def save(month, year, user, data):
        """
        Saves data to mongod
        :param month: month
        :type month: int
        :param year: year
        :type year: int
        :param user: user name
        :type user: str
        :param data: data to save
        :type data: dict
        :return: true is success
        :rtype: bool
        """

        for item in data:
            if 'no_work' in item:
                if item['no_work'] is True:
                    item['projects'] = []
                    item['total'] = 0

        result = ProjectHoursMongoDriver.get_month_data(month, year, user)
        if result:
            to_save = {
                '_id': result['_id'],
                'month': int(month),
                'year': int(year),
                'user': user,
                "days": data,
                "timestamp": datetime.datetime.now(),
            }
        else:
            to_save = {
                'month': int(month),
                'year': int(year),
                'user': user,
                "days": data,
                "timestamp": datetime.datetime.now(),
            }

        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name][options.mongod_name]
        return collection.save(to_save=to_save, safe=True)
