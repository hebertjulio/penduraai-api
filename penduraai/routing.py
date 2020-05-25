from channels.routing import ProtocolTypeRouter, URLRouter

from broker import routing as broker


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        broker.routing
    )
})
