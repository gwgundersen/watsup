"""Handles user/public key registration
"""

from flask import Blueprint, render_template, escape, request, jsonify

from watsup.config import config

from watsup import mongo


register = Blueprint('register',
                     __name__,
                     url_prefix='%s/register' % config.get('url', 'base'))


@register.route('/', methods=['POST'])
def register_user():
    if request.method == 'POST':
        required_fields = ['username', 'public_key']

        if not request.json:
            return jsonify({'Error': 'Incorrect request'}), 400 # Status BAD

        if not 'username' in request.json or not 'public_key' in request.json:
            return jsonify({'Error': 'Incorrect request'}), 400 # Status BAD

        user_name = escape(request.json['username'])
        
        # NOTE(tfs,2016/12/19): Just storing raw data for now,
        #                       still not entirely sure how formats will work out.
        user_key = request.json['public_key']

        old_user = mongo.db.users.find({'username': user_name})

        old_user_list = list(old_user)
        
        if len(old_user_list) > 0:
            content = {'Error': 'User already exists'}
            return jsonify(content), 409 # Status CONFLICT
        else:
            mongo.db.users.insert({'username': user_name, 'public_key': user_key})
            return jsonify("Success"), 200 # Status OK


