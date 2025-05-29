import os
import json
import requests
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("OPENROUTER_API_KEY")  # Obtém a chave da API do OpenRouter do ambiente

# Função para obter resposta da API OpenRouter (LLM)
def get_openrouter_response(message):
    api_key = os.getenv("OPENROUTER_API_KEY") 
    if api_key:
        api_key = api_key.strip()  # Remove espaços em branco extras
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
                # Prompt do sistema para definir o comportamento da IA
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

    response_json = response.json()  # Converte resposta para JSON

    # Se houver resposta válida, retorna o texto da IA, se não retorna um erro
    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Erro na resposta da API: {response_json}"
