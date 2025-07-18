import os
import django
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from django.db.models import Count, Window
from django.db.models.functions import RowNumber
from starlette.concurrency import run_in_threadpool
from core.models import DialogueContext, Event, Message, User
django.setup()


async def store_message(user: User, sender: str, content: str, is_voice: bool):
    await run_in_threadpool(
        Message.objects.create,
        user=user,
        sender=sender,
        content=content,
        is_voice=is_voice
    )
    print({'status': 'Success: message stored.'})

async def store_context(user: User, context):
    # Salva ou atualiza o contexto de diálogo de longo prazo no banco.
    await run_in_threadpool(
        DialogueContext.objects.update_or_create,
        defaults={"context": context},
        user=user,  # Usa o ID do usuário como session_id.
    )

async def retrieve_context(user: User):
    # Recupera o contexto de diálogo de longo prazo do banco.
    context = await run_in_threadpool(
        lambda: DialogueContext.objects.filter(user=user).first()
    )
    return context.context if context else None

async def update_user(user: User, name: str, email: str):
    def _update():
        user.name = name
        user.email = email
        user.waiting_user_data = None
        user.save()

    await run_in_threadpool(_update)
    print({'status': 'Success: user info edited. End of process.'})


async def delete_user(user: User):
    await run_in_threadpool(user.delete)
    print({'status': 'Success: User deleted. End of process'})


async def create_user(phone_number):
    def _create():
        user = User(phone_number=phone_number, waiting_user_data="waiting_for_name_and_email")
        user.save()

    await run_in_threadpool(_create)
    print({'status': 'Pending: user created but not yet registered! End of process.'})


async def retrieve_history(user: User, quantity: int):
    def _get_data():
        from django.db.models import Q

        # Todas as mensagens para histórico (user + assistant)
        base_qs = Message.objects.filter(user=user)

        # Apenas mensagens do usuário, para contagem
        user_message_count = base_qs.filter(sender='user').count()

        # Recupera as últimas `quantity` mensagens (de ambos)
        qs_with_row = base_qs.annotate(
            row_number=Window(expression=RowNumber())
        ).order_by('-timestamp')[:quantity][::-1]

        history = list(qs_with_row)
        return history, user_message_count

    return await run_in_threadpool(_get_data)


async def store_event(user: User, event_data: dict):
    try: 
        def create_event():
            event = Event(user=user, **event_data)
            event.save()
            return event
        
        event = await run_in_threadpool(create_event)
        print(f"Success: event stored.\n ID: {event.id},\n Summary: {event.event_summary}")
    except Exception as e:
        print(f"Error storing event: {e}")
        return None
