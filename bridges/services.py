from hashlib import sha256

from django.conf import settings

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from .exceptions import TokenEncodeException
from .tasks import push_notification, websocket_notification


TOKEN_AUDIENCE = 'v1'


def do_notification(group, message, ws, push):
    if ws:
        websocket_notification.apply([str(group), str(message)])
    if push:
        push_notification.apply([message])


def generate_signature(values):
    values = [str(value) for value in values]
    value = ''.join(sorted(values))
    value = sha256(value.encode()).hexdigest()
    return value


def token_encode(payload):
    payload.update({'aud': TOKEN_AUDIENCE})
    token = jwt_encode(payload, settings.SECRET_KEY, algorithm='HS256')
    token = token.decode('utf-8')
    return token


def token_decode(token):
    try:
        payload = jwt_decode(
            token, settings.SECRET_KEY, audience=TOKEN_AUDIENCE,
            algorithms=['HS256'])
        return payload
    except (
            InvalidSignatureError, InvalidAudience,
            ExpiredSignatureError, DecodeError):
        raise TokenEncodeException
