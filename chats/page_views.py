from django.shortcuts import render
from .models import ChatRoom
from django.shortcuts import get_object_or_404

# url 리다이렉트
def chat_room(request, room_id):
    # 'room_id'로 채팅방을 검색
    room = get_object_or_404(ChatRoom, id=room_id)
    # 채팅방 정보를 템플릿으로 전달
    return render(request, 'chats/chat_room.html', {'room_id': room_id})

def temp_friend_list(request):
    return render(request, 'chats/temp_friend_list.html')
