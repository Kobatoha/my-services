import pytest

from aioresponses import aioresponses
from unittest.mock import AsyncMock, patch
from aiohttp import ClientError

from services.transport_client import TransportClient, TransportResponse, HTTPStatusError


@pytest.mark.asyncio
async def test_get_request_returns_json():
    client = TransportClient()

    with aioresponses() as mocked:
        mocked.get("https://httpbin.org/get", payload={"hello": "world"})

        resp = await client.get("https://httpbin.org/get")

        assert resp.status == 200
        assert resp.json == {"hello": "world"}
        assert resp.is_ok


@pytest.mark.asyncio
async def test_get_success(monkeypatch):
    """Проверяем, что GET возвращает TransportResponse с корректными данными"""

    # Создаём поддельный ответ aiohttp
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text.return_value = "OK"
    mock_response.json.return_value = {"key": "value"}
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.cookies = {}
    mock_response.read.return_value = b"OK"

    # Мокаем метод request() у ClientSession
    session_mock = AsyncMock()
    session_mock.request = AsyncMock(return_value=mock_response)

    # Подменяем _get_session у TransportClient, чтобы он вернул наш session_mock
    client = TransportClient()
    monkeypatch.setattr(client, "_get_session", AsyncMock(return_value=session_mock))

    resp = await client.get("http://fake-url.com")

    assert isinstance(resp, TransportResponse)
    assert resp.status == 200
    assert resp.text == "OK"
    assert resp.json == {"key": "value"}


@pytest.mark.asyncio
async def test_post_success(monkeypatch):
    """Проверяем POST запрос"""

    mock_response = AsyncMock()
    mock_response.status = 201
    mock_response.text.return_value = "Created"
    mock_response.json.return_value = {"id": 123}
    mock_response.headers = {}
    mock_response.cookies = {}
    mock_response.read.return_value = b"Created"

    session_mock = AsyncMock()
    session_mock.request = AsyncMock(return_value=mock_response)

    client = TransportClient()
    monkeypatch.setattr(client, "_get_session", AsyncMock(return_value=session_mock))

    resp = await client.post("http://fake-url.com", json={"data": 1})

    assert resp.status == 201
    assert resp.json == {"id": 123}
    assert resp.text == "Created"


@pytest.mark.asyncio
async def test_raise_for_status():
    """Проверяем, что HTTPStatusError выбрасывается при статусе != 2xx"""

    resp = TransportResponse(
        url="http://fake-url.com",
        status=500,
        text="Internal Error",
        json=None,
        headers={},
        cookies={}
    )

    with pytest.raises(HTTPStatusError):
        resp.raise_for_status()


@pytest.mark.asyncio
async def test_close_session():
    client = TransportClient()
    session_mock = AsyncMock()
    client.session = session_mock

    await client.close()

    session_mock.close.assert_awaited()
    assert client.session is None


@pytest.mark.asyncio
async def test_context_manager(monkeypatch):
    client = TransportClient()
    session_mock = AsyncMock()
    monkeypatch.setattr(client, "_get_session", AsyncMock(return_value=session_mock))

    async with client as c:
        assert c is client

    session_mock.close.assert_awaited()
