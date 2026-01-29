# gogcli Configuration Reference

Complete guide to configuration options and environment variables.

## Configuration File

Configuration is stored as JSON5 in platform-specific directories:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/gogcli/config.json` |
| Linux | `~/.config/gogcli/config.json` |
| Windows | `%AppData%\gogcli\config.json` |

### Viewing Configuration

```bash
# Show config directory path
gog config path

# List all config values
gog config list

# Get specific value
gog config get default_timezone

# List all available keys
gog config keys
```

### Setting Configuration

```bash
# Set value
gog config set default_timezone America/New_York

# Remove value
gog config unset default_timezone
```

---

## Configuration Keys

### `keyring_backend`

Force specific credential storage backend.

```bash
gog config set keyring_backend keychain  # macOS Keychain
gog config set keyring_backend file      # Encrypted file
gog config set keyring_backend auto      # Auto-detect (default)
```

### `default_timezone`

Default timezone for time display (IANA format).

```bash
gog config set default_timezone America/New_York
gog config set default_timezone Europe/London
gog config set default_timezone UTC
```

### `default_account`

Default account when `--account` not specified.

```bash
gog config set default_account user@gmail.com
```

### `account_aliases`

Map short names to email addresses. Set via `gog auth alias` commands.

### `account_clients`

Map specific accounts to OAuth clients.

```json5
{
  "account_clients": {
    "work@example.com": "work",
    "personal@gmail.com": "personal"
  }
}
```

### `client_domains`

Map email domains to OAuth clients (auto-selection).

```json5
{
  "client_domains": {
    "example.com": "work",
    "company.org": "enterprise"
  }
}
```

---

## Environment Variables

Environment variables override configuration file values.

### Account Selection

```bash
# Default account
export GOG_ACCOUNT=user@gmail.com

# OAuth client selection
export GOG_CLIENT=work
```

### Output Format

```bash
# Default to JSON output
export GOG_JSON=1

# Default to plain/TSV output
export GOG_PLAIN=1

# Control colour output
export GOG_COLOR=auto    # Auto-detect (default)
export GOG_COLOR=always  # Force colours
export GOG_COLOR=never   # Disable colours

# Disable colours (standard)
export NO_COLOR=1
```

### Time Settings

```bash
# Default timezone
export GOG_TIMEZONE=America/New_York

# Always show weekday in calendar output
export GOG_CALENDAR_WEEKDAY=1
```

### Keyring Settings

```bash
# Force keyring backend
export GOG_KEYRING_BACKEND=file

# Encryption password for file backend
export GOG_KEYRING_PASSWORD=your-secure-password
```

### Command Allowlist

Restrict available commands (useful for sandboxed/agent execution):

```bash
# Allow only calendar and tasks commands
export GOG_ENABLE_COMMANDS=calendar,tasks

# Allow Gmail read-only operations
export GOG_ENABLE_COMMANDS=gmail
```

---

## Output Formats

All commands support three output modes:

### Human-Friendly (Default)

Coloured tables optimised for terminal display.

```bash
gog gmail search "is:unread"
```

### JSON

Machine-readable format for scripting and parsing.

```bash
gog gmail search "is:unread" --json

# Or via environment
GOG_JSON=1 gog gmail search "is:unread"
```

### Plain/TSV

Tab-separated values for piping to other tools.

```bash
gog gmail search "is:unread" --plain

# Or via environment
GOG_PLAIN=1 gog gmail search "is:unread"
```

---

## Pagination

List commands support pagination:

```bash
# Limit results
gog gmail search "is:unread" --max 10

# Get next page
gog gmail search "is:unread" --page <nextPageToken>
```

JSON output includes pagination token:

```bash
gog gmail search "is:unread" --json | jq '.nextPageToken'
```

---

## Scripting Best Practices

### Use JSON Output

```bash
# Parse with jq
gog gmail search "is:unread" --json | jq -r '.threads[].id'
```

### Use Plain Output

```bash
# Simple field extraction
gog gmail search "is:unread" --plain | cut -f1
```

### Batch Operations

```bash
# Process multiple items
gog gmail search "is:unread" --json | \
  jq -r '.threads[].id' | \
  xargs -I {} gog gmail thread modify {} --add LABEL_ID
```

### Error Handling

```bash
# Check exit codes
if gog gmail send --to user@example.com --subject "Test" --body "Hello"; then
  echo "Sent successfully"
else
  echo "Send failed"
fi
```

### Non-Interactive Mode

```bash
# Skip confirmations
gog gmail send --to user@example.com --subject "Test" --body "Hello" --force

# Fail instead of prompting
gog auth add user@gmail.com --no-input
```
