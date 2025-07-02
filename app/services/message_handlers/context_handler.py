import os
import django
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from app.services.context.context_storage import update_context
from app.services.storage.storage import retrieve_context
from core.models import User


async def context_handler(user: User, short_history: list, count: int):
    # Recupera o contexto geral da interação com o usuário.
    context = await retrieve_context(user)

    #Isso aqui é pra 
    if count % 10 == 0:
        # Se o número de mensagens for múltiplo de 10, atualiza o contexto.
        await update_context(user, short_history, context)

    return context