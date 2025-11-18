from django.test import TestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from chat.models import ChatRoom, Message
from chat_backend.asgi import application

User = get_user_model()

class ChatConsumerTest(TestCase):

    async def async_setup(self):
        self.user1 = await User.objects.acreate(username='testuser1')
        self.user2 = await User.objects.acreate(username='testuser2')
        self.room = await ChatRoom.objects.acreate()
        await self.room.users.aadd(self.user1, self.user2)

    async def test_single_message_delivery(self):
        """
        Tests that a message sent by a user in a chat room
        is delivered only once to all participants in that room.
        """
        await self.async_setup()

        # Communicator for user 1
        communicator1 = WebsocketCommunicator(application, f"/ws/chat/{self.room.id}/")
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)

        # Communicator for user 2
        communicator2 = WebsocketCommunicator(application, f"/ws/chat/{self.room.id}/")
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)

        # User 1 sends a message
        await communicator1.send_json_to({
            "type": "message",
            "text": "Hello, world!",
            "sender_id": self.user1.id
        })

        # Check if user 1 (the sender) receives the message
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1['type'], 'message')
        self.assertEqual(response1['message']['text'], 'Hello, world!')

        # Check if user 2 (the receiver) receives the message
        response2 = await communicator2.receive_json_from()
        self.assertEqual(response2['type'], 'message')
        self.assertEqual(response2['message']['text'], 'Hello, world!')

        # Verify that there are no more messages for either user
        self.assertTrue(await communicator1.receive_nothing(timeout=0.1))
        self.assertTrue(await communicator2.receive_nothing(timeout=0.1))

        # Disconnect communicators
        await communicator1.disconnect()
        await communicator2.disconnect()
