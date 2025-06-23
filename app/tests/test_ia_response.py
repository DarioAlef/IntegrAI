import os
import pytest
from app.services.openrouter import get_openrouter_response

@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY não configurada"
)
def test_get_openrouter_response_basico():
    messages = [{"role": "user", "content": "Qual é a capital do Brasil?"}]
    resposta = get_openrouter_response(messages, system_prompt="Responda em português.")
    assert isinstance(resposta, str)
    assert "Brasília" in resposta or "brasil" in resposta.lower()