import json
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

from moonbase_backend.asgi import application
from apps.chats.models import Chat
from apps.channels.models import Channel

User = get_user_model()

class ChatConsumerTests(TransactionTestCase):
    def setUp(self):
        async_to_sync(self.asyncSetUp)()

    async def asyncSetUp(self):
        self.channel_obj = await sync_to_async(Channel.objects.create)(
            name="general",
            description="General channel for testing"
        )
        self.user_obj = await sync_to_async(User.objects.create)(
            username="testuser",
            email="testuser@example.com",
            password=make_password("test")
        )
        self.url = "/ws/chats/general/"

    def test_connect_accepts(self):
        connected = async_to_sync(self._test_connect_accepts)()
        self.assertTrue(connected, "WebSocket connection should be accepted")

    async def _test_connect_accepts(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        await communicator.disconnect()
        return connected

    def test_disconnect(self):
        async_to_sync(self._test_disconnect)()

    async def _test_disconnect(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()
        with self.assertRaises(asyncio.TimeoutError):
            await communicator.receive_json_from(timeout=1)

    def test_send_valid_message(self):
        async_to_sync(self._test_send_valid_message)()

    async def _test_send_valid_message(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        payload = {"message": "Hello, world!", "username": "testuser"}
        await communicator.send_json_to(payload)
        response = await communicator.receive_json_from()
        self.assertEqual(response, payload)

        await asyncio.sleep(0.1)
        chat_obj = await sync_to_async(Chat.objects.filter(content="Hello, world!").first)()
        self.assertIsNotNone(chat_obj)
        author_username = await sync_to_async(lambda: chat_obj.author.username)()
        self.assertEqual(author_username, "testuser")
        channel_name = await sync_to_async(lambda: chat_obj.channel.name)()
        self.assertEqual(channel_name.lower(), "general")
        await communicator.disconnect()

    def test_send_invalid_json(self):
        async_to_sync(self._test_send_invalid_json)()

    async def _test_send_invalid_json(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.send_to("This is not JSON")
        with self.assertRaises(asyncio.TimeoutError):
            await communicator.receive_json_from(timeout=1)
        await communicator.disconnect()

    def test_send_message_missing_username(self):
        async_to_sync(self._test_send_message_missing_username)()

    async def _test_send_message_missing_username(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        payload = {"message": "Message without username"}
        await communicator.send_json_to(payload)
        response = await communicator.receive_json_from()
        self.assertEqual(response.get("message"), "Message without username")
        self.assertIsNone(response.get("username"))
        await asyncio.sleep(0.1)
        chat_obj = await sync_to_async(Chat.objects.filter(content="Message without username").first)()
        self.assertIsNone(chat_obj)
        await communicator.disconnect()

    def test_send_message_nonexistent_channel(self):
        async_to_sync(self._test_send_message_nonexistent_channel)()

    async def _test_send_message_nonexistent_channel(self):
        await sync_to_async(self.channel_obj.delete)()
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        payload = {"message": "Hello, no channel!", "username": "testuser"}
        await communicator.send_json_to(payload)
        response = await communicator.receive_json_from()
        self.assertEqual(response, payload)
        await asyncio.sleep(0.1)
        chat_obj = await sync_to_async(Chat.objects.filter(content="Hello, no channel!").first)()
        self.assertIsNone(chat_obj)
        await communicator.disconnect()

    def test_send_empty_message(self):
        async_to_sync(self._test_send_empty_message)()

    async def _test_send_empty_message(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        payload = {"message": "   ", "username": "testuser"}
        await communicator.send_json_to(payload)
        with self.assertRaises(asyncio.TimeoutError):
            await communicator.receive_json_from(timeout=1)
        await asyncio.sleep(0.1)
        chat_obj = await sync_to_async(Chat.objects.filter(content="   ").first)()
        self.assertIsNone(chat_obj)
        await communicator.disconnect()

    def test_send_message_with_extra_fields(self):
        async_to_sync(self._test_send_message_with_extra_fields)()

    async def _test_send_message_with_extra_fields(self):
        communicator = WebsocketCommunicator(application, self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        payload = {
            "message": "Extra fields test",
            "username": "testuser",
            "extra": "should be ignored",
            "another": 123
        }
        await communicator.send_json_to(payload)
        response = await communicator.receive_json_from()
        expected = {"message": "Extra fields test", "username": "testuser"}
        self.assertEqual(response, expected)
        await asyncio.sleep(0.1)
        chat_obj = await sync_to_async(Chat.objects.filter(content="Extra fields test").first)()
        self.assertIsNotNone(chat_obj)
        await communicator.disconnect()

    def test_chat_message_direct_call(self):
        async_to_sync(self._test_chat_message_direct_call)()

    async def _test_chat_message_direct_call(self):
        from apps.chats.consumers import ChatConsumer
        consumer = ChatConsumer()
        outputs = []

        async def dummy_send(text_data):
            outputs.append(json.loads(text_data))
        consumer.send = dummy_send
        event = {"message": "Direct test", "username": "testuser"}
        await consumer.chat_message(event)
        self.assertEqual(outputs, [{"message": "Direct test", "username": "testuser"}])
