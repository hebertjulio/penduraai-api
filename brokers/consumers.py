import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .dictdb import Transaction


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

    async def send(self, text):
        if text:
            await super().send({
                'type': 'websocket.send',
                'text': text,
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

    async def group_add(self, name):
        if name:
            await self.channel_layer.group_add(
                name, self.channel_name
            )

    async def group_discard(self, name):
        if name:
            await self.channel_layer.group_discard(
                name, self.channel_name
            )


class TransactionConsumer(BaseConsumer):

    async def websocket_connect(self, event):
        tran = Transaction(event['pk'])
        if tran.exist():
            await self.accept()
            await self.send(json.dumps(tran.data))
            await self.group_add(event['pk'])
        else:
            await self.reject()
            await self.close()

    async def websocket_send(self, event):
        if 'text' in event:
            await self.send(event['text'])

    async def websocket_disconnect(self, event):
        await self.close()
        await self.group_discard(event['pk'])
