from django.urls import path
from .page_views import (
    chat_room, temp_friend_list
)

app_name = 'chats_pages'

urlpatterns = [
    path("chat_room/<int:room_id>/", chat_room),
    path("temp_friend_list/", temp_friend_list)
]
