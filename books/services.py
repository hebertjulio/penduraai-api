from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .dictdb import Storage


def transaction_response(key, message):
    db = Storage(key)
    channel_name = db['channel_name'].decode()
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
    del db
