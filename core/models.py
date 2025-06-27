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
    
    waiting_data = models.CharField(
        max_length=100, 
        null=True,
        blank=True
    )  # Para armazenar o estado

    is_scheduling = models.BooleanField(
        default=False,
        help_text="Indica se o usuário está no processo de agendamento"
    )

    is_editing_event = models.BooleanField(
        default=False,
        help_text="Indica se o usuário está editando um evento"
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
        
            

# # Classe que representa integrações de um usuário com serviços externos (ex: Gmail, Google Calendar)
# class Integration(ModelBase):
#     user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE
#     )
    
#     type = models.CharField(
#         max_length=50
#     )  # e.g., 'gmail', 'google_calendar'
    
#     data = models.JSONField()  # Stores credentials and settings (encrypt in logic)
    
#     status = models.BooleanField(
#         default=True
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.type}"




# # Classe que representa uma instância de conexão do WhatsApp para um usuário
# class WhatsAppInstance(ModelBase):
#     user = models.OneToOneField(
#         User, 
#         on_delete=models.CASCADE
#     )
    
#     instance_key = models.CharField(
#         max_length=100
#     )
    
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='disconnected'
#     )
    
#     qr_code = models.TextField(
#         null=True, 
#         blank=True
#     )
#     connected_at = models.DateTimeField(
#         null=True, 
#         blank=True
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.instance_key}"



# COMMAND_STATUS_CHOICES = [
#     ('pending', 'Pending'),
#     ('completed', 'Completed'),
#     ('awaiting_parameters', 'Awaiting Parameters'),
# ]
# ACTION_STATUS_CHOICES = [
#     ('pending', 'Pending'),
#     ('success', 'Success'),
#     ('failed', 'Failed'),
# ]

# # Classe que representa um comando extraído de uma mensagem, com intenção e parâmetros
# class Command(ModelBase):
#     user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE
#     )
    
#     message = models.ForeignKey(
#         'Message', 
#         on_delete=models.CASCADE
#     )
    
#     intent = models.CharField(
#         max_length=100
#     )  # e.g., 'send_email', 'schedule_meeting'
    
#     parameters = models.JSONField(
#         default=dict
#     )  # e.g., {'to': 'email@exemplo.com', 'subject': 'Reunião'}
    
#     status = models.CharField(
#         max_length=20,
#         choices=COMMAND_STATUS_CHOICES,
#         default='pending'
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.intent} - {self.created_at}"

#     class Meta:
#         ordering = ['created_at']



# # Classe que representa uma ação executada a partir de um comando (ex: enviar email, criar evento)
# class Action(ModelBase):
#     user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE
#     )
    
#     command = models.ForeignKey(
#         'Command', 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True
#     )
    
#     type = models.CharField(
#         max_length=100
#     )  # e.g., 'send_email', 'create_event'
    
#     data = models.JSONField(
#         default=dict
#     )  # Details of the action
    
#     status = models.CharField(
#         max_length=20,
#         choices=ACTION_STATUS_CHOICES,
#         default='pending'
#     )
    
#     executed_at = models.DateTimeField(
#         null=True, 
#         blank=True
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.type} - {self.status}"

#     class Meta:
#         ordering = ['executed_at']



# # Classe que armazena e gerencia iamgens e figurinhas enviados pelo usuário
# class Image(ModelBase):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     message = models.ForeignKey(
#         'Message',
#         on_delete=models.CASCADE,
#         related_name='images'
#     )
#     file = models.ImageField(
#         upload_to='images/'
#     )
#     is_sticker = models.BooleanField(
#         default=False,
#         help_text="Se é figurinha do WhatsApp"
#     )

#     def __str__(self):
#         return f"{self.user.username} - Imagem de {self.message.timestamp} (Sticker: {self.is_sticker})"

#     class Meta:
#         ordering = ['-created_at']



# # Classe que armazena e gerencia vídeos GIFs enviados pelo usuário
# class Video(ModelBase):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     message = models.ForeignKey(
#         'Message',
#         on_delete=models.CASCADE,
#         related_name='videos'
#     )
#     file = models.FileField(
#         upload_to='videos/'
#     )
#     is_gif = models.BooleanField(
#         default=False,
#         help_text="Se é um GIF animado"
#     )
#     duration = models.FloatField(
#         null=True,
#         blank=True,
#         help_text="Duração em segundos"
#     )

#     def __str__(self):
#         return f"{self.user.username} - Vídeo de {self.message.timestamp} (GIF: {self.is_gif})"

#     class Meta:
#         ordering = ['-created_at']