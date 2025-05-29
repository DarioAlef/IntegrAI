
# Função para extrair o texto de diferentes tipos de mensagens recebidas do WhatsApp
def extrair_texto(msg_data):
    # Se a mensagem for do tipo simples (texto direto)
    if "conversation" in msg_data:
        return msg_data["conversation"]
    # Se a mensagem for do tipo estendida (ex: resposta a outra mensagem)
    if "extendedTextMessage" in msg_data and "text" in msg_data["extendedTextMessage"]:
        return msg_data["extendedTextMessage"]["text"]
    # Se não encontrar texto, retorna None
    return None
