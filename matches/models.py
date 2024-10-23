from django.db import models
from accounts.models import User
from django.conf import settings

# Create your models here.
# 좋아요 패스 기능
class Like(models.Model):
    # 좋아요 모델
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes_given')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user_profile', 'liked_by')

    def __str__(self):
        return f"{self.liked_by.username} likes {self.user_profile.username}"

class Pass(models.Model):
    # 패스 모델
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passes_given')
    passed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'passed_by')

    def __str__(self):
        return f"{self.passed_by.username} passed {self.user_profile.username}"
#매치 모델(사용자끼리의 상호 좋아요와 추천관계)
class Match(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    user1_likes_user2 = models.BooleanField(default=False)
    user2_likes_user1 = models.BooleanField(default=False)
    is_mutual = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"

    def update_mutual_status(self):
        self.is_mutual = self.user1_likes_user2 and self.user2_likes_user1
        self.save()

#친구 모델(요청및 수락 기능)
    #추후에 체팅 앱과 연동
class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', '대기중'),
        ('accepted', '수락됨'),
        ('rejected', '거절됨'),
    )
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} to {self.to_user.username} - {self.status}"

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"