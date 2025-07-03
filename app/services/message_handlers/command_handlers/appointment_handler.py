# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
import os
import django
from fastapi.concurrency import run_in_threadpool

from app.services.appointment.google_calendar.events_mgmt import create_event_async
from app.services.interpretation.appointment_interpretation import interpretar_agendamento
from app.services.interpretation.utils_interpretation import interpretar_confirmacao
from app.utils.event_date_format import formatar_data_evento
from app.utils.validation import validate_event_data
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.storage.storage import retrieve_history, store_event, store_message
from core.models import User
from app.services.conversation.evolutionAPI import EvolutionAPI



# - O agendamento deve ser sempre para o **futuro**, nunca para o passado.

async def appointment_handler(auth_user: User, message, sender_number):
    print("user appointment status:", auth_user.waiting_event_data, auth_user.appointment_message_counter, auth_user.current_event_data)
    if auth_user.waiting_event_data == None:
        auth_user.waiting_event_data = "waiting_for_event_data"
        auth_user.appointment_message_counter = 1
        await run_in_threadpool(auth_user.save)
        print("Iniciando o processo de agendamento do evento para o usuário:", sender_number)

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
##################### Funções auxiliares
#####################
#####################
#####################
#####################
#####################
#####################



async def listen_user_messages(auth_user: User, messenger: EvolutionAPI, sender_number: str):
    print("Iniciando escuta de mensagens do usuário:", sender_number)
    # Aqui você pode implementar a lógica para escutar as mensagens do usuário
    #Pega todas as mensagens desde que o processo de agendamento foi iniciado
    appointment_conversation, _ = await retrieve_history(auth_user, auth_user.appointment_message_counter)
    messages = []
    for m in appointment_conversation:
        role = 'user' if m.sender == 'user' else 'assistant' # Define o papel da mensagem.
        messages.append({"role": role, "content": m.content})
    #Manda pra LLM a conversa
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

    current_event_data, invalid_params = validate_event_data(event_data)
    print("Validando...\n\ncurrent_event_data:", current_event_data)
    print("invalid_params:", invalid_params)
    if invalid_params:
        auth_user.current_event_data = current_event_data  # Dados do evento validados.
        mensagem = f"Entendi que você quer agendar um evento:\n\n{current_event_data}\n\nMas tive dúvidas nos campos:\n\n{invalid_params}.\n\n**Me envie os dados corrigidos pra continuar. Tô te escutando!**"
        if await messenger.enviar_mensagem(mensagem, sender_number):
            auth_user.appointment_message_counter += 2 # Se nada bugar, quando o usuário vier de novo vão ser mais 2 mensagens da conversa
            await store_message(auth_user, 'assistant', mensagem, False)
        else:
            auth_user.appointment_message_counter += 1 # Se bugar, contar só a mensagem do usuário
        await run_in_threadpool(auth_user.save)

        return
    else:
        current_event_data['attendees'].append({
            'email': auth_user.email,  # Associa o evento ao usuário autenticado.
            'displayName': auth_user.name,
            'comment': 'Organizador'
        })
        auth_user.current_event_data = current_event_data  # Dados do evento validados.
        auth_user.waiting_event_data = "waiting_for_confirm"
        await messenger.enviar_mensagem(f"Verifica se tá tudo certinho: \n\n{auth_user.current_event_data} \n\n**Por favor, confirme o agendamento do evento ou se não, diga que não confirma e já me mande as alterações na mesma mensagem!**", sender_number)
        auth_user.appointment_message_counter += 2
        await run_in_threadpool(auth_user.save)
        print("Dados do evento validados e aguardando confirmação do usuário.")
        return
    
async def confirmation_handler(auth_user: User, message, messenger: EvolutionAPI, sender_number: str):
    print("Iniciando confirmação do agendamento do evento:\n", auth_user.current_event_data)
    confirm = interpretar_confirmacao(message).get("is_confirmation")
    print("Confirmação recebida:", confirm)
    if confirm == "yes":
        # Armazena o evento no banco de dados.
        await store_event(auth_user, auth_user.current_event_data)
        print("\n\nEvento armazenado no banco de dados:", auth_user.current_event_data)
        # Cria o evento no Google Calendar.
        created_event = await create_event_async(**auth_user.current_event_data)
        print("\n\nEvento agendado com sucesso:", auth_user.current_event_data)

        duration = formatar_data_evento(auth_user.current_event_data['event_start'], auth_user.current_event_data['event_end'])

        await messenger.enviar_mensagem(
            f"Agendamento realizado com sucesso: {auth_user.current_event_data['event_summary']} de {duration}.\n\nLink do evento: {created_event.get('htmlLink', 'Link não disponível')}",
            sender_number
        )
        auth_user.waiting_event_data = None
        auth_user.current_event_data = {}
        auth_user.appointment_message_counter = 0
        await run_in_threadpool(auth_user.save)
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