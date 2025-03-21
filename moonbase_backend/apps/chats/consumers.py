import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from apps.chats.models import Chat
from apps.channels.models import Channel

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
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
        username = data.get('username')
        await self.save_chat(message, username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        username = event.get('username')
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def save_chat(self, message, username):
        channel_obj = Channel.objects.filter(name=self.room_name).first()
        user_obj = User.objects.filter(username=username).first()
        print(user_obj)
        if channel_obj and user_obj:
            Chat.objects.create(channel=channel_obj, author=user_obj, content=message)
