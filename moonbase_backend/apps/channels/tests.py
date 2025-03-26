from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.channels.models import Channel, ChannelGroup

class ChannelGroupAPITestCase(APITestCase):
    def test_create_channel_group_success(self):
        url = reverse('create-channel-group')
        data = {
            "name": "Category A",
            "description": "Main category for discussion channels"
        }
        response = self.client.post(url, data, format='json')
        group = ChannelGroup.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChannelGroup.objects.count(), 1)
        self.assertEqual(group.name, "Category A")

    def test_create_channel_group_invalid(self):
        url = reverse('create-channel-group')
        data = {
            "name": "",
            "description": "Invalid group with no name"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_channel_group_success(self):
        group = ChannelGroup.objects.create(name="Category B", description="Category to delete")
        url = reverse('delete-channel-group', kwargs={'pk': group.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChannelGroup.objects.count(), 0)

    def test_delete_channel_group_invalid(self):
        url = reverse('delete-channel-group', kwargs={'pk': 9999})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_channel_group_detail_success(self):
        group = ChannelGroup.objects.create(name="Test Group", description="Test group detail")
        url = reverse('get-channel-group', kwargs={'pk': group.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), group.name)
        self.assertEqual(response.data.get('description'), group.description)
    
    def test_get_channel_group_detail_failure(self):
        url = reverse('get-channel-group', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChannelAPITestCase(APITestCase):
    def setUp(self):
        self.group = ChannelGroup.objects.create(name="Category X", description="Some category")

    def test_create_channel_success(self):
        url = reverse('create-channel')
        data = {
            "name": "General",
            "description": "General discussion channel",
            "channel_type": "text",
            "group": self.group.pk
        }
        response = self.client.post(url, data, format='json')
        channel = Channel.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(channel.name, "General")
        self.assertEqual(channel.group, self.group)

    def test_create_channel_invalid(self):
        url = reverse('create-channel')
        data = {
            "name": "",
            "description": "Channel with no name",
            "channel_type": "text",
            "group": self.group.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_channel_success(self):
        channel = Channel.objects.create(
            name="General", 
            description="General discussion channel", 
            channel_type="text", 
            group=self.group
        )
        url = reverse('delete-channel', kwargs={'pk': channel.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Channel.objects.count(), 0)

    def test_delete_channel_invalid(self):
        url = reverse('delete-channel', kwargs={'pk': 9999})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_channel_detail_success(self):
        channel = Channel.objects.create(
            name="Test Channel",
            description="Test channel detail",
            channel_type="text",
            group=self.group
        )
        url = reverse('get-channel', kwargs={'pk': channel.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), channel.name)
        self.assertEqual(response.data.get('description'), channel.description)
    
    def test_get_channel_detail_failure(self):
        url = reverse('get-channel', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
