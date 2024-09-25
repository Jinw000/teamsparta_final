from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class user(models.Model):
    pass


class Like(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'liked_by')


class Dislike(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    disliked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'disliked_by')
