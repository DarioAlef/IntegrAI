import os
import json

from dotenv import load_dotenv
from groq import Groq
from app.services.chatbot.chatbot import get_llm_response

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do Python.
load_dotenv()

# Obtém o valor da variável de ambiente 'GROQ_API_KEY' (sua chave de API da Groq) e armazena na variável 'api_key'.
api_key = os.getenv("GROQ_API_KEY")  # Use a variável do seu .env

# Importa o módulo para manipulação de variáveis de ambiente.

def gerar_resumo(messages, user, old_context):
    # Esta função interpreta uma mensagem e identifica se é um comando de agendamento ou envio de mensagem.
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    # Prompt base que orienta o modelo a resumir a conversa em português, focando nos pontos principais.
    system_prompt = f"""
        "Você é um assistente responsável por atualizar o **resumo** e o **perfil do usuário** com base em uma conversa recente entre o usuário e o assistente de IA.
            ## Regras:
            - Sempre responda com um JSON válido no seguinte formato:
            {{
              "resumo": str,  # Um resumo de até 400 caracteres da conversa,
              "user_profile_data": dict  # Um dicionário com dados relevantes sobre o usuário
            }}
            - Em 'resumo', faça uma descrição clara e curta resumindo o perfil de conversa e interesse do usuário e o que foi discutido ou solicitado nas últimas mensagens.
            - Em 'user_profile_data', adicione ou atualize dados úteis do usuário como: 'nickname', 'cidade_atual', 'aniversário', 'cpf', 'amigos', etc.
            - Se não houver dados suficientes para adicionar algum campo, não o faça (não crie chaves com valores imaginados).
            - Nunca remova campos já existentes — apenas adicione ou atualize valores.
    """
    # Prompt do usuário que contém o contexto da conversa e as mensagens recentes.
    user_prompt = f"""
            ## Contexto anterior:\n{old_context}\n\n"
            ## Novas mensagens:\n{messages}\n\n"
            ## Nome do usuário:\n{user.name}\n"
    """
    # Chama o modelo LLM para gerar o resumo, passando o prompt completo como se fosse uma mensagem do usuário.
    # O modelo irá retornar um texto resumido da conversa.
    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt}],
        temperature=0.0,
    )
    new_context = resposta.choices[0].message.content.strip()
    print("Resposta LLM bruta: ", new_context)

    try:
        return json.loads(new_context)
    except json.JSONDecodeError:
        return {"error": True}
