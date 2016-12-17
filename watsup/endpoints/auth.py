"""User authentication pages and API.
"""

from flask import Blueprint, request

from watsup.config import config
from watsup import mongo, crypto


auth = Blueprint('auth',
                 __name__,
                 url_prefix='%s/auth' % config.get('url', 'base'))


@auth.route('/', methods=['POST'])
def request_nonce():
    """Renders index page.
    """
    username = request.form.get('username')
    user = mongo.db.users.find_one({'username': username})

    # Generate, save, and encrypt nonce.
    nonce = crypto.generate_nonce()
    user['nonce'] = nonce
    mongo.db.users.save(user)
    pub_key_data = user['public_key']
    print(nonce)
    ciphertext = crypto.encrypt_nonce(nonce, pub_key_data)

    return ciphertext


@auth.route('/', methods=['GET'])
def test_user():

    # Create a new nonce using the following command:
    # curl --data "username=FirstUser" http://localhost:8080/watsup/auth/ > encrypted.txt

    from cryptography.hazmat.primitives.serialization import load_pem_private_key
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    with open('/Users/gwg/.ssh/private_key.pem', 'rb') as f:
        private_key_data = f.read()
    with open('/Users/gwg/watsup/encrypted.txt', 'rb') as f:
        ciphertext = f.read()

    private_key = load_pem_private_key(private_key_data,
                                       password=None,
                                       backend=default_backend())
    plaintext = private_key.decrypt(ciphertext,
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                 algorithm=hashes.SHA1(),
                                                 label=None))

    print(plaintext)
    return plaintext





