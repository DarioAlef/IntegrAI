import base64
import requests
from app.services.transcription.audio_transcription import transcrever_audio_groq
from app.utils.extract_text import split_message
from app.services.chatbot.chatbot import get_llm_response
from core.models import Message
from starlette.concurrency import run_in_threadpool

def extrair_audio_data(msg_data):
    audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
    if audio_base64:
        return base64.b64decode(audio_base64)
    if "audioMessage" in msg_data and "url" in msg_data["audioMessage"]:
        audio_url = msg_data["audioMessage"]["url"]
        audio_response = requests.get(audio_url)
        return audio_response.content
    return None

async def processar_audio(data, user, e, sender_number):
    msg_data = data["data"]["message"]
    audio_data = extrair_audio_data(msg_data)
    if not audio_data:
        return None

    texto_transcrito = transcrever_audio_groq(audio_data)
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
        role = 'user' if m.sender == 'user' else 'assistant'
        messages.append({"role": role, "content": [{"type": "text", "text": m.content}]})

    resposta = get_llm_response(messages)
    resposta = resposta.strip()

    await run_in_threadpool(
        Message.objects.create,
        user=user,
        sender='assistant',
        content=resposta,
        is_voice=False
    )

    for part in split_message(resposta):
        e.enviar_mensagem(part, sender_number)
    return resposta