from functools import wraps, partial

from .dbdict import Transaction
from .exceptions import (
    ScopeNotAllowedException, TransactionNotFoundException,
    StatusNotAllowedException
)


def use_transaction(
        func=None, scope=None,
        current_status=None, new_status=None):

    if scope is not None:
        if scope not in Transaction.SCOPES:
            ValueError('Transaction scope is invalid.')
    if current_status is not None:
        if current_status not in Transaction.STATUS:
            ValueError('Invalid current status \'%s\'.' % current_status)
    if new_status is not None:
        if new_status not in Transaction.STATUS:
            ValueError('Invalid new status \'%s\'.' % new_status)

    if func is None:
        return partial(
            use_transaction, scope=scope,
            current_status=current_status, new_status=new_status
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in kwargs:
            raise ValueError('Token not found in kwargs.')

        transaction = Transaction(kwargs['token'])
        save = False

        if not transaction.exist():
            raise TransactionNotFoundException
        if scope is not None:
            if transaction.scope != scope:
                raise ScopeNotAllowedException
        if current_status is not None:
            if transaction.status != current_status:
                raise StatusNotAllowedException
        if new_status is not None:
            transaction.status = new_status
            save = True

        kwargs.update({'transaction': transaction})
        ret = func(*args, **kwargs)

        if save:
            transaction.save()

        return ret
    return wrapper
