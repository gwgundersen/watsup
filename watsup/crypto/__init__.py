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


def generate_nonce(length=8):
    """Generate pseudorandom number. Credit:
    https://github.com/joestump/python-oauth2/blob/81326a07d1936838d844690b468660452aafdea9/oauth2/__init__.py#L165
    """
    return ''.join([str(random.randint(0, 9)) for i in range(length)])
