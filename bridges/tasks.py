from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from celery import shared_task


@shared_task(bind=True)
def websocket_notification(self, group, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )


@shared_task(bind=True)
def push_notification(self, message):
    pass
