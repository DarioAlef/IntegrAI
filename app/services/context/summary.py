# Importa a função que gera resposta do modelo LLM (Large Language Model).
from app.services.chatbot.chatbot import get_llm_response

# Importa utilitário para rodar funções bloqueantes em thread separada (não está sendo usado aqui, mas pode ser útil).
from starlette.concurrency import run_in_threadpool

import os  # Importa o módulo para manipulação de variáveis de ambiente.

# Garante que as configurações do Django estejam carregadas para acesso aos modelos, caso necessário.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')

def gerar_resumo(messages):
    """
    Gera um resumo de longo prazo da conversa, usando um modelo de linguagem (LLM).
    Parâmetros:
        messages (list): Lista de mensagens no formato [{"role": "user"/"assistant", "content": [{"type": "text", "text": ...}]}]
    Retorna:
        resumo (str): Texto resumido da conversa.
    """
    # Prompt base que orienta o modelo a resumir a conversa em português, focando nos pontos principais.
    prompt = (
        "Resuma a conversa abaixo em português, focando nos pontos principais e mantendo o contexto para futuras interações:\n\n"
    )

    # Concatena todas as mensagens em ordem cronológica, formatando cada uma como "role: texto".
    # Exemplo: "user: Olá\nassistant: Oi, como posso ajudar?\n..."
    texto = "\n".join(
        [f"{m['role']}: {m['content'][0]['text']}" for m in messages if m.get("content")]
    )

    # Junta o prompt de instrução com o histórico de mensagens.
    full_prompt = prompt + texto

    # Chama o modelo LLM para gerar o resumo, passando o prompt completo como se fosse uma mensagem do usuário.
    # O modelo irá retornar um texto resumido da conversa.
    resumo = get_llm_response([{"role": "user", "content": full_prompt}])

    # Retorna o resumo gerado.
    return resumo