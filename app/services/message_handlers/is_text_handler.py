from app.utils.text import extrair_texto

async def processar_texto(msg_data) -> str:
    text_data = extrair_texto(msg_data)
    if not text_data:
        return None


    return text_data