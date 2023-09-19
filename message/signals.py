from django.db import models
from django.db.models.signals import post_save
from .models import Message, Conversation, MessageStatus
from django.conf import settings

from django.dispatch import receiver

from pusher import Pusher
from django.db.models.signals import m2m_changed
from .serializers import MessageSerializer, MessageStatusSerializer

def _create_status(sender, instance, action, **kwargs):
    pusher_client = Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET,
        cluster=settings.PUSHER_CLUSTER,
    )
    # serializer = MessageStatusSerializer(instance=instance)
    users = instance.seen_by.all().values_list('name', flat=True)
    pusher_client.trigger(f'channel-{instance.message.conversation.id}', 'message:seen', {'message': instance.id, 'seen_by': list(users)})


@receiver(post_save, sender=Message)
def send_push_notification(sender, instance, created, **kwargs):
    if created:
        pusher_client = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
        )
        
        status = MessageStatus.objects.create(
            message=instance,
            status=0,
        )
        
        pusher_client.trigger(f'{instance.conversation.id}-conversation', 'new-message', {'conversation_id': instance.conversation.id, 'message': instance.content, 'sender': instance.sender.id})

    
        for user in instance.conversation.participants.all():
            if user.id != instance.sender.id:
                channel = f'{user.id}-conversations';
                print('trigger', channel)
                serializer = MessageSerializer(instance)
                pusher_client.trigger(channel, 'new-message', serializer.data)


def send_push_coversation(sender, instance, action, **kwargs):
    if action == 'post_add':
        pusher_client = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
        )
        participant_ids = [x for x in kwargs.get('pk_set')]
        for user in participant_ids:
            channel = f'{user}-conversations';

            
            pusher_client.trigger(channel, 'new-channel', {'conversation_id': instance.id})

m2m_changed.connect(send_push_coversation, sender=Conversation.participants.through)
m2m_changed.connect(_create_status, sender=MessageStatus.seen_by.through)
