from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'password', 'birth_date', 'gender', 'bio', 'location']
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