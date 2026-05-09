**Your entire Slack workspace, accessible through AI.**

A Model Context Protocol (MCP) server that exposes Slack's API for messaging, channel management, user discovery, and workspace administration.


## Overview

The Slack MCP Server provides comprehensive access to your Slack workspace:

- Send, read, edit, delete, and search messages across channels and threads
- Manage channels — create, archive, invite users, and browse the workspace roster
- Search files, find users, extract threads, and inspect workspace metadata

Perfect for:

- AI assistants that need to send or read Slack messages on your behalf
- Automating channel management, notifications, and team coordination
- Building tools that integrate Slack with other services and workflows


## Tools

### Messaging

<details>
<summary><code>send_message</code> — Post a message to a channel</summary>

Posts a message to a Slack channel or direct message, with optional rich formatting via Block Kit.

**Inputs:**
```
- `channel` (string, required) — Channel ID or name (e.g., #general or C123ABC456)
- `text` (string, optional) — Plain text message (up to 4000 characters)
- `blocks` (list, optional) — Slack Block Kit JSON for rich formatting
- `thread_ts` (string, optional) — Parent message timestamp to reply in a thread
- `reply_broadcast` (bool, optional) — Also broadcast the reply to the channel (default: false)
```

**Output:**

```json
{
  "ok": true,
  "channel": "C123ABC456",
  "ts": "1234567890.123456",
  "message": { "text": "Hello!", "user": "U123" }
}
```

</details>


<details>
<summary><code>read_messages</code> — Read message history from a channel</summary>

Retrieves message history from a channel with optional timestamp range filtering.

**Inputs:**
```
- `channel` (string, required) — Channel ID or name
- `limit` (int, optional) — Number of messages to return (1–100, default: 20)
- `oldest` (string, optional) — Oldest timestamp cutoff (Unix timestamp)
- `latest` (string, optional) — Latest timestamp cutoff (Unix timestamp)
```

**Output:**

```json
{
  "ok": true,
  "messages": [{ "type": "message", "text": "Hello!", "user": "U123", "ts": "..." }],
  "has_more": false
}
```

</details>


<details>
<summary><code>update_message</code> — Edit an existing message</summary>

Edits the text or blocks of an existing message in a channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `ts` (string, required) — Timestamp of the message to update
- `text` (string, optional) — New text content
- `blocks` (list, optional) — New Block Kit JSON
```

**Output:**

```json
{
  "ok": true,
  "channel": "C123ABC456",
  "ts": "1234567890.123456",
  "text": "Updated message"
}
```

</details>


<details>
<summary><code>delete_message</code> — Delete a message</summary>

Permanently deletes a message from a channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `ts` (string, required) — Timestamp of the message to delete
```

**Output:**

```json
{
  "ok": true,
  "channel": "C123ABC456",
  "ts": "1234567890.123456"
}
```

</details>


<details>
<summary><code>search_messages</code> — Full-text search across workspace messages</summary>

Searches all messages across the workspace using a query string, with sorting options.

**Inputs:**
```
- `query` (string, required) — Search query string
- `sort` (string, optional) — Sort by: score or timestamp (default: score)
- `sort_dir` (string, optional) — Sort direction: asc or desc (default: desc)
- `count` (int, optional) — Number of results to return (default: 20)
```

**Output:**

```json
{
  "ok": true,
  "messages": {
    "total": 5,
    "matches": [{ "text": "...", "channel": { "id": "C123" }, "ts": "..." }]
  }
}
```

</details>


<details>
<summary><code>reply_thread</code> — Post a reply in a message thread</summary>

