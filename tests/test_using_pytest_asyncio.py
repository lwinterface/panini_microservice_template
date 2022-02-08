import asyncio
import pytest
from panini.async_test_client import AsyncTestClient
from app.config_manager import get_panini_config
from nats.errors import NoRespondersError

panini_config = get_panini_config('test')


def run_app():
    from app.main import app

    app.start()


@pytest.fixture
async def client():
    nats_port = panini_config.nats_servers[0].split(':')[-1]
    nats_host = panini_config.nats_servers[0].replace(':'+nats_port, '')
    client = AsyncTestClient(
        run_app,
        nats_host=nats_host,
        nats_port=nats_port,
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
    with pytest.raises(NoRespondersError):
        await client.request("not.existing.subject", {"message": "test"})
