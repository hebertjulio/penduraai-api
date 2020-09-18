from django.db.models import Model

from functools import wraps, partial

from .db import Transaction


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
        transaction.status = 'unused'
        transaction.expire = expire
        transaction.data = data
        validated_data.update({'transaction': transaction.id})
        return func(self, validated_data)
    return wapper


def load_transaction(func):
    @wraps(func)
    def wapper(self, request, version, transaction_id):
        self.transaction = Transaction(transaction_id)
        self.transaction.exist(raise_exception=True)
        return func(self, request, version, transaction_id)
    return wapper
