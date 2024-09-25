from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer, ProfileUpdateSerializer, LikeSerializer, DislikeSerializer
from .models import User, Like, Dislike
# from accounts.models import User


class ProfileView(APIView):
    # 프로필 조회는 권한 없이도 가능, 조회가 목적이 아니면 기본 권한 설정 적용
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 조회
    def get(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    # 수정
    def put(self, request, user_id):
        # 현재 로그인된 사용자가 본인인지 확인
        if request.user.user_id != user_id:
            return Response({'detail': '본인의 프로필만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 사용자 조회
        user = User.objects.get(user_id=user_id)

        # Serializer로 데이터 업데이트
        serializer = ProfileUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class DislikeView(generics.CreateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_profile_id = request.data.get('user_profile')
        try:
            user_profile = User.objects.get(id=user_profile_id)
        except User.DoesNotExist:
            return Response({'error': '유저 프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        dislike, created = Dislike.objects.get_or_create(
            user_profile=user_profile,
            disliked_by=request.user
        )

        if created:
            return Response({'message': '패스하였습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 패스한 상대입니다.'}, status=status.HTTP_400_BAD_REQUEST)
