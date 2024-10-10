from django.urls import path
from . import views

urlpatterns = [
    path('room_list/<int:room_id>/', views.ChatRoomListView.as_view()),
    path('chat_room/with/<str:user_id>/', views.CreateChatRoomView.as_view())
]