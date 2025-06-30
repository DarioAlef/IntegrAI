import os  # Importa o módulo para manipulação de variáveis de ambiente.
from fastapi import APIRouter, Request  # Importa o roteador e o objeto de requisição do FastAPI.
import re  # Para trabalhar com expressões regulares (ex: remover tags <think>).
import django  # Para inicializar o Django fora do padrão (usando em scripts FastAPI).

# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

# Importa os modelos e funções utilitárias do projeto.
from app.utils.extract_text import split_message
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.mailing.send_message_command import processar_comando_enviar_mensagem
from app.services.message_handler.user_message_handler import user_message_handler
from app.services.transcription.audio_handler import processar_audio_webhook_completo

# Cria um roteador FastAPI para definir rotas/endpoints.
router = APIRouter()
e = EvolutionAPI()  # Instancia a classe de integração com Evolution API.

# Define o endpoint POST /webhook para receber notificações externas do Evolution API.
@router.post("/webhook")
async def webhook(request: Request):
    # Lê o corpo da requisição e converte de JSON para dicionário Python.
    data = await request.json()
    print("Webhook em formato JSON recebido:", data)
 
    
    # Desempacotando a tupla retornada pela função user_message_handler.
    message, from_me, sender_number, user, response_text = await user_message_handler(data)
    
    # =======================
    # 1. Processamento de áudio (MOVIDO PARA TRANSCRIPTION)
    # =======================
    processou_audio, resultado_audio = await processar_audio_webhook_completo(
        data, user, e, sender_number, from_me)
    
    if processou_audio:
        return resultado_audio


    # =======================
    # 3. Processamento de mensagens de texto normais
    # =======================
    if message and not from_me and user:
        processar_comando_enviar_mensagem(data, message)
   
        



    # Remove blocos <think>...</think> da resposta usando expressão regular.
    response_text = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL)
    # Remove tags <think> soltas (com ou sem quebra de linha).
    response_text = re.sub(r"<think>\s*", "", response_text, flags=re.IGNORECASE)
    response_text = re.sub(r"<think>\s*", "", response_text, flags=re.IGNORECASE)

    response_text = response_text.strip()  # Remove espaços extras do início/fim.

    print("Resposta do LLM:", response_text)  # Mostra a resposta no terminal para debug.




    # Divide a resposta em partes menores (se necessário) e envia cada parte pelo EvolutionAPI.
    for part in split_message(response_text):
        e.enviar_mensagem(part, sender_number)
    # Retorna a resposta para quem chamou o webhook.
        return {"response": response_text}

    # Se nenhuma das condições acima for satisfeita, retorna status ignorado.
    return {"status": "ignored"}  # Se não for mensagem relevante, retorna ignorado.