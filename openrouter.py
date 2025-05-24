import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# user_message = input(str("\nDigite sua mensagem: "))

def get_openrouter_response():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        api_key = api_key.strip()
    if not api_key:
        raise ValueError("API key not found. Please set the OPENROUTER_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "Responda sempre em português. Seu nome é IntegrAI"},
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_message},
                ]
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )

    response_json = response.json()

    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Erro na resposta da API: {response_json}"


resposta = get_openrouter_response()
print(resposta,"\n")