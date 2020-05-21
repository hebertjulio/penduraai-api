from channels.routing import ProtocolTypeRouter, URLRouter

from cashbooks.routing import routings


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        routings
    )
})
