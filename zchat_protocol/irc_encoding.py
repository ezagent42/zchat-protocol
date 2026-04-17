"""IRC PRIVMSG 内嵌前缀的编解码 — 三仓共享的唯一真源。

5 种消息种类通过前缀编码：
  __msg:<uuid>:<text>     普通消息（带 id，用于续写）
  __edit:<uuid>:<text>    编辑已有消息
  __side:<text>           side 可见性
  __zchat_sys:<json>      机对机控制信令
  <text>                  纯文本（无前缀）
"""

from __future__ import annotations
import json
import os
import time
from typing import Any

# 前缀常量
MSG_PREFIX = "__msg:"
EDIT_PREFIX = "__edit:"
SIDE_PREFIX = "__side:"
SYS_PREFIX = "__zchat_sys:"


def encode_msg(message_id: str, text: str) -> str:
    return f"{MSG_PREFIX}{message_id}:{text}"


def encode_edit(message_id: str, text: str) -> str:
    return f"{EDIT_PREFIX}{message_id}:{text}"


def encode_side(text: str) -> str:
    return f"{SIDE_PREFIX}{text}"


def encode_sys(payload: dict[str, Any]) -> str:
    """机对机控制消息：payload 里至少含 {'type': 'sys.xxx', 'nick': ..., 'body': ...}"""
    return f"{SYS_PREFIX}{json.dumps(payload)}"


def make_sys_payload(nick: str, sys_type: str, body: dict[str, Any], ref_id: str | None = None) -> dict[str, Any]:
    """构造一个 sys 消息 payload（等价于旧 sys_messages.make_sys_message）。"""
    return {
        "id": os.urandom(4).hex(),
        "nick": nick,
        "type": sys_type,
        "body": body,
        "ref_id": ref_id,
        "ts": time.time(),
    }


def parse(content: str) -> dict[str, Any]:
    """解析 IRC PRIVMSG 的 content，返回 {kind, text, [message_id], [payload]}。

    kind ∈ {'msg', 'edit', 'side', 'sys', 'plain'}
    """
    if content.startswith(EDIT_PREFIX):
        rest = content[len(EDIT_PREFIX):]
        colon_idx = rest.find(":")
        if colon_idx == -1:
            return {"kind": "plain", "text": content}
        return {
            "kind": "edit",
            "message_id": rest[:colon_idx],
            "text": rest[colon_idx + 1:],
        }

    if content.startswith(MSG_PREFIX):
        rest = content[len(MSG_PREFIX):]
        colon_idx = rest.find(":")
        if colon_idx == -1:
            return {"kind": "plain", "text": content}
        return {
            "kind": "msg",
            "message_id": rest[:colon_idx],
            "text": rest[colon_idx + 1:],
        }

    if content.startswith(SIDE_PREFIX):
        return {"kind": "side", "text": content[len(SIDE_PREFIX):]}

    if content.startswith(SYS_PREFIX):
        try:
            payload = json.loads(content[len(SYS_PREFIX):])
        except json.JSONDecodeError:
            return {"kind": "plain", "text": content}
        return {"kind": "sys", "payload": payload}

    return {"kind": "plain", "text": content}
