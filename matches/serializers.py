from rest_framework import serializers
from .models import Like, Pass, FriendRequest

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


#친구 요청 및 수락
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user']
        read_only_fields = ['from_user', 'created_at']