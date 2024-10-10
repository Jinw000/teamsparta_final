from .models import ChatRoom
from matches.models import Friend
from rest_framework.generics import ListAPIView, CreateAPIView
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import User
from rest_framework.response import Response

# # 친구 요청 보내기

# @login_required
# def send_friend_request(request, to_user_id):
#     to_user = get_object_or_404(CustomUser, id=to_user_id)
#     if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
#         FriendRequest.objects.create(from_user=request.user, to_user=to_user)
#     return redirect('friend_list')

# # 친구 요청 수락하기

# @login_required
# def accept_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id)
#     if friend_request.to_user == request.user:
#         friend_request.accepted = True
#         friend_request.save()

#         # 양방향 친구 관계 생성
#         Friend.objects.create(
#             user=request.user, friend=friend_request.from_user)
#         Friend.objects.create(
#             user=friend_request.from_user, friend=request.user)

#     return redirect('friend_list')


# # 친구 목록 보기
# @login_required
# def friend_list(request):
#     # 사용자의 친구 목록 가져오기
#     friends = Friend.objects.filter(user=request.user)

#     # 사용자가 받은 친구 요청 중 아직 수락되지 않은 요청 가져오기
#     friend_requests = FriendRequest.objects.filter(
#         to_user=request.user, accepted=False)

#     return render(request, 'friends_list.html', {
#         'friends': friends,
#         'friend_requests': friend_requests
#     })


# 채팅방 목록을 보여주는 뷰
class ChatRoomListView(ListAPIView):

    def room_list(request):
        rooms = ChatRoom.objects.all()  # 모든 채팅방을 가져옴
    # 각 채팅방에 참가한 다른 사용자를 찾아서 저장
        room_participants = []
        for room in rooms:
            other_participants = room.participants.exclude(id=request.user.id)
            if other_participants.exists():
                room_participants.append({
                'room': room,
                'other_participant': other_participants.first()  # 첫 번째 참가자를 저장
            })

        return Response(room_participants)


# 친구 요청이 수락된 경우에만 채팅방 생성 또는 접근
class CreateChatRoomView(CreateAPIView):

    def create_or_get_chat_room(request, friend_id):
        friend = get_object_or_404(User, id=friend_id)

    # 친구 요청이 수락되었는지 확인
        if not Friend.objects.filter(user=request.user, friend=friend).exists():
            return redirect('friend_list')  # 친구 요청이 수락되지 않았다면 채팅방 생성 불가

    # 채팅방이 이미 있으면 반환, 없으면 생성
        room, created = ChatRoom.objects.get_or_create(
            participants__in=[request.user, friend],
            defaults={'name': f'{request.user.id}_{friend.id}'}
        )

        room.participants.add(request.user)
        room.participants.add(friend)

        return redirect('chat_room', room_id=room.id)