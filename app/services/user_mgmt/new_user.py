import os
import django
from core.models import User  # Importa o modelo User do Django.
from starlette.concurrency import run_in_threadpool  # Permite rodar funções bloqueantes
from app.services.context.context_storage import armazenar_contexto  # Importa a função para armazenar contexto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()

async def check_user(sender_number, data):
    sender_number = data['data']['key']['remoteJid'].split("@")[0]
    
    # Busca ou cria o usuário no banco de dados, usando o número do remetente.
    if sender_number:
        # O método get_or_create retorna uma tupla (objeto, criado), por isso o "_".
        user, _ = await run_in_threadpool(
            User.objects.get_or_create, 
            phone_number=
            sender_number
            )
        
        await armazenar_contexto(user)
    return user
#     # =======================    