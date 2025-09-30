import pytest

from aioresponses import aioresponses
from services.transport_client import TransportClient


@pytest.mark.asyncio
async def test_get_request_returns_json():
    client = TransportClient()

    with aioresponses() as mocked:
        mocked.get("https://httpbin.org/get", payload={"hello": "world"})

        resp = await client.get("https://httpbin.org/get")

        assert resp.status == 200
        assert resp.json == {"hello": "world"}
        assert resp.is_ok
