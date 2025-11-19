from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ChatRoom, Message
from .serializers import UserSerializer, ChatRoomSerializer, MessageSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(chatroom_id=room_id).order_by('-timestamp')
    
class MarkMessageReadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.is_read = True
        message.save()
        return Response({"status": "marked as read"})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        active_user_id = request.user.id

        rooms = ChatRoom.objects.filter(users=active_user_id).order_by("-created_at")

        serializer = ChatRoomSerializer(
            rooms,
            many=True,
            context={"active_user_id": int(active_user_id)}
        )

        return Response(serializer.data)

class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.data.get("user_id")
        active_user_id = request.user.id

        user = User.objects.get(id=active_user_id)
        other_user = User.objects.get(id=user_id)

        existing = ChatRoom.objects.filter(users=user).filter(users=other_user).first()

        if existing:
            return Response(ChatRoomSerializer(existing).data)

        room = ChatRoom.objects.create()
        room.users.add(user, other_user)
        return Response(ChatRoomSerializer(room).data, status=201)
