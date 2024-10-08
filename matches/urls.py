from django.urls import path
from .views import (
    LikeView,
    PassView, 
    SendFriendRequestView, 
    RespondFriendRequestView, 
    FriendRequestListView,
    )

urlpatterns = [
    path('<int:user_profile_id>/like/', LikeView.as_view(), name='like-profile'),
    path('<int:user_profile_id>/pass/', PassView.as_view(), name='passed-profile'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/<int:pk>/', RespondFriendRequestView.as_view(), name='respond_friend_request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend_request_list'),
]
