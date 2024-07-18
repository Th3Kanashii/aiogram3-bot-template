from __future__ import annotations

import asyncio
from ssl import SSLContext
from typing import TYPE_CHECKING, Any

import backoff
from aiohttp.client import ClientSession, TCPConnector
from aiohttp.client_exceptions import ClientError, ContentTypeError
from aiohttp.web import HTTPOk
from ujson import dumps, loads


if TYPE_CHECKING:
    from collections.abc import Mapping

    from aiohttp.formdata import FormData
    from yarl import URL


# Taken from here: https://github.com/Latand/tgbot_template_v3/blob/master/infrastructure/some_api/base.py
class BaseClient:
    """
    Represents a base client for API services.
    """

    def __init__(self, base_url: str | URL) -> None:
        """
        Initializes the client.

        :param base_url: The base URL of the API.
        """
        self._base_url = base_url
        self._session: ClientSession | None = None

    async def _get_session(self) -> ClientSession:
        """
        Returns the session.

        :return: The session.
        """
        if not self._session:
            ssl_context: SSLContext = SSLContext()
            connector: TCPConnector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=dumps,
            )
        return self._session

    @backoff.on_exception(backoff.expo, ClientError, max_time=60)
    async def _make_request(
        self,
        method: str,
        url: str | URL,
        proxy: str | None = None,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any] | str]:
        """
        Makes a request to the API.

        :param method: The method of the request.
        :param url: The URL of the request.
        :param proxy: The proxy of the request.
        :param params: The parameters of the request.
        :param json: The payload of the request.
        :param headers: The headers of the request.
        :param data: The data of the request.
        :raises ClientError: If the status code is not 200.
        :return: The response.
        """
        session: ClientSession = await self._get_session()
        async with session.request(
            method,
            url,
            params=params,
            json=json,
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            status = response.status
            if status != HTTPOk.status_code:
                s = await response.text()
                raise ClientError(f"Got status {status} for {method} {url}: {s}")

            try:
                result = await response.json(loads=loads)
            except ContentTypeError:
                result = await response.text()

            return status, result

    async def close(self) -> None:
        """
        Closes the session.
        """
        if not self._session:
            return

        if self._session.closed:
            return

        await self._session.close()

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
