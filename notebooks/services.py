import hashlib

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def generate_hash(data):
    """generate hash to integrity check"""
    if not isinstance(data, dict):
        raise ValueError
    value = ';'.join(str(v) for _, v in sorted(data.items()))
    h = hashlib.sha256(value.encode())
    return h.hexdigest()


def send_message(group, message):
    """send message by websocket to group users"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
