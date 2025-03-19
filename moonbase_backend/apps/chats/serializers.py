from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'channel', 'author', 'content', 'sent_at']
        read_only_fields = ['id', 'sent_at']
