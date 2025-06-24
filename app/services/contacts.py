import os
import requests
from dotenv import load_dotenv

load_dotenv()

server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("AUTHENTICATION_API_KEY")

def get_contacts(instance, api_key, server_url):
    url = f"http://{server_url}/chat/findContacts/{instance}"
    payload = {}  # Pode ser vazio para buscar todos
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()




def find_number_by_name(contacts, name):
    for contact in contacts:
        if name.lower() in contact.get("name", "").lower():
            return contact.get("number")
    return None