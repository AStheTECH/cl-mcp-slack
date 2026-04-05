Manage Slack conversations, channels, users, and search workflows through MCP tools.

A Model Context Protocol (MCP) server that exposes Slack's API for messaging, channel operations, workspace discovery, and user-scoped automation.

---

## Overview

The CL Slack MCP Server provides stateless, token-based Slack API access:

- Core messaging and thread workflows
- Channel and workspace discovery tools
- User and file search capabilities

Perfect for:

- AI-assisted Slack operations
- Workflow automation across channels and users
- Building Slack copilots with MCP-compatible clients

---

## Tools

<details>
<summary><code>health_check</code> - Check server readiness and basic connectivity.</summary>

Returns a lightweight readiness response to confirm the MCP server is running.

**Inputs:**

- `none`

**Output:**

```json
{
	"status": "ok",
	"server": "CL Slack MCP Server"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/health_check
{}
```

</details>

<details>
<summary><code>send_message</code> - Post a message to a channel or direct message.</summary>

Posts text and optional Block Kit content to a Slack conversation.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token (`xoxb-...` or `xoxp-...`)
- `channel` (string, required) - Channel ID or name
- `text` (string, optional) - Message text
- `blocks` (array, optional) - Block Kit JSON
- `thread_ts` (string, optional) - Parent timestamp for threaded reply
- `reply_broadcast` (boolean, optional) - Broadcast threaded reply to channel

**Output:**

```json
{
	"ok": true,
	"channel": "C123ABC456",
	"ts": "1712000000.123456"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/send_message

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"text": "Hello from MCP"
}
```

</details>

<details>
<summary><code>read_messages</code> - Get message history from a channel.</summary>

Reads recent message history with optional time window filtering.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID or name
- `limit` (integer, optional) - Number of messages (1-100)
- `oldest` (string, optional) - Lower timestamp bound
- `latest` (string, optional) - Upper timestamp bound

**Output:**

```json
{
	"ok": true,
	"messages": []
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/read_messages

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"limit": 20
}
```

</details>

<details>
<summary><code>update_message</code> - Edit an existing message.</summary>

Updates message text or blocks for a specific channel timestamp.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `ts` (string, required) - Message timestamp
- `text` (string, optional) - Updated text
- `blocks` (array, optional) - Updated Block Kit payload

**Output:**

```json
{
	"ok": true,
	"ts": "1712000000.123456"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/update_message

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"ts": "1712000000.123456",
	"text": "Updated message"
}
```

</details>

<details>
<summary><code>delete_message</code> - Delete a message.</summary>

Deletes a Slack message by channel and timestamp.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `ts` (string, required) - Message timestamp

**Output:**

```json
{
	"ok": true,
	"channel": "C123ABC456",
	"ts": "1712000000.123456"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/delete_message

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"ts": "1712000000.123456"
}
```

</details>

<details>
<summary><code>search_messages</code> - Full-text search across workspace messages.</summary>

Searches Slack messages by query with score/timestamp sorting controls.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `query` (string, required) - Search query
- `sort` (string, optional) - `score` or `timestamp`
- `sort_dir` (string, optional) - `asc` or `desc`
- `count` (integer, optional) - Number of results

**Output:**

```json
{
	"ok": true,
	"messages": {
		"matches": []
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/search_messages

{
	"oauth_token": "xoxp-...",
	"query": "incident postmortem",
	"count": 10
}
```

</details>

<details>
<summary><code>reply_thread</code> - Post a reply in a message thread.</summary>

Adds a thread reply and optionally broadcasts it to the parent channel.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `thread_ts` (string, required) - Parent message timestamp
- `text` (string, optional) - Reply text
- `blocks` (array, optional) - Block Kit JSON
- `broadcast` (boolean, optional) - Broadcast to channel

**Output:**

```json
{
	"ok": true,
	"thread_ts": "1712000000.123456"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/reply_thread

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"thread_ts": "1712000000.123456",
	"text": "Follow-up update"
}
```

</details>

<details>
<summary><code>list_channels</code> - Browse workspace channels.</summary>

Lists channels with pagination, type filtering, and archived controls.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `exclude_archived` (boolean, optional) - Exclude archived channels
- `limit` (integer, optional) - Page size (1-100)
- `cursor` (string, optional) - Pagination cursor
- `types` (string, optional) - Comma-separated channel types
- `team_id` (string, optional) - Team ID for org-wide apps

**Output:**

