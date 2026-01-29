---
name: gog-cli
description: This skill provides comprehensive instructions for using gogcli (gog), a fast, script-friendly CLI for Google Workspace services including Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat, Classroom, Contacts, Tasks, People, Groups, and Keep. This skill should be used when the user wants to interact with Google services via the command line, including reading/sending email, managing calendar events, working with Google Drive files, managing classroom courses, or any other Google Workspace operations. The skill assumes gog is installed and authorised.
---

# gogcli (gog) CLI

A fast, script-friendly CLI for Google Workspace services with JSON-first output and multi-account support.

**Repository**: https://github.com/steipete/gogcli

## Prerequisites

This skill assumes `gog` is installed and authorised. If commands fail with authentication errors, inform the user they need to:
1. **Install gog**: `brew install steipete/tap/gogcli`
2. **Store OAuth credentials**: `gog auth credentials <path-to-credentials.json>`
3. **Add account**: `gog auth add user@gmail.com --services all`

Do not attempt to resolve authentication issues automatically. Provide the user with the relevant command and let them handle it.

## Supported Services

Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat (Workspace), Classroom, Contacts, Tasks, People, Groups (Workspace), Keep (Workspace, service account only).

## Quick Reference

### Global Flags

```bash
--account <email>    # Select account
--client <name>      # Select OAuth client
--json               # JSON output
--plain              # TSV output (for scripting)
--force              # Skip confirmations
--no-input           # Fail instead of prompting
```

### Common Patterns

```bash
gog --account work@example.com gmail search "is:unread"  # Use specific account
gog gmail search "is:unread" --json | jq '.threads[].id' # JSON for parsing
gog gmail search "is:unread" --plain | cut -f1           # Plain for shell
gog gmail search "is:unread" --max 10 --page <token>     # Pagination
```

## Gmail

### Search and Read

```bash
gog gmail search "is:unread from:boss@example.com newer_than:7d"
gog gmail messages search "is:unread" --include-body
gog gmail thread get <threadId>
gog gmail get <messageId> --format full
```

### Send Email

```bash
# Basic send
gog gmail send --to user@example.com --subject "Hello" --body "Message"

# With HTML and attachments
gog gmail send --to user@example.com --subject "Report" \
  --body-html "<h1>Report</h1>" --attach ~/report.pdf

# Reply
gog gmail send --to user@example.com --subject "Re: Original" \
  --body "Reply" --reply-to-message-id <messageId>
```

### Labels

```bash
gog gmail labels list
gog gmail labels create "Project/Subproject"
gog gmail thread modify <threadId> --add "Label" --remove INBOX
```

For full Gmail reference including drafts, filters, vacation, delegates, tracking, and watch, see `references/gmail.md`.

## Calendar

### Events

```bash
gog calendar events primary --from "2024-12-01" --to "2024-12-31" --weekday
gog calendar events primary --query "meeting"

# Create event
gog calendar create primary --summary "Meeting" \
  --from "2024-12-20T14:00:00" --to "2024-12-20T15:00:00"

# With attendees and recurrence
gog calendar create primary --summary "Weekly Standup" \
  --from "2024-12-20T09:00:00" --to "2024-12-20T09:30:00" \
  --attendees "alice@example.com,bob@example.com" \
  --rrule "FREQ=WEEKLY;BYDAY=MO,WE,FR"

# Respond
gog calendar respond primary <eventId> --status accepted
```

### Special Event Types

```bash
gog calendar focus-time create primary --from DT --to DT --auto-decline
gog calendar ooo create primary --from DT --to DT --decline-message "Away"
gog calendar working-location create primary --from DT --to DT --location home
```

For full Calendar reference, see `references/calendar.md`.

## Drive, Docs, Sheets, Slides

### Drive

```bash
gog drive ls --parent <folderId>
gog drive search "quarterly report"
gog drive download <fileId> --out ~/Downloads/
gog drive upload ~/report.pdf --parent <folderId>
gog drive mkdir "New Folder" --parent <folderId>
gog drive share <fileId> --email user@example.com --role writer
```

