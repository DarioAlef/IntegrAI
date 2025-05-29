from fastapi import APIRouter, Request
from fastapi import Request
import base64
import requests
from app.utils.message import extrair_texto
from app.services.groq import transcrever_audio_groq
from app.services.openrouter import get_openrouter_response
from app.services.evolutionAPI import EvolutionAPI  # Se estiver fora da pasta app, mantenha assim

router = APIRouter()
e = EvolutionAPI()

@router.post("/webhook")  # Define a rota para receber o webhook
async def webhook(request: Request):
    data = await request.json()  # Obtém os dados do webhook (JSON)
    print("Webhook recebido:", data)  # Exibe o JSON recebido no terminal

    message = None   # Variável para armazenar a mensagem recebida (texto)
    from_me = False  # Variável para verificar se a mensagem é do próprio bot
    audio_data = None  # Variável para armazenar dados de áudio, se necessário


    # Verifica se o JSON recebido possui os campos esperados para processar a mensagem
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]  # Extrai os dados da mensagem recebida
        from_me = data["data"].get("key", {}).get("fromMe", False)  # Verifica se a mensagem foi enviada pelo próprio bot
        message = extrair_texto(msg_data)  # Tenta extrair o texto da mensagem (se houver)
        # Tenta obter o áudio em base64 diretamente ou dentro do campo audioMessage
        audio_base64 = msg_data.get("base64") or msg_data.get("audioMessage", {}).get("audio")
        # Se encontrou áudio em base64, decodifica para bytes; caso contrário, permanece None
        audio_data = base64.b64decode(audio_base64) if audio_base64 else None
        # Se não encontrou áudio em base64, mas existe o campo audioMessage, tenta baixar o áudio via URL
        if not audio_data and "audioMessage" in msg_data:
            audio_url = msg_data["audioMessage"]["url"]  # Obtém a URL do áudio
            audio_response = requests.get(audio_url)  # Faz o download do arquivo de áudio
            audio_data = audio_response.content  # Armazena os bytes do áudio baixado


    # Se recebeu áudio e não foi enviado pelo próprio bot
    if audio_data and not from_me:
        instance = data['instance']  
        instance_key = data['apikey']  
        sender_number = data['data']['key']['remoteJid'].split("@")[0]  # Extrai o número do remetente
        texto_transcrito = transcrever_audio_groq(audio_data)  # Transcreve o áudio recebido
        resposta = get_openrouter_response(texto_transcrito)  # Gera resposta da IA para o texto transcrito
        e.enviar_mensagem(resposta, instance, instance_key, sender_number)  # Envia a resposta pelo WhatsApp
        return {"response": resposta}  # Retorna resposta para o Evolution API
    
    
    # Se recebeu mensagem de texto e não foi enviada pelo próprio bot
    if message and not from_me:
        instance = data['instance']  # ID da instância Evolution
        instance_key = data['apikey']  # Chave da API Evolution
        sender_number = data['data']['key']['remoteJid'].split("@")[0]  # Extrai o número do remetente

        response_text = get_openrouter_response(message)  # Gera resposta da IA para o texto recebido
        e.enviar_mensagem(response_text, instance, instance_key, sender_number)  # Envia a resposta pelo WhatsApp

        return {"response": response_text}  # Retorna resposta para o Evolution API

    return {"status": "ignored"}  # Se não for mensagem relevante, ignora