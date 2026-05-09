"""Type schemas for Slack MCP Server."""

from typing_extensions import TypedDict


class MessageData(TypedDict, total=False):
    """Message content structure."""

    channel: str
    text: str
    thread_ts: str
    parse: str  # "full" or "none"
    blocks: list
    attachments: list


class UserData(TypedDict, total=False):
    """User metadata structure."""

    id: str
    username: str
    name: str
    real_name: str
    email: str
    is_admin: bool
    is_owner: bool
    is_bot: bool


class ChannelData(TypedDict, total=False):
    """Channel metadata structure."""

    id: str
    name: str
    is_private: bool
    is_archived: bool
    is_general: bool
    creator: str
    created: int
    topic: str
    purpose: str
    num_members: int
    members: list[str]
