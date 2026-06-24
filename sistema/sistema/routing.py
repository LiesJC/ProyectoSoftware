from django.urls import path
from .consumers import *  # 🔹 cambiar CameraConsumer

websocket_urlpatterns = [
    path("ws/camara/", CameraConsumer.as_asgi()),  # 🔹 usar CameraStreamConsumer
    path("ws/vision/", VisionConsumer.as_asgi()),
]