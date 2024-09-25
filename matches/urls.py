from django.urls import path
from .views import LikeView, PassView

urlpatterns = [
    path('<int:user_profile_id>/like/', LikeView.as_view(), name='like-profile'),
    path('<int:user_profile_id>/pass/',
        PassView.as_view(), name='passed-profile'),
]
