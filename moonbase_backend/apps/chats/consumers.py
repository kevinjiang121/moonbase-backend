import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from apps.chats.models import Chat
from apps.channels.models import Channel

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.channel_id}'
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
        if not text_data.strip():
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        
        message = data.get('message')
        user_id = data.get('user_id')
        await self.save_chat(message, user_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        user_id = event.get('user_id')
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))

    @database_sync_to_async
    def save_chat(self, message, user_id):
        channel_obj = Channel.objects.filter(id=self.channel_id).first()
        user_obj = User.objects.filter(user_id=user_id).first()
        if channel_obj and user_obj:
            Chat.objects.create(channel=channel_obj, author=user_obj, content=message)
