from django.shortcuts import render
from rest_framework import viewsets
from .models import Chat
from .serializers import ChatSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('sent_at')
    serializer_class = ChatSerializer
