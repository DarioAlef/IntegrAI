import os  # Permite acessar variáveis e funções do sistema operacional.
from fastapi import APIRouter, Request  # Importa classes do FastAPI para criar rotas e manipular requisições.
import base64  # Permite codificar e decodificar dados em base64 (útil para arquivos de áudio).
import requests  # Permite fazer requisições HTTP (ex: baixar arquivos).
import re  # Permite trabalhar com expressões regulares (útil para limpar respostas).
import django  # Importa o framework Django para manipular o banco de dados e modelos.

#importações de dentro do código
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')  # Define qual arquivo de configurações do Django será usado.
django.setup()  # Inicializa o Django para que possamos usar seus recursos fora do padrão (como em scripts FastAPI).
from core.models import User, Message  # Importa os modelos User e Message do Django para manipular usuários e mensagens no banco.
from app.utils.message import extrair_texto, split_message  # Importa funções utilitárias para extrair texto e dividir mensagens longas.
from app.services.command_interpretation import transcrever_audio_groq  # Função para transcrever áudio usando a API Groq.
from app.services.openrouter import get_openrouter_response  # Função para obter resposta do modelo LLM.
from app.services.evolutionAPI import EvolutionAPI  # Classe para enviar mensagens via EvolutionAPI.
from starlette.concurrency import run_in_threadpool  # Permite rodar funções bloqueantes em threads, sem travar o FastAPI.


router = APIRouter()  # Cria um roteador para definir rotas do FastAPI.
e = EvolutionAPI()  # Instancia a classe EvolutionAPI para enviar mensagens depois.

@router.post("/webhook")  # Define a rota POST /webhook para receber notificações externas.
async def webhook(request: Request):  # Função assíncrona que será chamada quando receber um POST nessa rota.
    data = await request.json()  # Lê o corpo da requisição e converte de JSON para dicionário Python.
    print("Webhook em formato JSON recebido:", data)  # Mostra o JSON recebido no terminal para debug.

    message = None   # Vai guardar o texto da mensagem recebida (se houver).
    from_me = False  # Indica se a mensagem foi enviada pelo próprio bot.
    audio_data = None  # Vai guardar os bytes do áudio recebido (se houver).
    sender_number = None # Vai guardar o número do remetente (quem enviou a mensagem).
    user = None # Vai guardar o usuário do banco de dados associado ao remetente.

    # Trecho para ignorar mensagens que não são relevantes.
    # if "data" not in data or "message" not in data["data"]:
    #     return {"status": "ignored"}

    # Verifica se o JSON recebido tem os campos esperados para processar a mensagem.   
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]  # Extrai o dicionário da mensagem.
        from_me = data["data"].get("key", {}).get("fromMe", False)  # Checa se foi o bot que enviou.
        message = extrair_texto(msg_data)  # Usa função utilitária para extrair texto da mensagem.
        # Tenta pegar áudio em base64 direto ou dentro do campo audioMessage.
        audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
        # Se encontrou áudio em base64, decodifica para bytes.
        audio_data = base64.b64decode(audio_base64) if audio_base64 else None
        # Se não encontrou áudio em base64, mas existe o campo audioMessage, tenta baixar o áudio via URL.
        
        # Debug: imprime informações sobre a mensagem e áudio recebidos
        print("msg_data:", msg_data)
        print("audio_base64:", audio_base64)
        print("audio_data:", audio_data)
        print("Entrou no bloco de áudio!")
        
        if not audio_data and "audioMessage" in msg_data:
            audio_url = msg_data["audioMessage"]["url"]  # Pega a URL do áudio.
            audio_response = requests.get(audio_url)  # Baixa o arquivo de áudio.
            audio_data = audio_response.content  # Guarda os bytes do áudio baixado


    # Pega o número do remetente (quem enviou a mensagem).
    if "data" in data and "key" in data["data"]:
        sender_number = data['data']['key']['remoteJid'].split("@")[0]  # Extrai só o número do campo remoto.

    # Busca ou cria o usuário no banco de dados, usando o número do remetente.
    if sender_number:
        user, _ = await run_in_threadpool(User.objects.get_or_create, phone_number=sender_number)
        # get_or_create retorna uma tupla (objeto, criado?), por isso o _.

    # Se recebeu áudio e não foi enviado pelo próprio bot e tem usuário válido:
    if audio_data and not from_me and user:
        instance = data['instance']  # ID da instância Evolution (para enviar resposta depois).
        instance_key = data['apikey']  # Chave da API Evolution.
        texto_transcrito = transcrever_audio_groq(audio_data)  # Transcreve o áudio para texto usando Groq.

        # Salva a mensagem do usuário (áudio transcrito) no banco.
        msg_user = await run_in_threadpool(
            Message.objects.create,
            user=user,
            sender='user',
            content=texto_transcrito,
            is_voice=True
        )

        # Recupera as últimas 10 mensagens desse usuário (do mais antigo para o mais recente).
        history = await run_in_threadpool(
            lambda: list(Message.objects.filter(user=user).order_by('-timestamp')[:10][::-1])
        )
        messages = []
        for m in history:
            role = 'user' if m.sender == 'user' else 'assistant'  # Define o papel da mensagem.
            messages.append({"role": role, "content": [{"type": "text", "text": m.content}]})

        # Adiciona o system prompt no início do histórico.
        messages = [
            {"role": "system", "content": [{"type": "text", "text": "Responda sempre em português. Seu nome é IntegrAI"}]}
        ] + messages  # messages já contém o histórico do usuário

        resposta = get_openrouter_response(messages)  # Chama o modelo LLM para gerar a resposta.
        # Remove blocos <think>...</think> da resposta usando expressão regular.
        resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL)
        # Remove tags <think> soltas (com ou sem quebra de linha).
        resposta = re.sub(r"<think>\s*", "", resposta, flags=re.IGNORECASE)
        resposta = resposta.strip()  # Remove espaços extras do início/fim.

        # Salva a resposta do bot no banco de dados.
        await run_in_threadpool(
            Message.objects.create,
            user=user,
            sender='assistant',
            content=resposta,
            is_voice=False
        )

        # Divide a resposta em partes menores (se necessário) e envia cada parte pelo EvolutionAPI.
        for part in split_message(resposta):
            e.enviar_mensagem(part, instance, instance_key, sender_number)
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

        # Divide a resposta em partes menores (se necessário) e envia cada parte pelo EvolutionAPI.
        for part in split_message(response_text):
            e.enviar_mensagem(part, instance, instance_key, sender_number)
        return {"response": response_text}  # Retorna a resposta para quem chamou o webhook

    return {"status": "ignored"}  # Se não for mensagem relevante, retorna ignorado.