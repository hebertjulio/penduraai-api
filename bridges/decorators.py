from functools import wraps

from .services import send_messages


def use_transaction(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = func(self, validated_data)
        request = self.context['request']
        transaction = request.transaction
        transaction.usage -= 1
        transaction.save()
        send_messages(transaction)
        return obj
    return wapper
