import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from accounts.models import User
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # 사용자 둘이 같은 채팅방에 들어오는 코드
        # 방 id를 사용하여, 그룹 이름을 얻습니다.
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )  # 현재 채널을 그룹에 추가

        await self.accept()  # websocket 연결 수락

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']  # 수신된 json에서 파이썬 형식의 메시지를 추출합니다.

        if self.scope['user'].is_authenticated:
            sender = self.scope['user']
            room = await self.get_or_create_room(self.room_id)

            await self.save_message(sender, room, message)
        # # # # 메시지를 저장하고 브로드캐스트
        # print(self.scope['user'], message)
        # await self.save_message(self.scope['user'], message) # (발신자, 메시지 내용)

        # room_id = self.room_id
        await self.channel_layer.group_send(  # websocket에 전파하는 역할
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def save_message(self, sender, room, message):
        return Message.objects.create(
            room=room,
            sender=sender,
            content=message
        )

    @database_sync_to_async
    def get_previous_messages(self, room):
        return Message.objects.filter(room=room).order_by('timestamp')
