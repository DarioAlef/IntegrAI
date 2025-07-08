
import datetime
import json
import os
from typing import Any, Dict, List, Union
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




def interpretar_comando(mensagem: str) -> Dict[str, Union[bool, str]]:
    # Lista de comandos implementados e funcionando:
    comandos_disponiveis = ["agendamento", "conversa"]
    # Esta função interpreta uma mensagem e identifica se é um comando de agendamento ou envio de mensagem.
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
Você é um assistente que identifica se uma mensagem transcrita contém um comando e se é um comando disponível.

## Regras:
- O comando deve ser um dos seguintes comandos disponíveis: {comandos_disponiveis}.
## Instruções:
1. Se a mensagem **não for um comando**, responda apenas com:
{{"is_command": false}}
2. Se for um comando disponível, responda com um JSON **no seguinte formato**:
{{"is_command": true, "command": "nome_do_comando"}}
3. Se a mensagem expressar um comando, mas ele não está na lista, ela ainda deve ser considerada um comando, então responda com:
{{"is_command": true, "command": "comando_indisponível"}}

Um comando geralmente expressa uma **ação direta desejada pelo usuário**, como "marcar", "agendar", "colocar na agenda", "mandar uma mensagem".
Abaixo estão exemplos de frases e se são comandos:

[
    {{
    "input": "Manda pra mim um resumo da 2a guerra mundial",
    "output": {{"is_command": true, "command": "conversa"}}
  }},
  {{
    "input": "Marca comigo o check-up anual pra quinta de manhã",
    "output": {{"is_command": true, "command": "agendamento"}}
  }},
  {{
    "input": "Avisa o João que o relatório já foi enviado",
    "output": {{"is_command": true, "command": "comando_indisponível"}}
  }},
  {{
    "input": "Preciso avisar o João que o relatório já foi enviado",
    "output": {{"is_command": false}}
  }},
  {{
    "input": "Chama a galera no grupo e lembra da reunião",
    "output": {{"is_command": true, "command": "comando_indisponível"}}
  }},
  {{
    "input": "Fala sobre a história da Itália pra mim",
    "output": {{"is_command": true, "command": "conversa"}}
  }},
  {{
    "input": "Coloca aí: reunião com fornecedores quarta às 9",
    "output": {{"is_command": true, "command": "agendamento"}}
  }},
  {{
    "input": "Desliga a luz da varanda, por favor",
    "output": {{"is_command": true, "command": "comando_indisponível"}}
  }},
  {{
    "input": "Ontem quase esqueci de mandar aquele e-mail",
    "output": {{"is_command": false}}
  }},
  {{
    "input": "Reserva um horário no salão pra sábado à tarde",
    "output": {{"is_command": true, "command": "agendamento"}}
  }}
]
"""
    mensagem = f"Mensagem:\"{mensagem}\""

    resposta = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}, {"role": "user", "content": mensagem}],
            temperature=0.0,
        )
    comando = resposta.choices[0].message.content.strip()

    try:
        return json.loads(comando)
    except json.JSONDecodeError:
        return {"error": True}


