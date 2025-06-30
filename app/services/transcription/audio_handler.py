"""
Módulo centralizado para lidar com todas as operações relacionadas a áudio
Move toda a lógica de áudio do webhook para a pasta transcription
"""

import base64
import requests
from app.services.transcription.audio_transcription import transcrever_audio_groq
from app.utils.extract_text import split_message
from app.services.chatbot.chatbot import get_llm_response
from core.models import Message
from starlette.concurrency import run_in_threadpool


def processar_deteccao_audio_webhook(data):
    """
    Processa a detecção de áudio no webhook e retorna True/False
    """
    tem_audio = False
    
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]
        
        # Procura se tem áudio em msg_data (em base64 ou dentro do campo audioMessage).
        audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
        if audio_base64:
            tem_audio = True
        elif "audioMessage" in msg_data and "url" in msg_data["audioMessage"]:
            tem_audio = True
    
    return tem_audio


async def processar_audio_completo(data, user, e, sender_number):
    """
    Função completa para processar áudio (transcrição + resposta + envio)
    """
    msg_data = data["data"]["message"]
    
    # Extrai os dados do áudio
    audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
    if audio_base64:
        audio_data = base64.b64decode(audio_base64)
    elif "audioMessage" in msg_data and "url" in msg_data["audioMessage"]:
        audio_url = msg_data["audioMessage"]["url"]
        audio_response = requests.get(audio_url)
        audio_data = audio_response.content
    else:
        return None

    # Transcreve o áudio
    texto_transcrito = transcrever_audio_groq(audio_data)
    
    # Salva a mensagem do usuário
    msg_user = await run_in_threadpool(
        Message.objects.create,
        user=user,
        sender='user',
        content=texto_transcrito,
        is_voice=True
    )

    # Recupera histórico de mensagens
    history = await run_in_threadpool(
        lambda: list(Message.objects.filter(user=user).order_by('-timestamp')[:10][::-1])
    )
    
    messages = []
    for m in history:
        role = 'user' if m.sender == 'user' else 'assistant'
        messages.append({"role": role, "content": [{"type": "text", "text": m.content}]})

    # Gera resposta do LLM
    resposta = get_llm_response(messages)
    resposta = resposta.strip()

    # Salva a resposta do assistente
    await run_in_threadpool(
        Message.objects.create,
        user=user,
        sender='assistant',
        content=resposta,
        is_voice=False
    )

    # Envia a resposta em partes
    for part in split_message(resposta):
        e.enviar_mensagem(part, sender_number)
    
    return resposta


async def processar_audio_webhook_completo(data, user, e, sender_number, from_me=False):
    """
    Função completa que encapsula toda a lógica de processamento de áudio do webhook
    Retorna: (processou_audio, resposta)
    """
    # Verifica se tem áudio
    tem_audio = processar_deteccao_audio_webhook(data)
    
    # Se tem áudio, não é mensagem própria e tem usuário válido
    if tem_audio and not from_me and user:
        resposta = await processar_audio_completo(data, user, e, sender_number)
        if resposta:
            return True, {"response": resposta}
    
    return False, None
