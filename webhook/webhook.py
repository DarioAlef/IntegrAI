import requests
import os
from dotenv import load_dotenv
import flask
from flask import Flask, jsonify

load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("AUTHENTICATION_API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

@app.route("/chats-update", methods=["POST"])
def chats_update():
    data = flask.request.json
    print("Recebido /chats-update:", data)
    return jsonify({"status": "ok"})

@app.route("/messages-upsert", methods=["POST"])
def messages_upsert():
    data = flask.request.json
    print("Recebido /messages-upsert:", data)
    return jsonify({"status": "ok"})

@app.route("/contacts-update", methods=["POST"])
def contacts_update():
    data = flask.request.json
    print("Recebido /contacts-update:", data)
    return jsonify({"status": "ok"})

@app.route("/set-webhook", methods=["POST"])
def set_webhook():
    url = f"http://{server_url}/webhook/set/{instance}"

    payload = {
        "url": webhook_url,
        "webhook_by_events": True,
        "webhook_base64": True,
        "events": ["APPLICATION_STARTUP"]
    }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"status": "sucesso", "resposta": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)