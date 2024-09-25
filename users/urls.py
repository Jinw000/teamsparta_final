from django.urls import path
from .views import ProfileView, LikeView, DislikeView

urlpatterns = [
    path("<str:username>/", ProfileView.as_view()),
    path('<int:user_profile_id>/like/', LikeView.as_view(), name='like-profile'),
    path('<int:user_profile_id>/dislike/',
         DislikeView.as_view(), name='dislike-profile'),
]
