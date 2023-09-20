from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings

from django.http import JsonResponse, HttpResponseForbidden
from pusher import Pusher

from accounts.models import CustomUser
from .serializers import ConversationSerializer, MessageSerializer, MessageStatusSerializer
from .models import Conversation, Message, MessageStatus
from .permissions import IsParticipantInConversation

class ConversationView(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]

    def get_queryset(self):
        q = Conversation.objects.filter(participants=self.request.user)
        return q

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save(participants=[self.request.user], owner=request.user)
            for user_id in participant_ids:
                if user_id != request.user.id:
                    user = CustomUser.objects.get(pk=user_id)
                    conversation.participants.add(user)
                    conversation.title = user.name if user.name else user.username
                    conversation.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400)


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantInConversation]

    def get_queryset(self, *args, **kwargs):
        c_id = self.kwargs.get('conversation_id')
        self.queryset = Message.objects.filter(conversation_id=c_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        c_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(pk=c_id)

        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(status=201, data=serializer.data)
        return Response(status=400, data=serializer.errors)


class MessageStatusView(APIView):
    permission_classes = [IsParticipantInConversation]
    serializer_class = MessageStatusSerializer

    def put(self, request, *args, **kwargs):
        message = Message.objects.get(id=self.kwargs.get('message_id'))
        if self.request.user != message.sender: 
            msg = get_object_or_404(MessageStatus, message=message)
            msg.seen_by.add(self.request.user)    
            serializer = self.serializer_class(instance=msg)
            return Response(status=201, data=serializer.data)
        return Response(status=400)


from django.views.decorators.csrf import csrf_exempt  # Import the csrf_exempt decorator
from django.http import HttpResponseBadRequest  # Import HttpResponseBadRequest

class AuthView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        user = request.user
        channel_name = request.data.get('channel_name')
        socket_id = request.data.get('socket_id')
        pusher = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )

        payload = pusher.authenticate(
            channel=channel_name,
            socket_id=socket_id,
            custom_data={
                'user_id': request.user.id,
                'user_info': {  # We can put whatever we want here
                    'username': request.user.username,
                    'email': request.user.email,
                }
            }
        )
        # auth = pusher.authenticate(channel=channel_name, socket_id=socket_id, custom_data=user_info)
        # return JsonResponse(auth)
        # auth = pusher.authenticate(channel=channel_name, socket_id=socket_id)
        return JsonResponse(payload)
