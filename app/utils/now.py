import datetime as dt
from zoneinfo import ZoneInfo
now = dt.datetime.now().astimezone(ZoneInfo('America/Manaus')).isoformat()
if __name__ == "__main__":
    print(now)  # Exibe a data e hora atual no formato ISO 8601 com o fuso horário de Manaus