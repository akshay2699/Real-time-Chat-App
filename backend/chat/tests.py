from django.test import TestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from chat.models import ChatRoom, Message
from chat_backend.asgi import application
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_unauthorized_access(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)

    def test_authorized_access(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

class ChatConsumerTest(TestCase):

    async def async_setup(self):
        self.user1 = await User.objects.acreate_user(username='testuser1', password='password')
        self.user2 = await User.objects.acreate_user(username='testuser2', password='password')
        self.token1 = await Token.objects.acreate(user=self.user1)
        self.token2 = await Token.objects.acreate(user=self.user2)
        self.room = await ChatRoom.objects.acreate()
        await self.room.users.aadd(self.user1, self.user2)

    async def test_single_message_delivery(self):
        """
        Tests that a message sent by a user in a chat room
        is delivered only once to all participants in that room.
        """
        await self.async_setup()

        # Communicator for user 1
        communicator1 = WebsocketCommunicator(application, f"/ws/chat/{self.room.id}/?token={self.token1.key}")
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)

        # Communicator for user 2
        communicator2 = WebsocketCommunicator(application, f"/ws/chat/{self.room.id}/?token={self.token2.key}")
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)

        # User 1 sends a message
        await communicator1.send_json_to({
            "type": "message",
            "text": "Hello, world!",
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
