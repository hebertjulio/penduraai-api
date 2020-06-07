from channels.routing import ProtocolTypeRouter, URLRouter

import notebooks.routing


routing = [
    *notebooks.routing.urlpatterns
]

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(routing)
})
