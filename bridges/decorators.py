from functools import wraps

from .services import send_ws_message


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        ticket = validated_data.pop('ticket')
        ticket.usage = 1
        ret = func(self, validated_data)
        send_ws_message(ticket.id, 'confimed')
        return ret
    return wapper
