from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature


class TicketExpiredValidator:

    def __call__(self, value):
        if value.expired:
            message = _('Ticket already expired.')
            raise serializers.ValidationError(message)


class TicketUsageValidator:

    def __call__(self, value):
        if value.usage != 0:
            message = _('Ticket already usaged.')
            raise serializers.ValidationError(message)


class TicketSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        fields = value.payload_as_dict.keys()
        values = [request.data[field] for field in fields]
        signature = generate_signature(values)
        if value.signature != signature:
            message = _('Ticket signature invalid.')
            raise serializers.ValidationError(message)
