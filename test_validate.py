import sys
sys.path.append('/home/thiago/projects/IntegrAI')

from app.utils.validation import validate_event_data

# Testa com dados similares ao que está vindo da LLM
event_data = {
    'event_summary': 'Mostra Tech',
    'event_start': '2025-07-03T18:30:00-04:00',
    'event_end': None,  # LLM não retornou
    'description': '',
    'location': '',
    'attendees': [],
    'visibility': 'private',
    'reminders': [60, 120]
}

print("Testando validate_event_data...")
try:
    current_event_data, invalid_params = validate_event_data(event_data)
    print("✅ Sucesso!")
    print("current_event_data:", current_event_data)
    print("invalid_params:", invalid_params)
except Exception as e:
    print("❌ Erro:", e)
    import traceback
    traceback.print_exc()
