from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class TicketScopeValidator:

    def __init__(self, scope):
        self.scope = scope

    def __call__(self, value):
        if value.scope != self.scope:
            message = _('Ticket scope is invalid.')
            raise serializers.ValidationError(message)
