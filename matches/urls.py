from django.urls import path
from .views import (
    LikeView,
    PassView, 
    SendFriendRequestView, 
    RespondFriendRequestView, 
    FriendRequestListView,
    RecommendedMatchesView,
    NewMatchesView,
    )

app_name = 'matches'

urlpatterns = [
    path('recommended/', RecommendedMatchesView.as_view(), name='recommended'),
    path('like/', LikeView.as_view(), name='like-profile'),
    path('pass/', PassView.as_view(), name='passed-profile'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/<int:pk>/', RespondFriendRequestView.as_view(), name='respond_friend_request'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend_request_list'),
    path('new/', NewMatchesView.as_view(), name='new_matches'),
]
