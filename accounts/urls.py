from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserLoginView,
    UserLogoutView,
    UserSignupView,
    VerifyEmailView,
    UserProfileView,
    UserProfileUpdateView,
    UserInfoUpdateAPIView,
    UserLocationAPIView,
    CurrentUserView,
)

app_name = 'accounts'

urlpatterns = [
    # 사용자 관리
    path('api/login/', UserLoginView.as_view(), name='api_login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('api/current-user/', CurrentUserView.as_view(), name='current_user'),

    # 인증 및 보안
    path('api/signup/', UserSignupView.as_view(), name='api_signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    # 프로필 관리
    path('api/profile/', UserProfileView.as_view(), name='api_profile'),
    path('api/profile/<int:user_id>/', UserProfileView.as_view(), name='api_user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/update-info/', UserInfoUpdateAPIView.as_view(), name='profile_update_info'),
    path('profile/location/', UserLocationAPIView.as_view(), name='location'),

    # JWT 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
