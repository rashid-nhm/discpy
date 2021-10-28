from typing import Dict, Union

import aiohttp

from .. import utils, consts, config


class HTTPClient:
    def __init__(self, api_version: Union[int, str] = None, metadata: str = None):
        self.__api_version: str = f"v{str(api_version or config.DEFAULT_API_VERSION).lstrip('v')}"
        self.__base_api_endpoint: str = f"{consts.DISCORD_API_BASE_URL}/{self.__api_version}"
        self.__headers: Dict[str, str] = {
            "User-Agent": f"DiscordBot ({consts.GIT_URL}, {consts.VERSION}) {metadata or ''}".rstrip()
        }

    @property
    def base_api_endpoint(self) -> str:
        return self.__base_api_endpoint

    @property
    def headers(self) -> Dict[str, str]:
        return self.__headers

    def add_request_header(self, header_name: str, header_content: str) -> None:
        self.__headers[header_name] = header_content

    async def request(self, session: aiohttp.ClientSession, method: str, path: str, **kwargs) -> Dict:
        path = utils.generate_deterministic_url_path(path)
        if "headers" in kwargs:
            headers: Dict[str, str] = {**self.headers, **kwargs.get("headers", {})}
            kwargs.pop("headers", None)
        else:
            headers: Dict[str, str] = self.headers
        async with session.request(method, f"{self.base_api_endpoint}/{path}", headers=headers, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()
