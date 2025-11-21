import requests
import pytest

@pytest.fixture(scope="session")
def api_url():
    return "http://localhost:8000"

def test_health(api_url="http://localhost:8000"):
    response = requests.get(f"{api_url}/health")
    assert response.status_code == 200
    # Accept both common variants
    data = response.json()
    assert data["status"] in ["ok", "healthy"]
    
