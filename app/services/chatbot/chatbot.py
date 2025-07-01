import os  # Importa o módulo 'os', que permite interagir com variáveis de ambiente do sistema operacional.
import json  # Importa o módulo 'json', usado para trabalhar com dados no formato JSON (não está sendo usado neste trecho, mas é comum em APIs).
import requests  # Importa o módulo 'requests', utilizado para fazer requisições HTTP (não está sendo usado neste trecho, mas é comum em integrações de API).
from dotenv import load_dotenv  # Importa a função 'load_dotenv' para carregar variáveis de ambiente de um arquivo .env.
from groq import Groq  # Importa a classe 'Groq', que é o cliente oficial para acessar a API da Groq.

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do Python.
load_dotenv() 

# Obtém o valor da variável de ambiente 'GROQ_API_KEY' (sua chave de API da Groq) e armazena na variável 'api_key'.
api_key = os.getenv("GROQ_API_KEY")  # Use a variável do seu .env

def get_llm_response(messages, context=None):
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
    groq_messages.append({
        "role": "system",
        "content": (
            "Responda sempre em português. Seu nome é IntegrAI. Você é um assistente que responde mensagens do usuário no WhatsApp."
            "Abaixo uma contextualização resumida da sua interação anterior com o usuário: \n"
            f"{context}\n"
            "Continue a conversa com base nesse histórico e no que vier a seguir."
        )
    })
    
    # Para cada mensagem recebida na lista 'messages':
    for m in messages:
        content = m.get("content", "")
        # Adiciona a mensagem convertida para o formato esperado pela Groq.
        groq_messages.append({
            "role": m.get("role", "user"),  # Define o papel da mensagem ('user' ou 'assistant').
            "content": content  # O texto da mensagem.
        })

    # Envia as mensagens para o modelo da Groq usando o método 'chat.completions.create'.
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # Nome do modelo de linguagem a ser usado. #deepseek-r1-distill-llama-70b
        messages=groq_messages,  # Lista de mensagens já formatadas.
        temperature=0.6,         # Controla a criatividade da resposta (0 = resposta mais previsível, 1 = mais criativa).
        max_tokens=2048,         # Número máximo de tokens (palavras/frases) na resposta.
        top_p=0.95,              # Parâmetro de amostragem para diversidade das respostas.
        stream=False,            # Se True, a resposta vem em partes (streaming); False retorna tudo de uma vez.
        stop=None,               # Parâmetro para definir onde a resposta deve parar (None = até o limite de tokens).
    )

    # Retorna apenas o texto da resposta gerada pelo modelo.
    return completion.choices[0].message.content  # A resposta final do assistente.
