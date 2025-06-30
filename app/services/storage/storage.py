import os
import django
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from django.db.models import Count, Window
from django.db.models.functions import RowNumber
from fastapi.concurrency import run_in_threadpool
from core.models import DialogueContext, Event, Message, User
django.setup()


async def store_message(user: User, sender: str, content: str, is_voice: bool):
    msg_user = await run_in_threadpool(
        Message.objects.create,
        user=user,
        sender='user',
        content=content,
        is_voice=is_voice
    )
    print({'status': 'Success: message stored.'})

async def store_context(user: User, context):
    # Salva ou atualiza o contexto de diálogo de longo prazo no banco.
    await run_in_threadpool(
        DialogueContext.objects.update_or_create,
        user=user,
        session_id=str(user.id),  # Usa o ID do usuário como session_id.
        context=context
    )

async def retrieve_context(user: User):
    # Recupera o contexto de diálogo de longo prazo do banco.
    context = await run_in_threadpool(
        lambda: DialogueContext.objects.filter(user=user).first()
    )
    return context.context if context else None

async def update_user(user: User, name: str, email: str):
    user.name = name
    user.email = email
    user.waiting_user_data = None
    user.save()
    print ({'status': 'Success: user info edited. End of process.'})

async def delete_user(user: User):
    user.delete()
    print ({'status': 'Success: User deleted. End of process'})


async def create_user(phone_number):
    user = User(phone_number=phone_number, waiting_user_data="waiting_for_name_and_email")
    user.save()
    print({'status': 'Pending: user created but not yet registered! End of process.'})


async def retrieve_history(user: User, quantity: int):
    def _get_data():
        base_qs = Message.objects.filter(user=user)
        
        qs_with_count = base_qs.annotate(
            row_number=Window(expression=RowNumber()),
            total=Window(expression=Count('id'))
        ).order_by('-timestamp')[:quantity][::-1]

        history = list(qs_with_count)
        total = history[0].total if history else 0
        return history, total

    return await run_in_threadpool(_get_data) 

async def store_event(user: User, event_data: dict):
    event = await run_in_threadpool(
        lambda: Event.objects.create(user=user, **event_data)
    )
    event.save()
    print({'status': 'Success: event stored.'})
