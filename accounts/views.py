from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from .models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
# Create your views here.

# 사용자 관리
class UserCreateAPIView(generics.CreateAPIView):
    """사용자 계정 생성 API 뷰"""
    serializer_class = UserSerializer

# 인증 및 보안
# 프로필 관리
class UserUpdateAPIView(generics.UpdateAPIView):
    """사용자 프로필 업데이트 API 뷰"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        profile_picture = self.request.data.get('profile_picture')
        if profile_picture:
            serializer.save(profile_picture=profile_picture)
        else:
            serializer.save()
class UserProfileAPIView(generics.RetrieveAPIView):
    """사용자 프로필 조회 API 뷰"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
class UserProfileImageUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        profile_picture = request.data.get('profile_picture')
        if not profile_picture:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object()
        user.profile_picture = profile_picture
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
class ProfileView(APIView):
    # 프로필 조회는 권한 없이도 가능, 조회가 목적이 아니면 기본 권한 설정 적용
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 조회
    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
# 관심사 관리
