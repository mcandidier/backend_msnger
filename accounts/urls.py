
from django.urls import path, include, re_path

from .views import (
    UserRegistrationView, 
    UserTokenView, 
    UserView,
    UsersListView
)

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/', UserTokenView.as_view(), name='l'),
    path('users/', UsersListView.as_view(), name='users'),
    path('user/<int:id>/', UserView.as_view()),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
