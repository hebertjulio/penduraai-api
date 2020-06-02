from channels.routing import ProtocolTypeRouter, URLRouter

from brokers.routing import routing as brokers_routing


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(brokers_routing)
})
