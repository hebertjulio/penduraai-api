from rest_framework.fields import Field

from .services import token_decode
from .db import Ticket
from .validators import TicketScopeValidator, TicketSignatureValidator


class TicketTokenField(Field):

    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope')
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        data = token_decode(data)
        ticket = Ticket(data['scope'], data['key'])
        ticket.exist(raise_exception=True)
        return ticket

    def get_validators(self):
        validators = super().get_validators()
        validators += [
            TicketScopeValidator(self.scope),
            TicketSignatureValidator()
        ]
        return validators
