from django.utils.translation import gettext_lazy as _

from rest_framework.validators import ValidationError
from rest_framework.fields import Field

from .services import get_token_data
from .db import Ticket
from .validators import TicketScopeValidator, TicketSignatureValidator
from .exceptions import TokenDecodeException


class TicketTokenField(Field):

    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope')
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            data = get_token_data(data)
            ticket = Ticket(data['scope'], data['key'])
            ticket.exist(raise_exception=True)
            return ticket
        except (Ticket.DoesNotExist,
                TokenDecodeException) as e:
            raise ValidationError(_(str(e)))

    def get_validators(self):
        validators = super().get_validators()
        validators += [
            TicketScopeValidator(self.scope),
            TicketSignatureValidator()
        ]
        return validators
