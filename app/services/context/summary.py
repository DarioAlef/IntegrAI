from app.services.chatbot.chatbot import get_llm_response
from starlette.concurrency import run_in_threadpool
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')

def gerar_resumo(messages):
    prompt = (
        "Resuma a conversa abaixo em português, focando nos pontos principais e mantendo o contexto para futuras interações:\n\n"
    )
    # Concatene as mensagens em ordem cronológica
    texto = "\n".join(
        [f"{m['role']}: {m['content'][0]['text']}" for m in messages if m.get("content")]
    )
    full_prompt = prompt + texto
    resumo = get_llm_response([{"role": "user", "content": full_prompt}])
    return resumo