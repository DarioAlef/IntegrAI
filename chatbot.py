import os
from dotenv import load_dotenv
from utils.evolutionAPI import EvolutionAPI
import flask
import requests

e = EvolutionAPI()
app = flask.Flask(__name__)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_chat_response(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {"role": "system", "content": "Você é um atendente de IA, responda de forma clara e útil."},
            {"role": "user", "content": message}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = flask.request.json
    message = data['data']['message']['conversation']
    instance = data['instance']
    instance_key = data['apikey']
    sender_number = data['data']['key']['remoteJid'].split("@")[0]
    response_text = get_chat_response(message)
    e.enviar_mensagem(response_text, instance, instance_key, sender_number)
    return flask.jsonify({"response": response_text})

# Remova o bloco de execução principal
if __name__ == "__main__":
    app.run(port=5000)