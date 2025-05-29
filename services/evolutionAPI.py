from dotenv import load_dotenv
import requests
import os

load_dotenv()

# Classe que encapsula a lógica de envio de mensagens via Evolution API.
class EvolutionAPI():
    def __init__(self):
        # Construtor da classe para configurações futuras.
        pass

    # Método para o bot enviar uma mensagem de texto via Evolution API.
    def enviar_mensagem(self, message, instance, instance_key, sender_number):
        url = f"http://localhost:8080/message/sendText/{instance}"

        payload = {
            "number": sender_number,  
            "options": {
                "delay": 100,         
                "presence": "composing"  
            },
            "textMessage": {
                "text": message       
            },
            "isBotMessage": True      
        }

        headers = {
            "apikey": instance_key,           
            "Content-Type": "application/json"
        }

        # Envia a requisição POST para o Evolution API
        response = requests.post(url, json=payload, headers=headers)

        return response