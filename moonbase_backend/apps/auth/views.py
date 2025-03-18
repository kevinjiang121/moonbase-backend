from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from .serializers import SignupSerializer
from .serializers import LoginSerializer
import jwt

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Create a JWT payload with an expiration time (e.g., 24 hours)
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        
        return Response({
            "access_token": token,
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)