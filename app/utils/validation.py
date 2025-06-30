# O arquivo utils.py geralmente serve para armazenar funções utilitárias e auxiliares que 
# são usadas em diferentes partes do projeto, mas que não pertencem diretamente a modelos, 
# views ou ações específicas. Ele ajuda a organizar o código e evitar repetição.

def is_valid_name_and_email(message):
    if not message:
          return None
    try:
        name, email = [x.strip() for x in message.split(',')]
        if '@' in email and name:
            return {'name': name, 'email': email}
    except Exception:
        pass
    return None



def valid_user_message(message, from_me, user_authenticated):
                if message and not from_me and user_authenticated:
                    return True
                return False