import os
import pytest
from app.services.chatbot.chatbot import get_llm_response

@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY não configurada"
)
def test_get_llm_response_basico():
    messages = [{"role": "user", "content": "Qual é a capital do Brasil?"}]
    resposta = get_llm_response(messages, system_prompt="Responda em português.")
    assert isinstance(resposta, str)
    assert "Brasília" in resposta or "brasil" in resposta.lower()