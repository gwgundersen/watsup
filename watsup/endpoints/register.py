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
        u_name = escape(request.json['username'])
        
        # NOTE(tfs,2016/12/19): Just storing raw data for now,
        #                       still not entirely sure how formats will work out.
        u_key = request.json['publickey']

        old_user = mongo.db.users.find({'username': u_name})

        old_user_list = list(old_user)
        
        if len(old_user_list) > 0:
            content = {'Error': 'User already exists'}
            return jsonify(content), 409 # Status CONFLICT
        else:
            mongo.db.users.insert({'username': u_name, 'publickey': u_key})
            return jsonify("Success"), 200 # Status OK


