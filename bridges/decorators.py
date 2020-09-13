from functools import wraps, partial

from .db import Ticket


def use_ticket(func=None, discard=None, scope=None):
    if discard is None:
        raise ValueError

    if func is None:
        return partial(use_ticket, discard=discard, scope=scope)

    @wraps(func)
    def wapper(self, request, version, ticket_id):
        self.ticket = Ticket(ticket_id)
        self.ticket.exist(raise_exception=True)
        if scope and scope != self.ticket.scope:
            raise ValueError
        ret = func(self, request, version, ticket_id)
        if discard:
            self.ticket.delete()
        return ret

    return wapper
