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
