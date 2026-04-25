---
name: gog-cli
description: Use this skill whenever the user wants to operate Google Workspace from the command line with gog/gogcli, including Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Apps Script, Chat, Classroom, Contacts, Tasks, People, Groups, Admin, Keep, auth, configuration, scripting, or agent-safe Google automation. Prefer this skill for Google account/file/mail/calendar work when the user mentions gog, gogcli, Google CLI, Gmail search/send, Calendar events, Drive files, Docs/Sheets/Slides editing, Forms, Apps Script, Workspace admin, or command-line Google automation.
---

# gogcli (gog)

`gog` is a fast, script-friendly CLI for Google services. It is JSON-first, supports multiple accounts/OAuth clients, and has explicit guardrails for agent and CI usage.

Authoritative upstream: https://github.com/steipete/gogcli

This skill was refreshed against upstream `gog` v0.13.0 (2026-04-20). When exact syntax matters, run `gog <command> --help` or `gog schema --json`; the command surface moves quickly, rather inconveniently for anyone fond of stale notes.

## Operating rules

- Prefer `gog --json ... | jq ...` for inspection and scripting.
- Use `--plain` only when stable TSV is more convenient than JSON.
- Use `--dry-run` for supported mutating operations when preparing a change or when user intent is ambiguous.
- Use `--no-input` in automation so commands fail instead of prompting.
- Use `--force` only when the user asked for the destructive/public/send/admin operation or after you have clearly explained the effect.
- Do not repair OAuth, consent, keyring, or Workspace delegation problems silently. Show the exact command the user should run.
- Do not export tokens, print secrets, open public shares, add delegates/forwarding, send mail, suspend users, or permanently delete data unless the user explicitly requested that action.
- For agent runs that must not send mail, add `--gmail-no-send`, set `GOG_GMAIL_NO_SEND=1`, or configure `gog config no-send set <account>`.

## Install and auth

```bash
brew install gogcli
gog auth credentials set ~/Downloads/client_secret_....json
gog auth add you@example.com --services gmail,calendar,drive
gog auth list --check
```

Notes:

- Homebrew now uses `brew install gogcli`; old tap examples are obsolete.
- `gog auth add` defaults to `--services user`. Request the services needed for the task.
- `--services all` is accepted only as a backwards-compatible alias for `user`; do not use it when you need every API.
- Use `--readonly`, `--drive-scope readonly|file|full`, and `--gmail-scope readonly|full` for least privilege.
- Keep and Admin require Workspace service-account/domain-wide delegation. Google Chat, Groups, directory, and Classroom also have Workspace restrictions.
- For headless/CI, consider `--manual`, `--remote`, `--access-token`, or `GOG_AUTH_MODE=adc`.

Read `references/authentication.md` for full auth patterns.

## Global flags

```bash
--account, -a <email|alias|auto>   # account selection
--client <name>                    # named OAuth client/token bucket
--access-token <token>             # direct short-lived token; also GOG_ACCESS_TOKEN
--json, -j                         # machine-readable JSON
--plain, -p                        # stable TSV
--results-only                     # JSON primary result only
--select <fields>                  # best-effort JSON projection
--dry-run, -n                      # preview supported writes
--force, -y                        # skip confirmations
--no-input                         # never prompt
--enable-commands <csv>            # allowlist top-level or dotted commands
--disable-commands <csv>           # denylist top-level or dotted commands
--gmail-no-send                    # block Gmail send operations
--verbose, -v                      # debug logging
```

Useful command aliases:

```bash
gog send ...             # alias for gog gmail send
gog ls                   # alias for gog drive ls
gog search "budget"      # alias for gog drive search
gog download <fileId>    # alias for gog drive download
gog upload ./file.pdf    # alias for gog drive upload
gog me                   # alias for gog people me
gog status               # alias for gog auth status
gog open <id-or-url>     # best-effort Google web URL, offline
```

## High-value workflows

### Account selection

```bash
gog auth alias set work you@company.com
gog --account work gmail search 'is:unread newer_than:2d'
GOG_ACCOUNT=work gog calendar events primary --today
gog --client work auth credentials set ~/Downloads/work-client.json
gog --client work auth add you@company.com --services gmail,calendar
```

### Gmail

