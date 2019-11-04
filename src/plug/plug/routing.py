from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from data_sync.consumers import WsConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('measurements/<int:cycles>/<int:interval>/<uuid:socket_id>/<str:room_name>', WsConsumer)
            ])
        )
    )
})
