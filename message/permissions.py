from rest_framework import permissions
from .models import Conversation

class IsParticipantInConversation(permissions.BasePermission):

    def has_permission(self, request, view):
        conversation_id = view.kwargs.get('conversation_id')
        if conversation_id is None:
            return False

        try:
            conversation = Conversation.objects.get(id=conversation_id)
            return request.user in conversation.participants.all()
        except Conversation.DoesNotExist:
            return False