```bash
gog --json gmail search 'is:unread newer_than:7d' | jq -r '.threads[].id'
gog gmail messages search 'from:alice@example.com has:attachment' --include-body
gog gmail messages search 'subject:report newer_than:30d' --full
gog gmail thread get <threadId> --download --out-dir ./attachments
gog gmail labels modify <threadId> --add Project --remove INBOX
gog gmail messages modify <messageId> --add STARRED
gog gmail send --to user@example.com --subject "Hello" --body-file ./body.txt
gog gmail forward <messageId> --to user@example.com --note "FYI"
```

For forwarding, autoreply, watch/Pub/Sub, filters, delegates, send-as, label colours, batch operations, and tracking, read `references/gmail.md`.

### Calendar

```bash
gog calendar calendars
gog calendar events primary --today --weekday
gog calendar events --all --from "2026-04-25T00:00:00+02:00" --to "2026-04-26T00:00:00+02:00"
gog calendar freebusy --cal primary --from "2026-04-25T09:00:00+02:00" --to "2026-04-25T17:00:00+02:00"
gog calendar create primary --summary "Planning" --from "2026-04-25T14:00:00+02:00" --to "2026-04-25T14:30:00+02:00" --attendees "alice@example.com,bob@example.com" --with-meet
gog calendar respond primary <eventId> --status accepted --send-updates all
```

Use RFC3339 with timezone offsets for generated datetimes. Read `references/calendar.md` for aliases, subscriptions, secondary calendars, extended properties, Focus Time, OOO, working locations, team calendars, and conflict detection.

### Drive, Docs, Sheets, Slides, Forms, Apps Script

```bash
gog drive search "invoice filetype:pdf" --max 20
gog drive upload ./report.md --convert-to doc --parent <folderId>
gog drive upload ./deck.pdf --replace <fileId> --name "Board Deck.pdf"
gog drive share <fileId> --to user --email editor@example.com --role commenter
gog docs write <docId> --file ./brief.md --replace --markdown
gog docs sed <docId> 's/status/{b c=green}approved/g' --dry-run
gog sheets update <spreadsheetId> 'Sheet1!A1' '[["Name","Score"],["Ada",98]]'
gog sheets chart list <spreadsheetId>
gog slides thumbnail <presentationId> <slideId> --out ./slide.png
gog forms responses list <formId> --max 20
gog appscript run <scriptId> myFunction --params '["arg1", 123]'
```

Read `references/drive-docs.md` for current file/content commands. For Docs sed formatting, read `references/sedmat.md`.

### Other services

```bash
gog contacts search "Ada"
gog tasks lists
gog tasks add <tasklistId> --title "Weekly review" --due "2026-04-27" --repeat weekly
gog chat messages send spaces/<spaceId> --text "Build complete"
gog groups members engineering@example.com
gog admin users list --domain example.com
gog keep search "receipt"
```

Read `references/other-services.md` for Chat, Classroom, Contacts, Tasks, People, Groups, Admin, Keep, and time utilities.

## Scripting patterns

```bash
# Inspect shape first
gog --json gmail search 'is:unread' --max 3 | jq .

# Use pagination/all-pages where available
gog --json calendar events primary --from today --to tomorrow --all-pages

# Fail cleanly when a supported list command has no results
gog --json calendar events primary --query "unlikely query" --fail-empty

# Batch with xargs after checking output
gog --json gmail search 'older_than:1y label:newsletter' --max 200 | \
  jq -r '.threads[].id' | \
  xargs -n 50 gog gmail labels modify --remove INBOX

# Agent-safe command surface
GOG_ENABLE_COMMANDS=calendar.events,calendar.freebusy,tasks \
  gog --no-input --json calendar events primary --today
```

## Reference map

- `references/command-reference.md` - generated command index from `gog schema --json`
- `references/authentication.md` - OAuth clients, service accounts, scopes, keyrings, headless auth
- `references/configuration.md` - config keys, environment variables, output modes, safety switches
- `references/gmail.md` - Gmail search, read, send, labels, settings, watch, tracking, autoreply
- `references/calendar.md` - Calendar listing, event writes, scheduling, special events, aliases
- `references/drive-docs.md` - Drive, Docs, Sheets, Slides, Forms, Apps Script
- `references/sedmat.md` - Docs sed/formatting DSL
- `references/other-services.md` - Chat, Classroom, Contacts, Tasks, People, Groups, Admin, Keep
