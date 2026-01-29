# Gmail Operations Reference

Comprehensive guide to Gmail operations with `gog`.

## Search Syntax

Gmail search uses standard Gmail search operators:

| Operator | Description | Example |
|----------|-------------|---------|
| `from:` | Sender | `from:user@example.com` |
| `to:` | Recipient | `to:me` |
| `subject:` | Subject line | `subject:meeting` |
| `is:unread` | Unread messages | `is:unread` |
| `is:starred` | Starred messages | `is:starred` |
| `is:important` | Important messages | `is:important` |
| `has:attachment` | Has attachments | `has:attachment` |
| `label:` | Label name | `label:work` |
| `in:` | Location | `in:inbox`, `in:sent`, `in:trash` |
| `after:` | Date filter | `after:2024/01/01` |
| `before:` | Date filter | `before:2024/12/31` |
| `newer_than:` | Relative date | `newer_than:7d` |
| `older_than:` | Relative date | `older_than:1m` |
| `larger:` | Size filter | `larger:5M` |
| `smaller:` | Size filter | `smaller:1M` |
| `filename:` | Attachment name | `filename:report.pdf` |

### Combining Operators

```bash
# Unread from specific sender in last week
gog gmail search "is:unread from:boss@example.com newer_than:7d"

# Large attachments from anyone
gog gmail search "has:attachment larger:10M"

# Exclude certain labels
gog gmail search "is:unread -label:newsletters"
```

---

## Searching and Retrieving

### Search Threads

```bash
# Basic search
gog gmail search "is:unread"

# Limit results
gog gmail search "is:unread" --max 10

# Get next page
gog gmail search "is:unread" --page <token>

# JSON output for scripting
gog gmail search "is:unread" --json
```

### Search Messages

```bash
# Search individual messages
gog gmail messages search "from:user@example.com"

# Include message body
gog gmail messages search "is:unread" --include-body
```

### Get Thread

```bash
# Get full thread
gog gmail thread get <threadId>

# Download attachments
gog gmail thread get <threadId> --download
```

### Get Message

```bash
# Get message (default format)
gog gmail get <messageId>

# Specific format
gog gmail get <messageId> --format full
gog gmail get <messageId> --format metadata
gog gmail get <messageId> --format raw

# Get specific headers
gog gmail get <messageId> --headers Subject,From,Date
```

### Get Attachments

```bash
# Download attachment
gog gmail attachment <messageId> <attachmentId>

# Specify output path
gog gmail attachment <messageId> <attachmentId> --out ~/Downloads/

# Specify filename
gog gmail attachment <messageId> <attachmentId> --name report.pdf
```

### Get URLs

```bash
# Get Gmail web URLs
gog gmail url <threadId1> <threadId2>
```

---

## Sending Email

### Basic Send

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Hello" \
  --body "Plain text message"
```

### HTML Body

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Hello" \
  --body-html "<h1>Hello</h1><p>HTML message</p>"
```

### Multiple Recipients

```bash
gog gmail send \
  --to user1@example.com \
  --to user2@example.com \
  --cc manager@example.com \
  --bcc archive@example.com \
  --subject "Team Update"
  --body "Message to multiple recipients"
```

### Attachments

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Report" \
  --body "Please see attached" \
  --attach ~/Documents/report.pdf \
  --attach ~/Documents/data.xlsx
```

### Reply to Message

```bash
gog gmail send \
  --to recipient@example.com \
  --subject "Re: Original Subject" \
  --body "Reply content" \
  --reply-to-message-id <originalMessageId>
```

### With Open Tracking

```bash
# Send with tracking (requires setup)
gog gmail send \
  --to recipient@example.com \
  --subject "Tracked Email" \
  --body-html "<p>This email tracks opens</p>" \
  --track

# Track multiple recipients separately
gog gmail send \
  --to user1@example.com \
  --to user2@example.com \
  --subject "Tracked" \
  --body-html "<p>Each recipient tracked separately</p>" \
  --track-split
```

---

## Labels

### List Labels

```bash
gog gmail labels list
gog gmail labels list --json
```

### Get Label

```bash
gog gmail labels get INBOX
gog gmail labels get "Label Name"
gog gmail labels get <labelId>
```

### Create Label

```bash
gog gmail labels create "Project/SubLabel"
```

### Modify Thread Labels

```bash
# Add label
gog gmail thread modify <threadId> --add "Label Name"

# Remove label
gog gmail thread modify <threadId> --remove INBOX

# Multiple operations
gog gmail thread modify <threadId> --add Archive --remove INBOX
```

### Batch Label Modification

```bash
gog gmail labels modify <threadId1> <threadId2> --add "Done"
```

---

## Drafts

### List Drafts

```bash
gog gmail drafts list
gog gmail drafts list --max 10
```

### Create Draft

```bash
gog gmail drafts create \
  --to recipient@example.com \
  --subject "Draft Subject" \
  --body "Draft content"
```

### Update Draft

```bash
gog gmail drafts update <draftId> \
  --subject "Updated Subject" \
  --body "Updated content"
```

### Send Draft

```bash
gog gmail drafts send <draftId>
```

### Delete Draft

```bash
gog gmail drafts delete <draftId>
```

---

## Settings

### Autoforward

```bash
gog gmail autoforward status
gog gmail autoforward enable forward@example.com
gog gmail autoforward disable
```

### Delegates

```bash
gog gmail delegates list
gog gmail delegates add assistant@example.com
gog gmail delegates remove assistant@example.com
```

### Filters

```bash
# List filters
gog gmail filters list

# Get filter
gog gmail filters get <filterId>

# Delete filter
gog gmail filters delete <filterId>
```

### Vacation Responder

```bash
# Check status
gog gmail vacation status

# Enable
gog gmail vacation enable \
  --subject "Out of Office" \
  --body "I am currently away..." \
  --from "2024-12-20T00:00:00Z" \
  --to "2024-12-27T00:00:00Z"

# Disable
gog gmail vacation disable
```

### Send-As Addresses

```bash
gog gmail sendas list
gog gmail sendas get alias@example.com
```

---

## Email Tracking

### Setup Tracking

```bash
# Configure tracking worker URL
gog gmail track setup --worker-url https://your-worker.workers.dev
```

### Check Status

```bash
gog gmail track status
```

### View Opens

```bash
# By tracking ID
gog gmail track opens --id <trackingId>

# By recipient
gog gmail track opens --recipient user@example.com
```

---

## Watch (Pub/Sub Notifications)

### Start Watching

```bash
# Watch all labels
gog gmail watch start --topic projects/my-project/topics/gmail-notifications

# Watch specific labels
gog gmail watch start \
  --topic projects/my-project/topics/gmail-notifications \
  --label INBOX \
  --label "Important"
```

### Check Status

```bash
gog gmail watch status
```

### Renew Watch

```bash
gog gmail watch renew
```

### Stop Watching

```bash
gog gmail watch stop
```

### Run Handler Server

```bash
gog gmail watch serve \
  --bind 0.0.0.0 \
  --port 8080 \
  --path /webhook

# Include message body in notifications
gog gmail watch serve \
  --bind 0.0.0.0 \
  --port 8080 \
  --path /webhook \
  --include-body \
  --max-bytes 20000
```

### Get History

```bash
gog gmail history --since <historyId>
```
