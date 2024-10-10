import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from accounts.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.friend_id = self.scope['url_route']['kwargs']['friend_id']
        self.friend = await self.get_user(self.friend_id)
        # 사용자 둘이 같은 채팅방에 들어오는 코드
        users= sorted([self.scope['user'].id, self.friend.id])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # 메시지를 저장하고 브로드캐스트
        await self.save_message(self.scope['user'], self.friend, message)

        await self.channel_layer.group_send(
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
    def save_message(self, sender, receiver, message_content):
        Message.objects.create(sender=sender, receiver=receiver, content=message_content)
