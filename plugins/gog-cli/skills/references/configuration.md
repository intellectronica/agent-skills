# gogcli Configuration Reference

## Config files

Configuration is JSON5 in the platform config directory:

| Platform | Path |
| --- | --- |
| macOS | `~/Library/Application Support/gogcli/config.json` |
| Linux | `~/.config/gogcli/config.json` |
| Windows | `%AppData%\gogcli\config.json` |

```bash
gog config path
gog config list
gog config keys
gog config get default_timezone
gog config set default_timezone Europe/Zurich
gog config unset default_timezone
```

## Common config keys

```bash
gog config set default_account you@example.com
gog config set default_timezone Europe/Zurich
gog auth keyring file
```

Useful structured config:

```json5
{
  keyring_backend: "auto",
  default_timezone: "Europe/Zurich",
  default_account: "you@example.com",
  account_clients: {
    "you@company.com": "work",
  },
  client_domains: {
    "company.com": "work",
  },
}
```

Prefer `gog auth alias ...` and `gog --client ... auth credentials set --domain ...` over hand-editing aliases/client mappings.

## Environment variables

Account/auth:

```bash
export GOG_ACCOUNT=you@example.com
export GOG_CLIENT=work
export GOG_ACCESS_TOKEN="$(gcloud auth print-access-token)"
export GOG_AUTH_MODE=adc
```

Output:

```bash
export GOG_JSON=1
export GOG_PLAIN=1
export GOG_COLOR=never
export NO_COLOR=1
```

Time and calendar:

```bash
export GOG_TIMEZONE=Europe/Zurich
export GOG_CALENDAR_WEEKDAY=1
```

Keyring:

```bash
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD='...'
export GOG_KEYRING_SERVICE_NAME=gogcli
```

Agent safety:

```bash
export GOG_ENABLE_COMMANDS=calendar.events,calendar.freebusy,tasks
export GOG_DISABLE_COMMANDS=gmail.send,gmail.drafts.send,drive.share
export GOG_GMAIL_NO_SEND=1
```

## Output modes

Default text output is for humans. For agents and scripts, use JSON first:

```bash
gog --json gmail search 'is:unread' | jq '.threads'
gog --json --results-only drive search "budget" | jq .
gog --json --select id,name,mimeType drive ls
```

Use TSV when shell tools are enough:

```bash
gog --plain gmail search 'is:unread' | cut -f1
```

Errors, hints, and progress are intended for stderr so stdout remains parseable.

## Pagination and empty results

List commands commonly support `--max`, `--page`, and sometimes `--all-pages` or `--all`.

```bash
gog --json gmail search 'newer_than:7d' --max 10 | jq -r '.nextPageToken'
gog --json calendar events primary --today --all-pages
gog --json calendar events primary --query "unlikely query" --fail-empty
```

`--fail-empty` exits with a stable non-zero code when no results are found on commands that support it.

## Dates and times

Agent guidance:

- Generate RFC3339 datetimes with explicit timezone offsets for event-like fields.
- Use `YYYY-MM-DD` only for date-only fields.
- Calendar ranges also accept relative values such as `today`, `tomorrow`, `yesterday`, `monday`, and `next friday`.

Examples:

```bash
gog calendar events primary --from "2026-04-25T00:00:00+02:00" --to "2026-04-26T00:00:00+02:00"
gog calendar events primary --today
gog tasks add <tasklistId> --title "Renew" --due "2026-05-01"
```

## Safety controls

For read-only or constrained automation:

```bash
GOG_ENABLE_COMMANDS=calendar.events,calendar.freebusy,drive.search \
  gog --no-input --json calendar events primary --today

GOG_DISABLE_COMMANDS=gmail.send,gmail.forward,drive.share \
  gog --no-input --json drive search "report"

gog --gmail-no-send gmail send --to user@example.com --subject "Test" --body "Blocked"
```

Per-account send guard:

```bash
gog config no-send set you@example.com
gog config no-send list
gog config no-send remove you@example.com
```

Stable exit-code help:

```bash
gog agent exit-codes
gog exit-codes
```

## Discovering current syntax

```bash
gog --help
GOG_HELP=full gog --help
gog <service> --help
gog <service> <command> --help
gog schema --json | jq .
```

The generated local reference is `references/command-reference.md`.
