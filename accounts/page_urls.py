from django.urls import path
from .page_views import (
    SignupPageView,
    LoginPageView,
    MainPageView,
    ProfilePageView,
    HomePageView
)

app_name = 'accounts_pages'

urlpatterns = [
    # frontend 관리
    path('', HomePageView.as_view(), name='home'),

    # 인증 및 보안
    path('signup/', SignupPageView.as_view(), name='signup_page'),
    path('login/', LoginPageView.as_view(), name='login_page'),
    
    # 로그인 페이지로 이동
    path('main/', MainPageView.as_view(), name='main_page'),
    
    # 프로필
    path('profile/', ProfilePageView.as_view(), name='profile_page'),
    path('profile/<int:user_id>/', ProfilePageView.as_view(), name='user_profile_page'),
]
