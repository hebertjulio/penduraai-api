from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import generate_signature


class TicketSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        fields = value.data.keys()
        values = [request.data.get(field, '') for field in fields]
        signature = generate_signature(values)
        if value.signature != signature:
            message = _('Ticket signature invalid.')
            raise serializers.ValidationError(message)
