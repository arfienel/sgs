from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:channel_name>/", views.chat_room, name="chat_room"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create_server/", views.create_server, name="create_server"),
    path("create_channel/<int:server_id>/", views.create_channel, name="create_channel"),
    path("server_detail/<int:server_id>/", views.server_detail, name="server_detail"),
]