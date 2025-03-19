from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateChannelView, DeleteChannelView, CreateChannelGroupView, DeleteChannelGroupView

urlpatterns = [
    path('create-channel/', CreateChannelView.as_view(), name='create-channel'),
    path('delete-channel/<int:pk>/', DeleteChannelView.as_view(), name='delete-channel'),
    path('create-channel-group/', CreateChannelGroupView.as_view(), name='create-channel-group'),
    path('delete-channel-group/<int:pk>/', DeleteChannelGroupView.as_view(), name='delete-channel-group'),
]