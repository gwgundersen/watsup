"""Handles application-wide configurations.
"""


from ConfigParser import ConfigParser

import os


config = ConfigParser()
config.read('watsup/config.ini')

# db_connection_args = {
#     'user': config.get('db', 'user'),
#     'passwd': config.get('db', 'passwd'),
#     'db': config.get('db', 'db'),
#     'host': config.get('db', 'host')
# }

MONGO_URL = os.environ.get('WATSUP_MONGO_URL')
