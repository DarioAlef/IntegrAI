# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
from app.services.conversation.evolutionAPI import EvolutionAPI
from core.models import User
from app.services.storage.storage import retrieve_history, store_event, store_message
import os
import django
from fastapi.concurrency import run_in_threadpool

from app.services.appointment.google_calendar.events_mgmt import create_event_async
from app.services.interpretation.appointment_interpretation import interpretar_agendamento
from app.services.interpretation.utils_interpretation import interpretar_confirmacao
from app.services.message_handlers.command_handlers.cancel_handler import cancel_handler
from app.utils.formatting import format_event_confirmation_message, format_event_validation_message, formatar_data_evento
from app.utils.validation import extrair_json_da_resposta, validate_event_data
from app.utils.google_maps import get_formatted_address
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.


# - O agendamento deve ser sempre para o **futuro**, nunca para o passado.

async def appointment_handler(auth_user: User, message, sender_number):
    print("user appointment status:", auth_user.waiting_event_data,
          auth_user.appointment_message_counter, auth_user.current_event_data)
    if auth_user.waiting_event_data == None:
        auth_user.waiting_event_data = "waiting_for_event_data"
        auth_user.appointment_message_counter = 1
        await run_in_threadpool(auth_user.save)
        print(
            "Iniciando o processo de agendamento do evento para o usuário:", sender_number)

    messenger = EvolutionAPI()
    try:
        if auth_user.waiting_event_data == "waiting_for_event_data":
            await listen_user_messages(auth_user, messenger, sender_number)
            return

        if auth_user.waiting_event_data == "waiting_for_confirm":
            await confirmation_handler(auth_user, message, messenger, sender_number)
            return
    except Exception as e:
        print(f"Ocorreu um erro ao agendar o evento: {str(e)}", sender_number)
    print("Fim da função appointment_handler().")

#####################
#####################
#####################
#####################
#####################
#####################
# Funções auxiliares
#####################
#####################
#####################
#####################
#####################
#####################


async def listen_user_messages(auth_user: User, messenger: EvolutionAPI, sender_number: str):
    print("Iniciando escuta de mensagens do usuário:", sender_number)
    # Aqui você pode implementar a lógica para escutar as mensagens do usuário
    # Pega todas as mensagens desde que o processo de agendamento foi iniciado
    appointment_conversation, _ = await retrieve_history(auth_user, auth_user.appointment_message_counter)
    messages = [
        {"role": m.sender, "content": m.content}
        for m in appointment_conversation
        if m.sender in ['user', 'assistant']
    ]
    # Manda pra LLM a conversa
    print("enviando conversa sobre apontamento para a LLM: ", messages)
    llm_event_data = interpretar_agendamento(messages)
    print("llm_event_data:", llm_event_data)
    # Extrai os dados do evento da mensagem (json parse).
    event_data = {
        'event_summary': llm_event_data.get('event_summary', 'Evento sem título'),
        'event_start': llm_event_data.get('event_start'),
        'event_end': llm_event_data.get('event_end'),
        'description': llm_event_data.get('description', ''),
        'location': llm_event_data.get('location', ''),
        'attendees': llm_event_data.get('attendees', []),
        'visibility': llm_event_data.get('visibility', 'private'),
        'reminders': llm_event_data.get('reminders', [])
    }

    # Se houver location, busca o endereço formatado no Google Maps
    if event_data['location']: 
        formatted_address = await get_formatted_address(event_data['location'])
        if formatted_address:
            event_data['location'] = formatted_address
            print(f"📍 Endereço atualizado: {formatted_address}")
        else:
            print(f"⚠️ Mantendo endereço original: {event_data['location']}")
        
    current_event_data, invalid_params = validate_event_data(event_data)
    print("Validando...\n\ncurrent_event_data:", current_event_data)
    print("invalid_params:", invalid_params)
    if invalid_params:
        # Dados do evento validados.
        auth_user.current_event_data = current_event_data
        try:
            await run_in_threadpool(auth_user.save)
            print("Dados do evento salvos no banco de dados:",
                  auth_user.current_event_data)
        except Exception as e:
            import traceback
            print("❌ Erro ao salvar usuário:")
            traceback.print_exc()
            await messenger.enviar_mensagem(
                "Opa! Sinto muito. Ocorreu um erro ao tentar agendar o evento. Processo de agendamento cancelado. Tente novamente mais tarde.",
                sender_number
            )
            cancel_handler(auth_user, messenger, sender_number)

        print("Dados do evento inválidos. Enviando mensagem de validação:", mensagem)
        mensagem = format_event_validation_message(auth_user.current_event_data, invalid_params)
        await messenger.enviar_mensagem(mensagem, sender_number)
        await store_message(auth_user, 'assistant', f"{auth_user.current_event_data}", False)
        # Se nada bugar, quando o usuário vier de novo vão ser mais 2 mensagens da conversa
        auth_user.appointment_message_counter += 2
        
        return

    else:
        try:
            current_event_data['attendees'].append({
                # Associa o evento ao usuário autenticado.
                'email': auth_user.email,
                'displayName': auth_user.name,
                'comment': 'Organizador'
            })
            # Dados do evento validados.
            auth_user.current_event_data = current_event_data
            auth_user.waiting_event_data = "waiting_for_confirm"
            await run_in_threadpool(auth_user.save)
            print("Dados do evento atualizados no objeto User instanciado:",
                  auth_user.current_event_data, auth_user)
            # Envia mensagem de confirmação para o usuário.
            print("Enviando mensagem de confirmação para o usuário:", sender_number)
            mensagem = format_event_confirmation_message(auth_user.current_event_data)
            await messenger.enviar_mensagem(mensagem, sender_number)
            await store_message(auth_user, 'assistant', f"{auth_user.current_event_data}", False)
            auth_user.appointment_message_counter += 2
            await run_in_threadpool(auth_user.save)
            
            
        except Exception as e:
            print("❌ Erro ao salvar usuário:", repr(e))
            traceback.print_exc()
            await messenger.enviar_mensagem(
                "Opa! Ocorreu um erro ao tentar agendar o evento. Tente novamente mais tarde.",
                sender_number
            )
            cancel_handler(auth_user, messenger, sender_number)
        return


