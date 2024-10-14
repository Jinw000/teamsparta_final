from django.urls import path
from .views import ChatRoomMessageView, CreateOneToOneChatRoomView

urlpatterns = [
    # 1:1 채팅방의 메시지 내용 조회 및 메시지 전송
    path('api/rooms/<int:room_id>/messages/', ChatRoomMessageView.as_view(), name='chat_room_messages'),

    # 1:1 채팅방 생성
    path('api/rooms/create/<int:user_id>/', CreateOneToOneChatRoomView.as_view(), name='create_one_to_one_chat_room'),
]
