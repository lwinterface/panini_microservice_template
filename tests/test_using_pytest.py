import pytest
from panini.test_client import TestClient
from app.config_manager import get_panini_config

panini_config = get_panini_config('test')


def run_app():
    from app.main import app

    app.start()


@pytest.fixture(scope="module")
def client():
    client = TestClient(
        run_app, base_nats_url=panini_config.nats_servers[0]
    ).start()
    yield client
    client.stop()


def test_receive_message(client):
    response = client.request("some.request.subject", {"message": "test"})
    assert response["success"] is True
    assert response["data"]["message"] == "test"


def test_failure(client):
    with pytest.raises(OSError):
        client.request("not.existing.subject", {"message": "test"})
