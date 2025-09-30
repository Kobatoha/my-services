from typing import Any

import asyncio
import logging
import tenacity

from aiohttp import ClientSession, ClientTimeout, ClientError, CookieJar
from aiohttp_socks import ProxyConnector


logger = logging.getLogger(__name__)


class HTTPStatusError(RuntimeError):
    def __init__(self, status: int, body: str | None, url: str):
        super().__init__(f"{url} returned {status}")
        self.status = status
        self.body = body
        self.url = url


class TransportResponse:
    def __init__(self, url: str, status: int, text: str | None, json: Any,
                 headers: dict, cookies: dict, content: bytes | None = None):
        self.url = url
        self.status = status
        self.text = text
        self.json = json
        self.headers = headers
        self.cookies = cookies
        self.content = content

    @property
    def is_ok(self) -> bool:
        return 200 <= self.status < 300

    def raise_for_status(self) -> None:
        if not self.is_ok:
            raise HTTPStatusError(self.status, self.text, url=self.url)


class TransportClient:
    def __init__(self, proxy_url: str | None = None, timeout: int = 20, cookie_jar: CookieJar | None = None):
        self.proxy_url = proxy_url
        self.cookie_jar = cookie_jar or CookieJar()
        self.timeout = ClientTimeout(total=timeout)
        self.session: ClientSession | None = None

    async def _get_session(self) -> ClientSession:
        if self.session and not self.session.closed:
            return self.session

        if self.proxy_url:
            connector = ProxyConnector.from_url(self.proxy_url, verify_ssl=False)
            self.session = ClientSession(connector=connector, timeout=self.timeout, cookie_jar=self.cookie_jar)
        else:
            self.session = ClientSession(timeout=self.timeout, cookie_jar=self.cookie_jar)

        return self.session

    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    async def __aenter__(self):
        await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type((ClientError, asyncio.TimeoutError)),
        wait=tenacity.wait_fixed(2),
        stop=tenacity.stop_after_attempt(3),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: Any = None,
        json: Any = None,
        params: dict[str, Any] | None = None,
        allow_redirects: bool = True,
    ) -> TransportResponse:
        session = await self._get_session()
        try:
            async with session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                data=data,
                json=json,
                params=params,
                allow_redirects=allow_redirects,
            ) as response:
                text = None
                json_data = None

                try:
                    text = await response.text()
                except Exception:
                    pass

                try:
                    json_data = await response.json()
                except Exception:
                    pass

                content = await response.read()

                return TransportResponse(
                    url=url,
                    status=response.status,
                    text=text,
                    json=json_data,
                    headers=dict(response.headers),
                    cookies=dict(response.cookies),
                    content=content,
                )
        except ClientError as e:
            logger.error(f"Request failed: {e}")
            raise

    async def get(self, url: str, **kwargs) -> TransportResponse:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> TransportResponse:
        return await self.request("POST", url, **kwargs)
