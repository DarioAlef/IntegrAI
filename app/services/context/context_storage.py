import os
import django
# Inicializa o Django para permitir uso dos modelos fora do padrão Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integrai.settings')
django.setup()
from app.services.context.summary import gerar_resumo
from app.services.storage.storage import store_context
from core.models import User

async def update_context(user: User, short_history: list, old_context):
    result = gerar_resumo(short_history, user, old_context)
    new_context = result
    await store_context(user, new_context)

