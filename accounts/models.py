from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
        ('O', '기타'),
    ]

    nickname = models.CharField(max_length=20, unique=True, verbose_name="닉네임")
    email = models.EmailField(unique=True, verbose_name="이메일")
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="성별")
    bio = models.TextField(max_length=500, blank=True, verbose_name="자기소개")
    location = models.CharField(max_length=100, blank=True, verbose_name="위치")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="프로필 사진")
    is_verified = models.BooleanField(default=False, verbose_name="인증 여부")
    last_active = models.DateTimeField(auto_now=True, verbose_name="마지막 활동")

    def __str__(self):
        return self.username
    
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