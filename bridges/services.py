from hashlib import sha256

from django.conf import settings

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from .tasks import response_by_websocket, response_by_push_notification


TOKEN_AUDIENCE = 'v1'


def response_transaction(group, message):
    response_by_websocket.apply_async([str(group), str(message)])
    response_by_push_notification.apply_async([str(message)])


def generate_signature(values):
    values = [str(value) for value in values]
    value = ''.join(sorted(values))
    value = sha256(value.encode()).hexdigest()
    return value


def encode_token(payload):
    payload.update({'aud': TOKEN_AUDIENCE})
    token = jwt_encode(payload, settings.SECRET_KEY, algorithm='HS256')
    token = token.decode('utf-8')
    return token


def decode_token(token):
    try:
        payload = jwt_decode(
            token, settings.SECRET_KEY, audience=TOKEN_AUDIENCE,
            algorithms=['HS256'])
        return payload
    except (
            InvalidSignatureError, InvalidAudience,
            ExpiredSignatureError, DecodeError):
        return None
