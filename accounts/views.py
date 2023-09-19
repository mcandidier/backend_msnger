from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserTokenView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.request.user.id)
        serializer = self.serializer_class(instance=user)
        return Response(serializer.data, status=200)


class UserView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.serializer_class(instance=user)
        return Response(serializer.data, status=200)
