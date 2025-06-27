import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@patch("app.routes.webhook.get_openrouter_response", return_value="Resposta mockada")
@patch("app.routes.webhook.EvolutionAPI.enviar_mensagem")
@pytest.mark.django_db  # <-- para fazer ao banco de dados django
def test_webhook_text_message(mock_enviar, mock_llm, client):
    payload = {
        "data": {
            "message": {"conversation": "Oi, tudo bem?"},
            "key": {"fromMe": False, "remoteJid": "559999999999@c.us"}
        },
        "instance": "teste",
        "apikey": "fakekey"
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()
    mock_llm.assert_called_once()
    mock_enviar.assert_called()