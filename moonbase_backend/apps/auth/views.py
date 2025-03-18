from django.shortcuts import render
from rest_framework import generics
from .serializers import SignupSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer