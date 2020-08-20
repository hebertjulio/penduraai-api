from functools import wraps

from .services import send_ws_message
from .tasks import push_notification


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('ticket')
        ret = func(self, validated_data)
        obj.usage = 1
        obj.save()
        send_ws_message(obj.id, obj.usage)
        push_notification.apply([obj.id, obj.message])
        return ret
    return wapper
