from app.services.appointment.appointment_handler import appointment_handler
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.interpretation.command_interpretation import interpretar_comando
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from core.models import User


def command_handler(auth_user: User, message, sender_number):
    # Verificar processos em andamento
    if auth_user.waiting_event_data != None:
        appointment_handler(auth_user, message, sender_number)
        return True

    # Interpretar se é comando ou não
    command = interpretar_comando(message)
    if command.get("is_command", False):
        return False

    if command.get("command"):
        comandos_disponiveis = ["agendamento",
                                # "editar ou deletar dados da conta",
                                # "cancelar processo atual", 
                                # "ajuda"
                                # "envio_de_mensagem",
                                # "checkar_eventos",
                                # "lembretes",
                                # "enviar_email",
                                ]
        # Se for um comando, executa a ação correspondente
        if command.get("command") not in comandos_disponiveis:
            messenger = EvolutionAPI()
            messenger.enviar_mensagem(
                'Ops! Infelizmente ainda não temos suporte ao comando desejado. Por hora trabalhamos somente com agendamento. Posso ajudá-lo com isso?', sender_number)
            return True
        
        if command.get("command") == "agendamento":
            appointment_handler(auth_user, message, sender_number)
            return True
