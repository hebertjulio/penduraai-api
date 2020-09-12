from functools import wraps, partial

from .services import token_decode
from .db import Ticket


def use_ticket(func=None, discard=None, scope=None):
    if discard is None:
        raise ValueError

    if func is None:
        return partial(use_ticket, discard=discard, scope=scope)

    @wraps(func)
    def wapper(self, request, version, token):
        data = token_decode(token)
        self.ticket = Ticket(data['id'])
        self.ticket.exist(raise_exception=True)
        if scope and scope != self.ticket.scope:
            raise ValueError
        ret = func(self, request, version, token)
        if discard:
            self.ticket.delete()
        return ret

    return wapper
