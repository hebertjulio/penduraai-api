from functools import wraps, partial

from .dbdict import Transaction
from .exceptions import (
    ScopeNotAllowedException, TransactionNotFoundException,
    StatusNotAllowedException
)


def load_transaction(func=None, scope=None, status=None):

    if scope is not None:
        if scope not in Transaction.SCOPES:
            ValueError('Transaction scope is invalid.')

    if status is not None:
        if status not in Transaction.STATUS:
            ValueError('Transaction status is invalid.')

    if func is None:
        return partial(
            load_transaction, scope=scope, status=status)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in kwargs:
            raise ValueError('Token not found in kwargs.')

        transaction = Transaction(kwargs['token'])

        if not transaction.exist():
            raise TransactionNotFoundException

        if scope is not None:
            if transaction.scope != scope:
                raise ScopeNotAllowedException

        if status is not None:
            if transaction.status != status:
                raise StatusNotAllowedException

        kwargs.update({'transaction': transaction})
        ret = func(*args, **kwargs)

        return ret

    return wrapper
