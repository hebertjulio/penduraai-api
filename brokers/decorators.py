import json

from functools import wraps

from .services import send_message
from .dictdb import Transaction


def accept_transaction(func):
    @wraps(func)
    def wrapper(self, validated_data, **kwargs):
        transaction = str(validated_data.pop('transaction'))
        ret = func(self, validated_data, **kwargs)
        tran = Transaction(transaction)
        tran.status = Transaction.STATUS.accepted
        tran.save()
        send_message(tran.id, json.dumps(tran.data))
        return ret
    return wrapper
