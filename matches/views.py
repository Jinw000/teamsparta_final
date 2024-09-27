from django.shortcuts import render
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# 좋아요

class LikeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nickname):
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return Response({"message": "회원님을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        liked_profile = User.objects.filter(Profile__likes__user=user)

        if not liked_profile.exists():
            return Response({"message": "0"}, status=status.HTTP_204_NO_CONTENT)

        serializer = LikeSerializer(liked_profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)