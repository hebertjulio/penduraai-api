import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .serializers import TransactionReadSerializer
from .encoders import DecimalEncoder


def send_message(transaction):
    serializer = TransactionReadSerializer(transaction)
    group = str(transaction.id)
    message = json.dumps(serializer.data, cls=DecimalEncoder)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {
            'type': 'websocket.send',
            'text': message,
        },
    )