```json
{
	"ok": true,
	"channels": [],
	"response_metadata": {
		"next_cursor": ""
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/list_channels

{
	"oauth_token": "xoxp-...",
	"limit": 50,
	"types": "public_channel,private_channel"
}
```

</details>

<details>
<summary><code>create_channel</code> - Create a new channel.</summary>

Creates a public or private channel, with optional description.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `name` (string, required) - Channel name
- `is_private` (boolean, optional) - Create private channel
- `description` (string, optional) - Channel description

**Output:**

```json
{
	"ok": true,
	"channel": {
		"id": "C123ABC456",
		"name": "team-updates"
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/create_channel

{
	"oauth_token": "xoxp-...",
	"name": "team-updates",
	"is_private": false
}
```

</details>

<details>
<summary><code>archive_channel</code> - Archive or unarchive a channel.</summary>

Archives channel when `archive=true`; unarchives when `archive=false`.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `archive` (boolean, optional) - Archive toggle

**Output:**

```json
{
	"ok": true
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/archive_channel

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"archive": true
}
```

</details>

<details>
<summary><code>get_channel_info</code> - Get metadata for a channel.</summary>

Returns channel details including membership counts where available.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID

**Output:**

```json
{
	"ok": true,
	"channel": {
		"id": "C123ABC456"
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/get_channel_info

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456"
}
```

</details>

<details>
<summary><code>invite_users_to_channel</code> - Invite users to a channel.</summary>

Invites one or more user IDs to the target channel.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `users` (array[string], required) - User IDs to invite

**Output:**

```json
{
	"ok": true,
	"channel": {
		"id": "C123ABC456"
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/invite_users_to_channel

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"users": ["U111", "U222"]
}
```

</details>

<details>
<summary><code>search_files</code> - Search files across workspace.</summary>

Searches Slack files by query, type, and sorting options.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `query` (string, optional) - Search query
- `sort` (string, optional) - `score` or `timestamp`
- `sort_dir` (string, optional) - `asc` or `desc`
- `count` (integer, optional) - Number of results
- `types` (string, optional) - File type filter

**Output:**

```json
{
	"ok": true,
	"files": {
		"matches": []
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/search_files

{
	"oauth_token": "xoxp-...",
	"query": "roadmap pdf",
	"count": 10
}
```

</details>

<details>
<summary><code>map_channels</code> - Enumerate channels with metadata.</summary>

Paginates through channel listings and returns a combined map.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `include_archived` (boolean, optional) - Include archived channels

**Output:**

```json
{
	"ok": true,
	"channels": [],
	"total": 0
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/map_channels

{
	"oauth_token": "xoxp-...",
	"include_archived": false
}
```

</details>

<details>
<summary><code>find_user</code> - Find a user by name, email, or ID.</summary>

Performs direct ID lookup and fallback member filtering.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `query` (string, required) - Name, email, or user ID

**Output:**

```json
{
	"ok": true,
	"matches": [],
	"total": 0
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/find_user

{
	"oauth_token": "xoxp-...",
	"query": "alice@example.com"
}
```

</details>

<details>
<summary><code>extract_threads</code> - Extract thread metadata from a channel.</summary>

Collects root messages that represent thread starters and returns summary fields.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `channel` (string, required) - Channel ID
- `limit` (integer, optional) - Number of messages scanned

**Output:**

```json
{
	"ok": true,
	"threads": [],
	"note": "For full async summarization, implement polling with job ID"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/extract_threads

{
	"oauth_token": "xoxp-...",
	"channel": "C123ABC456",
	"limit": 20
}
```

</details>

<details>
<summary><code>list_users</code> - Get workspace roster.</summary>

Lists users with pagination controls.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `limit` (integer, optional) - Users per page (1-100)
- `cursor` (string, optional) - Pagination cursor

**Output:**

```json
{
	"ok": true,
	"members": []
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/list_users

{
	"oauth_token": "xoxp-...",
	"limit": 50
}
```

</details>

<details>
<summary><code>get_workspace_info</code> - Get workspace metadata.</summary>

Returns workspace details from Slack `team.info`.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token

**Output:**

```json
{
	"ok": true,
	"team": {
		"id": "T123ABC456",
		"name": "Workspace Name"
	}
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/get_workspace_info

{
	"oauth_token": "xoxp-..."
}
```

</details>

<details>
<summary><code>get_user_presence</code> - Get user presence status.</summary>

Fetches active/away style presence for a given user ID.

**Inputs:**

- `oauth_token` (string, required) - Slack OAuth token
- `user` (string, required) - Slack user ID

**Output:**

```json
{
	"ok": true,
	"presence": "active"
}
```

