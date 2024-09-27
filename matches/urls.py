from django.urls import path
from .views import LikeProfileView

urlpatterns = [
    path('<int:user_profile_id>/like/', LikeProfileView.as_view(), name='like-profile'),
]
