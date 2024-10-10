from accounts.models import User
from django.db import models

# # 친구 요청 모델

# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(
#         CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(
#         CustomUser, related_name='received_requests', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     accepted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.from_user.username} -> {self.to_user.username} ({'Accepted' if self.accepted else 'Pending'})"

# # 친구 관계 모델

# class Friend(models.Model):
#     user = models.ForeignKey(
#         CustomUser, related_name='friends', on_delete=models.CASCADE)
#     friend = models.ForeignKey(
#         CustomUser, related_name='friend_of', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} is friends with {self.friend.username}"


# 채팅방 모델
class ChatRoom(models.Model):

    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def save(self, *args, **kwargs):
        # 채팅방 이름이 비어있을 경우 자동으로 설정
        if not self.name and self.participants.count() == 2:
            participants = list(self.participants.all())  # 참가자 목록을 리스트로 변환
            user = participants[0]  # 첫 번째 사용자
            friend = participants[1]  # 두 번째 사용자

            # 로그인한 사용자가 첫 번째라면 두 번째 사용자의 닉네임을 이름으로 설정
            if user == kwargs.get('request_user'):
                self.name = friend.nickname  # 친구의 닉네임을 채팅방 이름으로 설정
            else:
                self.name = user.nickname  # 자신의 닉네임이 아닌 경우 상대방 닉네임 설정
        
        super(ChatRoom, self).save(*args, **kwargs)
        
        def __str__(self):
            return self.name


# 메시지 모델
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # 읽음 여부 저장

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

