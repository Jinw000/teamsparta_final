from rest_framework import serializers
# from accounts.models import User, UserInterest
from .models import User, Like, Dislike, UserInterest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'gender',
                  'birth_date', 'location', 'profile_picture']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        field = ["user", "interest"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'liked_by', 'created_at']


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['user', 'disliked_by', 'created_at']
