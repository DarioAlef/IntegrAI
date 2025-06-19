import requests
import os
from dotenv import load_dotenv
import base64

#transformar imagem em base64 e depois em string
with open("image.png", "rb") as arquivo:
    arq_binary = arquivo.read()
    arq_b64 = base64.b64encode(arq_binary).decode('utf-8')
    returned = arq_b64

load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("AUTHENTICATION_API_KEY")

def send_media(server_url, instance, api_key, arq_b64):
    url = f"http://{server_url}/message/sendMedia/{instance}"

    payload = {
        "number": "5592981147651",
        # "options": {
        #     "delay": 123,
        #     "presence": "composing"
        # },
        "mediaMessage": {
            "mediatype": "image",
            "fileName": "image.png",
            "caption": "teste",
            "media": arq_b64
        }
    }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

send_media(server_url, instance, api_key, arq_b64)