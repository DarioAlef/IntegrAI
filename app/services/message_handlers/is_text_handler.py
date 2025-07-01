from app.services.storage.storage import store_message
from app.utils.text import extrair_texto

async def processar_texto(msg_data, user) -> str:
    text_data = extrair_texto(msg_data)
    if not text_data:
        return None

    await store_message(user, 'user', text_data, is_voice=False)
    return text_data