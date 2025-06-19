import requests
import os
from dotenv import load_dotenv

load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("AUTHENTICATION_API_KEY")

def send_message(server_url, instance, api_key):

    url = f"http://{server_url}/message/sendText/{instance}"

    payload = {
        "number": "5592981147651",
        # "options": {
        #     "delay": 123,
        #     "presence": "composing",
        #     "linkPreview": True,
        #     "quoted": {
        #         "key": {
        #             "remoteJid": "<string>",
        #             "fromMe": True,
        #             "id": "<string>",
        #             "participant": "<string>"
        #         },
        #         "message": {"conversation": "<string>"}
        #     },
        #     "mentions": {
        #         "everyOne": True,
        #         "mentioned": ["<string>"]
        #     }
        # },
        "textMessage": {"text": "teste"}
        }
    headers = {
        
"apikey": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    
send_message(server_url, instance, api_key)