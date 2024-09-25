from rest_framework import serializers
from .models import Like, Pass

# 좋아요 패스
class LikeSerializer(serializers.ModelSerializer):
    # 좋아요
    class Meta:
        model = Like
        fields = ['user', 'liked_by', 'created_at']


class PassSerializer(serializers.ModelSerializer):
    # 패스
    class Meta:
        model = Pass
        fields = ['user', 'passed_by', 'created_at']