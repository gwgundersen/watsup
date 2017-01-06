""" Handles user/public key registration """

from flask import Blueprint, render_template, escape, request, jsonify
from watsup.config import config
from watsup import mongo


register = Blueprint('register',
                     __name__,
                     url_prefix='%s/register' % config.get('url', 'base'))


@register.route('/', methods=['GET', 'POST'])
def register_user():
    """ Render user registration page and handle user registration """
    
    # GET request: render registration HTML page
    if request.method == 'GET':
        return render_template('register.html')

    # POST request: if new user is not duplicate, save credentials
    else:
        required_fields = ['username', 'public_key']

        # Parse paramaters if they were sent as JSON data
        if request.json:
            for field in required_fields:
                if not field in request.json:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.json['username'])
            user_key = request.json['public_key']
        
        # Parse parameters if they were sent from HTML form
        elif request.form:
            for field in required_fields:
                if not field in request.form:
                    return jsonify({'Error': 'Poorly formed request'}), 400 # Status BAD

            user_name = escape(request.form['username'])
            user_key = request.form['public_key']

        # Reject request if no credentials were provided
        else:
            return jsonify({'Error': 'Poorly formed request'}), 400

        # Check if username is already taken
        old_user = mongo.db.users.find({'username': user_name})
        old_user_list = list(old_user)
        
        if len(old_user_list) > 0:
            content = {'Error': 'User already exists'}
            return jsonify(content), 409 # Status CONFLICT
        
        # Save new user's public key
        else:
            mongo.db.users.insert({'username': user_name, 'public_key': user_key})
            return jsonify("Success"), 200 # Status OK


