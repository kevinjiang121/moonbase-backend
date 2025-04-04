import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.chats.models import Chat
from apps.channels.models import Channel
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.channel_id = int(self.scope['url_route']['kwargs']['room_name'])
        except (ValueError, TypeError):
            await self.close()
            return
        self.room_group_name = f'chat_{self.channel_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message = data.get('message')
        if not message or not message.strip():
            return

        user_id = data.get('user_id')
        sent_at, username = await self.save_chat(message, user_id)
        if sent_at is None:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'sent_at': sent_at,
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        sent_at = event.get('sent_at')
        username = event.get('username')
        if username is None:
            user_id = event.get('user_id')
            username = await self.get_username(user_id)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'sent_at': sent_at,
        }))

    @database_sync_to_async
    def save_chat(self, message, user_id):
        channel_obj = Channel.objects.filter(id=self.channel_id).first()
        user_obj = User.objects.filter(user_id=user_id).first()
        if channel_obj and user_obj:
            chat_obj = Chat.objects.create(
                channel=channel_obj,
                author=user_obj,
                content=message,
                username=user_obj.username
            )
            return chat_obj.sent_at.isoformat(), chat_obj.username
        return None, None

    @database_sync_to_async
    def get_username(self, user_id):
        user = User.objects.filter(user_id=user_id).first()
        return user.username if user else None
