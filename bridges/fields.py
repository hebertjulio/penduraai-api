from django.utils.translation import gettext_lazy as _

from rest_framework.validators import ValidationError
from rest_framework.fields import Field

from .services import get_token_data
from .db import Ticket
from .validators import TicketSignatureValidator
from .exceptions import TokenEncodeException


class TicketTokenField(Field):

    validators = [
        TicketSignatureValidator()
    ]

    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope')
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            data = get_token_data(data)
            ticket = Ticket(data['key'], self.scope)
        except TokenEncodeException:
            raise ValidationError(_('Ticket of token is invalid.'))
        else:
            if not ticket.exist():
                raise ValidationError(_('Ticket does not exist.'))
            return ticket
