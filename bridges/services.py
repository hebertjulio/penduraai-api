from django.db.models import Model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .db import Transaction


def create_transaction(data, expire, scope):
    transaction = Transaction()
    transaction.scope = scope
    transaction.expire = expire
    transaction.data = {
        k: v.id if isinstance(v, Model) else v
        for k, v in data.items()
    }
    return transaction


def send_ws_message(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
