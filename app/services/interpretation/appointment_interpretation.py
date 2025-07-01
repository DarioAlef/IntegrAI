import json
import os
from typing import Any, Dict, List, Union
from dotenv import load_dotenv
from groq import Groq  # Importa o cliente Groq
from app.utils.now import now  # Importa a função de data e hora atual

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


def interpretar_agendamento(conversation: Dict[str, Any]) -> Union[Dict[str, Any], None]:

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    system_prompt = f"""
    Você é um assistente especializado em interpretar informações de agendamento com base em mensagens do usuário.

    ## Objetivo

    Com base nas mensagens trocadas entre o usuário e o assistente, seu objetivo é gerar um JSON **válido** que represente os dados completos do evento.  
    O usuário pode estar fornecendo os dados aos poucos, corrigindo ou completando o evento.

    ## Instruções:

    Responda somente com JSON válido **no seguinte formato** com os dados extraídos da conversa:

    {{
    "event_summary": str,              # Título ou motivo do evento. Se **não identificar um título claro**, use `"lembrete sem título" (ex: "Reunião com fornecedores"),
    "event_start": datetime,           # Data e hora de início do evento, sempre no fuso horário **-04:00 (America/Manaus)**. Se a mensagem **não contiver uma data**, deixe como `""` (ex: "2025-06-28T14:00:00-04:00")
    "event_end": datetime,             # Horário de término do evento, sempre no fuso horário **-04:00 (America/Manaus)**. Se não houver horário de término mencionado, defina como 1h após o horário de início (se tiver) (ex: "2025-06-28T15:00:00-04:00").
    "description": str,                # Descrição do evento, se mencionada pelo usuário. Se não houver descrição, deixe como `""` (ex: "Reunião para discutir o projeto X"),
    "location": str,                   # Local do evento, se mencionado. Se não houver local, deixe como `""` (ex: "Sala de reuniões 1"),
    "attendees": List[Dict[str, str]], # Convidados mencionados, se houver. Se não houver, deixe como uma lista vazia `[]` (ex: [{{"email": "joao@x.com"}}, {{"displayName": "Pedro", "email": "pedro_gg@gmail.com"}}])
    "visibility": str                  # Por padrão deixe como "private", mas se o usuário mencionar que é um evento público, use "public" (ex: "public" ou "private")
    "reminders": List[int]             # Lista de lembretes em minutos antes do evento. (ex: [60])
    }}

    ## Considere a Data e Hora atuais:
    "{now}"

    ## Regras:
    - O evento sempre deve ser para o futuro.
    - Se o usuário menciona dias da semana, considere a **próxima ocorrência futura** desse dia.
    - Se só há horário (ex: “às 15h”), agende para **hoje se ainda der tempo**, senão para amanhã.
    - Se contiver **data mas não horário**, use `09:00` da manhã como event_start.
    - Se não houver ano mencionado, use o ano vigente.
    - Se o usuário disser para lembrar ou notificar, como "me avisa 2h antes do evento", adicione o valor correspondente (neste caso seria 120) no array `reminders`. 60 é o padrão.

    ## Exemplos de conversa e como devem ser interpretadas:
        {{
        "conversation": [
            {{"role": "user", "content": "Marca reunião com o time de produto amanhã às 14h no Google Meet"}},
        ],
        "output": {{
            "event_summary": "Reunião com o time de produto",
            "event_start": "2025-06-30T14:00:00-04:00",
            "location": "Google Meet"
        }}
        }},
        {{
        "conversation": [
            {{"role": "user", "content": "Agende uma consulta com o Dr. João"}},
            {{"role": "assistant", "content": "Identifiquei que você quer agendar um evento:\n\n{{"event_summary": "Consulta com o Dr. João"}}\n\nMas tive dúvidas nos campos:\n\n{{"event_start": 'Este campo é obrigatório.'}}.\n\nMe envie os dados corrigidos pra continuar. Tô te escutando!"}}
            {{"role": "user", "content": "na terça-feira às 18h"}},
        ],
        "output": {{
            "event_summary": "Consulta com o Dr. João",
            "event_start": "2025-07-01T18:00:00-04:00"
        }}
        }},
        {{
        "conversation": [
            {{"role": "user", "content": "Marca dentista e bota pra lembrar na terça e 1 hora antes."}},
            {{"role": "assistant", "content": "Entendi que você quer agendar um evento:\n\n{{\"event_summary\": \"Dentista\"}}\n\nMas tive dúvidas nos campos:\n\n{{\"event_start\": \"'Este campo é obrigatório.'\"}}\n\nMe envie os dados corrigidos pra continuar. Tô te escutando!"}},
            {{"role": "user", "content": "Tinha me esquecido, é quarta-feira às 9h"}}
        ],
        "output": {{
            "event_summary": "Dentista",
            "event_start": "2025-07-02T09:00:00-04:00",
            "reminders": [60, 1440]
        }}
        }}
    """

    # ✅ Início dos logs e validações
    print("\n🔍 Verificando formato da conversa enviada à LLM...")

    for idx, msg in enumerate(conversation):
        if not isinstance(msg, dict):
            print(f"❌ ERRO: Mensagem {idx} não é um dicionário: {msg}")
        elif 'role' not in msg or 'content' not in msg:
            print(f"❌ ERRO: Mensagem {idx} está malformada: {msg}")
        else:
            print(f"✅ Mensagem {idx} OK - role: {msg['role']}, content: {msg['content'][:50]}...")


    groq_messages = [{"role": "system", "content": system_prompt}]
    groq_messages.extend(conversation)

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=groq_messages,
        temperature=0.0,
    )

    print("\n📥 Resposta bruta da LLM:\n", conteudo)

    conteudo = resposta.choices[0].message.content.strip()
    # print("🧾 Conteúdo bruto da LLM:\n", conteudo)

    try:
        return json.loads(conteudo)
    except json.JSONDecodeError as e:
        print("❌ Erro ao decodificar JSON da resposta:", e)
        return {"error": True}
