from functools import wraps

from .services import send_messages
from .models import Transaction


def use_transaction(func):
    @wraps(func)
    def wapper(self, validated_data):
        transaction = validated_data.pop('transaction')
        obj = func(self, validated_data)
        transaction.status = Transaction.STATUS.used
        transaction.save()
        send_messages(transaction)
        return obj
    return wapper
