"""Agent naming conventions."""

AGENT_SEPARATOR = "-"


def scoped_name(name: str, username: str) -> str:
    """Always add username prefix to agent name.
    'helper' + 'alice' → 'alice-helper'
    'alice-helper' + 'alice' → 'alice-alice-helper'
    """
    return f"{username}{AGENT_SEPARATOR}{name}"
