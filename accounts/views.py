from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, UserLoginSerializer, UserLocationSerializer
from .models import User, TempUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .utils import generate_verification_code, send_verification_email
# Create your views here.

# 사용자 관리


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return Response({"message": "회원탈퇴한 아이디입니다."}, status=status.HTTP_403_FORBIDDEN)
            refresh = RefreshToken.for_user(user)
            serializer = UserLoginSerializer(user)
            response_data = serializer.data
            response_data.update({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "아이디 또는 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "로그아웃 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# 인증 및 보안


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = generate_verification_code()
            TempUser.objects.create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                verification_code=verification_code,
                nickname=serializer.validated_data.get('nickname'),
                birth_date=serializer.validated_data.get('birth_date'),
                gender=serializer.validated_data.get('gender'),
                bio=serializer.validated_data.get('bio')
            )
            send_verification_email(
                serializer.validated_data['email'], verification_code)
            return Response({"message": "인증 코드가 이메일로 전송되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        temp_user = TempUser.objects.filter(email=email, verification_code=code).first()
        if temp_user:
            user = User.objects.create_user(
                username=temp_user.username,
                email=temp_user.email,
                password=temp_user.password,
                nickname=temp_user.username,  # 임시로 username을 nickname으로 사용
                is_verified=True
            )
            # TempUser에 저장된 추가 정보가 있다면 여기서 User 객체에 추가
            if hasattr(temp_user, 'birth_date'):
                user.birth_date = temp_user.birth_date
            if hasattr(temp_user, 'gender'):
                user.gender = temp_user.gender
            if hasattr(temp_user, 'bio'):
                user.bio = temp_user.bio
            user.profile_picture = 'static/images/default_user.png'
            
            user.save()
            
            temp_user.delete()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "잘못된 인증 코드입니다."}, status=status.HTTP_400_BAD_REQUEST)
# 프로필 관리


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        if user_id:
            # 특정 사용자의 프로필 조회
            user = get_object_or_404(User, id=user_id)
        else:
            # 현재 로그인한 사용자의 프로필 조회
            user = request.user

        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # 프로필 이미지 처리
            profile_picture = request.data.get('profile_picture')
            if profile_picture:
                user.profile_picture = profile_picture

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

# 위치 정보 관리
class UserLocationAPIView(generics.CreateAPIView):
    serializer_class = UserLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
# 관심사 관리
