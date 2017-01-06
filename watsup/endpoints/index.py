""" Serves index page """

from flask import Blueprint, render_template, jsonify
from watsup.config import config
from watsup import mongo


index = Blueprint('index',
                  __name__,
                  url_prefix=config.get('url', 'base'))


@index.route('/', methods=['GET'])
def index_page():
    """ Renders index page """
    users = mongo.db.users.find({})
    return render_template('index.html', data=list(users))


@index.route('/status/', methods=['GET'])
def watsup_status():
	"""
    For now, always responds with 'logged out'
		Verifies that server is running WATSUP protocol
	"""

	return jsonify("Logged out"), 200
