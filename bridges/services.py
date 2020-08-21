from hashlib import sha256

from django.conf import settings

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from jwt import (
    InvalidAudience, InvalidSignatureError, ExpiredSignatureError,
    DecodeError)

from jwt import decode as jwt_decode

from .exceptions import TokenEncodeException


def send_ws_message(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )


def generate_signature(values):
    values = [str(value) for value in values]
    value = ''.join(sorted(values))
    value = sha256(value.encode()).hexdigest()
    return value


def get_token_data(token):
    try:
        data = jwt_decode(
            token, settings.SECRET_KEY, audience='ticket',
            algorithms=['HS256'])
        return data
    except (InvalidSignatureError, InvalidAudience,
            ExpiredSignatureError, DecodeError):
        raise TokenEncodeException
