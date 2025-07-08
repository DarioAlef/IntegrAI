import locale
from datetime import datetime

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