__author__ = 'davidl'

import pymongo
from tornado.options import options
import logging

mongodb_connection = False


def get_mongodb_connection():
    global mongodb_connection
    if not mongodb_connection:
        try:
            mongodb_connection = pymongo.MongoClient(options.mongodb)
        except Exception as e:
            print('connection failed')
            print(e)
    return mongodb_connection


def get_logger(name=None):
    if name:
        return logging.getLogger(name)
    else:
        return logging.getLogger()


def import_class(cl):
    print(cl)
    d = cl.rfind(".")
    class_name = cl[d + 1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [class_name])
    return getattr(m, class_name)


def get_driver(class_path):
    """
    imports a driver with class path
    :param class_path:
    :return:
    """
    klass =  import_class(class_path)
    return klass()
