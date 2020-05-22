from channels.routing import ProtocolTypeRouter, URLRouter

from cashbooks.routing import paths as cashbooks_paths


application = ProtocolTypeRouter({
    'websocket': URLRouter(
        cashbooks_paths
    )
})
