from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# 사용자 관리
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]
    
    REQUIRED_FIELDS = ['username', 'nickname']
    
    nickname = models.CharField(max_length=20, unique=True, verbose_name="닉네임")
    email = models.EmailField(unique=True, verbose_name="이메일")
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="성별")
    bio = models.TextField(max_length=500, blank=True, verbose_name="자기소개")
    profile_picture = models.ImageField(upload_to='static/images',default='static/images/default_user.png', null=True, blank=True, verbose_name="프로필 사진")
    is_verified = models.BooleanField(default=False, verbose_name="인증 여부")
    last_active = models.DateTimeField(auto_now=True, verbose_name="마지막 활동")

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    def __str__(self):
        return self.username
    
# 인증 및 보안
    # 임시 사용자 모델 (이메일 인증용)
class TempUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    verification_code = models.CharField(max_length=6)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=User.GENDER_CHOICES, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
# 프로필 관리
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'nickname', 'password', 'birth_date', 'gender', 'bio', 'location', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'nickname': {'required': True},
        }

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            instance.profile_picture = profile_picture
        return super().update(instance, validated_data)

# 관심사 관리
class InterestCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="카테고리명")

    def __str__(self):
        return self.name

class Interest(models.Model):
    category = models.ForeignKey(InterestCategory, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=100, verbose_name="관심사")

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'interest')

    def __str__(self):
        return f"{self.user.username}의 관심사: {self.interest.name}"
    

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')  # 사용자와 연결
    location = models.CharField(max_length=255, blank=True)  # 주소 필드
    
    class Meta:
        unique_together = ('user', 'location')

    def __str__(self):
        return f"{self.user.nickname} - {self.location}"