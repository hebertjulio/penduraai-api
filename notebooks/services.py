import hashlib

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def generate_signature(creditor, payload):
    """generate signature to integrity check"""
    if not isinstance(payload, dict):
        raise ValueError
    if not isinstance(creditor, str):
        creditor = str(creditor)
    value = ';'.join(str(v) for _, v in sorted(payload.items()))
    value = creditor + ';' + value
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
