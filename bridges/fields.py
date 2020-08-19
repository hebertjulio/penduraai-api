from django.utils.translation import gettext_lazy as _

from rest_framework.validators import ValidationError
from rest_framework.fields import Field

from .services import decode_token
from .models import Ticket

from .validators import (
    TicketExpiredValidator, TicketSignatureValidator,
    TicketUsageValidator)

from .exceptions import TokenEncodeException


class TicketTokenField(Field):

    validators = [
        TicketExpiredValidator(),
        TicketSignatureValidator(),
        TicketUsageValidator()
    ]

    def to_representation(self, instance):
        print(instance)
        return instance

    def to_internal_value(self, data):
        try:
            payload = decode_token(data)
            obj = Ticket.objects.get(pk=payload['id'])
            return obj
        except (Ticket.DoesNotExist,
                TokenEncodeException,
                TypeError):
            raise ValidationError(_('Ticket of token is invalid.'))
