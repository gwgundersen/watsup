"""Wrapper for cryptography API.
"""

import random

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend


def encrypt_nonce(nonce, pub_key_data):
    """Encrypt a nonce using the user's public key.
    """
    pub_key_data = pub_key_data.encode('latin-1')
    pub_key = load_pem_public_key(pub_key_data, backend=default_backend())
    padding_ = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                            algorithm=hashes.SHA1(),
                            label=None)
    ciphertext = pub_key.encrypt(nonce, padding_)
    return ciphertext


def generate_nonce():
    """Generate pseudorandom number with cryptographically secure SystemRandom.
    Credit: https://github.com/joestump/python-oauth2/blob/master/oauth2/__init__.py#L510
    """
    return str(random.SystemRandom().randint(0, 100000000))
