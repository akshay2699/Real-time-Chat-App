from django.urls import path
from .views import (
    LoginView,
    UserListView,
    ChatRoomListView,
    CreateRoomView,
    MessageListView,
    MarkMessageReadView
)

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("users/", UserListView.as_view()),
    path("rooms/", ChatRoomListView.as_view()),
    path("rooms/create/", CreateRoomView.as_view()),
    path("rooms/<int:room_id>/messages/", MessageListView.as_view()),
    path("messages/<int:message_id>/read/", MarkMessageReadView.as_view()),
]
