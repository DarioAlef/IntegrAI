import requests

class EvolutionAPI():
    def __init__(self):
        pass

    def enviar_mensagem(self, message, instance, instance_key, sender_number):
        url = f"http://localhost:8080/message/sendText/{instance}"
        payload = {
            "number": sender_number,
            "options": {"delay": 123, "presence": "composing"},
            "textMessage": {"text": message},
            "isBotMessage": True
        }
        headers = {
            "apikey": instance_key,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response
