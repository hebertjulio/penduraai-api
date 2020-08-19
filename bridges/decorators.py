from functools import wraps

from .services import do_notification


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('ticket')
        ret = func(self, validated_data)
        obj.usage = 1
        obj.save()
        do_notification(
            obj.id, obj.usage, obj.ws_notification,
            obj.push_notification)
        return ret
    return wapper