### Sheets

```bash
gog sheets read <spreadsheetId> "Sheet1!A1:D10"
gog sheets write <spreadsheetId> "Sheet1!A1:B2" --values '[["Name","Age"],["Alice",30]]'
gog sheets append <spreadsheetId> "Sheet1!A:B" --values '[["Bob",25]]'
gog sheets format <spreadsheetId> "Sheet1!A1:D1" --bold --bg-color "#FFCC00"
```

### Export

```bash
gog docs export <documentId> --format pdf --out ~/doc.pdf
gog slides export <presentationId> --format pptx --out ~/slides.pptx
```

For full Drive/Docs/Sheets/Slides reference, see `references/drive-docs.md`.

## Tasks

```bash
gog tasks lists
gog tasks list <tasklistId>
gog tasks add <tasklistId> --title "Buy groceries" --due "2024-12-20"
gog tasks add <tasklistId> --title "Weekly review" --due "2024-12-20" --repeat weekly
gog tasks done <tasklistId> <taskId>
```

## Contacts

```bash
gog contacts search "john"
gog contacts create --given "John" --family "Doe" --email "john@example.com"
gog contacts directory search "smith"  # Workspace
```

## Classroom

```bash
gog classroom courses --state ACTIVE
gog classroom students <courseId>
gog classroom coursework create <courseId> --title "Homework" --type ASSIGNMENT --due "2024-12-31T23:59:59Z"
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 95
```

For Classroom, Chat, Contacts, Tasks, People, Groups, Keep, see `references/other-services.md`.

## Configuration

### Config Locations

- **macOS**: `~/Library/Application Support/gogcli/config.json`
- **Linux**: `~/.config/gogcli/config.json`
- **Windows**: `%AppData%\gogcli\config.json`

### Settings

```bash
gog config set default_timezone America/New_York
gog config set default_account user@gmail.com
gog config list
```

### Environment Variables

```bash
GOG_ACCOUNT=user@gmail.com      # Default account
GOG_CLIENT=work                 # OAuth client
GOG_JSON=1                      # Default JSON output
GOG_PLAIN=1                     # Default plain output
GOG_TIMEZONE=America/New_York   # Display timezone
GOG_ENABLE_COMMANDS=calendar,tasks  # Command allowlist
```

For full configuration, see `references/configuration.md`.

## Multi-Account Usage

```bash
gog --account work@example.com gmail search "is:unread"
gog auth alias set work work@example.com
gog --account work gmail search "is:unread"
gog auth list --check
```

For authentication including service accounts, see `references/authentication.md`.

## Scripting

```bash
# JSON processing
gog gmail search "is:unread" --json | jq -r '.threads[].id'

# Batch operations
gog gmail search "older_than:30d" --json | \
  jq -r '.threads[].id' | \
  xargs -I {} gog gmail thread modify {} --add Archive --remove INBOX

# Non-interactive
gog gmail send --to user@example.com --subject "Test" --body "Hi" --force
```

## Troubleshooting

If commands fail, inform the user of the likely cause:

| Error | Cause | Solution |
|-------|-------|----------|
| `no credentials` | OAuth not configured | `gog auth credentials <file>` |
| `token expired` | Auth invalid | `gog auth add <email> --force-consent` |
| `insufficient scope` | Missing permissions | `gog auth add <email> --services <services>` |
| `command not found` | Not installed | `brew install steipete/tap/gogcli` |

Status checks:
```bash
gog auth list --check
gog auth status
```

## Reference Files

- `references/command-reference.md` - Complete command specification
- `references/authentication.md` - Auth, credentials, multi-account
- `references/configuration.md` - Config and environment variables
- `references/gmail.md` - Gmail operations
- `references/calendar.md` - Calendar operations
- `references/drive-docs.md` - Drive, Docs, Sheets, Slides
- `references/other-services.md` - Classroom, Chat, Contacts, Tasks, People, Groups, Keep
