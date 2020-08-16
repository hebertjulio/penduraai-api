from json import dumps

from .serializers import TransactionReadSerializer
from .tasks import websocket_send
from .encoders import DecimalEncoder


def send_messages(transaction):
    if transaction:
        serializer = TransactionReadSerializer(transaction)
        group = str(transaction.id)
        message = dumps(serializer.data, cls=DecimalEncoder)
        websocket_send.apply_async((group, message))


def get_signature(keys, dataset):
    keys = sorted(keys)
    signature = ''.join([key + str(dataset[key]) for key in keys])
    return signature
