import base64
import re

from Crypto.Hash import SHA1, HMAC


def create_api_metadata(metadata):
    api_metadata = {
        'entries': {},
        'empty': True,
    }
    for key in metadata:
        value = metadata[key]
        api_metadata['entries'][key] = [
            {'value': value, 'lang': '*'}
        ]
    return api_metadata


def create_sumo_signature(method, path, secret, timestamp):
    plain_path = re.sub(r"\?.*", "", path)
    string_to_sign = method + "\n" + plain_path + "\n" + timestamp
    sig_hash = HMAC.new(secret.encode('utf-8'), digestmod=SHA1)
    sig_hash.update(string_to_sign.encode('utf-8'))
    return base64.b64encode(sig_hash.digest()).decode("utf-8")


def create_basic_auth_token(username, password):
    credentials_bytes = f'{username}:{password}'.encode("utf-8")
    return base64.b64encode(credentials_bytes).decode("ascii")
