"""Slack API client factory."""

from slack_sdk import WebClient


def get_client(oauth_token: str) -> WebClient:
    """
    Factory function to create Slack WebClient with token.

    Args:
        oauth_token: Bot token (xoxb-...) or User token (xoxp-...)

    Returns:
        Initialized WebClient instance
    """
    return WebClient(token=oauth_token)
