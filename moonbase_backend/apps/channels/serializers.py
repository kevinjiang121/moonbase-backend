from rest_framework import serializers
from .models import Channel, ChannelGroup

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class ChannelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelGroup
        fields = '__all__'
