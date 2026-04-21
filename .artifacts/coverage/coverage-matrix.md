# Coverage Matrix · zchat-protocol

> Bootstrap 2026-04-21 (V6 finalize 后)。

## 1. 代码测试覆盖

| Module | Source | Tests | 状态 |
|---|---|---|---|
| encoding | `zchat_protocol/irc_encoding.py` | `tests/test_irc_encoding.py` | ✅ 4 前缀 + encode/parse |
| ws_messages | `zchat_protocol/ws_messages.py` | `tests/test_ws_messages.py` | ✅ 6 WSType + build_* + parse |
| naming | `zchat_protocol/naming.py` | `tests/test_naming.py` | ✅ scoped_name + separator |
| tests | 自指 | — | — |
| meta | pyproject, __init__ 等 | — | 配置 |

**Unit baseline**: 32 passed / 0 failed / 0 skipped。

## 2. 架构红线

**零业务名命中**（grep customer/operator/admin/squad/feishu 全 No matches）。
`__init__.py` docstring 明文声明："协议层不含业务逻辑"。

## 3. 已知缺口

无。协议层小而纯，覆盖完整。
