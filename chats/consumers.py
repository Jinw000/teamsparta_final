import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from accounts.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # 사용자 둘이 같은 채팅방에 들어오는 코드
        self.room_group_name = f"chat_{self.room_id}"

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
        print(1111, text_data)
        data = json.loads(text_data)
        message = data['message']

        # # # 메시지를 저장하고 브로드캐스트
        print(self.scope['user'], message)
        await self.save_message(self.scope['user'], message) # (발신자, 메시지 내용)

        await self.channel_layer.group_send( # websocket에 전파하는 역할
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data,
                'sender': self.scope['user'].username,
            }
        )
        print(1111, self.scope['user'].username)
        print(1112, self.scope['user']) #DRF와 CHANNELS 어센틱케이션

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

    @database_sync_to_async # wsgi, asgi의 차이점을 알아야함. 서포트해주는 것
    def save_message(self, sender, message_content):
        Message.objects.create(sender=sender, content=message_content, room_id=self.room_id)

        # 1. 채팅 메시지 데이터 저장해보기 > 수신자 모델 설정
