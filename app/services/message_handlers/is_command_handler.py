from app.services.interpretation.utils_interpretation import interpretar_cancelamento
from app.services.message_handlers.command_handlers.appointment_handler import appointment_handler
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.interpretation.command_interpretation import interpretar_comando
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from app.services.message_handlers.command_handlers.cancel_handler import cancel_handler
from core.models import User


async def command_handler(auth_user: User, message, sender_number):
    print("Iniciando o command_handler para a mensagem:", message)
    # Verificar processos em andamento
    messenger = EvolutionAPI()
    if auth_user.waiting_event_data is not None:
        confirm = interpretar_cancelamento(message)
        if confirm and confirm.get("is_cancellation") == "yes":
            if await cancel_handler(auth_user, sender_number):
                print("Usuário confirmou o cancelamento do processo de agendamento.")
                return True
        else:
            print("Seguindo com o processo de agendamento...")
            await appointment_handler(auth_user, message, sender_number)
            return True


    # Interpretar se é comando ou não
    command = interpretar_comando(message)
    if not command.get("is_command"):
        # Se for um comando, executa a ação correspondente
        print("Mensagem não é um comando", command)
        return False

    if command.get("command"):
        print(f"Comando recebido: {command.get('command')}")
        comandos_disponiveis = ["agendamento",
                                # "cancelar processo atual", 
                                # "editar ou deletar dados da conta",
                                # "ajuda"
                                # "envio_de_mensagem",
                                # "checkar_eventos",
                                # "lembretes",
                                # "enviar_email",
                                "conversa"
                                ]
        # Se for um comando, executa a ação correspondente
        if command.get("command") not in comandos_disponiveis:
            await messenger.enviar_mensagem(
                'Ops! Infelizmente ainda não temos suporte ao comando desejado. Por hora trabalhamos somente com agendamento. Posso ajudá-lo com isso?', sender_number)
            return True
        
        if command.get("command") == "agendamento":
            await messenger.enviar_mensagem(
                'Ótimo! Vamos começar o processo de agendamento. Um momento...', sender_number
            )
            await appointment_handler(auth_user, message, sender_number)
            return True
        elif command.get("command") == "conversa":
            # Se for um comando, executa a ação correspondente
            print("Comando é: ", command)

            return False
