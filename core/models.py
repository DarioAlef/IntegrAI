from django.db import models
from django.http import JsonResponse

# Create your models here.
class ModelBase(models.Model):
    abstract = True
    
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        auto_now_add=True,
        null=True
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified',
        auto_now=True,
        null=True
    )
    active = models.BooleanField(
        db_column='is_active',
        null=False,
        default=True
    )

    class Meta:
        abstract = True
        managed = True
        


class User(ModelBase):
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True # Agora pode ser nulo e em branco
    )  
    
    phone_number = models.CharField(
        max_length=20, 
        unique=True, 
        null=False
    )
    
    email = models.EmailField(
        max_length=255, 
        unique=True, null=True, 
        blank=True
    )  
    
    waiting_user_data = models.CharField(
        max_length=100, 
        null=True,
        blank=True
    )  # Para armazenar o estado

    waiting_event_data = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    current_event_data = models.JSONField(
        default=dict,
        help_text="Armazena os dados do evento atual que está sendo agendado ou editado"
    )

    def __str__(self):
        return f"{self.name} ({self.phone_number})"



###################################
SENDER_CHOICES = [
    ('user', 'User'),
    ('assistant', 'Assistant'),
]
STATUS_CHOICES = [
    ('disconnected', 'Disconnected'),
    ('qr_code', 'QR Code'),
    ('connected', 'Connected'),
]

# Classe que representa uma mensagem trocada entre usuário e assistente
class Message(ModelBase):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    
    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )
    
    content = models.TextField()
    
    is_voice = models.BooleanField(
    default=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.sender} - {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
        
        

# Classe que armazena o contexto de diálogo de uma sessão de usuário
class DialogueContext(ModelBase):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    
    session_id = models.CharField(
        max_length=100, 
        unique=True
    )
    
    context = models.JSONField(
        default=dict
    )  # Contextual data for dialogue

    def __str__(self):
        return f"{self.user.username} - {self.session_id}"

    class Meta:
        ordering = ['modified_at']
        
        
# Classe que armazena e gerencia áudios enviados pelo usuário
class Audio(ModelBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        related_name='audios'
    )
    file = models.FileField(
        upload_to='audios/'
    )
    duration = models.FloatField(
        null=True,
        blank=True,
        help_text="Duração em segundos"
    )

    def __str__(self):
        return f"{self.user.username} - Áudio de {self.message.timestamp}"

    class Meta:
        ordering = ['-created_at']
        
            
class Event(ModelBase):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    
    event_summary = models.CharField(
        max_length=255, 
        null=False
    )
    
    event_start = models.DateTimeField(
        null=False
    )
    
    event_end = models.DateTimeField(
        null=True
    )
    
    description = models.TextField(
        null=True, 
        blank=True
    )
    
    location = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    
    attendees = models.JSONField(
        default=list,
        help_text="Lista de emails dos participantes"
    )
    
    visibility = models.CharField(
        max_length=10,
        choices=[('private', 'Private'), ('public', 'Public')],
        default='private'
    )

    reminders = models.JSONField(
            default=list,
            help_text="Lista de lembretes para o evento em minutos"
    )

    def __str__(self):
        return f"{self.title} - {self.start_time} ({self.user.name})"