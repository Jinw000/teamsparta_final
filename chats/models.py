from django.db import models
from accounts.models import User

# 채팅방 모델
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)  # 채팅방 이름
    participants = models.ManyToManyField(User, related_name='chatrooms')  # 채팅방 참가자들
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜

    def __str__(self):
        return self.name

# 메시지 모델
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)  # 메시지가 속한 방
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)  # 메시지 보낸 사람
    content = models.TextField()  # 메시지 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 메시지 전송 시간

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}' # 발신자의 이름과 메시지 내용의 처음 20글자를 결합하여 문자열을 반환
