"""Slack API client factory."""

from slack_sdk import WebClient
from fastmcp_credentials import get_credentials


def get_client() -> WebClient:
    cred = get_credentials()

    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")

    return WebClient(token=cred.access_token)
