"""Serves index page.
"""

from flask import Blueprint, render_template

from watsup.config import config


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    """Renders index page.
    """
    return render_template('index.html')