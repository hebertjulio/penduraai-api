from channels.routing import ProtocolTypeRouter, URLRouter

from books import routing as books


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        books.routing
    )
})
