"""Configuration and constants for Slack MCP Server."""

import logging

# Slack API Configuration
SLACK_API_BASE = "https://slack.com/api"
SLACK_OAUTH_AUTHORIZATION_URL = "https://slack.com/oauth_v2/authorize"
SLACK_OAUTH_TOKEN_URL = "https://slack.com/api/oauth.v2.access"

# Scopes required for full functionality (can be overridden per deployment)
DEFAULT_SCOPES = [
    "chat:write",
    "chat:write.public",
    "channels:manage",
    "channels:read",
    "users:read",
    "users:read.email",
    "search:read",
    "files:read",
    "users.profile:read",
    "emoji:read",
    "reactions:read",
    "team:read",
    "usergroups:read",
    "conversations:read",
]

# Request timeout and retry settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 1.5

# Pagination defaults
DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# Message and history limits
MESSAGE_TEXT_LIMIT = 4000
HISTORY_DEFAULT_LIMIT = 50


def configure_logging() -> None:
    """Configure logging for Slack MCP Server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
