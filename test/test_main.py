# Mock the genai.Client before importing main to prevent API key errors
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

with patch("google.genai.Client"):
    from app.main import VectorStoreManager, faq_app


def test_vector_store_manager_starts_uninitialized():
    """New manager should not be ready to use."""
    manager = VectorStoreManager()
    assert not manager.is_initialized()


def test_api_health_endpoint():
    """Health endpoint should return status."""
    client = TestClient(faq_app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "vector_store_initialized" in data


def test_vector_store_manager_raises_error_when_not_initialized():
    """Should raise error when trying to get uninitialized vector store."""
    manager = VectorStoreManager()
    with pytest.raises(RuntimeError):
        manager.get_vectorstore()
