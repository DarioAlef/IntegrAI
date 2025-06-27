# ajuste o path conforme seu projeto
from app.services.command_interpretation import interpretar_comando_novo_agendamento_e_reconhecer
import pytest

# Lista de 50 frases de teste com seus valores esperados (True = comando)
test_cases = [
    ("Marca pra mim no dia 12", True),
    ("Ontem foi dia 23 e eu ainda não...", False),
    ("Agende pra mim cabelereira na sexta-feira que vem", True),
    ("Coloca na agenda pra mim por favor", True),
    ("Aquele meu amigo tinha marcado de vir aqui", False),
    ("Por favor, coloque reunião segunda-feira", True),
    ("Amanhã é feriado", False),
    ("Preciso agendar consulta", True),
    ("Já fui ao médico ontem", False),
    ("Agende dentista quarta às 9h", True),
    ("Estava pensando em ir ao cinema", False),
    ("Marca reunião com equipe sexta", True),
    ("Ontem alguém me ligou", False),
    ("Agendar reunião amanhã às 10", True),
    ("Te falei ontem sobre aquele compromisso", False),
    ("Coloque no calendário: aula às 14h", True),
    ("Hoje está chovendo", False),
    ("Agende massagem pra sábado", True),
    ("Meu cachorro foi ao pet", False),
    ("Por favor, marca médico às 16h", True),
    ("Amanhã talvez eu viaje", False),
    ("Anote na agenda: reunião dia 30", True),
    ("Fui ao dentista semana passada", False),
    ("Coloca corte de cabelo pra segunda", True),
    ("Alguém comentou sobre um evento", False),
    ("Me lembra da consulta amanhã", True),
    ("Acho que vi isso na TV", False),
    ("Reserva um horário pra mim sexta", True),
    ("Faz tempo que não vou ao médico", False),
    ("Agende fisioterapia às 15h", True),
    ("Ele comentou que tinha uma reunião", False),
    ("Marcar terapia quinta às 18h", True),
    ("Vi no calendário que tenho compromisso", False),
    ("Pode agendar reunião de alinhamento", True),
    ("Me lembre do compromisso amanhã", True),
    ("Não lembro se tinha algo pra hoje", False),
    ("Anota um evento importante domingo", True),
    ("Disseram que o trânsito tá ruim", False),
    ("Preciso agendar retorno médico", True),
    ("Passei o dia fora ontem", False),
    ("Marca uma call com o time", True),
    ("Recebi uma ligação importante", False),
    ("Agende almoço com o cliente", True),
    ("A reunião de ontem foi cancelada", False),
    ("Anote: jantar com família sexta", True),
    ("Fui ao mercado mais cedo", False),
    ("Coloca na agenda: reunião às 14h", True),
    ("Te conto depois sobre aquele dia", False),
    ("Agenda reunião com fulano às 10h", True),
    ("Acho que amanhã tem jogo", False),
]

test_cases_with_data_recognition = [
    # ('Marca pra mim no dia 12', {'error': True}),
    ('Ontem foi dia 23 e eu ainda não...', {'error': True}),
    ('Agende pra mim cabelereira na sexta-feira que vem, chama o thsilva.developer@gmail.com', {
        'event_summary': 'cabelereira',
        'event_start': '2025-07-04T09:00:00-04:00',
        'event_end': '2025-07-04T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': [{"email": "thsilva.developer@gmail.com"}]
    }),
    # ('Coloca na agenda pra mim por favor', {'error': True}),
    ('Aquele meu amigo tinha marcado de vir aqui', {'error': True}),
    ('Por favor, coloque reunião segunda-feira com o dário e o josé', {
        'event_summary': 'reunião',
        'event_start': '2025-06-30T09:00:00-04:00',
        'event_end': '2025-06-30T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': [{"displayName": "Dário"}, {"displayName": "José"}]
    }),
    ('Amanhã é feriado', {'error': True}),
    # ('Preciso agendar consulta', {
    #     'event_summary': 'consulta',
    #     'event_start': '2025-06-27T09:00:00-04:00',
    #     'event_end': '2025-06-27T10:00:00-04:00',
    #     'description': '',
    #     'location': '',
    #     'attendees': []
    # }),
    ('Já fui ao médico ontem', {'error': True}),
    ('Agende dentista quarta às 9h', {
        'event_summary': 'dentista',
        'event_start': '2025-07-02T09:00:00-04:00',
        'event_end': '2025-07-02T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Estava pensando em ir ao cinema', {'error': True}),
    ('Marca reunião com equipe sexta', {
        'event_summary': 'reunião com equipe',
        'event_start': '2025-06-27T09:00:00-04:00',
        'event_end': '2025-06-27T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Ontem alguém me ligou', {'error': True}),
    ('Agendar reunião amanhã às 10', {
        'event_summary': 'reunião',
        'event_start': '2025-06-27T10:00:00-04:00',
        'event_end': '2025-06-27T11:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Te falei ontem sobre aquele compromisso', {'error': True}),
    ('Coloque no calendário: aula às 14h', {
        'event_summary': 'aula',
        'event_start': '2025-06-27T14:00:00-04:00',
        'event_end': '2025-06-27T15:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Hoje está chovendo', {'error': True}),
    # ('Agende massagem pra sábado', {
    #     'event_summary': 'massagem',
    #     'event_start': '2025-06-29T09:00:00-04:00',
    #     'event_end': '2025-06-29T10:00:00-04:00',
    #     'description': '',
    #     'location': '',
    #     'attendees': []
    # }),
    ('Meu cachorro foi ao pet', {'error': True}),
    ('Por favor, marca médico às 16h', {
        'event_summary': 'médico',
        'event_start': '2025-06-27T16:00:00-04:00',
        'event_end': '2025-06-27T17:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Amanhã talvez eu viaje', {'error': True}),
    ('Anote na agenda: reunião dia 30', {
        'event_summary': 'reunião',
        'event_start': '2025-06-30T09:00:00-04:00',
        'event_end': '2025-06-30T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Fui ao dentista semana passada', {'error': True}),
    ('Coloca corte de cabelo pra segunda', {
        'event_summary': 'corte de cabelo',
        'event_start': '2025-06-30T09:00:00-04:00',
        'event_end': '2025-06-30T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
    ('Marca pra mim no dia 12', {
        'event_summary': 'marcar',
        'event_start': '2025-07-12T12:00:00-04:00',
        'event_end': '2025-07-12T13:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),

    ('Coloca na agenda pra mim por favor', {
        'event_summary': '',
        'event_start': '',
        'event_end': '',
        'description': '',
        'location': '',
        'attendees': []
    }),

    ('Preciso agendar consulta', {
        'event_summary': 'consulta',
        'event_start': '',
        'event_end': '',
        'description': '',
        'location': '',
        'attendees': []
    }),

    ('Agende massagem pra sábado', {
        'event_summary': 'massagem',
        'event_start': '2025-06-28T09:00:00-04:00',
        'event_end': '2025-06-28T10:00:00-04:00',
        'description': '',
        'location': '',
        'attendees': []
    }),
]


@pytest.mark.parametrize("frase, esperado", test_cases_with_data_recognition)
def test_interpretar_comando_novo_agendamento(frase, esperado):
    resultado = interpretar_comando_novo_agendamento_e_reconhecer(frase)
    assert resultado == esperado, f"Falhou para: '{frase}'"
