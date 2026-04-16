"""Message Gate — 消息门控纯函数 (spec §5)

Gate 是 mechanism 级保证：根据 conversation.mode + sender.role 决定最终 visibility。
Agent 在 takeover 模式下无法绕过 gate 直接向客户发消息。
"""

from __future__ import annotations

from zchat_protocol.conversation import Conversation
from zchat_protocol.message_types import MessageVisibility
from zchat_protocol.mode import ConversationMode
from zchat_protocol.participant import Participant, ParticipantRole


# Gate 规则表: (mode, role) → 强制 visibility（覆盖 requested）
_GATE_RULES: dict[tuple[str, str], MessageVisibility] = {
    (ConversationMode.COPILOT.value, ParticipantRole.OPERATOR.value): MessageVisibility.SIDE,
    (ConversationMode.TAKEOVER.value, ParticipantRole.AGENT.value): MessageVisibility.SIDE,
}


def gate_message(
    conversation: Conversation,
    sender: Participant,
    requested_visibility: MessageVisibility,
) -> MessageVisibility:
    """决定消息的最终可见性。纯函数，无副作用。"""
    # system / side 消息不受 gate 影响（不可逆降级原则）
    if requested_visibility == MessageVisibility.SYSTEM:
        return MessageVisibility.SYSTEM
    if requested_visibility == MessageVisibility.SIDE:
        return MessageVisibility.SIDE

    # dict lookup: (mode, role) → forced visibility
    role_value = sender.role.value if hasattr(sender.role, "value") else sender.role
    key = (conversation.mode, role_value)
    forced = _GATE_RULES.get(key)
    if forced is not None:
        return forced
    return requested_visibility
