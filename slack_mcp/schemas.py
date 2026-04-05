"""Type schemas for Slack MCP Server."""

from typing_extensions import TypedDict


class OAuthTokenData(TypedDict, total=False):
    """OAuth token data for Slack API authentication."""

    token: str  # Bot token (xoxb-...) or User token (xoxp-...)
    refresh_token: str
    token_type: str  # "bot" or "user"
    scope: str
    bot_user_id: str
    app_id: str
    team_id: str
    team_name: str
    enterprise_id: str
    expires_in: int


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
