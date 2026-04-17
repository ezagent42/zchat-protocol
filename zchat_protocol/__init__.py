"""zchat-protocol — 格式合同与编解码函数库。

本包**只包含**:
- irc_encoding: IRC PRIVMSG 前缀编解码
- ws_messages: WebSocket JSON 信封
- naming: agent 命名规则

**不包含**任何运行时状态、I/O、业务逻辑。
"""

from zchat_protocol import irc_encoding, ws_messages, naming

__all__ = ["irc_encoding", "ws_messages", "naming"]