**Usage Example:**

```bash
POST /mcp/cl-slack-mcp/get_user_presence

{
	"oauth_token": "xoxp-...",
	"user": "U123ABC456"
}
```

</details>

---

## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `oauth_token` - Slack access token used for API authentication.
- `channel` - Slack channel ID (for example, `C123ABC456`) or channel name where supported.
- `ts` - Slack message timestamp identifier.
- `thread_ts` - Parent message timestamp for thread operations.
- `limit` - Page size/count for list and history operations.
- `cursor` - Pagination cursor from `response_metadata.next_cursor`.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Channel Resource:**

```
Channel ID format: C########
Example: C123ABC456
```

**User Resource:**

```
User ID format: U######## or W########
Example: U123ABC456
```

**Message Resource:**

```
Message timestamp format: 1712000000.123456
Example: 1712000000.123456
```

</details>

---

## Authentication Guide

<details>
<summary><strong>OAuth / API Key Setup</strong></summary>

All tools require a valid Slack OAuth token. This server supports user tokens (`xoxp-...`) and bot tokens (`xoxb-...`).

### Step 1: Create Slack App

1. Go to [Slack App Management](https://api.slack.com/apps)
2. Create a new app from scratch
3. Select your workspace

### Step 2: Configure OAuth Credentials

1. Open **OAuth & Permissions** in your app settings
2. Copy **Client ID** and **Client Secret**
3. Add redirect URL (HTTPS required), for example:
4. `https://your-tunnel-host/slack/oauth/callback`

### Step 3: Generate Token with Included Script

Use `get_slack_oauth_token.py` from this repository.

Example user token flow:

```bash
python3 get_slack_oauth_token.py \
	--type user \
	--oauth-flow standard \
	--scopes search:read,channels:read,chat:write
```

The script supports:

- `standard` flow: `/oauth/v2/authorize` + `oauth.v2.access`
- `user-centric` flow: `/oauth/v2_user/authorize` + `oauth.v2.user.access`

Refer to [Slack Authentication Guide](https://docs.slack.dev/authentication/installing-with-oauth) for full details.

### Step 4: Required Scopes

Ensure the token includes scopes required by the tools you will call.

- `chat:write` - Send, update, delete, and reply to messages
- `channels:read` - List and inspect public channels
- `channels:history` - Read message history in public channels
- `search:read` - Search workspace messages/files
- `users:read` - List users and resolve identity metadata

If you use private channels, DMs, MPIMs, and usergroups, add corresponding `groups:*`, `im:*`, `mpim:*`, and `usergroups:*` scopes.

</details>

---

## Troubleshooting

<details>
<summary><strong>Common Issues & Solutions</strong></summary>

### Missing or Invalid Token

- **Cause:** `oauth_token` is missing, malformed, expired, or revoked
- **Solution:**
	1. Generate a fresh token with `get_slack_oauth_token.py`
	2. Confirm token prefix (`xoxp-` or `xoxb-`)
	3. Verify token has required scopes

### Missing Scope Errors

- **Cause:** Token does not include scope required by the Slack endpoint
- **Solution:**
	1. Add needed scope in Slack app dashboard
	2. Reinstall/reauthorize app
	3. Generate a new token

### bad_redirect_uri During OAuth

- **Cause:** Redirect URI mismatch between authorize and token-exchange steps
- **Solution:**
	1. Ensure exact same redirect URI is used in both steps
	2. Confirm redirect URL is added in Slack app settings
	3. Use HTTPS tunnel (zrok/ngrok) and keep it running

### App Requests Bot Install Unexpectedly

- **Cause:** Bot scopes/features are configured in Slack app while attempting user-only flow
- **Solution:**
	1. Remove unneeded bot scopes/capabilities from app config
	2. Use user-only scopes and rerun with `--type user`
	3. Reinstall/reauthorize after configuration changes

### MCP Server Not Reachable

- **Cause:** Server transport/host/port mismatch
- **Solution:**
	1. Start server with expected transport
	2. Confirm host/port arguments
	3. Check client points to `/mcp` path for HTTP transport

</details>

---

## Resources

<details>
<summary><strong>External Documentation</strong></summary>

- **[Slack API Documentation](https://api.slack.com/apis)** - Official Slack API overview
- **[Slack OAuth Guide](https://docs.slack.dev/authentication/installing-with-oauth)** - OAuth installation and token flows
- **[Slack Web API Reference](https://api.slack.com/methods)** - Endpoint reference for methods used by this server
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** - FastMCP runtime and tool framework

</details>

---
