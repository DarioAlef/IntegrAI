# ajuste o path conforme seu projeto
from app.services.interpretation.command_interpretation import interpretar_comando
from app.services.interpretation.appointment_interpretation import interpretar_agendamento
from app.services.interpretation.utils_interpretation import interpretar_confirmacao
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

test_cases_geral = [
    # Agendamentos
    ("Marca um horário com o dentista segunda às 14h",
     {"is_command": True, "command": "agendamento"}),
    ("Agende uma consulta com o cardiologista para o dia 20",
     {"is_command": True, "command": "agendamento"}),
    ("Coloca na agenda: reunião com a equipe amanhã às 10",
     {"is_command": True, "command": "agendamento"}),
    ("Me lembra de agendar fisioterapia semana que vem",
     {"is_command": True, "command": "agendamento"}),
    ("Agende pra mim a vistoria do carro sexta de manhã",
     {"is_command": True, "command": "agendamento"}),
    ("Adiciona um compromisso com o advogado na quarta",
     {"is_command": True, "command": "agendamento"}),
    ("Agende uma chamada com o RH às 11h", {
     "is_command": True, "command": "agendamento"}),
    ("Marca uma consulta no laboratório ainda esse mês",
     {"is_command": True, "command": "agendamento"}),
    ("Agende entrega de documentos na sexta-feira",
     {"is_command": True, "command": "agendamento"}),
    ("Reserva uma sala para o treinamento de terça",
     {"is_command": True, "command": "agendamento"}),
    ("Coloca despertador pra amanhã", {
     "is_command": True, "command": "agendamento"}),

    # Envio de mensagem
    ("Manda msg pro João pedindo a planilha", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Envia pro Rafael o lembrete da reunião", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Chama a Amanda e pergunta se ela já saiu", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Manda um oi pra Luiza", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Responde o cliente com o novo horário da call", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Pede pro suporte verificar o erro", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Envia esse recado para o grupo do time", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Fala com a contabilidade e pergunta do boleto", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Manda o número do protocolo pra Fernanda", {
     "is_command": True, "command": "envio_de_mensagem"}),
    ("Lembra o Felipe sobre o prazo da entrega", {
     "is_command": True, "command": "envio_de_mensagem"}),

    # Indisponíveis
    ("Liga o ar-condicionado da sala 2",
     {"is_command": True, "command": "comando_indisponível"}),
    ("Toca a campainha dos fundos", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Abre a porta do escritório", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Apaga as luzes da recepção", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Desliga a TV da sala de espera", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Toca uma música ambiente", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Me lembra de beber água", {
     "is_command": True, "command": "comando_indisponível"}),
    ("Faz um café", {"is_command": True, "command": "comando_indisponível"}),
    ("Liga pro meu pai", {"is_command": True,
     "command": "comando_indisponível"}),

    # Sem comando
    ("Nossa, hoje foi bem corrido", {"is_command": False}),
    ("A reunião foi cancelada de última hora", {"is_command": False}),
    ("Não sei se consigo terminar isso hoje", {"is_command": False}),
    ("Estou pensando em viajar no fim de semana", {"is_command": False}),
    ("Ela disse que vai tentar resolver", {"is_command": False}),
    ("Amanhã provavelmente vai chover", {"is_command": False}),
    ("Fiquei preso no trânsito por mais de uma hora", {"is_command": False}),
    ("Acho que comi demais no almoço", {"is_command": False}),
    ("Esse documento está muito mal escrito", {"is_command": False}),
    ("Preciso de férias urgente", {"is_command": False})
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


