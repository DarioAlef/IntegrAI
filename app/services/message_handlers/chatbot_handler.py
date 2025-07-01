import re # Para trabalhar com expressões regulares (ex: remover tags <think>).
import os
import django
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

from app.services.chatbot.chatbot import get_llm_response
from app.services.conversation.evolutionAPI import EvolutionAPI
from app.services.message_handlers.context_handler import context_handler
from app.services.storage.storage import  retrieve_history, store_message
from app.utils.text import split_message
from core.models import User


async def chatbot_response(user: User, sender_number):
    messenger = EvolutionAPI()
    # Recupera as últimas 10 mensagens desse usuário (do mais antigo para o mais recente).
    short_history, count = await retrieve_history(user, 10)
    messages = []
    for m in short_history:
        role = 'user' if m.sender == 'user' else 'assistant' # Define o papel da mensagem.
        messages.append({"role": role, "content": [{"type": "text", "text": m.content}]})
    
    
    # (Atualiza se oportuno) e recupera o contexto de diálogo de longo prazo.
    context = await context_handler(user, messages, count)

    resposta = get_llm_response(messages, context=context)
        # Remove blocos <think>...</think> da resposta usando expressão regular.
    resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL)
    # Remove tags <think> soltas (com ou sem quebra de linha).
    resposta = re.sub(r"<think>\s*", "", resposta, flags=re.IGNORECASE)
    resposta = re.sub(r"<think>\s*", "", resposta, flags=re.IGNORECASE)
    resposta = resposta.strip()

    for part in split_message(resposta):
        messenger.enviar_mensagem(part, sender_number)

    store_message(user, 'assistant', resposta, False)

    return resposta