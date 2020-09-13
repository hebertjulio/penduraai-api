from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_ws_message(group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
