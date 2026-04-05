"""MCP tool definitions for Slack integration."""

import json
import logging
from typing import Any, Optional

from fastmcp import FastMCP
from pydantic import Field
from slack_sdk.errors import SlackApiError

from slack_mcp.service import get_client

logger = logging.getLogger("slack-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    """Register all Slack MCP tools."""

    # =========== HEALTH CHECK ===========
    @mcp.tool(
        name="health_check",
        description="Check server readiness and basic connectivity.",
    )
    def health_check() -> str:
        """Health check endpoint."""
        return json.dumps({"status": "ok", "server": "CL Slack MCP Server"})

    # =========== TIER 1: CORE MESSAGING ===========

    @mcp.tool(
        name="send_message",
        description="Post a message to a Slack channel or direct message with text and optional blocks.",
    )
    def send_message(
        oauth_token: str = Field(
            ..., description="Slack OAuth token (xoxb-... or xoxp-...)"
        ),
        channel: str = Field(
            ..., description="Channel ID or name (e.g., #general or C123ABC456)"
        ),
        text: str = Field(
            default="", description="Plain text message (up to 4000 characters)"
        ),
        blocks: list = Field(
            default=None,
            description="Slack Block Kit JSON for rich formatting (optional)",
        ),
        thread_ts: str = Field(
            default=None,
            description="Parent message timestamp to reply in thread (optional)",
        ),
        reply_broadcast: bool = Field(
            default=False, description="Also broadcast reply to channel"
        ),
    ) -> str:
        """Post message to channel."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.chat_postMessage(
                channel=channel,
                text=text if text else None,
                blocks=blocks,
                thread_ts=thread_ts,
                reply_broadcast=reply_broadcast,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in send_message: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed send_message: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="read_messages",
        description="Get message history from a channel with optional filtering.",
    )
    def read_messages(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID or name"),
        limit: int = Field(default=20, description="Number of messages (1-100)"),
        oldest: Optional[str] = Field(
            default=None, description="Timestamp cutoff (oldest)"
        ),
        latest: Optional[str] = Field(
            default=None, description="Timestamp cutoff (latest)"
        ),
    ) -> str:
        """Get message history."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.conversations_history(
                channel=channel,
                limit=min(limit, 100),
                oldest=oldest,
                latest=latest,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in read_messages: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed read_messages: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="update_message",
        description="Edit an existing message.",
    )
    def update_message(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        ts: str = Field(..., description="Message timestamp"),
        text: Optional[str] = Field(default=None, description="New text (optional)"),
        blocks: Optional[list] = Field(
            default=None, description="New blocks (optional)"
        ),
    ) -> str:
        """Update message."""
        try:
            if not text and not blocks:
                return json.dumps(
                    {"ok": False, "error": "Either text or blocks required"}
                )

            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.chat_update(
                channel=channel,
                ts=ts,
                text=text,
                blocks=blocks,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in update_message: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed update_message: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="delete_message",
        description="Delete a message.",
    )
    def delete_message(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        ts: str = Field(..., description="Message timestamp"),
    ) -> str:
        """Delete message."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.chat_delete(channel=channel, ts=ts)
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in delete_message: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed delete_message: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="search_messages",
        description="Full-text search across workspace messages.",
    )
    def search_messages(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        query: str = Field(..., description="Search query"),
        sort: str = Field(default="score", description="Sort by score or timestamp"),
        sort_dir: str = Field(default="desc", description="asc or desc"),
        count: int = Field(default=20, description="Number of results"),
    ) -> str:
        """Search messages."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.search_messages(
                query=query,
                sort=sort,
                sort_dir=sort_dir,
                count=count,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in search_messages: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed search_messages: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="reply_thread",
        description="Post a reply in a message thread.",
    )
    def reply_thread(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        thread_ts: str = Field(..., description="Parent message timestamp"),
        text: str = Field(default="", description="Reply text"),
        blocks: Optional[list] = Field(
            default=None, description="Block Kit JSON (optional)"
        ),
        broadcast: bool = Field(default=False, description="Broadcast to channel"),
    ) -> str:
        """Reply to a thread."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.chat_postMessage(
                channel=channel,
                text=text if text else None,
                blocks=blocks,
                thread_ts=thread_ts,
                reply_broadcast=broadcast,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in reply_thread: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed reply_thread: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    # =========== TIER 2: CHANNEL MANAGEMENT ===========

    @mcp.tool(
        name="list_channels",
        description="Browse channels in the workspace. Maps to conversations.list API.",
    )
    def list_channels(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        exclude_archived: bool = Field(
            default=True, description="Skip archived channels"
        ),
        limit: int = Field(default=20, description="Channels per page (1-100)"),
        cursor: Optional[str] = Field(
            default=None,
            description="Pagination cursor from response_metadata.next_cursor",
        ),
        types: Optional[str] = Field(
            default="public_channel",
            description="Comma-separated channel types: public_channel, private_channel, mpim, im",
        ),
        team_id: Optional[str] = Field(
            default=None, description="Team ID (for org-wide apps only)"
        ),
    ) -> str:
        """List channels."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            kwargs = {
                "exclude_archived": exclude_archived,
                "limit": min(limit, 100),
            }
            if cursor:
                kwargs["cursor"] = cursor
            if types:
                kwargs["types"] = types
            if team_id:
                kwargs["team_id"] = team_id

            response = client.conversations_list(**kwargs)
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in list_channels: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed list_channels: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="create_channel",
        description="Create a new channel.",
    )
    def create_channel(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        name: str = Field(..., description="Channel name (lowercase, no spaces)"),
        is_private: bool = Field(default=False, description="Make private"),
        description: Optional[str] = Field(
            default=None, description="Description (optional)"
        ),
    ) -> str:
        """Create channel."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            kwargs = {"name": name, "is_private": is_private}
            if description:
                kwargs["description"] = description

            response = client.conversations_create(**kwargs)
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in create_channel: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed create_channel: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="archive_channel",
        description="Archive or unarchive a channel.",
    )
    def archive_channel(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        archive: bool = Field(
            default=True, description="True to archive, False to unarchive"
        ),
    ) -> str:
        """Archive/unarchive channel."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            if archive:
                response = client.conversations_archive(channel=channel)
            else:
                response = client.conversations_unarchive(channel=channel)

            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in archive_channel: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed archive_channel: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="get_channel_info",
        description="Get metadata for a channel.",
    )
    def get_channel_info(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
    ) -> str:
        """Get channel info."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.conversations_info(
                channel=channel,
                include_num_members=True,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in get_channel_info: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed get_channel_info: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="invite_users_to_channel",
        description="Invite users to a channel.",
    )
    def invite_users_to_channel(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        users: list[str] = Field(..., description="List of user IDs"),
    ) -> str:
        """Invite users to channel."""
        try:
            if not users:
                return json.dumps({"ok": False, "error": "At least one user required"})

            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.conversations_invite(
                channel=channel,
                users=users,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in invite_users_to_channel: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed invite_users_to_channel: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    # =========== TIER 3: SEARCH & DISCOVERY ===========

    @mcp.tool(
        name="search_files",
        description="Search files across workspace.",
    )
    def search_files(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        query: Optional[str] = Field(
            default=None, description="Search query (optional)"
        ),
        sort: str = Field(default="score", description="Sort by score or timestamp"),
        sort_dir: str = Field(default="desc", description="asc or desc"),
        count: int = Field(default=20, description="Number of results"),
        types: Optional[str] = Field(default=None, description="File types (optional)"),
    ) -> str:
        """Search files."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            kwargs = {
                "sort": sort,
                "sort_dir": sort_dir,
                "count": count,
            }
            if query:
                kwargs["query"] = query
            if types:
                kwargs["types"] = types

            response = client.search_files(**kwargs)
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in search_files: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed search_files: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="map_channels",
        description="List all channels with metadata.",
    )
    def map_channels(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        include_archived: bool = Field(default=False, description="Include archived"),
    ) -> str:
        """Map all channels."""
        try:
            client = get_client(oauth_token)
            all_channels = []
            cursor = None

            # API call directly in the tool with pagination
            while True:
                response = client.conversations_list(
                    exclude_archived=not include_archived,
                    limit=100,
                    cursor=cursor,
                )
                all_channels.extend(response.data.get("channels", []))
                cursor = response.data.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break

            return json.dumps(
                {
                    "ok": True,
                    "channels": all_channels,
                    "total": len(all_channels),
                }
            )
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in map_channels: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed map_channels: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="find_user",
        description="Search for a user by name, email, or ID.",
    )
    def find_user(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        query: str = Field(..., description="User name, email, or ID"),
    ) -> str:
        """Find user."""
        try:
            client = get_client(oauth_token)

            # Try direct lookup if looks like user ID
            if query.startswith("U") or query.startswith("W"):
                try:
                    response = client.users_info(user=query)
                    return json.dumps(response.data)
                except SlackApiError:
                    pass

            # Otherwise list and filter
            response = client.users_list(limit=100)
            users = response.data.get("members", [])

            # Filter matches
            matches = [
                u
                for u in users
                if query.lower() in u.get("name", "").lower()
                or query.lower() in u.get("real_name", "").lower()
                or query.lower() in u.get("profile", {}).get("email", "").lower()
            ]

            return json.dumps(
                {
                    "ok": True,
                    "matches": matches,
                    "total": len(matches),
                }
            )
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in find_user: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed find_user: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    # =========== TIER 4: ADVANCED ===========

    @mcp.tool(
        name="extract_threads",
        description="Extract thread metadata.",
    )
    def extract_threads(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        channel: str = Field(..., description="Channel ID"),
        limit: int = Field(default=10, description="Number of threads"),
    ) -> str:
        """Extract threads."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.conversations_history(
                channel=channel,
                limit=limit,
            )

            threads = []
            for msg in response.data.get("messages", []):
                if msg.get("thread_ts") == msg.get("ts"):
                    thread_info = {
                        "ts": msg.get("ts"),
                        "user": msg.get("user"),
                        "text": msg.get("text"),
                        "reply_count": msg.get("reply_count", 0),
                        "latest_reply": msg.get("latest_reply"),
                    }
                    threads.append(thread_info)

            return json.dumps(
                {
                    "ok": True,
                    "threads": threads,
                    "note": "For full async summarization, implement polling with job ID",
                }
            )
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in extract_threads: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed extract_threads: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    # =========== TIER 5: ADMIN/WORKSPACE ===========

    @mcp.tool(
        name="list_users",
        description="Get workspace roster.",
    )
    def list_users(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        limit: int = Field(default=20, description="Users per page (1-100)"),
        cursor: Optional[str] = Field(default=None, description="Pagination cursor"),
    ) -> str:
        """List users."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.users_list(
                limit=min(limit, 100),
                cursor=cursor,
            )
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in list_users: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed list_users: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="get_workspace_info",
        description="Get workspace metadata.",
    )
    def get_workspace_info(
        oauth_token: str = Field(..., description="Slack OAuth token"),
    ) -> str:
        """Get workspace info."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.team_info()
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in get_workspace_info: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed get_workspace_info: {e}")
            return json.dumps({"ok": False, "error": str(e)})

    @mcp.tool(
        name="get_user_presence",
        description="Get user presence status.",
    )
    def get_user_presence(
        oauth_token: str = Field(..., description="Slack OAuth token"),
        user: str = Field(..., description="User ID"),
    ) -> str:
        """Get user presence."""
        try:
            client = get_client(oauth_token)
            # API call directly in the tool
            response = client.users_getPresence(user=user)
            return json.dumps(response.data)
        except SlackApiError as e:
            error_code = e.response.get("error", "unknown_error")
            logger.error(f"Slack API error in get_user_presence: {error_code}")
            return json.dumps({"ok": False, "error": error_code})
        except Exception as e:
            logger.error(f"Failed get_user_presence: {e}")
            return json.dumps({"ok": False, "error": str(e)})
