from django.db.models import Model

from functools import wraps, partial

from .db import Transaction
from .services import send_ws_message


def create_transaction(func=None, expire=None, scope=None):
    if expire is None:
        raise ValueError

    if scope is None:
        raise ValueError

    if func is None:
        return partial(create_transaction, expire=expire, scope=scope)

    @wraps(func)
    def wapper(self, validated_data):
        data = {
            k: v.id if isinstance(v, Model) else v
            for k, v in validated_data.items()
        }
        transaction = Transaction()
        transaction.scope = scope
        transaction.expire = expire
        transaction.data = data
        validated_data.update({'transaction': transaction.id})
        return func(self, validated_data)
    return wapper


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
