from app.utils.extract_text import extrair_texto
from core.models import User, Message, DialogueContext
from app.services.chatbot.chatbot import get_llm_response
from starlette.concurrency import run_in_threadpool
from app.services.mailing.send_message_command import processar_comando_enviar_mensagem
from app.services.user_mgmt.new_user import check_user

async def user_message_handler(data):
    # Inicializa variáveis que serão usadas no processamento da mensagem.
    message = None   # Texto da mensagem recebida (se houver) - a string.
    from_me = False  # Indica se a mensagem foi enviada pelo próprio bot.
    sender_number = None  # Número do remetente (quem enviou a mensagem).
    user = None  # Usuário do banco de dados associado ao remetente.
    msg_data = None  # Dados brutos da mensagem.

    msg_data = data["data"]["message"]
    # Checa se foi o bot que enviou a mensagem.
    from_me = data["data"].get("key", {}).get("fromMe", False)
    # Extrai o texto da mensagem (se houver).
    message = extrair_texto(msg_data)
    
    # Pega o número do remetente (quem enviou a mensagem) a partir do campo remoteJid.
    if "data" in data and "key" in data["data"]:
        sender_number = data['data']['key']['remoteJid'].split("@")[0]
        # SERÁ ANALISADO POSTERIORMENTE SE SERÁ USADO CHECK_USER DO BEHAVIOR
        user = await check_user(sender_number, data)
        
    
        # =======================
    # 1. Processamento de comandos em mensagens de texto
    # =======================
    if message and not from_me and user:
        processar_comando_enviar_mensagem(data, message)
        
        
        
    if message and not from_me and user:
        instance = data['instance']      # ID da instância Evolution.
        instance_key = data['apikey']    # Chave da API Evolution.

        # Salva a mensagem do usuário no banco de dados.
        msg_user = await run_in_threadpool(
            Message.objects.create,
            user=user,
            sender='user',
            content=message,
            is_voice=False
        )
        
        # Recupera as últimas 10 mensagens desse usuário (do mais antigo para o mais recente).
        history = await run_in_threadpool(
            lambda: list(Message.objects.filter(user=user).order_by('-timestamp')[:10][::-1])
        )
        messages = []
        for m in history:
            role = 'user' if m.sender == 'user' else 'assistant'  # Define o papel da mensagem.
            messages.append({"role": role, "content": [{"type": "text", "text": m.content}]})
            
            
        # Chama o modelo LLM para gerar a resposta.
        response_text = get_llm_response(messages)   
            
        # Salva a resposta do bot no banco de dados.
        await run_in_threadpool(
            Message.objects.create,
            user=user,
            sender='assistant',
            content=response_text,
            is_voice=False
        )

    
    return message, from_me, sender_number, user, response_text
