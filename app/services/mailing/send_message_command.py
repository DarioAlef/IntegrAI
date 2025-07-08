from app.services.conversation.contacts import get_contacts, find_number_by_name
from app.services.conversation.evolutionAPI import EvolutionAPI
import os
import re

e = EvolutionAPI()


    # 1. Bloco para comandos especiais: "enviar mensagem para ..."
    # =======================
    # Esse bloco detecta se a mensagem é um comando para enviar mensagem a um contato.
def processar_comando_enviar_mensagem(data, message):
    # Usa expressão regular para identificar o comando.
    match = re.match(r"enviar mensagem para (.+?): (.+)", message, re.IGNORECASE)
    if match:
        contact_name = match.group(1).strip()  # Nome do contato extraído do comando.
        msg_to_send = match.group(2).strip()   # Mensagem a ser enviada.
        instance = data['instance']            # ID da instância Evolution.
        instance_key = data['apikey']          # Chave da API Evolution.
        server_url = os.getenv("SERVER_URL")   # URL do Evolution API.
        try:
            # Busca todos os contatos do usuário.
            contacts = get_contacts(instance, instance_key, server_url)
            print("Contatos retornados:", contacts)  # DEBUG
            # Procura o número do contato pelo nome.
            number = find_number_by_name(contacts, contact_name)
            print("Número encontrado para envio:", number)  # DEBUG
            if number:
                # Envia a mensagem para o contato encontrado.
                e.enviar_mensagem(msg_to_send, number)
                return {"response": f"Mensagem enviada para {contact_name}!"}
            else:
                return {"response": f"Contato '{contact_name}' não encontrado."}
        except Exception as ex:
            print("Erro ao buscar contatos ou enviar mensagem:", ex)
            return {"response": "Erro ao buscar contatos ou enviar mensagem."}

    # =======================
    # 2. Bloco para processamento de áudio do WhatsApp
    # =======================
    # Se recebeu áudio e não foi enviado pelo próprio bot e tem usuário válido: