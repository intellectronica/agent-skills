# Gmail Operations Reference

Use this for Gmail search, reading, organization, sending, forwarding, autoreply, settings, watches, tracking, and batch mail workflows.

## Search syntax

Gmail queries use normal Gmail search operators:

| Operator | Example |
| --- | --- |
| sender/recipient | `from:alice@example.com`, `to:me` |
| subject/body | `subject:invoice`, `"exact phrase"` |
| state | `is:unread`, `is:starred`, `is:important` |
| labels/location | `label:Project`, `in:inbox`, `in:sent`, `in:trash` |
| attachments | `has:attachment`, `filename:pdf` |
| dates | `after:2026/04/01`, `before:2026/05/01`, `newer_than:7d`, `older_than:1m` |
| size | `larger:10M`, `smaller:1M` |
| exclusion | `-label:newsletters`, `-from:noreply@example.com` |

## Reading mail

Thread search:

```bash
gog gmail search 'is:unread newer_than:7d'
gog --json gmail search 'from:boss@example.com has:attachment' --max 20
gog --json gmail search 'older_than:1y' --max 200 | jq -r '.threads[].id'
```

Message search:

```bash
gog gmail messages search 'from:alice@example.com'
gog gmail messages search 'is:unread' --include-body
gog gmail messages search 'subject:report newer_than:30d' --full
```

Retrieve:

```bash
gog gmail thread get <threadId>
gog gmail thread get <threadId> --full
gog gmail thread get <threadId> --download --out-dir ./attachments
gog gmail get <messageId> --format full
gog gmail get <messageId> --format metadata --headers Subject,From,Date
gog gmail get <messageId> --format raw
gog gmail url <threadId1> <threadId2>
```

Attachments:

```bash
gog gmail thread attachments <threadId>
gog gmail attachment <messageId> <attachmentId> --out ./attachments/
gog gmail attachment <messageId> <attachmentId> --name report.pdf
```

History:

```bash
gog gmail history --since <historyId>
```

## Sending and drafts

Before sending from an agent, verify the user asked to actually send. Use `--dry-run` where possible or configure no-send guards when preparing content.

```bash
gog gmail send --to recipient@example.com --subject "Hello" --body "Plain text"
gog gmail send --to recipient@example.com --subject "Report" --body-file ./body.txt --attach ./report.pdf
gog gmail send --to user@example.com --subject "HTML" --body-html '<p>Hello</p>'
gog gmail send --to user@example.com --subject "Alias" --from alias@example.com --body-file ./body.txt
```

Replies:

```bash
gog gmail send --reply-to-message-id <messageId> --reply-all --subject "Re: Topic" --body-file ./reply.txt
gog gmail send --thread-id <threadId> --reply-all --quote --subject "Re: Topic" --body-file ./reply.txt
```

Forwarding:

```bash
gog gmail forward <messageId> --to user@example.com
gog gmail forward <messageId> --to user@example.com --note "FYI" --from alias@example.com
```

Drafts:

```bash
gog gmail drafts list --max 10
gog gmail drafts get <draftId> --download
gog gmail drafts create --to user@example.com --subject "Draft" --body-file ./draft.txt
gog gmail drafts update <draftId> --subject "Updated" --body-file ./draft.txt
gog gmail drafts send <draftId>
gog gmail drafts delete <draftId>
```

Tracking:

```bash
gog gmail track setup --worker-url https://your-worker.workers.dev
gog gmail send --to user@example.com --subject "Tracked" --body-html '<p>Hello</p>' --track
gog gmail send --to a@example.com --to b@example.com --subject "Tracked" --body-html '<p>Hello</p>' --track-split
gog gmail track status
gog gmail track opens <trackingId>
gog gmail track opens --recipient user@example.com
```

## Labels and organization

Labels:

```bash
gog gmail labels list
gog gmail labels get INBOX
gog gmail labels create "Project/Subproject"
gog gmail labels rename "Old Label" "New Label"
gog gmail labels style "Project" --text-color "#ffffff" --background-color "#16a34a"
gog gmail labels style "Project" --label-list-visibility labelShow --message-list-visibility show
gog gmail labels delete "Project/Old"
```

Thread/message label changes:

