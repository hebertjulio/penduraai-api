from functools import wraps, partial
from json import dumps
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Model

from .exceptions import BadRequest
from .models import Transaction
from .encoders import DecimalEncoder


def create_transaction(func=None, scope=None, expire=60):

    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(create_transaction, scope=scope, expire=expire)

    @wraps(func)
    def wrapper(self, validated_data, **kwargs):
        expire_at = timezone.now() + timedelta(minutes=expire)

        data = dumps({
                k: v.id if isinstance(v, Model) else v
                for k, v in validated_data.items()
            }, cls=DecimalEncoder
        )

        transaction = Transaction(**{
            'scope': scope, 'data': data, 'expire_at': expire_at
        })
        transaction.save()

        validated_data.update({'transaction': transaction.id})
        return func(self, validated_data, **kwargs)
    return wrapper


def use_transaction(func=None, scope=None):

    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(use_transaction, scope=scope)

    def get_transaction(pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            return transaction
        except Transaction.DoesNotExist:
            detail = _('Transaction not found.')
            raise BadRequest(detail)

    @wraps(func)
    def wrapper(self, request, **kwargs):
        if 'pk' not in kwargs:
            detail = _('Key \'pk\' not found in kwargs.')
            raise BadRequest(detail)

        transaction = get_transaction(kwargs['pk'])

        if transaction.scope != scope:
            detail = _(
                'Scope \'%s\' invalid for this transaction.'
                % transaction.scope)
            raise BadRequest(detail)

        if transaction.status != Transaction.STATUS.awaiting:
            detail = _(
                'Transaction status \'%s\' not allowed.'
                % transaction.status)
            raise BadRequest(detail)

        if transaction.is_expired():
            detail = _('Transaction live time expired.')
            raise BadRequest(detail)

        request.data.update(transaction.datajson)
        ret = func(self, request, **kwargs)

        transaction.status = Transaction.STATUS.accepted
        transaction.save()

        return ret
    return wrapper
