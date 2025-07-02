# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
from fastapi.concurrency import run_in_threadpool

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.storage.storage import retrieve_history, store_event
from core.models import User
from app.services.conversation.evolutionAPI import EvolutionAPI

async def cancel_handler(auth_user: User, sender_number):
    print("user appointment status:", auth_user.waiting_event_data, auth_user.appointment_message_counter, auth_user.current_event_data)
    
    if auth_user.waiting_event_data is None:
        messenger = EvolutionAPI()
        mensagem = "Você não está agendando nada no momento. Se precisar de ajuda, é só me chamar!"
        await messenger.enviar_mensagem(mensagem, sender_number)
        return True

    # Cancela o processo de agendamento atual
    auth_user.waiting_event_data = None
    auth_user.appointment_message_counter = 0
    auth_user.current_event_data = {}
    await run_in_threadpool(auth_user.save)

    messenger = EvolutionAPI()
    mensagem = "O processo de agendamento foi cancelado com sucesso. Se precisar de ajuda, é só me chamar!"
    await messenger.enviar_mensagem(mensagem, sender_number)
    
    return True