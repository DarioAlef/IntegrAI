# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
from fastapi.concurrency import run_in_threadpool

from app.services.interpretation.appointment_interpretation import interpretar_agendamento
from app.services.interpretation.utils_interpretation import interpretar_confirmacao
from app.utils.validation import validate_event_data
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.storage.storage import retrieve_history, store_event
from core.models import User
from app.services.conversation.evolutionAPI import EvolutionAPI



# - O agendamento deve ser sempre para o **futuro**, nunca para o passado.

async def appointment_handler(auth_user: User, message, sender_number):
    print("user appointment status:", auth_user.waiting_event_data, auth_user.appointment_message_counter, auth_user.current_event_data)
    if auth_user.waiting_event_data == None:
        auth_user.waiting_event_data = "waiting_for_event_data"
        auth_user.appointment_message_counter = 1
        await run_in_threadpool(auth_user.save)

    messenger = EvolutionAPI()
    try:
        if auth_user.waiting_event_data == "waiting_for_event_data":
            #Pega todas as mensagens desde que o processo de agendamento foi iniciado
            appointment_conversation, _ = await retrieve_history(auth_user, auth_user.appointment_message_counter)
            messages = []
            for m in appointment_conversation:
                role = 'user' if m.sender == 'user' else 'assistant' # Define o papel da mensagem.
                messages.append({"role": role, "content": m.content})
            #Manda pra LLM a conversa
            llm_event_data = interpretar_agendamento(messages)
            print("llm_event_data:", llm_event_data)
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
            print("event_data:", event_data)

            current_event_data, invalid_params = validate_event_data(event_data)

            if invalid_params:
                auth_user.current_event_data = current_event_data  # Dados do evento validados.
                mensagem = f"Entendi que você quer agendar um evento:\n\n{current_event_data}\n\nMas tive dúvidas nos campos:\n\n{invalid_params}.\n\nMe envie os dados corrigidos pra continuar. Tô te escutando!"
                if await messenger.enviar_mensagem(mensagem, sender_number):
                    auth_user.appointment_message_counter += 2 # Se nada bugar, quando o usuário vier de novo vão ser mais 2 mensagens da conversa
                else:
                    auth_user.appointment_message_counter += 1 # Se bugar, contar só a mensagem do usuário
                await run_in_threadpool(auth_user.save)

                return
            else:
                event_data['attendees'].append({
                    'email': auth_user.email,  # Associa o evento ao usuário autenticado.
                    'displayName': auth_user.name,
                    'comment': 'Organizador'
                })
                auth_user.waiting_event_data = "waiting_for_confirm"
                if await messenger.enviar_mensagem("Por favor, confirme o agendamento do evento.", sender_number):
                    auth_user.appointment_message_counter += 2
                else: 
                    auth_user.appointment_message_counter += 1
                await run_in_threadpool(auth_user.save)
                return


        if auth_user.waiting_event_data == "waiting_for_confirm":
            confirm = interpretar_confirmacao(message).get("is_confirmation")

            if confirm:
                # Armazena o evento no banco de dados.
                await store_event(auth_user, auth_user.current_event_data)

                await messenger.enviar_mensagem(
                    f"Agendamento realizado com sucesso: {auth_user.current_event_data['event_summary']} de {auth_user.current_event_data['event_start']} até {auth_user.current_event_data['event_end']}.",
                    sender_number
                )
                auth_user.waiting_event_data == None
                auth_user.current_event_data == {}
                auth_user.appointment_message_counter = None
                await run_in_threadpool(auth_user.save)
                return
            else:
                if await messenger.enviar_mensagem(
                    f"Opa! Você gostaria de mudar algo no evento? É só falar!\n\n Informações do Evento: {auth_user.current_event_data}\n\nSe quiser cancelar o comando de agendamento, é só pedir também. Tou te escutando!",
                    sender_number
                ):
                    auth_user.appointment_message_counter += 2
                else: 
                    auth_user.appointment_message_counter += 1
                    
                auth_user.waiting_event_data = "waiting_for_event_data"
                await run_in_threadpool(auth_user.save)
                return
    except Exception as e:
        await messenger.enviar_mensagem(f"Ocorreu um erro ao agendar o evento: {str(e)}", sender_number)
