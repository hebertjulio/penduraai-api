from json import loads

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import get_signature


class TransactionValidator:

    requires_context = True

    @classmethod
    def expired_validator(cls, transaction):
        if transaction.expired:
            message = _('Transaction already expired.')
            raise serializers.ValidationError(message)

    @classmethod
    def usage_validator(cls, transaction):
        if transaction.usage < 1:
            message = _('Transaction usage invalid.')
            raise serializers.ValidationError(message)

    @classmethod
    def signature_validator(cls, transaction, dataset):
        keys = loads(transaction.data).keys()
        signature = get_signature(keys, dataset)
        if transaction.signature != signature:
            message = _('Transaction signature invalid.')
            raise serializers.ValidationError(message)

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        transaction = request.transaction
        self.expired_validator(transaction)
        self.usage_validator(transaction)
        self.signature_validator(transaction, request.data)
