import json

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Transaction


class TransactionIntegrityValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        data = serializer_field.context['request'].data
        keys = json.loads(value.data).keys()
        signature = ''.join([key + str(data[key]) for key in keys])
        if value.signature != signature:
            message = _('Transaction signature is invalid.')
            raise serializers.ValidationError(message)


class TrasactionStatusValidator:

    def __call__(self, value):
        if value.status != Transaction.STATUS.unused:
            message = _('Transaction status is invalid.')
            raise serializers.ValidationError(message)


class TrasactionScopeValidator:

    def __init__(self, scope):
        self.scope = scope

    def __call__(self, value):
        if value.scope != self.scope:
            message = _('Transaction scope is invalid.')
            raise serializers.ValidationError(message)


class TransactionExpiredValidator:

    def __call__(self, value):
        if value.expired:
            message = _('Transaction has expired.')
            raise serializers.ValidationError(message)
