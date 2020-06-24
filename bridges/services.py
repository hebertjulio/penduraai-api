import json
import datetime

from django.utils import timezone
from django.db.models import Model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Transaction
from .encoders import DecimalEncoder


def send_message(group, message):
    """Send message by websocket to group users"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(group), {
            'type': 'websocket.send',
            'text': message,
        },
    )


def new_transaction(scope, user, profile, data, expire=30):
    """ Create new transaction and return it"""
    expire_at = timezone.now() + datetime.timedelta(minutes=expire)
    data = json.dumps({
        k: v.id if isinstance(v, Model) else v
        for k, v in data.items()}, cls=DecimalEncoder
    )
    obj = Transaction(**{
        'scope': scope, 'data': data, 'expire_at': expire_at,
        'user': user, 'profile': profile
    })
    obj.save()
    return obj
