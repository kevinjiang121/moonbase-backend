from datetime import datetime, timedelta
from django.core import signing
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt

from apps.users.models import User
from .serializers import SignupSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
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

def generate_reset_token(user):
    expiration = (datetime.utcnow() + timedelta(hours=1)).timestamp()
    data = {'user_id': user.user_id, 'exp': expiration}
    token = signing.dumps(data, key=settings.SECRET_KEY)
    return token

def validate_reset_token(token):
    try:
        data = signing.loads(token, key=settings.SECRET_KEY)
        if datetime.utcnow().timestamp() > data['exp']:
            return None
        return data['user_id']
    except signing.BadSignature:
        return None

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If the email is registered, a reset link has been sent."},
                            status=status.HTTP_200_OK)
        token = generate_reset_token(user)
        frontend = settings.FRONTEND_URL_DEV
        reset_link = f"{frontend}/reset-password?token={token}"
        return Response({"message": "Password reset link sent.", "reset_link": reset_link},
                        status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        if not token or not new_password:
            return Response({"error": "Token and new password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user_id = validate_reset_token(token)
        if not user_id:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
