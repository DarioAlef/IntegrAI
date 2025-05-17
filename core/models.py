from django.db import models
from django.contrib.auth.models import User

# Create your models here.


SENDER_CHOICES = [
    ('user', 'User'),
    ('assistant', 'Assistant'),
]
STATUS_CHOICES = [
    ('disconnected', 'Disconnected'),
    ('qr_code', 'QR Code'),
    ('connected', 'Connected'),
]

class Integration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)  # e.g., 'gmail', 'google_calendar'
    data = models.JSONField()  # Stores credentials and settings (encrypt in logic)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

class WhatsAppInstance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instance_key = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disconnected'
    )
    qr_code = models.TextField(null=True, blank=True)
    connected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.instance_key}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )
    content = models.TextField()
    is_voice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.sender} - {self.timestamp}"

    class Meta:
        ordering = ['timestamp']


COMMAND_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('awaiting_parameters', 'Awaiting Parameters'),
]
ACTION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]


class Command(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    intent = models.CharField(max_length=100)  # e.g., 'send_email', 'schedule_meeting'
    parameters = models.JSONField(default=dict)  # e.g., {'to': 'email@exemplo.com', 'subject': 'Reunião'}
    status = models.CharField(
        max_length=20,
        choices=COMMAND_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.intent} - {self.created_at}"

    class Meta:
        ordering = ['created_at']

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command = models.ForeignKey('Command', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100)  # e.g., 'send_email', 'create_event'
    data = models.JSONField(default=dict)  # Details of the action
    status = models.CharField(
        max_length=20,
        choices=ACTION_STATUS_CHOICES,
        default='pending'
    )
    executed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.status}"

    class Meta:
        ordering = ['executed_at']

class DialogueContext(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    context = models.JSONField(default=dict)  # Contextual data for dialogue
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_id}"

    class Meta:
        ordering = ['last_updated']