from channels.routing import ProtocolTypeRouter, URLRouter

import brokers.routing


routing = [
    *brokers.routing.urlpatterns
]

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(routing)
})
