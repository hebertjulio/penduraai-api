from functools import wraps

from .services import response_transaction


def use_transaction(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = validated_data.pop('transaction')
        ret = func(self, validated_data)
        obj.tickets -= 1
        obj.save()
        response_transaction(obj.id, obj.tickets)
        return ret
    return wapper
