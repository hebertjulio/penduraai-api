from functools import wraps, partial

from rest_framework.exceptions import NotFound

from .exceptions import InvalidScopeException, InvalidUsageException
from .models import Transaction
from .services import send_ws_message


def use_transaction(func=None, lookup_url_kwarg=None):
    if func is None:
        return partial(use_transaction, lookup_url_kwarg=lookup_url_kwarg)

    @wraps(func)
    def wapper(self, request, *args, **kwargs):
        transaction_id = kwargs[lookup_url_kwarg]
        try:
            self.transaction = Transaction.objects.get(pk=transaction_id)
        except Transaction.DoesNotExist:
            raise NotFound

        if self.transaction.scope != scope:
            raise InvalidScopeException

        if -1 >= self.transaction.usage >= self.transaction.max_usage:
            raise InvalidUsageException

        result = func(self, request, *args, **kwargs)
        self.transaction.usage += 1
        self.save()
        send_ws_message(transaction_id, 'CONFIRMED')
        return result
    return wapper
