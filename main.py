import os
import requests
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from services.evolutionAPI import EvolutionAPI
import uvicorn

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

#Instanciando a classe
e = EvolutionAPI()

#função para obter a resposta da API OpenRouter
def get_openrouter_response(message):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        api_key = api_key.strip() # Remove espaços em branco extras da chave
    if not api_key:
        # Se não encontrar a chave, lança um erro
        raise ValueError("API key not found. Please set the OPENROUTER_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {
                # aqui será o system promt, que define o comportamento da IA
                "role": "system",
                "content": [
                    {"type": "text", "text": "Responda sempre em português. Seu nome é IntegrAI"},
                ]
            },
            {
                # Mensagem do usuário recebida no WhatsApp
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                ]
            }
        ]
    }

    # Faz a requisição POST para a API do OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )

    response_json = response.json()

    # Se houver resposta válida, retorna o texto da IA, se não retorna um erro
    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Erro na resposta da API: {response_json}"

# Endpoint para receber o webhook do Evolution API
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json() # Obtém os dados do webhook
    print("Webhook recebido:", data)

    message = None   # Variável para armazenar a mensagem recebida
    from_me = False  # Variável para verificar se a mensagem é do bot

    # Verifica se o JSON contém os dados esperados
    if "data" in data and "message" in data["data"]:
        msg_data = data["data"]["message"]
        from_me = data["data"].get("key", {}).get("fromMe", False)

        # Verifica se a mensagem é do tipo texto ou extendedTextMessage
        if "conversation" in msg_data:
            message = msg_data["conversation"]
        elif "extendedTextMessage" in msg_data and "text" in msg_data["extendedTextMessage"]:
            message = msg_data["extendedTextMessage"]["text"]

    # Se a mensagem é do bot e existir uma mensagem válida, para evitar loops
    if message and not from_me:
        instance = data['instance']
        instance_key = data['apikey']
        sender_number = data['data']['key']['remoteJid'].split("@")[0]

        response_text = get_openrouter_response(message)
        e.enviar_mensagem(response_text, instance, instance_key, sender_number)

        return {"response": response_text}

    return {"status": "ignored"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )