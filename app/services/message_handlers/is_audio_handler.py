from app.services.storage.storage import store_message
from app.services.transcription.audio_transcription import transcrever_audio_groq
from app.utils.audio import extrair_audio_data

async def processar_audio(data, user) -> str:
    msg_data = data["data"]["message"]
    audio_data = extrair_audio_data(msg_data)
    if not audio_data:
        return None

    if not (texto_transcrito := transcrever_audio_groq(audio_data)):
        return None

    await store_message(user, 'user', texto_transcrito, is_voice=True)
    return texto_transcrito

