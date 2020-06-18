from functools import wraps, partial

from rest_framework.exceptions import NotFound

from .dbdict import Transaction


def use_transaction_token(func=None, scope=None):
    if scope is None:
        raise ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(use_transaction_token, scope=scope)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in kwargs:
            raise ValueError
        transaction = Transaction(kwargs['token'])
        if transaction.status != Transaction.STATUS.awaiting:
            raise NotFound  # @TODO: improve error
        if transaction.scope != scope:
            raise NotFound  # @TODO: improve error
        kwargs.update({'transaction': transaction})
        ret = func(*args, **kwargs)
        transaction.status = Transaction.STATUS.accepted
        transaction.save()
        return ret

    return wrapper
