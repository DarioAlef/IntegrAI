import os  # Importa o módulo para manipulação de variáveis de ambiente.
import requests  # Importa o módulo para fazer requisições HTTP.
from dotenv import load_dotenv  # Importa função para carregar variáveis do .env.

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env para o ambiente Python.

def get_contacts(instance, api_key, server_url):
    """
    Busca a lista de contatos do usuário via Evolution API.
    Parâmetros:
        instance (str): Nome da instância Evolution.
        api_key (str): Chave de autenticação da Evolution API.
        server_url (str): URL base do Evolution API (ex: localhost:8080).
    Retorna:
        list: Lista de contatos (cada contato é um dicionário).
    """
    # Monta a URL do endpoint para buscar contatos.
    url = f"http://{server_url}/chat/findContacts/{instance}"
    payload = {}  # Payload vazio, pois a API não exige dados no corpo para essa requisição.
    headers = {
        "apikey": api_key,  # Chave de autenticação no header.
        "Content-Type": "application/json"
    }
    # Faz uma requisição POST para o Evolution API para buscar os contatos.
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Lança exceção se a resposta for erro HTTP.
    data = response.json()  # Converte a resposta JSON em dicionário Python.
    print("Resposta da Evolution API (contatos):", data)  # DEBUG: imprime resposta recebida.

    # Tenta extrair a lista de contatos de diferentes formatos de resposta.
    if isinstance(data, dict):
        # Se a resposta for um dicionário e tiver a chave "contacts", retorna essa lista.
        if "contacts" in data:
            return data["contacts"]
        # Se a resposta for um dicionário e tiver a chave "result", retorna essa lista.
        if "result" in data:
            return data["result"]
        # Se houver outros formatos, adicione aqui.
    elif isinstance(data, list):
        # Se a resposta já for uma lista, retorna diretamente.
        return data
    # Se não encontrou contatos, retorna lista vazia.
    return []

def find_number_by_name(contacts, name):
    """
    Procura o número de telefone de um contato pelo nome.
    Parâmetros:
        contacts (list): Lista de contatos (cada contato é um dicionário).
        name (str): Nome (ou parte do nome) do contato a ser buscado.
    Retorna:
        str ou None: Número do contato encontrado, ou None se não encontrar.
    """
    print("Buscando contato:", name)  # DEBUG: mostra o nome buscado.
    for contact in contacts:
        # Tenta diferentes campos de nome para maior compatibilidade.
        contact_name = contact.get("name") or contact.get("pushName") or contact.get("displayName")
        print("Contato encontrado:", contact_name, contact)  # DEBUG: mostra o nome e o dicionário do contato.
        # Compara ignorando maiúsculas/minúsculas e verifica se o nome buscado está contido no nome do contato.
        if contact_name and name.lower() in contact_name.lower():
            # Tenta diferentes campos de número para maior compatibilidade.
            number = contact.get("number") or contact.get("id") or contact.get("user")
            print("Número encontrado:", number)  # DEBUG: mostra o número encontrado.
            return number  # Retorna o número assim que encontrar.
    # Se não encontrou nenhum contato correspondente, retorna None.