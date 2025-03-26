from rest_framework import viewsets
from apps.chats.models import Chat
from apps.chats.serializers import ChatSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('sent_at')
    serializer_class = ChatSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        channel_id = self.request.query_params.get('channel')
        if channel_id:
            queryset = queryset.filter(channel_id=channel_id)
        return queryset
