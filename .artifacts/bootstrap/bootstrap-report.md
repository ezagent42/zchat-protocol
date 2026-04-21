# Bootstrap Report · zchat-protocol

> Skill 0 · 2026-04-21 V6 finalize 后重跑

## 环境

Python 3.13.5 + uv + pytest。**32 passed / 0 failed / 0 skipped** / 32 tests in 0.2s。

## 5 模块

1. **encoding** — `irc_encoding.py`：`__msg/__side/__edit/__zchat_sys` 4 前缀编解码（phase 6 加 `ensure_ascii=False` 避 IRC MessageTooLong）
2. **ws_messages** — 6 WSType + `build_message/command/event/register` + `parse`
3. **naming** — `scoped_name` + `AGENT_SEPARATOR = "-"`（IRC RFC 2812 兼容）
4. **tests** — 3 个 test_*.py，30 个用例
5. **meta** — pyproject + `__init__.py` docstring + publish workflow

## 红线审计

**零违规**。grep `customer|operator|admin|squad|feishu` 全 `No matches`。
`__init__.py` 明文声明："The protocol layer does NOT contain business logic."

## V6 改动

- `encode_sys`: `json.dumps(payload, ensure_ascii=False)` — 防 IRC 512 字节超限
- `test_ws_messages.py`: 测试 fixture 去业务名（`customer_message` → `made_up_type`）

## 下一步

小库稳定。无后续工作。
