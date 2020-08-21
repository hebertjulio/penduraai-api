from hashlib import sha256

from django.conf import settings

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from .exceptions import TokenDecodeException


_AUDIENCE = 'ticket'


def send_ws_message(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )


def get_signature(data, scope):
    if not isinstance(data, dict):
        raise ValueError
    fields = {
        'profile': ['user', 'role'],
        'sheet': ['merchant'],
        'record': ['note', 'merchant', 'value', 'operation']
    }
    value = [str(data.get(field, '')) for field in fields[scope]]
    value = ':'.join(value)
    value = sha256(value.encode()).hexdigest()
    return value


def token_encode(data, expire):
    data = {**data, **{'aud': _AUDIENCE, 'exp': expire}}
    token = jwt_encode(data, settings.SECRET_KEY, algorithm='HS256')
    token = token.decode('utf-8')
    return token


def token_decode(token):
    try:
        data = jwt_decode(
            token, settings.SECRET_KEY, audience=_AUDIENCE,
            algorithms=['HS256'])
        return data
    except (InvalidSignatureError, InvalidAudience,
            ExpiredSignatureError, DecodeError) as e:
        raise TokenDecodeException(str(e))