Posts a reply to a specific thread, with the option to broadcast it to the channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `thread_ts` (string, required) — Timestamp of the parent message to reply to
- `text` (string, optional) — Reply text content
- `blocks` (list, optional) — Block Kit JSON for rich formatting
- `broadcast` (bool, optional) — Broadcast the reply to the channel (default: false)
```

**Output:**

```json
{
  "ok": true,
  "ts": "1234567890.999999",
  "message": { "text": "Reply text", "thread_ts": "..." }
}
```

</details>


### Channel Management

<details>
<summary><code>list_channels</code> — List channels in the workspace</summary>

Returns a paginated list of channels with optional type and archived filtering.

**Inputs:**
```
- `exclude_archived` (bool, optional) — Skip archived channels (default: true)
- `limit` (int, optional) — Channels per page (1–100, default: 20)
- `cursor` (string, optional) — Pagination cursor from response_metadata.next_cursor
- `types` (string, optional) — Comma-separated channel types: public_channel, private_channel, mpim, im (default: public_channel)
- `team_id` (string, optional) — Team ID for org-wide apps only
```

**Output:**

```json
{
  "ok": true,
  "channels": [{ "id": "C123", "name": "general", "is_private": false }],
  "response_metadata": { "next_cursor": "cursor-string" }
}
```

</details>


<details>
<summary><code>create_channel</code> — Create a new channel</summary>

Creates a new public or private Slack channel.

**Inputs:**
```
- `name` (string, required) — Channel name (lowercase, no spaces or special characters)
- `is_private` (bool, optional) — Create as a private channel (default: false)
- `description` (string, optional) — Channel description
```

**Output:**

```json
{
  "ok": true,
  "channel": { "id": "C456", "name": "new-channel", "is_private": false }
}
```

</details>


<details>
<summary><code>archive_channel</code> — Archive or unarchive a channel</summary>

Archives or unarchives a Slack channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `archive` (bool, optional) — true to archive, false to unarchive (default: true)
```

**Output:**

```json
{
  "ok": true
}
```

</details>


<details>
<summary><code>get_channel_info</code> — Get channel metadata</summary>

Returns metadata for a specific channel including member count and settings.

**Inputs:**
```
- `channel` (string, required) — Channel ID
```

**Output:**

```json
{
  "ok": true,
  "channel": {
    "id": "C123",
    "name": "general",
    "num_members": 42,
    "topic": { "value": "Company news" },
    ...
  }
}
```

</details>


<details>
<summary><code>invite_users_to_channel</code> — Invite users to a channel</summary>

