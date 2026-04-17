"""test_irc_encoding — irc_encoding 模块单元测试。"""

import json
import pytest

from zchat_protocol.irc_encoding import (
    MSG_PREFIX, EDIT_PREFIX, SIDE_PREFIX, SYS_PREFIX,
    encode_msg, encode_edit, encode_side, encode_sys,
    make_sys_payload, parse,
)


def test_prefix_constants():
    assert MSG_PREFIX == "__msg:"
    assert EDIT_PREFIX == "__edit:"
    assert SIDE_PREFIX == "__side:"
    assert SYS_PREFIX == "__zchat_sys:"


def test_encode_msg_roundtrip():
    mid = "abc-123"
    text = "hello world"
    encoded = encode_msg(mid, text)
    result = parse(encoded)
    assert result["kind"] == "msg"
    assert result["message_id"] == mid
    assert result["text"] == text


def test_encode_edit_roundtrip():
    mid = "def-456"
    text = "edited content"
    encoded = encode_edit(mid, text)
    result = parse(encoded)
    assert result["kind"] == "edit"
    assert result["message_id"] == mid
    assert result["text"] == text


def test_encode_side_roundtrip():
    text = "side channel message"
    encoded = encode_side(text)
    result = parse(encoded)
    assert result["kind"] == "side"
    assert result["text"] == text


def test_encode_sys_roundtrip():
    payload = make_sys_payload("alice-agent0", "sys.stop_request", {"reason": "test"})
    encoded = encode_sys(payload)
    result = parse(encoded)
    assert result["kind"] == "sys"
    assert result["payload"]["nick"] == "alice-agent0"
    assert result["payload"]["type"] == "sys.stop_request"
    assert result["payload"]["body"]["reason"] == "test"
    assert "id" in result["payload"]
    assert "ts" in result["payload"]


def test_parse_plain_text():
    result = parse("hello, just a normal message")
    assert result["kind"] == "plain"
    assert result["text"] == "hello, just a normal message"


def test_parse_malformed_msg_falls_back_to_plain():
    # __msg: 后面没有冒号分隔 message_id，退化为 plain
    malformed = "__msg:noColon"
    result = parse(malformed)
    assert result["kind"] == "plain"
    assert result["text"] == malformed


def test_parse_malformed_edit_falls_back_to_plain():
    malformed = "__edit:noColon"
    result = parse(malformed)
    assert result["kind"] == "plain"
    assert result["text"] == malformed


def test_parse_malformed_sys_falls_back_to_plain():
    malformed = "__zchat_sys:not-json-at-all{{"
    result = parse(malformed)
    assert result["kind"] == "plain"
    assert result["text"] == malformed


def test_make_sys_payload_fields():
    payload = make_sys_payload("alice-agent0", "sys.join", {"channel": "#general"}, ref_id="ref-001")
    assert payload["nick"] == "alice-agent0"
    assert payload["type"] == "sys.join"
    assert payload["body"]["channel"] == "#general"
    assert payload["ref_id"] == "ref-001"
    assert "id" in payload
    assert "ts" in payload
    assert isinstance(payload["ts"], float)


def test_make_sys_payload_no_ref_id():
    payload = make_sys_payload("bob-helper", "sys.stop_request", {})
    assert payload["ref_id"] is None


def test_encode_msg_text_with_colon():
    # text 本身含冒号时，parse 只取第一个冒号作为分隔
    mid = "msg-001"
    text = "time is 12:30:00"
    encoded = encode_msg(mid, text)
    result = parse(encoded)
    assert result["kind"] == "msg"
    assert result["message_id"] == mid
    assert result["text"] == text


def test_encode_side_empty_text():
    encoded = encode_side("")
    result = parse(encoded)
    assert result["kind"] == "side"
    assert result["text"] == ""


def test_parse_empty_string():
    result = parse("")
    assert result["kind"] == "plain"
    assert result["text"] == ""
