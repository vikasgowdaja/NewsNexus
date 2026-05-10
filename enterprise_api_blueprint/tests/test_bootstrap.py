from fastapi.testclient import TestClient

from enterprise_api_blueprint.src.main import app


def test_root_bootstrap() -> None:
    client = TestClient(app)
    response = client.get("/")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "bootstrapped"
