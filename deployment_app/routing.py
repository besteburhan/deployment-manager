from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/deployment_app/deployment_notes/(?P<note_id>[^/]+)/$', consumers.CommentConsumer),
]

# Root routing is deployment_manager/routing.py