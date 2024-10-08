from django.urls import path
from .page_views import (
    home,
    SignupPageView,
)

app_name = 'accounts_pages'

urlpatterns = [
    # frontend 관리
    path('', home, name='home'),

    # 인증 및 보안
    path('signup/', SignupPageView.as_view(), name='signup_page'),
]
