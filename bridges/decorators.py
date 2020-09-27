from functools import wraps, partial

from .db import Transaction
from .services import send_ws_message


def use_transaction(func=None, lookup_url_kwarg=None):
    if func is None:
        return partial(use_transaction, lookup_url_kwarg=lookup_url_kwarg)

    @wraps(func)
    def wapper(self, request, *args, **kwargs):
        transaction_id = kwargs[lookup_url_kwarg]
        self.transaction = Transaction(transaction_id)
        self.transaction.exist(raise_exception=True)
        result = func(self, request, *args, **kwargs)
        self.transaction.delete()
        send_ws_message(transaction_id, 'CONFIRMED')
        return result
    return wapper
