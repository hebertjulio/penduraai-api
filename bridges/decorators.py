import json
import datetime

from functools import wraps, partial

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Model

from .exceptions import BadRequest
from .models import Transaction
from .encoders import DecimalEncoder


def new_transaction(func=None, scope=None, expire=30):

    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(new_transaction, scope=scope, expire=expire)

    @wraps(func)
    def wrapper(self, validated_data):
        request = self.context['request']
        expire_at = timezone.now() + datetime.timedelta(minutes=expire)

        data = json.dumps({
            k: v.id if isinstance(v, Model) else v
            for k, v in validated_data.items()}, cls=DecimalEncoder
        )
        obj = Transaction(**{
            'scope': scope, 'data': data, 'expire_at': expire_at,
            'user': request.user, 'profile': request.user.profile
        })
        obj.save()

        validated_data.update({'transaction': obj.id})
        ret = func(self, validated_data)
        return ret

    return wrapper


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
