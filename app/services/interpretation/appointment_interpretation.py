
import datetime
import json
import os
from typing import Any, Dict, List, Union
from dotenv import load_dotenv
from groq import Groq  # Importa o cliente Groq
from app.utils.now import now  # Importa a função de data e hora atual

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


def interpretar_agendamento(mensagem: str, missing_data: Dict[str, Any]) -> Union[Dict[str, Any], None]:

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
    Você é um assistente que vai identificar informações sobre agendamentos em mensagens.

    ## Instruções:

    Responda somente com JSON válido **no seguinte formato** com os dados extraídos da mensagem:

    {{
    "event_summary": str,              # Título ou motivo do evento. Se **não identificar um título claro**, use `"lembrete sem título" (ex: "Reunião com fornecedores"),
    "event_start": datetime,           # Data e hora de início do evento, sempre no fuso horário **-04:00 (America/Manaus)**. Se a mensagem **não contiver uma data**, deixe como `""` (ex: "2025-06-28T14:00:00-04:00")
    "event_end": datetime,             # Horário de término do evento, sempre no fuso horário **-04:00 (America/Manaus)**. Se não houver horário de término mencionado, defina como 1h após o horário de início (se tiver) (ex: "2025-06-28T15:00:00-04:00").
    "description": str,                # Descrição do evento, se mencionada na mensagem. Se não houver descrição, deixe como `""` (ex: "Reunião para discutir o projeto X"),
    "location": str,                   # Local do evento, se mencionado. Se não houver local, deixe como `""` (ex: "Sala de reuniões 1"),
    "attendees": List[Dict[str, str]], # Convidados mencionados, se houver. Se não houver, deixe como uma lista vazia `[]` (ex: [{{"email": "joao@x.com"}}, {{"displayName": "Pedro", "email": "pedro_gg@gmail.com"}}])
    "visibility": str                  # Por padrão deixe como "private", mas se a mensagem mencionar que é um evento público, use "public" (ex: "public" ou "private")
    "reminders": List[int]             # Se houver pedidos de lembrete na mensagem, como "me avisa", "notifica", etc., adicione o tempo de antecedência especificado para cada lembrete na lista. (ex: [60])
    }}

    ## Considere a Data e Hora atuais:
    "{now}"

    ## Considere o current_event_data -> se não estiver vazio, é porque já há dados de evento em andamento e o usuário pode estar corrigindo ou complementando esses dados. Use esses dados como base para completar as informações do evento de acordo com a mensagem.

    ## Regras:
    - O agendamento deve ser sempre para o **futuro**, nunca para o passado.
    - Quando a mensagem mencionar um dia da semana (ex: segunda, terça, quarta), converta sempre para a próxima ocorrência futura desse dia considerando a data atual."
    - Se houver **horário mas não data**, agende para hoje se ainda der tempo, senão para amanhã.
    - Se contiver **data mas não horário**, use `09:00` da manhã como event_start.
    - O datetime de event_end nunca pode ser menor que o de event_start.
    - Se não houver ano mencionado, use o ano vigente.
    - Se a mensagem disser para lembrar ou notificar antes do evento, inclua no campo `reminders.overrides` com `"method": "popup"` e `"minutes"` com o tempo mencionado. 60 minutos é o padrão se não houver tempo especificado.

    ## Exemplos de mensagens e como devem ser interpretadas:
        {{
        "mensagem": "Marca reunião com o time de produto amanhã às 14h no Google Meet",evento
        "output": {{
            "event_summary": "Reunião com o time de produto",
            "event_start": "2025-06-30T14:00:00-04:00",
            "location": "Google Meet"
            }}
        }},
        {{
        "mensagem": "Agende uma consulta com o Dr. João na terça-feira às 9h",
        "output": {{
            "event_summary": "Consulta com o Dr. João",
            "event_start": "2025-07-01T09:00:00-04:00"
            }}
        }},
        {{
        "mensagem": "Marca dentista quarta-feira às 9h e bota pra lembrar na terça e 1 hora antes.",
        "output": {{
            "event_summary": "Dentista",
            "event_start": "2025-07-02T09:00:00-04:00",
            "event_end": "2025-07-02T10:00:00-04:00",
            "description": "",
            "location": "",
            "attendees": [],
            "visibility": "private",
            "reminders": [60, 1440]
            }}
        }},
        {{
            "missing_data": event_start,
            "mensagem": "18h no Golden Gol",
            "output": {{
                "event_start": "2025-07-01T18:00:00-04:00",
                "location": "Golden Gol"
            }}
        }}

    ## missing_data:
    {missing_data}
    ## Mensagem:
    "{mensagem}"
    """
    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    conteudo = resposta.choices[0].message.content.strip()
    # print("🧾 Conteúdo bruto da LLM:\n", conteudo)

    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        return {"error": True}
