from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def transaction_response(channel_name, message):
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
