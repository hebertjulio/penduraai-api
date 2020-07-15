import json
import datetime

from functools import wraps, partial

from django.utils import timezone
from django.db.models import Model

from rest_framework.exceptions import NotFound

from .serializers import TransactionDetailSerializer
from .services import send_message
from .models import Transaction
from .encoders import DecimalEncoder
from .exceptions import (
    TransactionScopeInvalid, TransactionStatusInvalid,
    TransactionExpired
)


def use_transaction(func=None, scope=None):
    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(use_transaction, scope=scope)

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.lookup_field)

        try:
            obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise NotFound

        if obj.scope != scope:
            raise TransactionScopeInvalid

        if obj.status != Transaction.STATUS.not_used:
            raise TransactionStatusInvalid

        if obj.is_expired():
            raise TransactionExpired

        request.transaction = obj
        ret = func(self, request, **kwargs)

        obj.status = Transaction.STATUS.used
        obj.save()

        serializer = TransactionDetailSerializer(obj)
        message = json.dumps(serializer.data, cls=DecimalEncoder)
        send_message(obj.id, message)

        return ret
    return wrapper


def new_transaction(func=None, scope=None, expire=30):
    if scope is None:
        ValueError('Scope can\'t be empty.')

    if func is None:
        return partial(new_transaction, scope=scope, expire=expire)

    expire_at = timezone.now() + datetime.timedelta(minutes=expire)

    @wraps(func)
    def wrapper(self, validated_data):
        data = json.dumps({
            k: v.id if isinstance(v, Model) else v
            for k, v in validated_data.items()}, cls=DecimalEncoder
        )

        request = self.context['request']
        obj = Transaction(**{
            'scope': scope, 'data': data, 'expire_at': expire_at,
            'user': request.user, 'profile': request.profile
        })

        obj.save()
        validated_data = {'transaction': obj.id}

        return func(self, validated_data)
    return wrapper
