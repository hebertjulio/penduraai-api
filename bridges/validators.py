from json import loads

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import get_signature


class TransactionExpiredValidator:

    def __call__(self, value):
        if value.expired:
            message = _('Transaction already expired.')
            raise serializers.ValidationError(message)


class TransactionUsageValidator:

    def __call__(self, value):
        if not(0 <= value.usage < value.max_usage):
            message = _('Transaction usage invalid.')
            raise serializers.ValidationError(message)


class TransactionSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        fields = loads(value.data).keys()
        signature = get_signature(fields, request.data)
        if value.signature != signature:
            message = _('Transaction signature invalid.')
            raise serializers.ValidationError(message)
