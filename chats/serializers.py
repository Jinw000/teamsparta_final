from rest_framework import serializers
from .models import ChatRoom, Message

# 메시지 목록을 위한 Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['sender_username', 'content', 'timestamp']

# 메시지 생성 Serializer
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']

# 채팅방 직렬화
class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants']
