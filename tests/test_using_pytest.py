import pytest

from panini.test_client import TestClient

from app.utils import get_broker

BROKER_HOST, BROKER_PORT = get_broker(True)


def run_app():
    from app.main import app

    app.start()


@pytest.fixture(scope="module")
def client():
    client = TestClient(
        run_app, base_nats_url=f"nats://{BROKER_HOST}:{BROKER_PORT}"
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
