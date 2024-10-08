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
)

app_name = 'accounts'

urlpatterns = [
    # 사용자 관리
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # 인증 및 보안
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    # 프로필 관리
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile/update-info/', UserInfoUpdateAPIView.as_view(), name='profile_update_info'),
    path('profile/location/', UserLocationAPIView.as_view(), name='location'),

    # JWT 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
