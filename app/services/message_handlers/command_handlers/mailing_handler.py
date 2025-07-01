### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
### NÃO UTILIZADO NO MOMENTO ###
import os
from app.services.conversation.contacts import get_contacts, find_number_by_name


def mailing(data):

    ## atual sistema de envio de mensagem

    match = ""
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