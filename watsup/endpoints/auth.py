""" User authentication pages and API """

from flask import Blueprint, request, jsonify
from watsup.config import config
from watsup import mongo, crypto

auth = Blueprint('auth',
                 __name__,
                 url_prefix='%s/auth' % config.get('url', 'base'))

@auth.route('/', methods=['POST'])
def request_nonce():
    """
        Generates and encrypts nonce with a user's public key
    """

    username = request.form.get('username')
    user = mongo.db.users.find_one({'username': username})

    # Generate, save, and encrypt nonce.
    nonce = crypto.generate_nonce()
    user['password'] = nonce
    mongo.db.users.save(user)
    pub_key_data = user['public_key']
    ciphertext = crypto.encrypt_nonce(nonce, pub_key_data)

    return ciphertext

