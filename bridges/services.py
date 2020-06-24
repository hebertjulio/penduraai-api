from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_message(group, message):
    """Send message by websocket to group users"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
