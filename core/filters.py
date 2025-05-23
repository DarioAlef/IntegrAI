from django_filters import rest_framework as filters
from core import models

class UserFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    class Meta:
        model = models.User
        fields = ['id']
        

class MessageFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    user_id = filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    
    class Meta:
        model = models.Message
        fields = ['id', 'user_id']
    
class DialogueContextFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    user_id = filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    
    class Meta:
        model = models.DialogueContext
        fields = ['id', 'user_id']
        
        
class AudioFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')
    user_id = filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    
    class Meta:
        model = models.Audio
        fields = ['id', 'user_id']