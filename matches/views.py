from django.shortcuts import render
from rest_framework import generics, permissions
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Like, Pass
from .serializers import LikeSerializer, PassSerializer
# Create your views here.
# 좋아요


class LikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_profile_id = request.data.get('user_profile')
        try:
            user_profile = User.objects.get(id=user_profile_id)
        except User.DoesNotExist:
            return Response({'error': '유저 프로필을 찾을 수 없습니다 '}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(
            user_profile=user_profile,
            liked_by=request.user
        )

        if created:
            return Response({'message': '좋아요를 눌렀렀습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

# 패스


class PassView(generics.CreateAPIView):
    serializer_class = PassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_profile_id = request.data.get('user_profile')
        try:
            user_profile = User.objects.get(id=user_profile_id)
        except User.DoesNotExist:
            return Response({'error': '유저 프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        Pass, created = Pass.objects.get_or_create(
            user_profile=user_profile,
            passed_by=request.user
        )

        if created:
            return Response({'message': '패스하였습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 패스한 상대입니다.'}, status=status.HTTP_400_BAD_REQUEST)