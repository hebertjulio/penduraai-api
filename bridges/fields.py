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

    def to_internal_value(self, data):
        try:
            payload = decode_token(data)
            obj = Ticket.objects.get(pk=payload['id'])
            return obj
        except (Ticket.DoesNotExist,
                TokenEncodeException,
                TypeError):
            raise ValidationError(_('Ticket of token is invalid.'))

    def get_validators(self):
        validators = super().get_validators()
        validators += [
            TicketExpiredValidator(),
            TicketSignatureValidator(),
            TicketUsageValidator()
        ]
        return validators
