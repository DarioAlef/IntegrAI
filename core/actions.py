# O arquivio actions.py deve conter funções diretas(enviar mensagem, mostrar menu, 
# editar/deletar usuário, etc). Não devem conter lógica de fluxo ou controle de estado,
# apenas executar tarefas específicas.
# Exemplo: send_message, menu, funções para editar ou deletar usuário, etc.


import os
import requests
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()
server_url = os.getenv("SERVER_URL")
instance = os.getenv("INSTANCE")
api_key = os.getenv("API_KEY")

def send_message(number, text):
    url = f"http://{server_url}/message/sendText/{instance}"
    payload = {
        "number": number,
        "options": {"delay": 123, "presence": "composing"},
        "textMessage": {"text": text},
        "isBotMessage": True
    }
    headers = {"apikey": api_key, "Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

def menu(user, message):
    if message == '1':
        user.waiting_data = "waiting_for_edit"
        user.save()
        send_message(user.phone_number, "Por favor, envie seu novo nome e email, separados por uma vírgula.")
        return JsonResponse({'status': 'waiting_for_edit'})
    elif message == '2':
        user.waiting_data = "waiting_for_delete_confirmation"
        user.save()
        send_message(user.phone_number, "Tem certeza que deseja deletar seu cadastro? Responda com SIM para confirmar.")
        return JsonResponse({'status': 'waiting_for_delete_confirmation'})
    else:
        send_message(user.phone_number, "Opa! Tudo bem? Por enquanto só operamos um simples CRUD.\n\nDigite o número conforme a opção desejada:\n\n1 - Editar dados\n\n2 - Deletar conta.")
        return JsonResponse({'status': 'invalid_option'})