from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ConversationView, MessageView, MessageStatusView,AuthView


router = DefaultRouter()
router.register(r'conversations', ConversationView),

message_list = MessageView.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = [
    path('api/conversations/<int:conversation_id>/messages/', message_list, name='message_list'),
    path('api/conversations/<int:conversation_id>/messages/<int:pk>/', MessageView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='message-detail'),
    path('api/conversations/<int:conversation_id>/messages/<int:message_id>/seen/', MessageStatusView.as_view()),
    path('api/test/', AuthView.as_view(), name='pusher_auth'),
    path('api/', include(router.urls)),

]
