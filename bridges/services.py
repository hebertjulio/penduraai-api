from hashlib import sha256

from django.conf import settings

from jwt import decode as jwt_decode

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)


def get_signature(fields, data):
    value = ''.join([str(data[field]) for field in fields])
    value = sha256(value.encode()).hexdigest()
    return value


def get_payload(token):
    try:
        payload = jwt_decode(
            token, settings.SECRET_KEY, audience='v1',
            algorithms=['HS256'])
        return payload
    except (
        InvalidSignatureError, InvalidAudience,
            ExpiredSignatureError, DecodeError):
        return None
