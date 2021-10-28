import json
from enum import IntEnum
from typing import Any, Dict, Union


class GatewayPacketOpType(IntEnum):
    DISPATCH: int = 0
    HEARTBEAT: int = 1
    IDENTIFY: int = 2
    PRESENCE_UPDATE: int = 3
    VOICE_STATE_UPDATE: int = 4
    RESUME: int = 6
    RECONNECT: int = 7
    REQUEST_GUILD_MEMBERS: int = 8
    INVALID_SESSION: int = 9
    HELLO: int = 10
    HEARTBEAT_ACK: int = 11


class GatewayPacket:
    def __init__(self, op: Union[int, GatewayPacketOpType], d: Dict, s: int = None, t: str = None):
        if isinstance(op, GatewayPacketOpType):
            op = op.value

        assert 0 <= op < 11 and op != 5, f"Invalid op code {op}"

        self.op = op
        self.d = d
        self.s = s
        self.t = t

    def __getitem__(self, item: str) -> Union[int, str, None]:
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def get(self, item: str, default: Any = None) -> Any:
        if hasattr(self, item):
            return getattr(self, item)
        return default


class GatewayPacketEncoder(json.JSONEncoder):
    def default(self, o: Union[Dict, GatewayPacket]) -> Any:
        ret = {
            "op": o["op"],
            "d": o["d"]
        }

        s = o.get("s")
        t = o.get("t")
        if s:
            ret["s"] = s
        if t:
            ret["t"] = t
        return ret
