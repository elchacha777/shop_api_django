from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from . import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)
        


class LoginView(ObtainAuthToken):
    serializer_class = serializers.LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Customize the response data
        response_data = {
            'token': token.key,
            'user_id': user.username,
            'username': 'id',
            'additional_field': 'Custom additional field value'
        }

        return Response(response_data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        print(user)
        Token.objects.filter(user=user).delete()
        return Response('Вы вышли со своего аккаунта')
