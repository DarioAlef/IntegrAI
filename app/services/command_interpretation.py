
import datetime
import json
import os
from typing import Dict, List, Union
from dotenv import load_dotenv
from groq import Groq  # Importa o cliente Groq
from app.utils.now import now  # Importa a função de data e hora atual

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# ██ ███    ██ ████████ ███████ ██████  ██████  ██████  ███████ ████████  █████  ██████   ██████  ██████
# ██ ████   ██    ██    ██      ██   ██ ██   ██ ██   ██ ██         ██    ██   ██ ██   ██ ██    ██ ██   ██
# ██ ██ ██  ██    ██    █████   ██████  ██████  ██████  █████      ██    ███████ ██   ██ ██    ██ ██████
# ██ ██  ██ ██    ██    ██      ██   ██ ██      ██   ██ ██         ██    ██   ██ ██   ██ ██    ██ ██   ██
# ██ ██   ████    ██    ███████ ██   ██ ██      ██   ██ ███████    ██    ██   ██ ██████   ██████  ██   ██


def interpretar_comando_novo_agendamento(mensagem: str) -> bool:

    recognized_event_data = {
        "event_summary": str,
        "event_start": datetime,
        "event_end": datetime,
        "description": str,
        "location": str,
        "attendees": List[Dict[str, str]]
    }

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
    Você é um assistente que identifica se uma mensagem transcrita contém um comando para agendamento.
    Responda apenas com "SIM" ou "NÃO", sem explicações.
    Um comando geralmente expressa uma **ação direta desejada pelo usuário**, como "marcar", "agendar", "colocar na agenda".
    Abaixo estão exemplos de frases e se são comandos:

    "Marca pra mim no dia 12" → SIM  
    "Ontem foi dia 23 e eu ainda não..." → NÃO  
    "Agende pra mim cabelereira na sexta-feira que vem" → SIM  
    "Coloca na agenda pra mim por favor" → SIM  
    "Aquele meu amigo tinha marcado de vir aqui" → NÃO  

    Agora analise a seguinte frase:
    "{mensagem}"
    """
    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    comando = resposta.choices[0].message.content.strip().lower()
    return False if comando == "não" else True


def interpretar_comando_novo_agendamento_e_reconhecer(mensagem: str) -> Union[Dict, None]:

    recognized_event_data = {
        "event_summary": str,
        "event_start": datetime,
        "event_end": datetime,
        "description": str,
        "location": str,
        "attendees": List[Dict[str, str]]
    }

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
    Você é um assistente que interpreta mensagens transcritas de voz e detecta se são comandos de agendamento.

    ## Instruções:

    1. Se a mensagem **não for um comando de agendamento**, responda apenas com:
    {{"error": true}}

    2. Se for um comando de agendamento, responda com um JSON **no seguinte formato**:
    {{
    "event_summary": "Título ou motivo do evento",
    "event_start": "AAAA-MM-DDTHH:MM:SS-04:00",
    "event_end": "AAAA-MM-DDTHH:MM:SS-04:00",
    "description": "",
    "location": "",
    "attendees": [{{"email": "exemplo@email.com", "displayName": "Nome do Participante"}}]
    }}

    ## Regras:
    - O agendamento deve ser sempre para o **futuro**, nunca para o passado.
    - Se a mensagem **não contiver uma data**, deixe `event_start` e `event_end` como `""`.
    - Se contiver **data mas não horário**, use `09:00` da manhã como horário inicial.
    - Se tiver horário de início mas **não mencionar o horário de término**, defina como 1h de duração.
    - Se **não identificar um título claro**, use `"lembrete sem título"`.
    - Se não houver ano mencionado, use o ano vigente.
    - Use sempre o fuso horário **-04:00 (America/Manaus)**.
    - O campo `attendees` pode ser uma lista vazia.

    ## Hora atual:
    "{now}"

    ## Mensagem:
    "{mensagem}"
    """
    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    
    conteudo = resposta.choices[0].message.content.strip()

    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        return {"error": True}
