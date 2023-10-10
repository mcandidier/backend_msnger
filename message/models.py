from typing import Iterable, Optional
from django.db import models

from accounts.models import CustomUser


class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.conversation.id}-messages'


    class Meta:
        ordering = ['timestamp']

STATUS_CHOICE = (
    ('sent', 0),
    ('delivered', 1),
    ('read', 2),
)

class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    seen_by = models.ManyToManyField(CustomUser, related_name='seen_messages')
    status = models.CharField(choices=STATUS_CHOICE, default=0, max_length=9)
    timestamp = models.DateTimeField(auto_now=True)

    