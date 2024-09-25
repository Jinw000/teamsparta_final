from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateAPIView, UserUpdateAPIView, UserProfileAPIView, UserProfileImageUpdateAPIView

app_name = 'accounts'

urlpatterns = [
    # 회원가입
    path('signup/', UserCreateAPIView.as_view(), name='signup'),
    
    # 프로필 수정
    path('profile/update/', UserUpdateAPIView.as_view(), name='profile_update'),
    
    # 프로필 조회
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    
    # JWT 토큰 (로그인)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 프로필 이미지 업데이트
    path('profile/image/', UserProfileImageUpdateAPIView.as_view(), name='profile_image_update'),
    
    # 비밀번호 변경 (선택적)
    # path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    
    # 비밀번호 재설정 (선택적)
    # path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]