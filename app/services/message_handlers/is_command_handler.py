from app.services.interpretation.command_interpretation import interpretar_comando

def command_handler(message):
    # Interpretar se é comando ou não
    interpretar_comando(message)
