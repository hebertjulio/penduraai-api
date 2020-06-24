import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .models import Transaction


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


class TransactionConsumer(BaseConsumer):

    async def websocket_connect(self, event):
        try:
            pk = event['pk']
            transaction = Transaction.objects.get(pk=pk)
            await self.accept()
            await self.send(json.dumps(dict(transaction)))
            await self.channel_layer.group_add(
                event['pk'], self.channel_name)
        except Transaction.DoesNotExist:
            await self.reject()
            await self.close()

    async def websocket_send(self, event):
        if 'text' in event:
            await self.send(event['text'])

    async def websocket_receive(self, event):
        pass

    async def websocket_disconnect(self, event):
        await self.close()
        await self.channel_layer.group_discard(
            event['pk'], self.channel_name)
