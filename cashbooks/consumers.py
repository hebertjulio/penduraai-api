from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer


class RecordAwaitingAcceptConsumer(AsyncConsumer):

    http_user = False

    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
        })
        await self.send({
            'type': 'websocket.send',
            'text': self.channel_name,
        })

    async def websocket_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    async def websocket_disconnect(self, event):
        raise StopConsumer()
