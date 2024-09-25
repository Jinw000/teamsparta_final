from django.db import models
from accounts.models import User

# Create your models here.
# 좋아요 패스 기능
class Like(models.Model):
    # 좋아요 모델
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'liked_by')


class Pass(models.Model):
    #패스 모델
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    passed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'passed_by')
