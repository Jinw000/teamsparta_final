from django.db import models
from accounts.models import User

# 채팅방 모델
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)  # 채팅방 id
    participants = models.ManyToManyField(User, related_name='chatrooms')  # 채팅방 참가자들
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 메시지 모델
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)  # 메시지가 속한 방
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)  # 발신자
    content = models.TextField()  # 메시지 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 메시지 전송 시간
    is_read = models.BooleanField(default=False)  # 메시지가 읽혔는지 여부

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.content[:20]}'
