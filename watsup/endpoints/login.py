""" Serves login page """

from flask import Blueprint, render_template, request, escape, jsonify
from watsup.config import config
from watsup import mongo

login = Blueprint('login',
                  __name__,
                  url_prefix='%s/login' % config.get('url', 'base'))


@login.route('/', methods=['GET', 'POST'])
def login_user():
    """ Renders login page and handles login request """
   
    # GET request: render login HTML page
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST request: validates provided user credentials
    else:
        required_fields = ['username', 'password']

        # Parse paramaters if they were sent as JSON data
        if request.json:
            for field in required_fields:
                if not field in request.json:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.json['username'])
            user_otp = request.json['password']
        
        # Parse parameters if they were sent from HTML form
        elif request.form:
            for field in required_fields:
                if not field in request.form:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.form['username'])
            user_otp = request.form['password']

        # Respond to login request without credentials
        else:
            return jsonify({'Error': 'Poorly formed request'}), 400

        # Lookup and validate user based on provided credentials
        users_by_name = mongo.db.users.find({'username': user_name})
        users = mongo.db.users.find({'username': user_name, 'password': user_otp})

        user_name_list = list(users_by_name)
        user_list = list(users)

        # If no user found with provided username, reject login attempt
        if len(user_name_list) == 0:
            return jsonify({'Error': 'User not registered'}), 401 # Status UNAUTHORIZED

        # If no user found with provided username/password pair, reject login attempt
        elif len(user_list) == 0:
            return jsonify({'Error': "Bad user/pass combination"}), 401
        
        # If user found with correct username/password pair, log in user
        else:
            return jsonify('Logged In'), 200
