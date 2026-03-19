"""Tests for the /chat endpoint — request/response contract."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a TestClient with LLMService mocked out."""
    mock_llm = MagicMock()
    mock_llm.run_agent.return_value = "Te recomiendo Inception (2010)."

    with (
        patch("app.services.llm_service.settings") as mock_settings,
        patch("app.services.tmdb_service.settings") as mock_tmdb_settings,
    ):
        mock_settings.openai_api_key = "fake"
        mock_settings.default_model = "gpt-4"
        mock_tmdb_settings.tmdb_base_url = "https://api.themoviedb.org/3"
        mock_tmdb_settings.tmdb_api_key = "fake"

        from main import app
        from app.services.llm_service import get_llm_service

        app.dependency_overrides[get_llm_service] = lambda: mock_llm
        yield TestClient(app), mock_llm
        app.dependency_overrides.clear()


class TestChatEndpoint:
    def test_successful_chat(self, client):
        test_client, mock_llm = client
        response = test_client.post("/chat", json={"message": "Quiero una de terror"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Te recomiendo Inception (2010)."
        mock_llm.run_agent.assert_called_once_with("Quiero una de terror", history=[])

    def test_chat_with_history(self, client):
        test_client, mock_llm = client
        response = test_client.post("/chat", json={
            "message": "Otra más",
            "history": [
                {"role": "user", "content": "Hola"},
                {"role": "assistant", "content": "¡Hola! ¿Qué tipo de película buscas?"},
            ],
        })
        assert response.status_code == 200
        mock_llm.run_agent.assert_called_once_with(
            "Otra más",
            history=[
                {"role": "user", "content": "Hola"},
                {"role": "assistant", "content": "¡Hola! ¿Qué tipo de película buscas?"},
            ],
        )

    def test_chat_empty_history(self, client):
        test_client, _ = client
        response = test_client.post("/chat", json={"message": "Hola"})
        assert response.status_code == 200

    def test_missing_message_returns_422(self, client):
        test_client, _ = client
        response = test_client.post("/chat", json={})
        assert response.status_code == 422

    def test_invalid_body_returns_422(self, client):
        test_client, _ = client
        response = test_client.post("/chat", json={"message": 123})
        assert response.status_code == 422

    def test_response_schema(self, client):
        test_client, _ = client
        response = test_client.post("/chat", json={"message": "test"})
        data = response.json()
        assert set(data.keys()) == {"response"}
        assert isinstance(data["response"], str)


class TestRootEndpoint:
    def test_root(self, client):
        test_client, _ = client
        response = test_client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
