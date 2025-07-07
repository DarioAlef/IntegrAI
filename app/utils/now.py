import datetime as dt
from zoneinfo import ZoneInfo

dias_semana = [
    'segunda-feira', 'terça-feira', 'quarta-feira',
    'quinta-feira', 'sexta-feira', 'sábado', 'domingo'
]

meses = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
    'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
]


def datetime_now():
    """
    Retorna a data e hora atual formatada como uma string.
    A data é ajustada para o fuso horário de Manaus (America/Manaus).
    """
    return dt.datetime.now().astimezone(ZoneInfo('America/Manaus'))


def formated_now():
    """
    Retorna a data e hora atual formatada como uma string no formato:
    'dia da semana, dia de mês de ano, hora:minuto'.
    Exemplo: 'segunda-feira, 1 de janeiro de 2024, 12:00'.
    """

    now = datetime_now()

    dia_semana = dias_semana[now.weekday()]
    dia = now.day
    mes = meses[now.month - 1]
    ano = now.year
    hora = now.strftime('%H:%M')

    data_formatada = f"{dia_semana}, {dia} de {mes} de {ano}, {hora}"
    return data_formatada
