import json
import uuid

from asgiref.sync import sync_to_async

from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer

from .serializers import RecordCreateSerializer
from .storages import Transaction
from .services import foreignkey_adjust


class TransactionConsumer(AsyncConsumer):

    http_user = False

    serializers = {
        'record-create': RecordCreateSerializer
    }

    async def websocket_connect(self, _):
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):

        @sync_to_async
        def persist(operation, data, channel_name):
            serializer = self.serializers[operation](data=data)
            if serializer.is_valid():
                tran = Transaction(str(uuid.uuid4()))
                tran.channel_name = channel_name
                tran.data = json.dumps(foreignkey_adjust(data))
                serializer.save()
                return {'transaction': tran.key}
            return serializer.errors

        if 'text' in event and event['text']:
            data = json.loads(event['text'])
            data = await persist(
                data['operation'], data['data'],
                self.channel_name
            )
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(data),
            })

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
        raise StopConsumer()
