from functools import wraps

from .services import send_ws_message
from .tasks import push_notification


def use_ticket(func):
    @wraps(func)
    def wapper(self, validated_data):
        ticket = validated_data.pop('ticket')
        ret = func(self, validated_data)
        send_ws_message(ticket.key, 'confimed')
        push_notification.apply([ticket.key, '*message*'])
        ticket.discard()
        return ret
    return wapper
