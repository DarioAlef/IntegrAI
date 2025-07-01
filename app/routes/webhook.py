import os  # Importa o módulo para manipulação de variáveis de ambiente.
from fastapi import APIRouter, Request  # Importa o roteador e o objeto de requisição do FastAPI.
from app.services.message_handlers.chatbot_handler import chatbot_response
from app.services.message_handlers.is_command_handler import command_handler
from app.services.message_handlers.is_text_handler import processar_texto
from app.utils.validation import valid_user_message  
# Para inicializar o Django fora do padrão (usando em scripts FastAPI).
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.services.message_handlers.authentication import authenticate
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.message_handlers.is_audio_handler import processar_audio


# Cria um roteador FastAPI para definir rotas/endpoints.
router = APIRouter()
e = EvolutionAPI()  # Instancia a classe de integração com Evolution API.

# Define o endpoint POST /webhook para receber notificações externas do Evolution API.
@router.post("/webhook")
async def webhook(request: Request):
    # Lê o corpo da requisição e converte de JSON para dicionário Python.
    data = await request.json()
    print("Webhook em formato JSON recebido:", data)

    # Inicializa variáveis que serão usadas no processamento da mensagem.
    message = None   # Texto da mensagem recebida (se houver).
    from_me = False  # Indica se a mensagem foi enviada pelo próprio bot.
    sender_number = None  # Número do remetente (quem enviou a mensagem).
    user = None  # Usuário do banco de dados associado ao remetente.
    msg_data = None  # Dados brutos da mensagem.

    # ==============================================================================================
    # 1. Verifica se o JSON recebido tem "message" e extrai informações relevantes.
    # ==============================================================================================
    if "data" in data and "message" in data["data"] and "key" in data["data"]:
        msg_data = data["data"]["message"]
        print("msg_data:", msg_data)
        # Checa se foi o bot que enviou a mensagem.
        from_me = data["data"].get("key", {}).get("fromMe", False)
        # Extrai o texto da mensagem (se houver).
        message = await processar_texto(msg_data, user)
        # Pega o número do remetente (quem enviou a mensagem) a partir do campo remoteJid.
        sender_number = data['data']['key']['remoteJid'].split("@")[0]
    else:
        messenger = EvolutionAPI()
        messenger.enviar_mensagem("Infelizmente não pudemos capturar sua mensagem por problemas técnicos. Tente novamente mais tarde.")
        return {"error": "Data could not be verified", "data": data}

    # ==============================================================================================
    # 2. Authentication - Busca ou cria o usuário no banco de dados, usando o número do remetente.
    # ==============================================================================================
    if sender_number:
       if not (authenticated_user := await authenticate(sender_number, message)):
           return {"response": "User not authenticated yet"}

    # ==============================================================================================
    # 3. Bloco para processamento de áudio do WhatsApp
    # ==============================================================================================
    if not message and (texto_transcrito := processar_audio(data, authenticated_user)):
        message = texto_transcrito

    # ==============================================================================================
    # 4. Validar a mensagem.
    # ==============================================================================================
    if valid_user_message(message, from_me, authenticated_user):

    # ==============================================================================================
    # 5. Iniciar o serviço.
    # ==============================================================================================
        if not command_handler(authenticated_user, message, sender_number):
            await chatbot_response(authenticated_user, sender_number)

    # Se nenhuma das condições acima for satisfeita, retorna status ignorado.
    return {"status": "ignored"}  # Se não for mensagem relevante, retorna ignorado.