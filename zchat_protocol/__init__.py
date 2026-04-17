"""zchat protocol specification — authoritative definitions for conversation primitives.

Modules:
- naming: Agent naming conventions (scoped_name, AGENT_SEPARATOR)
- sys_messages: IRC system message encode/decode
- conversation: Conversation + ConversationState state machine
- mode: ConversationMode + transition rules
- event: EventType + Event
- commands: Command parsing
- participant: Participant + ParticipantRole
- message_types: Message + MessageVisibility
- timer: Timer + TimerAction
"""

PROTOCOL_VERSION = "0.2"
