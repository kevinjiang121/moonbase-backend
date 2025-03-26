from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreateChannelView, DeleteChannelView,
    CreateChannelGroupView, DeleteChannelGroupView,
    GetChannelView, GetChannelGroupView,
    GetChannelsListView, GetChannelGroupsListView
)

urlpatterns = [
    path('create-channel/', CreateChannelView.as_view(), name='create-channel'),
    path('delete-channel/<int:pk>/', DeleteChannelView.as_view(), name='delete-channel'),
    path('create-channel-group/', CreateChannelGroupView.as_view(), name='create-channel-group'),
    path('delete-channel-group/<int:pk>/', DeleteChannelGroupView.as_view(), name='delete-channel-group'),
    path('get-channel/<int:pk>/', GetChannelView.as_view(), name='get-channel'),
    path('get-channel-group/<int:pk>/', GetChannelGroupView.as_view(), name='get-channel-group'),
    path('get-channels-list/', GetChannelsListView.as_view(), name='get-channels-list'),
    path('get-channel-groups-list/', GetChannelGroupsListView.as_view(), name='get-channel-groups-list'),
]