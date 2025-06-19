import os
from dotenv import load_dotenv
from app.services.audio import convert_opus_to_wav  # Importa a função de conversão
from groq import Groq  # Importa o cliente Groq

load_dotenv() 
api_key = os.getenv("GROQ_API_KEY")

# Função para transcrever áudio usando Groq (Whisper)
def transcrever_audio_groq(audio_bytes):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Instancia o cliente Groq com a chave da API
    wav_file = convert_opus_to_wav(audio_bytes)  # Converte o áudio OPUS para WAV
    transcription = client.audio.transcriptions.create(
        file=wav_file,  # Arquivo WAV em memória
        model="whisper-large-v3-turbo",  # Modelo Whisper usado para transcrição
        response_format="json",  # Formato da resposta
        language="pt",  # Define o idioma como português
        temperature=0.0  # Temperatura (criatividade) da transcrição
    )
    
    return transcription.text  # Retorna o texto transcrito