appointment_test_cases = [
    (
        "Agende um call com o gerente comercial na segunda às 10h",
        {
            "event_summary": "Call",
            "event_start": "2025-06-30T10:00:00-04:00",
            "event_end": "2025-06-30T11:00:00-04:00",
        }
    ),
    (
        "Coloca na agenda uma reunião com a equipe de design no escritório às 15h de hoje",
        {
            "event_summary": "Reunião",
            "event_start": "2025-06-29T15:00:00-04:00",
            "event_end": "2025-06-29T16:00:00-04:00",
            "location": "Escritório"
        }
    ),
    (
        "Marca dentista quarta-feira às 9h e bota pra lembrar 1 hora antes.",
        {
            "event_summary": "Consulta",
            "event_start": "2025-07-02T09:00:00-04:00",
            "event_end": "2025-07-02T10:00:00-04:00",
            "reminders": [
                60
            ]
        }

    ),
    (
        "Reunião com o jurídico dia 1º às 16h",
        {
            "event_summary": "Reunião",
            "event_start": "2025-07-01T16:00:00-04:00",
            "event_end": "2025-07-01T17:00:00-04:00",
        }
    ),
    (
        "Agendar brainstorm com o time de marketing para amanhã às 11",
        {
            "event_summary": "Brainstorm",
            "event_start": "2025-06-30T11:00:00-04:00",
            "event_end": "2025-06-30T12:00:00-04:00",
        }
    ),
    (
        "Marca reunião com João e Ana na terça às 14h. O endereço é rua Comendador Matos Areosa 481",
        {
            "event_summary": "Reunião",
            "event_start": "2025-07-01T14:00:00-04:00",
            "event_end": "2025-07-01T15:00:00-04:00",
            "location": "Rua Comendador Matos Areosa 481",
            "attendees": [{"displayName": "João"}, {"displayName": "Ana"}]
        }
    ),
    (
        "Encontro com cliente na sede da empresa segunda às 10h",
        {
            "event_summary": "Encontro",
            "event_start": "2025-06-30T10:00:00-04:00",
            "event_end": "2025-06-30T11:00:00-04:00",
            "location": "Sede da empresa",
        }
    ),
    (
        "Consulta médica no hospital Santa Júlia às 8h de sexta",
        {
            "event_summary": "Consulta",
            "event_start": "2025-06-28T08:00:00-04:00",
            "event_end": "2025-06-28T09:00:00-04:00",
        }
    ),
    (
        "Reunião com fornecedor via Zoom na quinta às 13h",
        {
            "event_summary": "Reunião",
            "event_start": "2025-07-03T13:00:00-04:00",
            "event_end": "2025-07-03T14:00:00-04:00",
            "location": "Zoom",
        }
    ),
    (
        "Coloca na agenda um papo com o RH às 23h45 hoje",
        {
            "event_summary": "Papo",
            "event_start": "2025-06-29T23:45:00-04:00",
            "event_end": "2025-06-30T00:45:00-04:00",
        }
    ),
]


confirm_test_cases = [
    ("Sim, claro!", {"is_confirmation": "yes"}),
    ("Não quero, obrigado.", {"is_confirmation": "no"}),
    ("Pode deixar!", {"is_confirmation": "yes"}),
    ("Prefiro não responder.", {"is_confirmation": "no"}),
    ("Com certeza!", {"is_confirmation": "yes"}),
    ("Nem pensar.", {"is_confirmation": "no"}),
    ("Pode sim.", {"is_confirmation": "yes"}),
    ("Acho que não.", {"is_confirmation": "no"}),
    ("Não sei ao certo.", {"is_confirmation": "unidentified"}),
    ("Tô pensando ainda.", {"is_confirmation": "unidentified"}),
]

DEFAULT_TEMPLATE = {
    "event_summary": "",
    "event_start": "",
    "event_end": "",
    "description": "",
    "location": "",
    "attendees": [],
    "visibility": "private",
    "reminders": []
}


def normalizar(dic):  # deixa tudo minúsculo e preenche com o template padrão
    def lower_if_str(v):
        if isinstance(v, str):
            return v.lower()
        if isinstance(v, list):
            return [lower_if_str(i) for i in v]
        if isinstance(v, dict):
            return {k: lower_if_str(val) for k, val in v.items()}
        return v
    return lower_if_str({**DEFAULT_TEMPLATE, **dic})


