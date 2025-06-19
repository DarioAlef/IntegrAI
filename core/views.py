from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from core import serializers, models, filters

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UserFilter
    # pagination_class = pagination.CustomPagination
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.MessageFilter
    # pagination_class = pagination.CustomPagination
    
class DialogueContextViewSet(viewsets.ModelViewSet):
    queryset = models.DialogueContext.objects.all()
    serializer_class = serializers.DialogueContextSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.DialogueContextFilter
    # pagination_class = pagination.CustomPagination
    
class AudioViewSet(viewsets.ModelViewSet):
    queryset = models.Audio.objects.all()
    serializer_class = serializers.AudioSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.AudioFilter
    # pagination_class = pagination.CustomPagination