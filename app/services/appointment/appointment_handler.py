# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django

from app.services.interpretation.appointment_interpretation import interpretar_agendamento
from app.services.interpretation.utils_interpretation import interpretar_confirmacao
from app.utils.validation import validate_event_data
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.storage.storage import store_event
from core.models import User
from app.services.conversation.evolutionAPI import EvolutionAPI



# - O agendamento deve ser sempre para o **futuro**, nunca para o passado.

def appointment_handler(auth_user: User, message, sender_number):
    if auth_user.waiting_event_data == None:
        auth_user.waiting_event_data = "waiting_for_event_data"
        auth_user.save()

    messenger = EvolutionAPI()
    try:
        if auth_user.waiting_event_data == "waiting_for_event_data":

            llm_event_data = interpretar_agendamento(message) 
            # Extrai os dados do evento da mensagem.
            event_data = {
                'event_summary': llm_event_data.get('title', 'Evento sem título'),
                'event_start': llm_event_data.get('start_time'),
                'event_end': llm_event_data.get('end_time'),
                'description': llm_event_data.get('description', ''),
                'location': llm_event_data.get('location', ''),
                'attendees': llm_event_data.get('attendees', []),
                'visibility': llm_event_data.get('visibility', 'private'),
                'reminders': llm_event_data.get('reminders', [])
            }

            current_event_data, invalid_params = validate_event_data(event_data)
            auth_user.current_event_data = current_event_data  # Dados do evento validados.
            auth_user.save()
            if invalid_params:                
                mensagem = f"Identifiquei que você quer agendar um evento mas me perdi no(s) campos:\n {invalid_params}.\nMe mande os valores corrigidos para que eu possa agendar o evento. Tou te escutando!"
                messenger.enviar_mensagem(mensagem, sender_number)
                return
            else:
                event_data['attendees'].append({
                    'email': auth_user.email,  # Associa o evento ao usuário autenticado.
                    'displayName': auth_user.name,
                    'comment': 'Organizador'
                })
                auth_user.waiting_event_data = "waiting_for_confirm"
                messenger.enviar_mensagem("Por favor, confirme o agendamento do evento.", sender_number)
                auth_user.save()
                return


        if auth_user.waiting_event_data == "waiting_for_confirm":
            confirm = interpretar_confirmacao(message).get("is_confirmation")

            if confirm:
                # Armazena o evento no banco de dados.
                store_event(auth_user, auth_user.current_event_data)

            # Envia uma confirmação ao usuário.
            messenger.enviar_mensagem(
                f"Agendamento realizado com sucesso: {auth_user.current_event_data['event_summary']} de {auth_user.current_event_data['event_start']} até {auth_user.current_event_data['event_end']}.",
                sender_number
            )
            auth_user.waiting_event_data == None
            auth_user.save()
            return
    except Exception as e:
        messenger.enviar_mensagem(f"Ocorreu um erro ao agendar o evento: {str(e)}", sender_number)
