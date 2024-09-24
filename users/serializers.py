from rest_framework import serializers
from accounts.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'distance', 'job', 'mbti', 'hobby']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['distance', 'job', 'mbti', 'hobby']