from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInterest, UserLocation
from django.contrib.auth import authenticate

User = get_user_model()


# 사용자 관리
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'password', 'birth_date', 'gender', 'bio']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'nickname': {'required': True},
        }

    def validate_nickname(self, value):
        if self.instance:  # 업데이트 시
            if User.objects.exclude(pk=self.instance.pk).filter(nickname=value).exists():
                raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        else:  # 생성 시
            if User.objects.filter(nickname=value).exists():
                raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def validate_email(self, value):
        if self.instance:  # 업데이트 시
            if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        else:  # 생성 시
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        user.birth_date = validated_data.get('birth_date')
        user.gender = validated_data.get('gender')
        user.bio = validated_data.get('bio', '')
        user.location = validated_data.get('location', '')
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data
# 인증 및 보안
# 프로필 관리
class ProfileSerializer(serializers.ModelSerializer):
    # 프로필 조회
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'gender', 'birth_date', 'location', 'profile_picture']

# 위치 정보 관리
class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('user', 'location')  # 반환할 필드들

# 관심사 관리
class InterestSerializer(serializers.ModelSerializer):
    # 관심사
    class Meta:
        model = UserInterest
        field = ["user", "interest"]