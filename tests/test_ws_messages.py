"""test_ws_messages — ws_messages 模块单元测试。"""

import json
import pytest

from zchat_protocol.ws_messages import (
    WSType,
    build_register, build_message, build_command, build_event,
    parse,
)


def test_build_message_minimum():
    msg = build_message(channel="#general", source="alice", content="hello")
    assert msg["type"] == WSType.MESSAGE
    assert msg["channel"] == "#general"
    assert msg["source"] == "alice"
    assert msg["content"] == "hello"
    assert "message_id" not in msg


def test_build_message_with_message_id():
    msg = build_message(channel="#dev", source="bob", content="hi", message_id="uuid-001")
    assert msg["message_id"] == "uuid-001"
    assert msg["content"] == "hi"


def test_message_has_no_visibility_field():
    msg = build_message(channel="#general", source="alice", content="hello")
    assert "visibility" not in msg


def test_build_command():
    msg = build_command(channel="#general", source="alice", command="stop", args={"reason": "done"})
    assert msg["type"] == WSType.COMMAND
    assert msg["command"] == "stop"
    assert msg["args"]["reason"] == "done"
    assert msg["channel"] == "#general"
    assert msg["source"] == "alice"


def test_build_command_no_args():
    msg = build_command(channel="#general", source="alice", command="status")
    assert msg["args"] == {}


def test_build_event():
    msg = build_event(channel="#general", event="agent_joined", data={"nick": "alice-agent0"})
    assert msg["type"] == WSType.EVENT
    assert msg["event"] == "agent_joined"
    assert msg["data"]["nick"] == "alice-agent0"
    assert msg["channel"] == "#general"


def test_build_event_no_data():
    msg = build_event(channel="#general", event="ping")
    assert msg["data"] == {}


def test_build_register():
    msg = build_register(bridge_type="test", instance_id="inst-001", capabilities=["send", "receive"])
    assert msg["type"] == WSType.REGISTER
    assert msg["bridge_type"] == "test"
    assert msg["instance_id"] == "inst-001"
    assert "send" in msg["capabilities"]


def test_build_register_no_capabilities():
    msg = build_register(bridge_type="slack", instance_id="inst-002")
    assert msg["capabilities"] == []


def test_parse_known_types():
    for ws_type in [WSType.MESSAGE, WSType.COMMAND, WSType.EVENT, WSType.REGISTER,
                    WSType.REGISTERED, WSType.ACK]:
        raw = {"type": ws_type, "channel": "#x", "source": "s", "content": "c"}
        result = parse(raw)
        assert result["type"] == ws_type


def test_parse_unknown_type_raises():
    with pytest.raises(ValueError, match="unknown WS message type"):
        parse({"type": "made_up_type", "channel": "#x"})


def test_parse_dict_or_str():
    d = {"type": WSType.MESSAGE, "channel": "#x", "source": "s", "content": "c"}
    # 接受 dict
    result_dict = parse(d)
    assert result_dict["type"] == WSType.MESSAGE

    # 接受 str
    result_str = parse(json.dumps(d))
    assert result_str["type"] == WSType.MESSAGE


def test_parse_invalid_type_raises_typeerror():
    for bad_input in [None, [], 42, 3.14]:
        with pytest.raises(TypeError):
            parse(bad_input)


def test_parse_no_type_field_raises():
    with pytest.raises(ValueError):
        parse({"channel": "#x", "source": "s"})


def test_wstype_constants():
    assert WSType.REGISTER == "register"
    assert WSType.REGISTERED == "registered"
    assert WSType.MESSAGE == "message"
    assert WSType.COMMAND == "command"
    assert WSType.EVENT == "event"
    assert WSType.ACK == "ack"
