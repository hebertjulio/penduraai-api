from functools import wraps

from .services import send_ws_message


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        ticket = validated_data.pop('ticket')
        ret = func(self, validated_data)
        send_ws_message(ticket.key, 'confimed')
        ticket.discard()
        return ret
    return wapper
