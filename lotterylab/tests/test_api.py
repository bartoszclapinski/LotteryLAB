import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint returns proper JSON."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert data["status"] == "healthy"


def test_frequency_endpoint_basic():
    """Test frequency endpoint returns expected structure."""
    response = client.get("/api/v1/analysis/frequency")
    assert response.status_code == 200
    data = response.json()

    # Check required fields
    required_fields = [
        "game_type", "window_days", "date_from", "date_to",
        "num_draws", "frequency", "expected_each", "delta", "pct_delta",
        "hot_numbers", "cold_numbers"
    ]
    for field in required_fields:
        assert field in data

    # Check data types
    assert isinstance(data["frequency"], dict)
    assert isinstance(data["hot_numbers"], list)
    assert isinstance(data["cold_numbers"], list)
    assert data["num_draws"] >= 0
    assert data["expected_each"] > 0


def test_frequency_endpoint_with_params():
    """Test frequency endpoint with query parameters."""
    response = client.get("/api/v1/analysis/frequency?game_type=lotto&window_days=30")
    assert response.status_code == 200
    data = response.json()

    assert data["game_type"] == "lotto"
    assert data["window_days"] == 30


def test_draws_endpoint():
    """Test draws endpoint returns expected structure."""
    response = client.get("/api/v1/draws?limit=5")
    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 5
    assert data["total"] >= 0


def test_draws_endpoint_pagination():
    """Test draws endpoint pagination."""
    # Get first page
    response1 = client.get("/api/v1/draws?limit=2&offset=0")
    assert response1.status_code == 200
    data1 = response1.json()

    # Get second page
    response2 = client.get("/api/v1/draws?limit=2&offset=2")
    assert response2.status_code == 200
    data2 = response2.json()

    # Items should be different if we have enough data
    if len(data1["items"]) >= 2 and len(data2["items"]) >= 1:
        assert data1["items"][0]["draw_number"] != data2["items"][0]["draw_number"]


def test_frequency_partial():
    """Test frequency partial endpoint returns HTML."""
    # Test with English language to ensure consistent assertions
    response = client.get("/partials/frequency?lang=en")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    html_content = response.text
    assert "frequency" in html_content.lower()
    # Check for content that should be present (num_draws value)
    assert "Draws:" in html_content or "Losowania:" in html_content


def test_recent_draws_partial():
    """Test recent draws partial endpoint returns HTML."""
    response = client.get("/partials/recent-draws")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    html_content = response.text
    assert "recent" in html_content.lower()


def test_generator_partial():
    """Test number generator partial endpoint returns HTML."""
    response = client.get("/partials/generator")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    html_content = response.text
    assert "generator" in html_content.lower()
    assert "generate" in html_content.lower()


def test_index_page():
    """Test main index page loads."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    html_content = response.text
    assert "lottery lab" in html_content.lower()
    assert "frequency" in html_content.lower()


def test_404_handling():
    """Test 404 responses for invalid endpoints."""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404

    response = client.get("/partials/nonexistent")
    assert response.status_code == 404
