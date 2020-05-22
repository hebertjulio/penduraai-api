from channels.routing import ProtocolTypeRouter, URLRouter

from cashbooks import routing as cashbooks


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        cashbooks.routing
    )
})
