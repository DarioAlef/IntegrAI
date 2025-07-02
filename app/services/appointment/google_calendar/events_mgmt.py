import os
from typing import List, Optional, Dict
import datetime as dt
from zoneinfo import ZoneInfo

# from app.utils.now import now  # Importa a função de data e hora atual
# Importa as bibliotecas necessárias para autenticação e acesso à API do Google Calendar

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.utils.validation import format_event_time

# Escopo de acesso ao Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials() -> Credentials:
    """Autentica e retorna as credenciais do usuário"""
    creds = None

    # Caminho absoluto até a pasta onde está este script
    dir_path = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(dir_path, 'credentials.json')
    token_path = os.path.join(dir_path, 'token.json')
    print(f"credentials_path: {credentials_path}")
    print(f"token_path: {token_path}")
    print(f"SCOPES: {SCOPES}")
    

    if os.path.exists(token_path):
        print(f"Token file found at: {token_path}")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        print("Credenciais inválidas ou expiradas. Iniciando o fluxo de autenticação...")
        if creds and creds.expired and creds.refresh_token:
            print("Tentando atualizar as credenciais...")
            creds.refresh(Request())
        else:
            print("Nenhum token encontrado ou credenciais inválidas. Iniciando o fluxo de autenticação...")
            print("creds: ", creds)
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_user_events(user_email: str) -> List[Dict]:
    """Retorna os próximos 10 eventos do calendário do usuário, filtrando por e-mail do organizador"""
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        

        events_result = service.events().list(
            calendarId='primary',
            timeMin= dt.datetime.now().astimezone(ZoneInfo('America/Manaus')).isoformat(),
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        print(events)
        print(events_result)
        filtered_events = []
        for event in events:
            organizer = next(
                (a for a in event.get('attendees', []) if a.get('comment') == 'Organizador'),
                None
            )

            if organizer and organizer.get('email') == user_email:
                filtered_events.append(event)

        return filtered_events

    except HttpError as error:
        print(f'Erro ao buscar eventos: {error}')
        return []


from fastapi.concurrency import run_in_threadpool

async def create_event_async(
    event_summary: str,
    event_start: Dict,
    event_end: Dict,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[Dict[str, str]]] = None,
    visibility: Optional[str] = 'private',
    reminders: Optional[List[int]] = None
) -> Optional[Dict]:
    def blocking_create_event():
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': event_summary,
            'start': format_event_time(event_start),
            'end': format_event_time(event_end),
            'visibility': visibility or 'private'
        }

        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if attendees:
            event['attendees'] = attendees
        if visibility:
            event['visibility'] = visibility
        if reminders:
            event['reminders'] = {
                'useDefault': False,
                'overrides': [{'method': 'popup', 'minutes': r} for r in reminders]
            }

        return service.events().insert(calendarId='primary', body=event).execute()

    try:
        created_event = await run_in_threadpool(blocking_create_event)
        print('Evento criado:', created_event.get('htmlLink'))
        return created_event
    except HttpError as error:
        print(f'Erro ao criar evento: {error}')
        return None


# if __name__ == "__main__":
#     # Testar a funcao de ver eventos do usuario
#     user_email = 'thsilva.developer@gmail.com'
#     events = get_user_events(user_email)
#     print(f'Eventos encontrados para {user_email}:')
#     for event in events:
#         print(f" - {event['summary']} ({event['start'].get('dateTime', event['start'].get('date'))})")