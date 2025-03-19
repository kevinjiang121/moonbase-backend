from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Channel, ChannelGroup
from .serializers import ChannelSerializer, ChannelGroupSerializer

# Endpoint to create a channel
class CreateChannelView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to delete a channel by its primary key
class DeleteChannelView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        channel = get_object_or_404(Channel, pk=pk)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Endpoint to create a channel group
class CreateChannelGroupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChannelGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to delete a channel group by its primary key
class DeleteChannelGroupView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        channel_group = get_object_or_404(ChannelGroup, pk=pk)
        channel_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
