from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import MessageSerializer, MessageCreateSerializer, ChatRoomSerializer
from django.contrib.auth.models import User


# 1:1 채팅방에서 메시지 주고받기 및 조회
class ChatRoomMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        # 채팅방(room_id)에 로그인된 사용자가 속해 있는지 확인
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in room.participants.all():
            return Response({"error": "You do not have permission to view this chat room."}, status=status.HTTP_403_FORBIDDEN)

        # 채팅방의 모든 메시지 가져오기
        messages = Message.objects.filter(room=room).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        # 채팅방(room_id)에 로그인된 사용자가 속해 있는지 확인
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user not in room.participants.all():
            return Response({"error": "You do not have permission to send a message in this chat room."}, status=status.HTTP_403_FORBIDDEN)

        # 메시지 생성
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, room=room)  # 로그인한 사용자를 발신자로 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 1:1 채팅방 생성 뷰
class CreateOneToOneChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # 채팅 상대방을 찾음
        other_user = get_object_or_404(User, id=user_id)

        # 두 명의 사용자만 참가할 수 있는 1:1 채팅방이 이미 있는지 먼저 확인
        room = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()

        if room:
            return Response({"message": "Chat room already exists.", "room_id": room.id}, status=status.HTTP_200_OK)

        # 채팅방이 없으면 새로운 1:1 채팅방 생성
        room = ChatRoom.objects.create(name=f"Chat between {request.user.username} and {other_user.username}")
        room.participants.add(request.user)
        room.participants.add(other_user)

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
