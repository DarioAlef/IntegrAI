import os  # Importa o módulo 'os', que permite interagir com variáveis de ambiente do sistema operacional.
import json  # Importa o módulo 'json', usado para trabalhar com dados no formato JSON (não está sendo usado neste trecho, mas é comum em APIs).
import requests  # Importa o módulo 'requests', utilizado para fazer requisições HTTP (não está sendo usado neste trecho, mas é comum em integrações de API).
from dotenv import load_dotenv  # Importa a função 'load_dotenv' para carregar variáveis de ambiente de um arquivo .env.
from groq import Groq  # Importa a classe 'Groq', que é o cliente oficial para acessar a API da Groq.

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do Python.
load_dotenv() 

# Obtém o valor da variável de ambiente 'GROQ_API_KEY' (sua chave de API da Groq) e armazena na variável 'api_key'.
api_key = os.getenv("GROQ_API_KEY")  # Use a variável do seu .env

def get_openrouter_response(messages, system_prompt=None):
    """
    Função para enviar mensagens para o modelo de linguagem da Groq e receber uma resposta.
    - messages: lista de dicionários, cada um representando uma mensagem no formato [{"role": "user", "content": "mensagem"}]
    - system_prompt: texto opcional para definir o comportamento do assistente (ex: "Responda sempre em português.")
    """
    # Se a chave da API não estiver definida, gera um erro explicativo.
    if not api_key:
        raise ValueError("API key not found. Please set the GROQ_API_KEY environment variable.")
    
    # Cria um cliente Groq usando a chave da API. Esse cliente será usado para enviar requisições para o modelo.
    client = Groq(api_key=api_key)

    # Lista que irá armazenar as mensagens no formato esperado pela API da Groq.
    groq_messages = []
    
    # Se um system_prompt foi fornecido, adiciona como a primeira mensagem (role 'system').
    if system_prompt:
        groq_messages.append({
            "role": "system",  # Define o papel da mensagem como 'system', que serve para orientar o modelo.
            "content": system_prompt  # O texto do prompt do sistema.
        })
    
    # Para cada mensagem recebida na lista 'messages':
    for m in messages:
        # Se o campo 'content' for uma lista (ex: [{"type": "text", "text": ...}]), junta todos os textos em uma única string.
        if isinstance(m.get("content"), list):
            # Percorre cada item da lista e pega o valor do campo 'text', juntando tudo em uma string separada por espaço.
            content = " ".join([c.get("text", "") for c in m["content"]])
        else:
            # Se não for lista, pega o valor diretamente.
            content = m.get("content", "")
        # Adiciona a mensagem convertida para o formato esperado pela Groq.
        groq_messages.append({
            "role": m.get("role", "user"),  # Define o papel da mensagem ('user' ou 'assistant').
            "content": content  # O texto da mensagem.
        })

    # Envia as mensagens para o modelo da Groq usando o método 'chat.completions.create'.
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",  # Nome do modelo de linguagem a ser usado.
        messages=groq_messages,  # Lista de mensagens já formatadas.
        temperature=0.6,         # Controla a criatividade da resposta (0 = resposta mais previsível, 1 = mais criativa).
        max_tokens=2048,         # Número máximo de tokens (palavras/frases) na resposta.
        top_p=0.95,              # Parâmetro de amostragem para diversidade das respostas.
        stream=False,            # Se True, a resposta vem em partes (streaming); False retorna tudo de uma vez.
        stop=None,               # Parâmetro para definir onde a resposta deve parar (None = até o limite de tokens).
    )

    # Retorna apenas o texto da resposta gerada pelo modelo.
    return completion.choices[0].message.content  # A resposta final do assistente.
