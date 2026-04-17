from zchat_protocol.naming import scoped_name, AGENT_SEPARATOR


def test_separator_is_dash():
    assert AGENT_SEPARATOR == "-"


def test_scoped_name_adds_prefix():
    assert scoped_name("helper", "alice") == "alice-helper"


def test_scoped_name_always_prepends_even_if_already_prefixed():
    """scoped_name 无脑 prepend username，不做去重。"""
    assert scoped_name("alice-helper", "alice") == "alice-alice-helper"
    assert scoped_name("bob-helper", "alice") == "alice-bob-helper"
