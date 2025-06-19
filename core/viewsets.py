from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from core import models, serializers, filters

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.UserFilter

class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.MessageFilter
    
class DialogueContextViewSet(viewsets.ModelViewSet):
    queryset = models.DialogueContext.objects.all()
    serializer_class = serializers.DialogueContextSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.DialogueContextFilter
    
class AudioViewSet(viewsets.ModelViewSet):
    queryset = models.Audio.objects.all()
    serializer_class = serializers.AudioSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.AudioFilter