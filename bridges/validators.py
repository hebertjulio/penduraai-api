from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class TransactionScopeValidator:

    def __init__(self, scope):
        self.scope = scope

    def __call__(self, value):
        if value.scope != self.scope:
            message = _('Transaction scope is invalid for this request.')
            raise serializers.ValidationError(message)


class TrasactionUsedValidator:

    def __call__(self, value):
        if value.used:
            message = _('Transaction already in use.')
            raise serializers.ValidationError(message)


class TransactionExpiredValidator:

    def __call__(self, value):
        if value.expired:
            message = _('Transaction has expired.')
            raise serializers.ValidationError(message)
