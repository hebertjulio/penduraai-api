from functools import wraps, partial

from django.utils.translation import gettext_lazy as _

from .exceptions import BadRequest
from .models import Transaction


def use_transaction(func=None, scope=None, lookup_field='pk'):
    """Decorator to transaction use and accept after"""

    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(
            use_transaction, scope=scope, lookup_field=lookup_field)

    @wraps(func)
    def wrapper(self, request, **kwargs):
        if lookup_field not in kwargs:
            detail = _('Key \'pk\' not found in kwargs.')
            raise BadRequest(detail)

        try:
            tran = Transaction.objects.get(pk=kwargs[lookup_field])
        except Transaction.DoesNotExist:
            detail = _('Transaction not found.')
            raise BadRequest(detail)

        if tran.scope != scope:
            detail = _(
                'Scope \'%s\' invalid for this transaction.' % tran.scope)
            raise BadRequest(detail)

        if tran.status != Transaction.STATUS.awaiting:
            detail = _(
                'Transaction status \'%s\' not allowed.' % tran.status)
            raise BadRequest(detail)

        if tran.is_expired():
            detail = _('Transaction live time expired.')
            raise BadRequest(detail)

        request.data.update(tran.json())
        response = func(self, request, **kwargs)

        tran.status = Transaction.STATUS.used
        tran.save()

        return response
    return wrapper
