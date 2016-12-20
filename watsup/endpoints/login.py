"""Serves login page.
"""

from flask import Blueprint, render_template, request, escape, jsonify

from watsup.config import config
from watsup import mongo

login = Blueprint('login',
                  __name__,
                  url_prefix='%s/login' % config.get('url', 'base'))


@login.route('/', methods=['GET', 'POST'])
def login_user():
    """Renders login page and handles login request.
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        required_fields = ['username', 'password']

        if request.json:
            for field in required_fields:
                if not field in request.json:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.json['username'])
            
            # NOTE(tfs,2016/12/19): Just storing raw data for now,
            #                       still not entirely sure how formats will work out.
            user_otp = request.json['password']
        elif request.form:
            for field in required_fields:
                if not field in request.form:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.form['username'])
            user_otp = request.form['password']

        else:
            return jsonify({'Error': 'Poorly formed request'}), 400

        users_by_name = mongo.db.users.find({'username': user_name})
        users = mongo.db.users.find({'username': user_name, 'password': user_otp})

        user_name_list = list(users_by_name)
        user_list = list(users)

        if len(user_name_list) == 0:
            return jsonify({'Error': 'User not registered'}), 401 # Status UNAUTHORIZED
        elif len(user_list) == 0:
            return jsonify({'Error': 'Bad username/password combination'}), 401
        else:
            return jsonify('Temporary confirmation page'), 200
