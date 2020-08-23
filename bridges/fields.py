from rest_framework.fields import Field

from .services import token_decode
from .db import Ticket

from .validators import (
    TicketScopeValidator, TicketSignatureValidator,
    TicketStatusValidator)


class TicketTokenField(Field):

    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope')
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        value = super().to_representation(value)
        return value

    def to_internal_value(self, data):
        data = token_decode(data)
        ticket = Ticket(data['id'])
        ticket.exist(raise_exception=True)
        return ticket

    def get_validators(self):
        validators = super().get_validators()
        validators += [
            TicketStatusValidator(),
            TicketScopeValidator(self.scope),
            TicketSignatureValidator()
        ]
        return validators
