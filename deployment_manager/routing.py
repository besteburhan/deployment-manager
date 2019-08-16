from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import deployment_app.routing

# application found via settings.py with the ASGI_APPLICATION = 'deployment_manager.routing.application' row
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            deployment_app.routing.websocket_urlpatterns
        )
    ),
})

# This root routing configuration specifies that
# when a connection is made to the Channels development
# server, the ProtocolTypeRouter will first inspect the
# type of connection. If it is a WebSocket connection
# (ws:// or wss://), the connection will be given to
# the AuthMiddlewareStack.
#
# The URLRouter will examine the HTTP path of the
# connection to route it to a particular consumer,
# based on the provided url patterns.
