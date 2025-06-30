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



from datetime import datetime

from app.utils.now import now

def validate_event_data(event_data):

    current_event_data = {}
    invalid_params = {}

    # 1. Validar se 'event_summary' e 'event_start' existem
    if event_data.get('event_summary'):
        current_event_data['event_summary'] = event_data['event_summary']
    else:
        invalid_params['event_summary'] = 'Este campo é obrigatório.'

    if event_data.get('event_start'):
        try:
            start = datetime.fromisoformat(event_data['event_start'])
            if start >= now:
                current_event_data['event_start'] = event_data['event_start']
            else:
                invalid_params['event_start'] = 'A data de início não pode estar no passado.'
        except ValueError:
            invalid_params['event_start'] = 'Formato de data inválido (use ISO 8601).'
    else:
        invalid_params['event_start'] = 'Este campo é obrigatório.'
        start = None  # Para evitar erro nas próximas validações
    # 2. Validar se 'event_end' não é antes de 'event_start'
    if event_data.get('event_end'):
        try:
            end = datetime.fromisoformat(event_data['event_end'])
            if start and end < start:
                invalid_params['event_end'] = 'A data de término não pode ser antes da data de início.'
            else:
                current_event_data['event_end'] = event_data['event_end']
        except ValueError:
            invalid_params['event_end'] = 'Formato de data inválido (use ISO 8601).'
    else:
        invalid_params['event_start'] = 'Este campo é obrigatório.'
        start = None  # Para evitar erro nas próximas validações

    # 3. Campos opcionais
    for key in ['description', 'location', 'attendees', 'reminders']:
        if key in event_data:
            current_event_data[key] = event_data[key]

    # 4. Validar visibility
    visibility = event_data.get('visibility', 'private')
    if visibility in ['private', 'public']:
        current_event_data['visibility'] = visibility
    else:
        invalid_params['visibility'] = "Valor inválido. Use 'private' ou 'public'."

    return current_event_data, invalid_params
