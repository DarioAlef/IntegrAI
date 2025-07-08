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

now = dt.datetime.now().astimezone(ZoneInfo('America/Manaus'))

dia_semana = dias_semana[now.weekday()]
dia = now.day
mes = meses[now.month - 1]
ano = now.year
hora = now.strftime('%H:%M')

data_formatada = f"{dia_semana}, {dia} de {mes} de {ano}, {hora}"