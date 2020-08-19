from asgiref.sync import sync_to_async

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .services import decode_token
from .models import Ticket
from .exceptions import TokenEncodeException


class BaseConsumer(AsyncConsumer):

    async def get_url_route(self):
        kwargs = self.scope['url_route']['kwargs']
        return kwargs

    async def dispatch(self, message):
        url_route = await self.get_url_route()
        message.update(url_route)
        await super().dispatch(message)

    async def accept(self):
        await super().send({
            'type': 'websocket.accept'
        })

    async def send(self, message):
        if message:
            await super().send({
                'type': 'websocket.send',
                'text': message,
            })

    async def reject(self):
        await super().send({
            'type': 'websocket.reject'
        })

    async def close(self):
        await super().send({
            'type': 'websocket.close'
        })
        raise StopConsumer


class TicketConsumer(BaseConsumer):

    async def websocket_connect(self, event):
        try:
            payload = decode_token(event['token'])
            pk = payload['id']
            obj = await sync_to_async(Ticket.objects.get)(pk=pk)
            await self.accept()
            await self.send(str(obj.usage))
            await self.channel_layer.group_add(str(pk), self.channel_name)
        except (Ticket.DoesNotExist,
                TokenEncodeException):
            await self.reject()
            await self.close()

    async def websocket_send(self, event):
        if 'text' in event:
            await self.send(event['text'])

    async def websocket_receive(self, event):
        pass

    async def websocket_disconnect(self, event):
        group = str(event['token'])
        await self.close()
        await self.channel_layer.group_discard(group, self.channel_name)
