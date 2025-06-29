import os
from typing import List, Optional, Dict

from app.utils.now import now  # Importa a função de data e hora atual
# Importa as bibliotecas necessárias para autenticação e acesso à API do Google Calendar

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopo de acesso ao Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials() -> Credentials:
    """Autentica e retorna as credenciais do usuário"""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def get_events(user_email: str) -> List[Dict]:
    """Retorna os próximos 10 eventos do calendário do usuário, filtrando por e-mail do organizador"""
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

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


def create_event(
    event_summary: str,
    event_start: Dict,
    event_end: Dict,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[Dict[str, str]]] = None,
) -> Optional[Dict]:
    """Cria um evento no calendário do usuário"""
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': event_summary,
            'start': event_start,
            'end': event_end,
        }

        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if attendees:
            event['attendees'] = attendees

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print('Evento criado:', created_event.get('htmlLink'))
        return created_event

    except HttpError as error:
        print(f'Erro ao criar evento: {error}')
        return None
