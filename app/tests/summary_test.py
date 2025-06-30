import pytest

# Suponha que esta seja a função que você quer testar
from app.services.context.summary import gerar_resumo # ajuste o nome do arquivo/função

@pytest.mark.parametrize("mensagens, old_context", [
    (
        [],
        "Anteriormente conversamos sobre preferências alimentares e localização atual do usuário."
    ),
    (
        [
    {"role": "user", "content": "Você pode me mostrar o que gastei essa semana?"},
    {"role": "assistant", "content": "Claro! Você teve gastos de R$ 180 com alimentação e R$ 220 com transporte."},
    {"role": "user", "content": "E com quem eu mais fiz transferências nos últimos dias?"},
    {"role": "assistant", "content": "Você transferiu três vezes para João e duas vezes para Maria."},
    {"role": "user", "content": "Beleza, e qual meu saldo atual?"},
    {"role": "assistant", "content": "Seu saldo atual é de R$ 2.450,00."},
    {"role": "user", "content": "Me avisa quando chegar em mil reais, por favor."},
    {"role": "assistant", "content": "Alerta configurado! Te aviso assim que o saldo ficar abaixo de R$ 1.000."},
    {"role": "user", "content": "Ah, e tem alguma fatura próxima do vencimento?"},
    {"role": "assistant", "content": "Sim, sua fatura do cartão vence amanhã, no valor de R$ 320,00."}
        ],
        "Falamos sobre histórico financeiro e contatos frequentes."
    )
])
def test_gerar_resumo_llm(mensagens, old_context):
    user_mock = type("User", (), {"name": "Thiago"})()  # mock simples de usuário

    resultado = gerar_resumo(mensagens, user_mock, old_context)

    assert isinstance(resultado, dict), "Resultado não é um dicionário"
    assert "resumo" in resultado, "Campo 'resumo' ausente no resultado"
    assert "user_profile_data" in resultado, "Campo 'user_profile_data' ausente no resultado"
    assert isinstance(resultado["resumo"], str), "'resumo' não é uma string"
    assert isinstance(resultado["user_profile_data"], dict), "'user_profile_data' não é um dicionário"
    assert len(resultado["resumo"]) <= 400, f"'resumo' tem mais de 400 caracteres: {len(resultado['resumo'])}"
