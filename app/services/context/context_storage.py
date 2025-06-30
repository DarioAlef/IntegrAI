import os
import django
from core.models import Message, DialogueContext
from app.services.context.summary import gerar_resumo
from starlette.concurrency import run_in_threadpool
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
   
async def armazenar_contexto(user):
   
        # Recupera todas as mensagens do usuário para gerar um resumo de longo prazo.
        all_msgs = await run_in_threadpool(
            lambda: list(Message.objects.filter(user=user).order_by('timestamp'))
        )
        # Prepara o histórico para o resumo.
        all_msgs_fmt = []
        for m in all_msgs:
            role = 'user' if m.sender == 'user' else 'assistant'
            all_msgs_fmt.append({"role": role, "content": [{"type": "text", "text": m.content}]})

        # Gera o resumo do histórico de longo prazo.
        resumo = gerar_resumo(all_msgs_fmt)

        # Salva ou atualiza o contexto de diálogo de longo prazo no banco.
        await run_in_threadpool(
            DialogueContext.objects.update_or_create,
            user=user,
            session_id=str(user.id),  # Usa o ID do usuário como session_id.
            defaults={"context": {"resumo": resumo}}
        )