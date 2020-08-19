from functools import wraps

from .services import websocket_response


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('ticket')
        ret = func(self, validated_data)
        obj.usage = 1
        obj.save()
        if obj.callback:
            websocket_response(str(obj.id), str(obj.usage))
        return ret
    return wapper
