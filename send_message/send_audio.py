import requests
import os
from dotenv import load_dotenv
import base64

# script_directory = os.path.dirname(os.path.abspath(__file__))
# audio_file_path = os.path.join(script_directory, "audio.opus")

#transformar audio em base64 e depois em string
try:
    with open("audio.opus", "rb") as arquivo:
        arq_binary = arquivo.read()
        arq_b64 = base64.b64encode(arq_binary).decode('utf-8')
        returned = arq_b64
except FileNotFoundError:
    print(f"Error: The file {audio_file_path} was not found.")
    exit()

load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("AUTHENTICATION_API_KEY")

def send_audio(server_url, instance, api_key, arq_b64):
    url = f"http://{server_url}/message/sendWhatsAppAudio/{instance}"

    payload = {
        "number": "5592981147651",
        # "options": {
        #     "delay": 123,
        #     "presence": "recording",
        #     "encoding": True
        # },
        "audioMessage": {"audio": arq_b64}
    }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    
send_audio(server_url, instance, api_key, arq_b64)