import json

from functools import wraps

from .dictdb import Transaction
from .services import send_message


def accept_transaction(func):
    @wraps(func)
    def wrapper(self, validated_data, **kwargs):
        transaction = str(validated_data.pop('transaction'))
        r = func(self, validated_data, **kwargs)
        tran = Transaction(transaction)
        tran.status = Transaction.STATUS.accepted
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return r
    return wrapper
