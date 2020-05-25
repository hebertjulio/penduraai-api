import json

from asgiref.sync import sync_to_async

from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer

from .serializers import TransactionSerializer


class TransactionConsumer(AsyncConsumer):

    http_user = False

    async def websocket_connect(self, _):
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        if ('text' not in event
                or not event['text'].strip()):
            return

        @sync_to_async
        def persist(data):
            serializer = TransactionSerializer(data=data)
            if serializer.is_valid():
                data = serializer.save()
                return data
            return serializer.errors

        data = json.loads(event['text'])
        data.update({'channel_name': self.channel_name})
        data = await persist(data)
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data),
        })

    async def websocket_send(self, event):
        if ('text' not in event
                or not event['text'].strip()):
            return

        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })

    async def websocket_disconnect(self, event):
        await self.send({
            'type': 'websocket.close'
        })
        raise StopConsumer()
