from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .storages import Transaction


def transaction_response(key, message):
    t = Transaction(key)
    channel_name = t.channel_name.decode()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name, {
            'type': 'websocket.send',
            'text': message.upper(),
        },
    )
    async_to_sync(channel_layer.send)(
        channel_name, {
            'type': 'websocket.disconnect',
        },
    )
    del t.channel_name
    del t.record
