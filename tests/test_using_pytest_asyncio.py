import asyncio

import pytest

from panini.async_test_client import AsyncTestClient

from app.utils import Environment

Environment.load("test")
BROKER_HOST, BROKER_PORT = Environment.get_broker()


def run_app():
    from app.main import app

    app.start()


@pytest.fixture
async def client():
    client = AsyncTestClient(
        run_app,
        nats_host=BROKER_HOST,
        nats_port=BROKER_PORT,
    )
    await client.start()
    yield client
    await client.stop()


@pytest.mark.asyncio
async def test_receive_message(client):
    response = await client.request("some.request.subject", {"message": "test"})
    assert response["success"] is True
    assert response["data"]["message"] == "test"


@pytest.mark.asyncio
async def test_failure(client):
    with pytest.raises(asyncio.TimeoutError):
        await client.request("not.existing.subject", {"message": "test"})