Invites one or more users to an existing channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `users` (list, required) — List of user IDs to invite
```

**Output:**

```json
{
  "ok": true,
  "channel": { "id": "C123", "name": "general", "members": ["U123", "U456"] }
}
```

</details>


### Search & Discovery

<details>
<summary><code>search_files</code> — Search files across the workspace</summary>

Searches files in the workspace by query and optional type filter.

**Inputs:**
```
- `query` (string, optional) — Search query string
- `sort` (string, optional) — Sort by: score or timestamp (default: score)
- `sort_dir` (string, optional) — Sort direction: asc or desc (default: desc)
- `count` (int, optional) — Number of results to return (default: 20)
- `types` (string, optional) — File type filter (e.g., images, pdfs, docs)
```

**Output:**

```json
{
  "ok": true,
  "files": {
    "total": 3,
    "matches": [{ "name": "report.pdf", "url_private": "..." }]
  }
}
```

</details>


<details>
<summary><code>map_channels</code> — List all channels with full metadata</summary>

Fetches all channels in the workspace (with automatic pagination) and returns them with metadata.

**Inputs:**
```
- `include_archived` (bool, optional) — Include archived channels (default: false)
```

**Output:**

```json
{
  "ok": true,
  "channels": [{ "id": "C123", "name": "general", "num_members": 50 }, ...],
  "total": 12
}
```

</details>


<details>
<summary><code>find_user</code> — Search for a user by name, email, or ID</summary>

Looks up a user by their Slack ID, display name, real name, or email address.

**Inputs:**
```
- `query` (string, required) — User name, email address, or Slack user ID (e.g., U123ABC)
```

**Output:**

```json
{
  "ok": true,
  "matches": [{ "id": "U123", "name": "jane", "real_name": "Jane Doe", ... }],
  "total": 1
}
```

</details>


<details>
<summary><code>extract_threads</code> — Extract thread metadata from a channel</summary>

Retrieves thread metadata (reply count, latest reply, original message) from recent messages in a channel.

**Inputs:**
```
- `channel` (string, required) — Channel ID
- `limit` (int, optional) — Number of messages to scan for threads (default: 10)
```

**Output:**

```json
{
  "ok": true,
  "threads": [
    { "ts": "...", "user": "U123", "text": "...", "reply_count": 5, "latest_reply": "..." }
  ]
}
```

</details>


### Workspace & Users

<details>
<summary><code>list_users</code> — List workspace members</summary>

Returns a paginated list of all users in the workspace.

**Inputs:**
```
- `limit` (int, optional) — Users per page (1–100, default: 20)
- `cursor` (string, optional) — Pagination cursor from a previous response
```

**Output:**

```json
{
  "ok": true,
  "members": [{ "id": "U123", "name": "jane", "real_name": "Jane Doe", ... }],
  "response_metadata": { "next_cursor": "cursor-string" }
}
```

</details>


<details>
<summary><code>get_workspace_info</code> — Get workspace metadata</summary>

Returns information about the Slack workspace including name, domain, and settings.

**Inputs:**
```
None
```

**Output:**

```json
{
  "ok": true,
  "team": {
    "id": "T123",
    "name": "My Company",
    "domain": "mycompany",
    "email_domain": "mycompany.com"
  }
}
```

</details>


<details>
<summary><code>get_user_presence</code> — Get user presence status</summary>

Returns the current presence status (active or away) of a workspace user.

**Inputs:**
```
- `user` (string, required) — Slack user ID (e.g., U123ABC456)
```

**Output:**

```json
{
  "ok": true,
  "presence": "active",
  "online": true,
  "auto_away": false
}
```

</details>


<details>
<summary><code>health_check</code> — Check server readiness</summary>

Verifies the server is operational. No authentication required.

**Inputs:**
```
None
```

**Output:**

```json
{
  "status": "ok",
  "server": "CL Slack MCP Server"
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Channel IDs vs Names</strong></summary>

Most tools accept either a channel ID or a channel name:

```
Channel ID:   C123ABC456   (preferred — stable even if channel is renamed)
Channel name: #general     (convenient but can break if channel is renamed)
```

Use `list_channels` or `map_channels` to look up channel IDs.

</details>

<details>
<summary><strong>Message Timestamps (ts)</strong></summary>

Slack uses Unix timestamps with microseconds as unique message identifiers:

```
Format:  1234567890.123456
Example: 1712345678.000200
```

The `ts` field from any message response can be used to reply, update, delete, or identify a message. The `thread_ts` is the `ts` of the first message in a thread.

</details>

<details>
<summary><strong>Pagination</strong></summary>

List tools that return large result sets support cursor-based pagination:

- `cursor` — Pass the `next_cursor` value from `response_metadata` in the previous response
- `limit` — Number of results per page (max: 100)

Omit `cursor` to start from the beginning.

</details>

<details>
<summary><strong>Block Kit (Rich Formatting)</strong></summary>

The `blocks` parameter accepts Slack Block Kit JSON for rich message formatting:

```json
[
  {
    "type": "section",
    "text": { "type": "mrkdwn", "text": "*Hello!* This is bold." }
  }
]
```

Full Block Kit reference: [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check your Slack OAuth credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Slack credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Slack workspace via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check that `blocks` is a valid Slack Block Kit JSON array

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Slack API Error</strong></summary>

- **Cause:** Upstream Slack API returned an error
- **Solution:**
  1. Check Slack service status at [Slack Status](https://status.slack.com)
  2. Verify your OAuth token has the required scopes for the operation (e.g. `chat:write`, `channels:read`)
  3. Review the error message in the response — common errors: `not_in_channel`, `channel_not_found`, `missing_scope`

</details>

---

### Resources

- **[Slack API Documentation](https://api.slack.com/docs)** — Official API reference
- **[Slack Web API Methods](https://api.slack.com/methods)** — Complete method reference
- **[Slack Block Kit Builder](https://app.slack.com/block-kit-builder)** — Visual block builder
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling
