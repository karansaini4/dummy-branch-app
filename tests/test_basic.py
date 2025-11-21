import requests
import pytest

@pytest.fixture(scope="session")
def api_url():
    return "http://localhost:8000"

def test_health(api_url):
    response = requests.get(f"{api_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"} 