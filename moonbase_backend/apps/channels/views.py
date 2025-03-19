from django.shortcuts import render
from rest_framework import viewsets
from .models import Channel
from .serializers import ChannelSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all().order_by('created_at')
    serializer_class = ChannelSerializer