```bash
gog gmail thread modify <threadId> --add Project --remove INBOX
gog gmail labels modify <threadId1> <threadId2> --add Done --remove UNREAD
gog gmail messages modify <messageId> --add STARRED
gog gmail batch modify <messageId1> <messageId2> --remove UNREAD
```

Convenience actions:

```bash
gog gmail archive <messageId1> <messageId2>
gog gmail mark-read <messageId>
gog gmail unread <messageId>
gog gmail trash <messageId>
gog gmail batch delete <messageId1> <messageId2>
```

Use care: `batch delete` permanently deletes messages.

Batch patterns:

```bash
gog --json gmail search 'from:noreply@example.com' --max 200 | \
  jq -r '.threads[].id' | \
  xargs -n 50 gog gmail labels modify --remove INBOX

gog --json gmail messages search 'older_than:90d label:updates' --max 500 | \
  jq -r '.messages[].id' | \
  xargs -n 50 gog gmail batch modify --add UpdatesArchive --remove INBOX
```

## Autoreply

`gog gmail autoreply` is a one-shot command intended for cron/launchd or agent workflows. It replies once to matching messages, then labels them for dedupe.

```bash
gog gmail autoreply \
  'to:support@example.com in:inbox -label:AutoReplied' \
  --body-file ./support-autoreply.txt \
  --label AutoReplied \
  --archive \
  --mark-read
```

Useful flags:

```bash
--max 20
--subject "Re: ..."
--body / --body-file / --body-html
--from alias@example.com
--reply-to support@example.com
--label AutoReplied
--archive
--mark-read
--skip-bulk
--allow-self
```

It adds `Auto-Submitted: auto-replied` and skips common bulk/list/auto-generated mail by default.

## Gmail settings

Most settings commands work both as `gog gmail <group> ...` and `gog gmail settings <group> ...`.

Filters:

```bash
gog gmail filters list
gog gmail filters get <filterId>
gog gmail filters create --from newsletters@example.com --add-label Newsletters --remove-label INBOX
gog gmail filters export --out filters.json
gog gmail filters delete <filterId>
```

Forwarding and auto-forward:

```bash
gog gmail forwarding list
gog gmail forwarding create forward@example.com
gog gmail forwarding delete forward@example.com
gog gmail autoforward get
gog gmail autoforward update --enabled --email forward@example.com --disposition archive
```

Delegates:

```bash
gog gmail delegates list
gog gmail delegates get assistant@example.com
gog gmail delegates add assistant@example.com
gog gmail delegates remove assistant@example.com
```

Send-as aliases:

```bash
gog gmail sendas list
gog gmail sendas get alias@example.com
gog gmail sendas create alias@example.com --display-name "Ada Example"
gog gmail sendas verify alias@example.com
gog gmail sendas update alias@example.com --reply-to support@example.com
gog gmail sendas delete alias@example.com
```

Vacation responder:

```bash
gog gmail vacation get
gog gmail vacation update --enabled --subject "Out of office" --body "Back Monday"
gog gmail vacation update --disabled
```

Settings that create forwarding, delegates, or public-ish automation may prompt or require `--force` in non-interactive contexts. Explain the effect first.

## Pub/Sub watch

```bash
gog gmail watch start --topic projects/my-project/topics/gmail-notifications
gog gmail watch start --topic projects/my-project/topics/gmail-notifications --label INBOX --label IMPORTANT
gog gmail watch status
gog gmail watch renew
gog gmail watch stop
```

Handler:

```bash
gog gmail watch serve --bind 0.0.0.0 --port 8080 --path /webhook
gog gmail watch serve --bind 0.0.0.0 --port 8080 --path /webhook --include-body --max-bytes 20000
```

Recent versions also support history-type filtering on watch serve. Check `gog gmail watch serve --help` before relying on exact flags.

## Auth/scopes

Readonly mail:

```bash
gog auth add you@example.com --services gmail --gmail-scope readonly
```

Full Gmail automation/settings:

```bash
gog auth add you@example.com --services gmail --gmail-scope full --force-consent
```

Settings commands need Gmail settings scopes. If a settings/filter/delegate command fails with insufficient scopes, re-auth with `--services gmail --force-consent`.

