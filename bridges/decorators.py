from json import dumps

from functools import wraps

from .serializers import TransactionReadSerializer
from .encoders import DecimalEncoder
from .tasks import websocket_send


def use_transaction(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('transaction')
        ret = func(self, validated_data)
        obj.usage += 1
        obj.save()
        serializer = TransactionReadSerializer(obj)
        group = str(obj.id)
        message = dumps(serializer.data, cls=DecimalEncoder)
        websocket_send.apply_async((group, message))
        return ret
    return wapper
