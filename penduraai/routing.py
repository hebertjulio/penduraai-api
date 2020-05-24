from channels.routing import ProtocolTypeRouter, URLRouter

from books.routing import urlpatterns as books_urlpatterns


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        books_urlpatterns
    )
})
