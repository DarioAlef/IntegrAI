import os
from dotenv import load_dotenv
import flask
import requests
from utils.evolutionAPI import EvolutionAPI
import json

# Instancia a classe EvolutionAPI para enviar mensagens pelo Evolution API
e = EvolutionAPI()

# Cria a aplicação Flask (servidor web)
app = flask.Flask(__name__)

# Carrega variáveis de ambiente do arquivo .env (como a chave da API)
load_dotenv()

# Obtém a chave da API do OpenRouter da variável de ambiente
api_key = os.getenv("OPENROUTER_API_KEY")

def get_openrouter_response(message):
    """
    Envia uma mensagem para a API de IA do OpenRouter e retorna a resposta.
    """
    # Busca novamente a chave da API (garante que está sempre atualizada)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        api_key = api_key.strip()
    if not api_key:
        # Se não encontrar a chave, lança um erro
        raise ValueError("API key not found. Please set the OPENROUTER_API_KEY environment variable.")

    # Cabeçalhos HTTP para autenticação e tipo de conteúdo
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Monta o payload (dados) para a requisição da IA
    data = {
        "model": "meta-llama/llama-4-maverick:free",  # Modelo de IA a ser usado
        "messages": [
            {
                "role": "system",
                "content": [
                    # Instrução para a IA responder sempre em português e se identificar como IntegrAI
                    {"type": "text", "text": "Responda sempre em português. Seu nome é IntegrAI"},
                ]
            },
            {
                "role": "user",
                "content": [
                    # Mensagem do usuário recebida no WhatsApp
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

    # Converte a resposta para JSON
    response_json = response.json()

    # Se houver resposta válida, retorna o texto da IA
    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["message"]["content"]
    else:
        # Caso contrário, retorna o erro recebido
        return f"Erro na resposta da API: {response_json}"


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Endpoint que recebe mensagens do Evolution API (Webhook).
    Processa a mensagem recebida e envia para a IA, depois responde ao usuário.
    """
    data = flask.request.json  # Recebe o JSON enviado pelo Evolution API
    print("Webhook recebido:", data)  # Log para debug

    message = None  # Vai armazenar o texto da mensagem recebida
    from_me = False  # Flag para saber se a mensagem foi enviada pelo próprio bot

    # Verifica se o JSON tem os campos esperados
    if (
        "data" in data and
        "message" in data["data"]
    ):
        msg_data = data["data"]["message"]
        # Checa se a mensagem foi enviada por você mesmo (para evitar loop)
        from_me = data["data"].get("key", {}).get("fromMe", False)
        # Extrai o texto da mensagem, seja ela simples ou estendida
        if "conversation" in msg_data:
            message = msg_data["conversation"]
        elif "extendedTextMessage" in msg_data and "text" in msg_data["extendedTextMessage"]:
            message = msg_data["extendedTextMessage"]["text"]

    # Só responde se NÃO foi enviada por você mesmo (evita loop infinito)
    if message and not from_me:
        instance = data['instance']  # ID da instância do Evolution API
        instance_key = data['apikey']  # Chave de autenticação da instância
        # Extrai o número do remetente (quem enviou a mensagem)
        sender_number = data['data']['key']['remoteJid'].split("@")[0]
        # Chama a função que consulta a IA e obtém a resposta
        response_text = get_openrouter_response(message)
        # Envia a resposta da IA de volta para o usuário via Evolution API
        e.enviar_mensagem(response_text, instance, instance_key, sender_number)
        # Retorna a resposta para o Evolution API (opcional, para log)
        return flask.jsonify({"response": response_text})
    # Se não for mensagem válida ou foi enviada por você, apenas ignora
    return flask.jsonify({"status": "ignored"})

# Bloco principal para rodar o servidor Flask, aceitando conexões externas (necessário para ngrok)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)