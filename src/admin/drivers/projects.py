__author__ = 'michaell'


import pprint
import datetime
import pymongo
from tornado.options import options

class ProjectsManager(object):
    """
    Projects manager for projects hours app
    """
    @staticmethod
    def load_projects(group_name='the_group'):
        """
        Tries to find project in database
        :return:
        :rtype:
        """
        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name]['projects']
        result = collection.find_one({
            '_id': group_name
        })
        if result:
            return result['projects']

        return None

    @staticmethod
    def save_projects(data, user, group_name='the_group'):
        """
        Tries to find project in database
        :param data:
        :return:
        :rtype:
        """
        verdict = True
        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name]['projects']
        to_save = {
            "_id": group_name,
            'projects': data,
            'last_save': datetime.datetime.now(),
            'user': user
        }
        result = collection.save(to_save)
        if result != group_name:
            verdict = False
        return verdict