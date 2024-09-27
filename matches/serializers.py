from rest_framework import serializers
from .models import Like

# 좋아요 패스
class LikeSerializer(serializers.ModelSerializer):
    # 좋아요
    class Meta:
        model = Like
        fields = ['user', 'profile']