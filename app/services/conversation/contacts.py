import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_contacts(instance, api_key, server_url):
    url = f"http://{server_url}/chat/findContacts/{instance}"
    payload = {}
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    print("Resposta da Evolution API (contatos):", data)  # DEBUG

    # Tente extrair a lista de contatos de diferentes formatos
    if isinstance(data, dict):
        if "contacts" in data:
            return data["contacts"]
        if "result" in data:
            return data["result"]
        # Se for uma lista dentro de outra chave, adicione aqui
    elif isinstance(data, list):
        return data
    return []

def find_number_by_name(contacts, name):
    print("Buscando contato:", name)  # DEBUG
    for contact in contacts:
        # Tente diferentes campos de nome
        contact_name = contact.get("name") or contact.get("pushName") or contact.get("displayName")
        print("Contato encontrado:", contact_name, contact)
        if contact_name and name.lower() in contact_name.lower():
            # Tente diferentes campos de número
            number = contact.get("number") or contact.get("id") or contact.get("user")
            print("Número encontrado:", number)
            return number
    return None