from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from celery import shared_task


@shared_task(bind=True)
def websocket_send(self, group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(group), {
            'type': 'websocket.send',
            'text': message,
        },
    )
