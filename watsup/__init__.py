"""Configures and starts the web server.
"""

from flask import Flask, render_template

from flask_pymongo import PyMongo

from watsup.config import config


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')


# Database connection
# ----------------------------------------------------------------------------
app.config['MONGO_URI'] = config.get('db', 'MONGODB_URI')
mongo = PyMongo(app)


if config.getboolean('mode', 'debug'):
    # Add a trailing slash, so the base tag URL will be "/watsup/"
    app.config.base_tag_url = '%s/' % config.get('url', 'base')
else:
    # Manually set the base tag URL to "/watsup/". Why can't we use the config
    # value? Because in production, the application runs on the server in the
    # `watsup` directory. To the application in production, "/" is this
    # directory, so "/watsup" would result in a URL mapping to
    # "/watsup/watsup". Yes, this is annoying.
    app.config.base_tag_url = '/watsup/'


# Server endpoints
# ----------------------------------------------------------------------------

from watsup import endpoints
app.register_blueprint(endpoints.index)
app.register_blueprint(endpoints.auth)
app.register_blueprint(endpoints.register)
app.register_blueprint(endpoints.login)


# Error handling
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests.
    """
    return render_template('404.html')

