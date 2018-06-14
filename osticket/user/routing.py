# chat/routing.py
from django.conf.urls import url

from . import consumers
from agent import views

websocket_urlpatterns = [
    url(r'^ws/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/user/(?P<username>[^/]+)/$', consumers.UserConsumer),
    url(r'^ws/agent/(?P<username>[^/]+)/$', consumers.AgentConsumer),
]
