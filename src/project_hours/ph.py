__author__ = 'davidl'

import os
from tornado.options import options, define, parse_config_file
from ate_logger import AteLogger

class ProjectHours(object):
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
