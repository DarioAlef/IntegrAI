import json
import os
from typing import Any, Dict, List, Union
from dotenv import load_dotenv
from groq import Groq  # Importa o cliente Groq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


def interpretar_confirmacao(mensagem: str) -> Dict[str, Union[bool, str]]:
    # Esta função interpreta uma mensagem e identifica se é uma confirmação de agendamento.
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""Você é um assistente que identifica se uma mensagem transcrita contém é uma mensagem confirmativa (SIM) ou negativa (não).
        ## Instruções:
        1. Se a mensagem **não for uma confirmação**, responda apenas com um JSON **no seguinte formato**:
        {{
            "is_confirmation": "no"
        }}
        2. Se for uma confirmação, responda com um JSON **no seguinte formato**:
        {{
            "is_confirmation": "yes",
        }}
        3. Se você não identificar nem confirmação, nem negação, responda com um JSON válido **no seguinte formato**:
        {{
            "is_confirmation": "unidentified",
        }}

        ## Exemplos de mensagens e como devem ser interpretadas:
        [
            {{
                "input": "Sim, está ótimo.",
                "output": {{"is_confirmation": "yes" }}
            }},
            {{
                "input": "Claro, sem problemas.",
                "output": {{"is_confirmation": "yes" }}
            }},
            {{
                "input": "Beleza, pode confirmar.",
                "output": {{"is_confirmation": "yes" }}
            }},
            {{
                "input": "Não, melhor não.",
                "output": {{"is_confirmation": "no" }}
            }},
            {{
                "input": "Prefiro que não.",
                "output": {{"is_confirmation": "no" }}
            }},
            {{
                "input": "Negativo.",
                "output": {{"is_confirmation": "no" }}
            }},
            {{
                "input": "Perfeito, mas muda o título do evento para festa.",
                "output": {{"is_confirmation": "no" }}
            }},
            {{
                "input": "Pode mandar ver!",
                "output": {{"is_confirmation": "yes" }}
            }},
            {{
                "input": "Tanto faz pra mim.",
                "output": {{"is_confirmation": "unidentified" }}
            }},
            {{
                "input": "Isso não é comigo.",
                "output": {{"is_confirmation": "unidentified" }}
            }},
            {{
                "input": "9 horas da noite",
                "output": {{"is_confirmation": "no"}}
            }}
        ]

        ## Mensagem
        {mensagem}
        """

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    try:
        return json.loads(resposta.choices[0].message.content.strip())
    except json.JSONDecodeError:
        return {"error": "Erro na interpretação"}
    


def interpretar_cancelamento(mensagem: str) -> Dict[str, Union[bool, str]]:
    # Esta função interpreta uma mensagem e identifica se é um pedido de cancelamento de processo.
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""Você é um assistente que identifica se uma mensagem do usuário expressa o desejo de **cancelar um processo de agendamento**.

    ## Instruções:
    1. Se a mensagem indicar **claramente** que o usuário quer cancelar, encerrar ou desistir do agendamento, responda com um JSON válido **no seguinte formato**:
    {{
        "is_cancellation": "yes"
    }}
    2. Se a mensagem indicar que ele quer continuar, mudar algo ou retomar, mas **não cancelar**, responda com um JSON válido **no seguinte formato**:
    {{
        "is_cancellation": "no"
    }}
    3. Se não for possível identificar, responda com um JSON válido **no seguinte formato**:
    {{
        "is_cancellation": "unidentified"
    }}

    ## Exemplos de mensagens e como devem ser interpretadas:
    [
        {{
            "input": "Deixa pra lá",
            "output": {{"is_cancellation": "yes"}}
        }},
        {{
            "input": "Esquece isso",
            "output": {{"is_cancellation": "yes"}}
        }},
        {{
            "input": "Cancela tudo",
            "output": {{"is_cancellation": "yes"}}
        }},
        {{
            "input": "Não quero mais agendar",
            "output": {{"is_cancellation": "yes"}}
        }},
        {{
            "input": "Na real, depois eu marco isso",
            "output": {{"is_cancellation": "yes"}}
        }},
        {{
            "input": "Só quero mudar o horário",
            "output": {{"is_cancellation": "no"}}
        }},
        {{
            "input": "Sim, pode confirmar",
            "output": {{"is_cancellation": "no"}}
        }},
        {{
            "input": "Me mostra os dados do evento de novo",
            "output": {{"is_cancellation": "no"}}
        }},
        {{
            "input": "Hmmm",
            "output": {{"is_cancellation": "unidentified"}}
        }},
        {{
            "input": "Tanto faz pra mim",
            "output": {{"is_cancellation": "unidentified"}}
        }}
    ]

    ## Mensagem:
    {mensagem}
    """

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    try:
        return json.loads(resposta.choices[0].message.content.strip())
    except json.JSONDecodeError:
        return {"error": "Erro na interpretação"}
