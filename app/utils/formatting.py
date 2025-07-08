import locale
from datetime import datetime
import re

# Configura a localidade para português (pt_BR)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR')  # Windows
    except locale.Error:
        locale.setlocale(locale.LC_TIME, '')  # fallback pro default

def formatar_data_evento(data_inicio_iso: str, data_fim_iso: str) -> str:
    """Formata datas ISO para string em português, incluindo o dia do fim se for diferente."""
    data_inicio = datetime.fromisoformat(data_inicio_iso)
    data_fim = datetime.fromisoformat(data_fim_iso)

    mesmo_dia = data_inicio.date() == data_fim.date()

    inicio_formatado = data_inicio.strftime("%A, %-d de %B de %Y às %H:%M")

    if mesmo_dia:
        fim_formatado = data_fim.strftime("%H:%M")
        return f"{inicio_formatado} até {fim_formatado}"
    else:
        fim_formatado = data_fim.strftime("%A, %-d de %B de %Y às %H:%M")
        return f"{inicio_formatado} até {fim_formatado}"
    


def format_event_confirmation_message(current_event_data: dict) -> str:
    def format_datetime(iso_str: str) -> str:
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime('%d/%m/%Y às %H:%M')
        except Exception:
            return 'Data inválida'

    def format_reminders(reminders: list) -> str:
        if not reminders:
            return 'Nenhum lembrete definido'

        formatted = []
        for reminder in reminders:
            # Se for dict com chave 'minutes'
            if isinstance(reminder, dict):
                minutes = reminder.get('minutes')
            # Se for int direto
            elif isinstance(reminder, int):
                minutes = reminder
            else:
                continue  # ignora qualquer outro tipo

            if not isinstance(minutes, int):
                continue
            if minutes < 60:
                formatted.append(f"{minutes} min")
            elif minutes < 1440:
                hours = minutes // 60
                formatted.append(f"{hours}h")
            else:
                days = minutes // 1440
                remaining_minutes = minutes % 1440
                hours = remaining_minutes // 60
                suffix = f"{days}d"
                if hours:
                    suffix += f"{hours}h"
                formatted.append(suffix)
        return ', '.join(formatted) if formatted else 'Nenhum lembrete válido'

    # Formatação principal
    summary = current_event_data.get('event_summary', 'Não informado')
    start = format_datetime(current_event_data.get('event_start', ''))
    end = format_datetime(current_event_data.get('event_end', ''))
    location = current_event_data.get('location', 'Não informado')
    description = current_event_data.get('description', 'Não informada')
    visibility = current_event_data.get('visibility', 'private')

    attendees_list = current_event_data.get('attendees', [])
    attendees_str = '\n'.join(f"  - {a.get('email')}" for a in attendees_list) if attendees_list else "  - Nenhum participante"

    reminders_str = format_reminders(current_event_data.get('reminders', []))

    return f"""✅ Verifica se está tudo certinho para o agendamento:

📌 *Título do evento:* {summary}
🕒 *Início:* {start}
🕓 *Término:* {end}
📍 *Local:* {location}
📝 *Descrição:* {description}
👥 *Participantes:*
{attendees_str}
🔒 *Visibilidade:* {visibility}
⏰ *Lembretes:* {reminders_str}

Por favor, *confirme o agendamento do evento*.  
Caso *não* confirme, envie nesta mesma mensagem quais campos você deseja alterar!
"""


def format_event_validation_message(current_event_data: dict, invalid_params: dict) -> str:
    def format_datetime(iso_str: str) -> str:
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime('%d/%m/%Y às %H:%M')
        except Exception:
            return 'Data inválida'

    def format_reminders(reminders: list) -> str:
        if not reminders:
            return 'Nenhum lembrete definido'

        formatted = []
        for reminder in reminders:
            # Se for dict com chave 'minutes'
            if isinstance(reminder, dict):
                minutes = reminder.get('minutes')
            # Se for int direto
            elif isinstance(reminder, int):
                minutes = reminder
            else:
                continue  # ignora qualquer outro tipo

            if not isinstance(minutes, int):
                continue
            if minutes < 60:
                formatted.append(f"{minutes} min")
            elif minutes < 1440:
                hours = minutes // 60
                formatted.append(f"{hours}h")
            else:
                days = minutes // 1440
                remaining_minutes = minutes % 1440
                hours = remaining_minutes // 60
                suffix = f"{days}d"
                if hours:
                    suffix += f"{hours}h"
                formatted.append(suffix)
        return ', '.join(formatted) if formatted else 'Nenhum lembrete válido'


    def format_attendees(attendees: list) -> str:
        if not attendees:
            return "  - Nenhum participante"
        return '\n'.join(f"  - {a.get('email', 'sem email')}" for a in attendees)

    def format_invalid_fields(errors: dict, current_event_data: dict) -> str:
        if not errors:
            return "Nenhum campo inválido encontrado."

        linhas = []
        for field_path, message in errors.items():
            if field_path.startswith("attendees[") and ".email" in field_path:
                # Tenta extrair o índice, ex: attendees[1].email
                match = re.match(r"attendees\[(\d+)\]\.email", field_path)
                if match:
                    idx = int(match.group(1))
                    try:
                        name = current_event_data.get("attendees", [])[idx].get("name")
                    except Exception:
                        name = None
                    if name:
                        display = f"{name}"
                    else:
                        display = f"Participante {idx + 1}"
                    linhas.append(f"❌ *{display}*: {message}")
                    continue

            # Fallback genérico
            linhas.append(f"❌ *{field_path}*: {message}")

        return "\n".join(linhas)

    # Montar mensagem com campos válidos
    summary = current_event_data.get('event_summary', 'Não informado')
    start = format_datetime(current_event_data.get('event_start', ''))
    end = format_datetime(current_event_data.get('event_end', ''))
    location = current_event_data.get('location', 'Não informado')
    description = current_event_data.get('description', 'Não informada')
    visibility = current_event_data.get('visibility', 'private')
    attendees_str = format_attendees(current_event_data.get('attendees', []))
    reminders_str = format_reminders(current_event_data.get('reminders', []))
    invalid_str = format_invalid_fields(invalid_params)

    return f"""📅 Entendi que você quer agendar um evento com os seguintes dados:

📌 *Título do evento:* {summary}
🕒 *Início:* {start}
🕓 *Término:* {end}
📍 *Local:* {location}
📝 *Descrição:* {description}
👥 *Participantes:*
{attendees_str}
🔒 *Visibilidade:* {visibility}
⏰ *Lembretes:* {reminders_str}

⚠️ Mas tive dúvidas ou encontrei erros nos seguintes campos:
{invalid_str}

✍️ Por favor, me envie os dados corrigidos para continuar. Tô te escutando!
"""



def limpar_think_tags(resposta: str) -> str:
    # Remove blocos <think>...</think> com qualquer conteúdo entre eles
    resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL | re.IGNORECASE)

    # Remove tags <think> ou </think> soltas
    resposta = re.sub(r"</?think>", "", resposta, flags=re.IGNORECASE)

    # Limpa espaços desnecessários
    return resposta.strip()