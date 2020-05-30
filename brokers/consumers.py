import urllib.parse

from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .dictdb import Transaction


class TransactionConsumer(AsyncConsumer):

    async def get_id(self, query_string):
        qs = urllib.parse.parse_qs(query_string)
        _id = qs.get(b'id', (None,))[0]
        return _id if _id is None else _id.decode()

    async def websocket_connect(self, event):
        _id = await self.get_id(self.scope['query_string'])

        if _id is None:
            await self.send({
                "type": "websocket.disconnect",
            })
            return

        tran = Transaction(_id)
        if not tran.exist():
            await self.send({
                "type": "websocket.disconnect",
            })
            return

        await self.send({
            "type": "websocket.accept",
        })

        await self.send({
            "type": "websocket.send",
            "text": tran.status,
        })

        await self.channel_layer.group_add(_id, self.channel_name)

    async def websocket_send(self, event):

        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })

    async def websocket_disconnect(self, event):
        await self.send({
            "type": "websocket.close",
        })

        _id = await self.get_id(self.scope['query_string'])
        await self.channel_layer.group_discard(_id, self.channel_name)

        raise StopConsumer
