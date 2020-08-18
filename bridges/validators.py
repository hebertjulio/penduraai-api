from json import loads

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature


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
        values = [request.data[field] for field in loads(value.data).keys()]
        signature = generate_signature(values)
        if value.signature != signature:
            message = _('Transaction signature invalid.')
            raise serializers.ValidationError(message)
