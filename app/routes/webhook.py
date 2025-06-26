import os  
from fastapi import APIRouter, Request 
import base64 
import requests 
import re  # regex para remover as tags <think> da resposta do modelo LLM.
import django 

#importações de dentro do código
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')  # Define qual arquivo de configurações do Django será usado.
django.setup()  # Inicializa o Django para que possamos usar seus recursos fora do padrão (como em scripts FastAPI).
from core.models import User, Message, DialogueContext 
from app.utils.message import extrair_texto, split_message 
from app.services.openrouter import get_openrouter_response  
from app.services.evolutionAPI import EvolutionAPI 
from app.services.contacts import get_contacts, find_number_by_name
from app.services.summary import gerar_resumo
from app.services.audio import processar_audio
from starlette.concurrency import run_in_threadpool  # Permite rodar funções bloqueantes em threads, sem travar o FastAPI.


router = APIRouter()  
e = EvolutionAPI()  


# "data" é o que chega do EvolutionAPI via webhook
@router.post("/webhook")  # Define a rota POST /webhook para receber notificações externas.
async def webhook(request: Request): 
    data = await request.json()  # Lê o corpo da requisição e converte de JSON para dicionário Python.
    print("Webhook em formato JSON recebido:", data)  
    
    
    message = None   # Vai guardar o texto da mensagem recebida (se houver).
    from_me = False  # Indica se a mensagem foi enviada pelo próprio bot.
    audio_data = None  # Vai guardar os bytes do áudio recebido (se houver).
    sender_number = None # Vai guardar o número do remetente (quem enviou a mensagem).
    user = None # Vai guardar o usuário do banco de dados associado ao remetente.
    msg_data = None


    # Verifica se o JSON recebido tem "message" e "audioMessage".   
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]
        print("msg_data:", msg_data)  
        from_me = data["data"].get("key", {}).get("fromMe", False)  # Checa se foi o bot que enviou.
        message = extrair_texto(msg_data)
        
        # Procura se tem áudio em msg_data. Tenta pegar áudio em base64 direto ou dentro do campo audioMessage.
        audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
        # Se encontrou áudio em base64, decodifica para bytes.
        audio_data = base64.b64decode(audio_base64) if audio_base64 else None
        # Se não encontrou áudio em base64, mas existe o campo audioMessage, tenta baixar o áudio via URL.
        
        # Debug: imprime informações sobre a mensagem e áudio recebidos
        print("msg_data:", msg_data)
        # print("audio_base64:", audio_base64)
        # print("audio_data:", audio_data)
        # print("Entrou no bloco de áudio!")
        
        # Se não encontrou áudio em base64, mas existe o campo audioMessage, tenta baixar o áudio via URL.
        if not audio_data and "audioMessage" in msg_data:
            audio_url = msg_data["audioMessage"]["url"]  # Pega a URL do áudio.
            audio_response = requests.get(audio_url)  # Baixa o arquivo de áudio.
            audio_data = audio_response.content  # Guarda os bytes do áudio baixado


    # Pega o número do remetente (quem enviou a mensagem).
    if "data" in data and "key" in data["data"]:
        sender_number = data['data']['key']['remoteJid'].split("@")[0]

    # Busca ou cria o usuário no banco de dados, usando o número do remetente.
    if sender_number:
        user, _ = await run_in_threadpool(User.objects.get_or_create, phone_number=sender_number)        
        



    # Envio de mensagem para contato específico (deve vir ANTES do bloco de mensagem normal!)
    if message and not from_me and user:
        match = re.match(r"enviar mensagem para (.+?): (.+)", message, re.IGNORECASE)
        if match:
            contact_name = match.group(1).strip()
            msg_to_send = match.group(2).strip()
            instance = data['instance']
            instance_key = data['apikey']
            server_url = os.getenv("SERVER_URL")
            try:
                contacts = get_contacts(instance, instance_key, server_url)
                print("Contatos retornados:", contacts)  # DEBUG
                number = find_number_by_name(contacts, contact_name)
                print("Número encontrado para envio:", number)  # DEBUG
                if number:
                    e.enviar_mensagem(msg_to_send, instance, instance_key, number)
                    return {"response": f"Mensagem enviada para {contact_name}!"}
                else:
                    return {"response": f"Contato '{contact_name}' não encontrado."}
            except Exception as ex:
                print("Erro ao buscar contatos ou enviar mensagem:", ex)
                return {"response": "Erro ao buscar contatos ou enviar mensagem."}
        



    # Se recebeu áudio e não foi enviado pelo próprio bot e tem usuário válido:
    if (
        "data" in data and "message" in data["data"]
        and not from_me and user
        and processar_audio is not None
    ):
        instance = data['instance']
        instance_key = data['apikey']
        resposta = await processar_audio(data, user, e, instance, instance_key, sender_number)
        if resposta:
            return {"response": resposta}

    # Se recebeu mensagem de texto e não foi enviada pelo próprio bot e tem usuário válido:
    if message and not from_me and user:
        instance = data['instance']  # ID da instância Evolution.
        instance_key = data['apikey']  # Chave da API Evolution.

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

        # Chama o modelo LLM para gerar a resposta, passando o system prompt como argumento.
        response_text = get_openrouter_response(
            messages,
            system_prompt="Responda sempre em português. Seu nome é IntegrAI"
        )

        # Remove blocos <think>...</think> da resposta usando expressão regular.
        response_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)
        # Remove tags <think> soltas (com ou sem quebra de linha).
        response_text = re.sub(r"<think>\s*", "", response_text, flags=re.IGNORECASE)
        response_text = re.sub(r"<think>\s*", "", response_text, flags=re.IGNORECASE)

        response_text = response_text.strip()  # Remove espaços extras do início/fim.

        print("Resposta do LLM:", response_text)  # Mostra a resposta no terminal para debug.

        # Salva a resposta do bot no banco de dados.
        await run_in_threadpool(
            Message.objects.create,
            user=user,
            sender='assistant',
            content=response_text,
            is_voice=False
        )

        # 1. Recupere todas as mensagens do usuário (ou as N últimas, se preferir)
        all_msgs = await run_in_threadpool(
            lambda: list(Message.objects.filter(user=user).order_by('timestamp'))
        )
        # 2. Prepare para o resumo (mesmo formato do histórico curto)
        all_msgs_fmt = []
        for m in all_msgs:
            role = 'user' if m.sender == 'user' else 'assistant'
            all_msgs_fmt.append({"role": role, "content": [{"type": "text", "text": m.content}]})

        # 3. Gere o resumo
        resumo = gerar_resumo(all_msgs_fmt)

        # 4. Salve ou atualize DialogueContext
        await run_in_threadpool(
            DialogueContext.objects.update_or_create,
            user=user,
            session_id=str(user.id),  # Use o ID do usuário como session_id (ou outro identificador único)
            defaults={"context": {"resumo": resumo}}
        )

        # Divide a resposta em partes menores (se necessário) e envia cada parte pelo EvolutionAPI.
        for part in split_message(response_text):
            e.enviar_mensagem(part, instance, instance_key, sender_number)
        return {"response": response_text}  # Retorna a resposta para quem chamou o webhook


    return {"status": "ignored"}  # Se não for mensagem relevante, retorna ignorado.