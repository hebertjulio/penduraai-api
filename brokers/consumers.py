import json

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .dictdb import Transaction


class TransactionConsumer(AsyncConsumer):

    async def get_url_route(self):
        kwargs = self.scope['url_route']['kwargs']
        return kwargs

    async def dispatch(self, message):
        url_route = await self.get_url_route()
        message.update(url_route)
        await super().dispatch(message)

    async def websocket_connect(self, event):
        tran = Transaction(event['pk'])
        if not tran.exist():
            await self.send({
                'type': 'websocket.reject'
            })
            await self.send({
                'type': 'websocket.close'
            })
            raise StopConsumer
        data = json.dumps(tran.data)
        await self.send({
            'type': 'websocket.accept'
        })
        await self.send({
            'type': 'websocket.send',
            'text': data
        })
        await self.channel_layer.group_add(
            event['pk'], self.channel_name
        )

    async def websocket_send(self, event):
        if 'text' in event and event['text']:
            await self.send({
                'type': 'websocket.send',
                'text': event['text'],
            })

    async def websocket_disconnect(self, event):
        await self.send({
            'type': 'websocket.close'
        })
        await self.channel_layer.group_discard(
            event['pk'], self.channel_name
        )
        raise StopConsumer
