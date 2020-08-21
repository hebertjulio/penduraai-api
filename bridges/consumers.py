from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .services import get_token_data
from .exceptions import TokenEncodeException


class BaseConsumer(AsyncConsumer):

    def get_url_route(self):
        kwargs = self.scope['url_route']['kwargs']
        return kwargs

    async def dispatch(self, message):
        url_route = self.get_url_route()
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
            data = get_token_data(event['token'])
            group = data['key']
            await self.accept()
            await self.channel_layer.group_add(group, self.channel_name)
        except TokenEncodeException:
            await self.reject()
            await self.close()

    async def websocket_send(self, event):
        if 'text' in event:
            await self.send(event['text'])

    async def websocket_receive(self, event):
        pass

    async def websocket_disconnect(self, event):
        try:
            data = get_token_data(event['token'])
            group = data['key']
            await self.channel_layer.group_discard(group, self.channel_name)
        except TokenEncodeException:
            pass
        await self.close()
