from rest_framework import serializers
from accounts.models import User, UserInterest

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'gender', 'birth_date', 'location', 'profile_picture']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['']

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        field = ["user", "interest"]
