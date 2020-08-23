from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .services import get_signature


class TicketUsageValidator:

    def __call__(self, value):
        if value.usage != 0:
            message = _('Ticket usage is invalid.')
            raise serializers.ValidationError(message)


class TicketScopeValidator:

    def __init__(self, scope):
        self.scope = scope

    def __call__(self, value):
        if value.scope != self.scope:
            message = _('Ticket scope is invalid.')
            raise serializers.ValidationError(message)


class TicketSignatureValidator:

    requires_context = True

    def __call__(self, value, serializer_field):
        request = serializer_field.context['request']
        signature = get_signature(request.data, value.scope)
        if value.signature != signature:
            message = _('Ticket signature is invalid.')
            raise serializers.ValidationError(message)
