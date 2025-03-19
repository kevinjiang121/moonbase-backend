from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'channel', 'author', 'content', 'sent_at']
        read_only_fields = ['id', 'sent_at']