async def confirmation_handler(auth_user: User, message, messenger: EvolutionAPI, sender_number: str):
    print("Iniciando confirmação do agendamento do evento:\n",
          auth_user.current_event_data)
    confirm = interpretar_confirmacao(message).get("is_confirmation")
    print("Confirmação recebida:", confirm)
    if confirm == "yes":
        # Armazena o evento no banco de dados.
        await store_event(auth_user, auth_user.current_event_data)
        print("\n\nEvento armazenado no banco de dados:",
              auth_user.current_event_data)
        # Cria o evento no Google Calendar.
        created_event = await create_event_async(**auth_user.current_event_data)
        print("\n\nEvento agendado com sucesso:", auth_user.current_event_data)
        try:
            duration = formatar_data_evento(
                auth_user.current_event_data['event_start'], auth_user.current_event_data['event_end'])
            print("Duração do evento formatada:", duration)
            await messenger.enviar_mensagem(
                f"Agendamento realizado com sucesso: {auth_user.current_event_data['event_summary']} de {duration}.\n\nLink do evento: {created_event.get('htmlLink', 'Link não disponível')}",
                sender_number
            )
            auth_user.waiting_event_data = None
            auth_user.current_event_data = {}
            auth_user.appointment_message_counter = 0
            await run_in_threadpool(auth_user.save)
        except Exception as e:
            print("❌ Erro ao enviar mensagem de confirmação:", repr(e))
            await messenger.enviar_mensagem(
                "Opa! Ocorreu um erro ao tentar agendar o evento. Tente novamente mais tarde.",
                sender_number
            )
            cancel_handler(auth_user, messenger, sender_number)
        return
    else:
        await messenger.enviar_mensagem(
            f"Opa! Você gostaria de mudar algo no evento? Deixa eu verificar...",
            sender_number
        )
        # Se o usuário não confirmar, volta a escutar as mensagens do usuário.
        await listen_user_messages(auth_user, messenger, sender_number)
        # Atualiza o contador de mensagens do usuário.
        if await messenger.enviar_mensagem(
            f"Se quiser cancelar o comando de agendamento, é só pedir também. Tou te escutando!",
            sender_number
        ):
            auth_user.appointment_message_counter += 2
        else:
            auth_user.appointment_message_counter += 1

        await run_in_threadpool(auth_user.save)
        return
