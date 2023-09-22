from rest_framework import permissions
from .models import Conversation

class IsParticipantInConversation(permissions.BasePermission):

    def has_permission(self, request, view):

        pk = view.kwargs.get('pk') 
        conversation_id = view.kwargs.get('conversation_id', None)
        convo_id =  conversation_id if conversation_id else pk
        if convo_id is None:
            return False
        try:
            conversation = Conversation.objects.get(id=convo_id)
            return request.user in conversation.participants.all()
        except Conversation.DoesNotExist:
            return False
