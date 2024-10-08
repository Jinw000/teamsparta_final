from django.shortcuts import render
from rest_framework import generics, permissions, status
from accounts.models import User
from rest_framework.response import Response
from .models import Like, Pass, Match, FriendRequest
from .serializers import LikeSerializer, PassSerializer, FriendRequestSerializer
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

        match, created = Match.objects.get_or_create(
            user1=request.user,
            user2=user_profile,
            defaults={'user1_likes_user2': True}
        )

        if not created:
            if match.user1 == request.user:
                match.user1_likes_user2 = True
            else:
                match.user2_likes_user1 = True
            match.update_mutual_status()
            match.save()

        like, created = Like.objects.get_or_create(
            user_profile=user_profile,
            liked_by=request.user
        )

        if created:
            return Response({'message': '좋아요를 눌렀습니다.'}, status=status.HTTP_201_CREATED)
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
            passed_by=Pass.request.user
        )

        if created:
            return Response({'message': '패스하였습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 패스한 상대입니다.'}, status=status.HTTP_400_BAD_REQUEST)


#친구요청 및 수락
class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user')
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': '유저를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == to_user:
            return Response({'error': '자기 자신에게 친구 요청을 보낼 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
            defaults={'status': 'pending'}
        )

        if created:
            return Response({'message': '친구 요청을 보냈습니다.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '이미 친구 요청을 보냈습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class RespondFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        action = request.data.get('action')

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            # 여기에 친구 관계를 설정하는 로직을 추가할 수 있습니다.
            return Response({'message': '친구 요청을 수락했습니다.'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'message': '친구 요청을 거절했습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '잘못된 액션입니다.'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')