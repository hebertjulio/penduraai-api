from json import loads

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class TransactionSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        transaction = request.transaction
        data = request.data
        keys = sorted(loads(transaction.data).keys())
        signature = ''.join([key + str(data[key]) for key in keys])
        if transaction.signature != signature:
            message = _('Invalid transaction signature.')
            raise serializers.ValidationError(message)
