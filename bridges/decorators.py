from functools import wraps

from .services import send_messages
from .models import Transaction


def use_transaction(func):
    @wraps(func)
    def wapper(self, validated_data):
        obj = func(self, validated_data)
        request = self.context['request']
        transaction = getattr(request, 'transaction', None)
        if transaction:
            transaction.status = Transaction.STATUS.used
            transaction.save()
            send_messages(transaction)
        return obj
    return wapper
