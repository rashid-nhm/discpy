import zlib
from typing import List, Optional, Union

import aiohttp

from .. import config
from ..objects.intents import Intents


class WebsocketClient:
    def __init__(self, session: aiohttp.ClientSession, gateway_url: str, intents: Union[int, List[Intents]],
                 gateway_version: Union[str, int] = None):
        self.__gateway_url: str = gateway_url
        self.__gateway_version: str = str(gateway_version or config.DEFAULT_GATEWAY_VERSION).lstrip("v")
        self.__encoding: str = "json"
        self.__gateway_endpoint: str = f"{gateway_url}?" \
                                       f"v={self.__gateway_version}&" \
                                       f"encoding={self.__encoding}"
        self.__intents: int = intents if isinstance(intents, int) else sum(intents)

        self.__msg_decompressor: zlib.decompressobj = zlib.decompressobj()
        self.__msg_buffer: bytearray = bytearray()

        self.__ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.__session: aiohttp.ClientSession = session

        self.__keep_alive_thread = None
        self.__keep_alive_sent = None
        self.__keep_alive_acked = None

        self.__last_sequence_id: Optional[int] = None

    def connect(self):
        pass

