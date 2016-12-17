"""Handles application-wide configurations.
"""

from ConfigParser import ConfigParser

import os


config = ConfigParser()
config.read('watsup/config.ini')

# Read MONGODB_URI and set to configuration object. We use this name because it
# is the default environment variable on Heroku.
config.set('db', 'MONGODB_URI', os.environ.get('MONGODB_URI'))
