from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

