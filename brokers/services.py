import hashlib

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def generate_signature(payload):
    """generate signature to integrity check"""
    if not isinstance(payload, dict):
        raise ValueError
    value = ';'.join(str(v) for _, v in sorted(payload.items()))
    h = hashlib.sha256(value.encode())
    return h.hexdigest()


def push_notification(group, message):
    """send message by websocket to group users"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
