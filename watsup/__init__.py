"""Configures and starts the web server.
"""

from flask import Flask, g, session as flask_session, render_template

from flask.ext.sqlalchemy import SQLAlchemy

from watsup.config import config


app = Flask(__name__,
            static_url_path='%s/static' % config.get('url', 'base'),
            static_folder='static')


# Database connection
# ----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:3306/%s' % (
    config.get('db', 'user'),
    config.get('db', 'passwd'),
    config.get('db', 'host'),
    config.get('db', 'db')
)
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800 # Recycle every 30 min.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


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


# Error handling
# ----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests.
    """
    return render_template('404.html')

