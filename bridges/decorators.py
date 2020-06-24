from functools import wraps, partial

from django.utils.translation import gettext_lazy as _

from .exceptions import BadRequest
from .models import Transaction


def use_transaction(func=None, scope=None):

    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(use_transaction, scope=scope)

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        pk = kwargs[self.lookup_field]

        try:
            obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            detail = _('Transaction \'%s\' not found.' % pk)
            raise BadRequest(detail)

        if obj.scope != scope:
            detail = _(
                'Transaction scope \'%s\' is invalid.' % obj.scope)
            raise BadRequest(detail)

        if obj.status != Transaction.STATUS.not_used:
            detail = _(
                'Transaction already was %s.' % obj.status)
            raise BadRequest(detail)

        if obj.is_expired():
            detail = _('Transaction live time expired.')
            raise BadRequest(detail)

        request.data.update(obj.json())
        ret = func(self, request, **kwargs)
        obj.status = Transaction.STATUS.used
        obj.save()

        return ret
    return wrapper
