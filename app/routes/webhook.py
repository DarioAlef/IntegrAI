import os  # Importa o módulo para manipulação de variáveis de ambiente.
from fastapi import APIRouter, Request  # Importa o roteador e o objeto de requisição do FastAPI.
import base64  # Para decodificar áudios em base64.
import requests  # Para fazer requisições HTTP (ex: baixar arquivos de áudio).
import re  # Para trabalhar com expressões regulares (ex: remover tags <think>).
import django  # Para inicializar o Django fora do padrão (usando em scripts FastAPI).

# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from core.models import User, Message, DialogueContext
from app.utils.extract_text import extrair_texto, split_message
from app.services.chatbot.chatbot import get_llm_response
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.conversation.contacts import get_contacts, find_number_by_name
from app.services.context.summary import gerar_resumo
from app.services.transcription.audio_processing import processar_audio
from starlette.concurrency import run_in_threadpool  # Permite rodar funções bloqueantes em threads assíncronas.

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
    audio_data = None  # Bytes do áudio recebido (se houver).
    sender_number = None  # Número do remetente (quem enviou a mensagem).
    user = None  # Usuário do banco de dados associado ao remetente.
    msg_data = None  # Dados brutos da mensagem.

    # Verifica se o JSON recebido tem "message" e extrai informações relevantes.
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]
        print("msg_data:", msg_data)
        # Checa se foi o bot que enviou a mensagem.
        from_me = data["data"].get("key", {}).get("fromMe", False)
        # Extrai o texto da mensagem (se houver).
        message = extrair_texto(msg_data)

        # Procura se tem áudio em msg_data (em base64 ou dentro do campo audioMessage).
        audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
        # Se encontrou áudio em base64, decodifica para bytes.
        audio_data = base64.b64decode(audio_base64) if audio_base64 else None

        # Debug: imprime informações sobre a mensagem e áudio recebidos.
        print("msg_data:", msg_data)
        print("Entrou no bloco de áudio!")

        # Se não encontrou áudio em base64, mas existe o campo audioMessage, tenta baixar o áudio via URL.
        if not audio_data and "audioMessage" in msg_data:
            audio_url = msg_data["audioMessage"]["url"]  # Pega a URL do áudio.
            audio_response = requests.get(audio_url)  # Baixa o arquivo de áudio.
            audio_data = audio_response.content  # Guarda os bytes do áudio baixado.

    # Pega o número do remetente (quem enviou a mensagem) a partir do campo remoteJid.
    if "data" in data and "key" in data["data"]:
        sender_number = data['data']['key']['remoteJid'].split("@")[0]

    # Busca ou cria o usuário no banco de dados, usando o número do remetente.
    if sender_number:
        # O método get_or_create retorna uma tupla (objeto, criado), por isso o "_".
        user, _ = await run_in_threadpool(User.objects.get_or_create, phone_number=sender_number)

    # =======================
    # 1. Bloco para comandos especiais: "enviar mensagem para ..."
    # =======================
    # Esse bloco detecta se a mensagem é um comando para enviar mensagem a um contato.
    if message and not from_me and user:
        # Usa expressão regular para identificar o comando.
        match = re.match(r"enviar mensagem para (.+?): (.+)", message, re.IGNORECASE)
        if match:
            contact_name = match.group(1).strip()  # Nome do contato extraído do comando.
            msg_to_send = match.group(2).strip()   # Mensagem a ser enviada.
            instance = data['instance']            # ID da instância Evolution.
            instance_key = data['apikey']          # Chave da API Evolution.
            server_url = os.getenv("SERVER_URL")   # URL do Evolution API.
            try:
                # Busca todos os contatos do usuário.
                contacts = get_contacts(instance, instance_key, server_url)
                print("Contatos retornados:", contacts)  # DEBUG
                # Procura o número do contato pelo nome.
                number = find_number_by_name(contacts, contact_name)
                print("Número encontrado para envio:", number)  # DEBUG
                if number:
                    # Envia a mensagem para o contato encontrado.
                    e.enviar_mensagem(msg_to_send, number)
                    return {"response": f"Mensagem enviada para {contact_name}!"}
                else:
                    return {"response": f"Contato '{contact_name}' não encontrado."}
            except Exception as ex:
                print("Erro ao buscar contatos ou enviar mensagem:", ex)
                return {"response": "Erro ao buscar contatos ou enviar mensagem."}

    # =======================
    # 2. Bloco para processamento de áudio do WhatsApp
    # =======================
    # Se recebeu áudio e não foi enviado pelo próprio bot e tem usuário válido:
    if (
        "data" in data and "message" in data["data"]
        and not from_me and user
        and processar_audio is not None
    ):
        # Chama a função que processa o áudio (transcreve, responde, etc).
        resposta = await processar_audio(data, user, e, sender_number)
        if resposta:
            return {"response": resposta}

    # =======================
    # 3. Bloco para mensagens de texto normais
    # =======================
    # Se recebeu mensagem de texto e não foi enviada pelo próprio bot e tem usuário válido:
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

        # Recupera todas as mensagens do usuário para gerar um resumo de longo prazo.
        all_msgs = await run_in_threadpool(
            lambda: list(Message.objects.filter(user=user).order_by('timestamp'))
        )
        # Prepara o histórico para o resumo.
        all_msgs_fmt = []
        for m in all_msgs:
            role = 'user' if m.sender == 'user' else 'assistant'
            all_msgs_fmt.append({"role": role, "content": [{"type": "text", "text": m.content}]})

        # Gera o resumo do histórico de longo prazo.
        resumo = gerar_resumo(all_msgs_fmt)

        # Salva ou atualiza o contexto de diálogo de longo prazo no banco.
        await run_in_threadpool(
            DialogueContext.objects.update_or_create,
            user=user,
            session_id=str(user.id),  # Usa o ID do usuário como session_id.
            defaults={"context": {"resumo": resumo}}
        )

        # Divide a resposta em partes menores (se necessário) e envia cada parte pelo EvolutionAPI.
        for part in split_message(response_text):
            e.enviar_mensagem(part, sender_number)
        # Retorna a resposta para quem chamou o webhook.
        return {"response": response_text}

    # Se nenhuma das condições acima for satisfeita, retorna status ignorado.
    return {"status": "ignored"}  # Se não for mensagem relevante, retorna ignorado.

#