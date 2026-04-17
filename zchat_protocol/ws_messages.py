"""WebSocket JSON 消息信封 — bridge ↔ channel-server 通信合同。

消息内容本身（text）由 irc_encoding 承载其种类前缀；
ws_messages 只管包装层：type、channel、source、content、...
"""

from __future__ import annotations
import json
from typing import Any


class WSType:
    REGISTER = "register"      # bridge → cs 注册
    REGISTERED = "registered"  # cs → bridge 注册确认
    MESSAGE = "message"        # 双向：普通消息（content 含 IRC 前缀）
    COMMAND = "command"        # 备用：显式命令（目前走 message 中的 "/" 前缀路径）
    EVENT = "event"            # cs → bridge 状态事件
    ACK = "ack"                # cs → bridge 操作确认


def build_register(bridge_type: str, instance_id: str, capabilities: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": WSType.REGISTER,
        "bridge_type": bridge_type,
        "instance_id": instance_id,
        "capabilities": capabilities or [],
    }


def build_message(
    channel: str,
    source: str,
    content: str,
    message_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": WSType.MESSAGE,
        "channel": channel,
        "source": source,
        "content": content,
    }
    if message_id is not None:
        payload["message_id"] = message_id
    return payload


def build_command(channel: str, source: str, command: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "type": WSType.COMMAND,
        "channel": channel,
        "source": source,
        "command": command,
        "args": args or {},
    }


def build_event(channel: str, event: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "type": WSType.EVENT,
        "channel": channel,
        "event": event,
        "data": data or {},
    }


def parse(raw: str | dict) -> dict[str, Any]:
    """解析 WS JSON 消息，返回 dict。已是 dict 直接返回；字符串则 json.loads。

    校验 type 字段存在；未知 type 抛 ValueError。
    """
    if isinstance(raw, str):
        data = json.loads(raw)
    elif isinstance(raw, dict):
        data = raw
    else:
        raise TypeError(f"ws_messages.parse expects str or dict, got {type(raw)}")

    msg_type = data.get("type")
    known_types = {WSType.REGISTER, WSType.REGISTERED, WSType.MESSAGE, WSType.COMMAND, WSType.EVENT, WSType.ACK}
    if msg_type not in known_types:
        raise ValueError(f"unknown WS message type: {msg_type!r}")
    return data