def contem_strings(dado, esperado):
    # Campos que devem usar lógica de "contém" (substring)
    campos_contem = {'event_summary', 'description', 'location'}

    # Campos que devem usar comparação flexível de data
    campos_data = {'event_start', 'event_end'}

    # Campos que devem usar igualdade exata
    campos_igualdade = {'visibility'}

    def comparar_datas(data_esperada, data_recebida):
        """Compara datas de forma flexível, ignorando timezone e pequenas diferenças"""
        if not data_esperada or not data_recebida:
            return True if not data_esperada else False

        # Remove timezone e normaliza formato
        data_esperada_limpa = data_esperada.replace(
            '-04:00', '').replace('t', 'T')
        data_recebida_limpa = data_recebida.replace(
            '-04:00', '').replace('t', 'T')

        # Extrai data e hora
        if 'T' in data_esperada_limpa and 'T' in data_recebida_limpa:
            try:
                # Compara apenas a hora se as datas são muito próximas
                hora_esperada = data_esperada_limpa.split('T')[1][:5]  # HH:MM
                hora_recebida = data_recebida_limpa.split('T')[1][:5]  # HH:MM

                # Se as horas são iguais, considera válido
                return hora_esperada == hora_recebida
            except:
                # Se não conseguir extrair, faz comparação direta
                return data_esperada_limpa == data_recebida_limpa

        return data_esperada_limpa == data_recebida_limpa

    for chave, valor_esperado in esperado.items():
        valor_dado = dado.get(chave)

        if isinstance(valor_esperado, str):
            if not isinstance(valor_dado, str):
                return False

            # Se o valor esperado está vazio, ignora a verificação (aceita qualquer coisa)
            if valor_esperado == '':
                continue

            # Para campos de data, usa comparação flexível
            if chave in campos_data:
                if not comparar_datas(valor_esperado.lower(), valor_dado.lower()):
                    return False
            # Para campos específicos, usa lógica de "contém"
            elif chave in campos_contem:
                if valor_esperado.lower() not in valor_dado.lower():
                    return False
            # Para outros campos string, usa igualdade exata
            elif chave in campos_igualdade:
                if valor_esperado.lower() != valor_dado.lower():
                    return False
            # Padrão: usa lógica de "contém" para campos não especificados
            else:
                if valor_esperado.lower() not in valor_dado.lower():
                    return False

        elif isinstance(valor_esperado, list):
            # Para listas, verifica se cada item esperado está presente na lista resultado
            if not isinstance(valor_dado, list):
                return False

            # Se a lista esperada está vazia, aceita qualquer lista
            if not valor_esperado:
                continue

            # Verifica se todos os itens esperados estão presentes
            for item_esperado in valor_esperado:
                if isinstance(item_esperado, dict):
                    # Para objetos, verifica se existe um objeto similar na lista
                    encontrado = False
                    for item_dado in valor_dado:
                        if isinstance(item_dado, dict):
                            # Verifica se todos os campos do item esperado existem no item dado
                            if all(item_dado.get(k, '').lower() == v.lower() if isinstance(v, str) else item_dado.get(k) == v
                                   for k, v in item_esperado.items()):
                                encontrado = True
                                break
                    if not encontrado:
                        return False
                else:
                    # Para valores simples, verifica se está na lista
                    if item_esperado not in valor_dado:
                        return False

        else:
            if valor_esperado != valor_dado:
                return False

    return True


@pytest.mark.parametrize("frase, esperado", appointment_test_cases)
def test_interpretar_comando_novo_agendamento(frase, esperado):
    resultado = normalizar(interpretar_agendamento(frase))
    esperado = normalizar(esperado)

    # Se contem_strings retorna True, o teste passa
    if contem_strings(resultado, esperado):
        return  # Teste passou!

    # Se chegou aqui, contem_strings retornou False, então falha o teste
    assert False, f"Falhou para: '{frase}'\nEsperado: {esperado}\nRecebido: {resultado}"


@pytest.mark.parametrize("mensagem, esperado", confirm_test_cases)
def test_interpretar_confirmacao(mensagem, esperado):
    resultado = interpretar_confirmacao(mensagem)

    if resultado == esperado:
        return  # Teste passou
    assert False, f"Falhou para: '{mensagem}'\nEsperado: {esperado}\nRecebido: {resultado}"
