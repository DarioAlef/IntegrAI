from app.services.storage.storage import store_message
from app.utils.text import extrair_texto

def processar_texto(data, user) -> str:
    msg_data = data["data"]["message"]
    text_data = extrair_texto(msg_data)
    if not text_data:
        return None

    store_message(user, 'user', text_data, is_voice=False)
    return text_data