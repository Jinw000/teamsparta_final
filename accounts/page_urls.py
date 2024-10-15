from django.urls import path
from .page_views import (
    home,
    SignupPageView,
    LoginPageView
)

app_name = 'accounts_pages'

urlpatterns = [
    # frontend 관리
    path('', home, name='home'),

    # 인증 및 보안
    path('signup/', SignupPageView.as_view(), name='signup_page'),
    path('login/', LoginPageView.as_view(), name='login_page'),
    
    # 로그인 페이지로 이동
]
