import asyncio
from typing import Dict, Optional, Union

import aiohttp

from .objects import user
from .helper_clients.http import HTTPClient

__all__ = (
    "Client"
)


class Client:
    def __init__(self, application_id: str = None, bot_token: str = None):
        self.__application_id: str = application_id
        self.__bot_token: str = bot_token

        self.__user: Optional[user.BotClientUser] = None
        self.__gateway_url: Optional[str] = None

        self.__connector: aiohttp.TCPConnector = aiohttp.TCPConnector()
        self.__session: Optional[aiohttp.ClientSession] = None
        self.__http: HTTPClient = HTTPClient()

    def _session(self, *args, **kwargs) -> aiohttp.ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession(*args, **kwargs)
        return self.__session

    async def login(self, bot_token: str = None) -> None:
        current_token = self.__bot_token
        if bot_token is not None:
            self.__bot_token = bot_token
        assert self.__bot_token is not None, "A bot token is required to login to the API Endpoint"

        headers: Dict[str, str] = self.__http.headers
        headers["Authorization"] = self._authorization_header

        async with self._session(
            skip_auto_headers=set(headers.keys()),
            headers=headers,
            connector=self.__connector,
            connector_owner=False
        ) as session:
            data_login: Dict[str, Union[str, bool, None]] = await self.__http.request(
                session=session,
                method="GET",
                path="/users/@me"
            )

            self.__bot_token = current_token
            self.__user = user.BotClientUser(**data_login)

            data_gateway: Dict[str, str] = await self.__http.request(
                session=session,
                method="GET",
                path="/gateway"
            )
            self.__gateway_url = data_gateway["url"]

    async def test(self):
        async with self._session(
                connector=self.__connector,
                connector_owner=False
        ) as session:
            print(await self.__http.request(
                session=session,
                method="GET",
                path="/gateway"
            ))

    async def logout(self):
        await self.__connector.close()

    @property
    def _authorization_header(self) -> str:
        return f"Bot {self.__bot_token}"

    @property
    def logged_in(self) -> bool:
        return self.__user is not None

    @property
    def gateway_url(self) -> Optional[str]:
        return self.__gateway_url

    @property
    def user(self) -> user.BaseUser:
        return self.__user

    async def connect_to_gateway(self):
        pass
