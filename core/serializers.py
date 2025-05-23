from rest_framework import serializers
from core import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
        
class DialogueContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DialogueContext
        fields = '__all__'
        
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Audio
        fields = '__all__'