from django.urls import path
from . import views

urlpatterns = [
    path('<str:channel_name>/', views.chat_room, name='chat_room'),
]