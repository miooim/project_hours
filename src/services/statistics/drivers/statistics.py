import pprint
import datetime

__author__ = 'michaell'

import pymongo
from tornado.options import options


class Statistics(object):
    """
    Projects manager for projects hours app
    """

    @staticmethod
    def half_year_statistics(month, year, user):
        """
        Tries to find project in database
        :return:
        :rtype:
        """
        sweep = [5, 4, 3, 2, 1, 0]
        stats = {}
        series = []
        labels = []
        for i in sweep:
            if month - i < 1:
                m = 12 + (month - i)
                y = year - 1
            else:
                m = month - i
                y = year
            result = Statistics.month_statistics(m, y, user)
            labels.append("{}/{}".format(m, y))
            if result:
                for i, item in enumerate(result['labels']):
                    if item not in series:
                        if item is not None:
                            series.append(item)
                    if item not in stats:
                        stats[item] = [{
                            "{}/{}".format(m, y): result['hours'][i]
                        }]
                    else:
                        stats[item].append({"{}/{}".format(m, y): result['hours'][i]})
        values = []
        for _ in series:
            values.append([])

        update = False
        for i, label in enumerate(labels):
            for k, seria in enumerate(series):
                for item in stats[seria]:
                    if label in item:
                        values[k].append(item[label])
                        update = True
                if update:
                    update = False
                else:
                    values[k].append(0)

        return {
            'labels': labels,
            'series': series,
            'values': values
        }

    @staticmethod
    def month_statistics(month, year, user):
        """
        Tries to find project in database
        :return:
        :rtype:
        """
        collection = pymongo.MongoClient(host=options.mongodb)[options.mongod_name][options.mongod_name]

        pipeline = [
            {
                '$match': {
                    'year': year, 'month': month, 'user': user
                }
            },
            {
                '$unwind': "$days"
            },
            {
                '$group': {
                    '_id': "$days.project.name",
                    'hours': {"$sum": "$days.total"}
                }
            }
        ]
        result = collection.aggregate(pipeline)
        if len(result['result']) == 0:
            return None
        label = []
        hours = []
        for item in result['result']:
            if item['_id'] is not None:
                label.append(item['_id'])
                hours.append(item['hours'])

        return {
            'labels': label,
            'hours': hours,
        }
