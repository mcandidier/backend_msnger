from rest_framework import serializers

from .models import Message, Conversation, MessageStatus


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'conversation',]


class MessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageStatus
        fields = '__all__'
        # read_only_fields = ['sender', 'conversation',]

    