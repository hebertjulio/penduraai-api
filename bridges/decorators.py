from functools import wraps

from .services import response_ticket


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('ticket')
        ret = func(self, validated_data)
        obj.usage = 1
        obj.save()
        response_ticket(obj.id, obj.usage)
        return ret
    return wapper
