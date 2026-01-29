# gogcli Command Reference

Complete command specification for all `gog` commands.

## Global Flags

All commands support these flags:

| Flag | Description |
|------|-------------|
| `--color=auto\|always\|never` | Control colour output (default: `auto`) |
| `--json` | Output in JSON format |
| `--plain` | Output in TSV format (stable/parseable) |
| `--force` | Skip confirmations |
| `--no-input` | Fail instead of prompting |
| `--version` | Show version |
| `--client <name>` | Select OAuth client |
| `--account <email>` | Select account |

---

## Auth Commands

```bash
# Store OAuth credentials
gog auth credentials <credentials.json|->

# List stored credentials
gog auth credentials list

# Add account with auth flow
gog auth add <email> [options]
  --services user|all|gmail,calendar,etc.
  --readonly
  --drive-scope full|readonly|file
  --manual                              # Browserless flow
  --force-consent                       # Force consent prompt

# Show available services
gog auth services [--markdown]

# Add Google Keep (Workspace only)
gog auth keep <email> --key <service-account.json>

# Service account management
gog auth service-account set <email> --key <service-account.json>
gog auth service-account status

# List authenticated accounts
gog auth list [--check]

# Alias management
gog auth alias list
gog auth alias set <alias> <email>
gog auth alias unset <alias>

# Show auth status
gog auth status

# Remove account
gog auth remove <email>

# Token management
gog auth tokens list
gog auth tokens delete <email>
```

---

## Config Commands

```bash
gog config get <key>              # Retrieve config value
gog config keys                   # List all config keys
gog config list                   # Show all config
gog config path                   # Show config directory
gog config set <key> <value>      # Set config value
gog config unset <key>            # Remove config value
```

---

## Gmail Commands

### Search & Retrieve

```bash
# Search threads
gog gmail search <query> [--max N] [--page TOKEN]

# Search messages
gog gmail messages search <query> [options]
  [--max N] [--page TOKEN] [--include-body]

# Get thread
gog gmail thread get <threadId> [--download]

# Modify thread labels
gog gmail thread modify <threadId> [--add ...] [--remove ...]

# Get message
gog gmail get <messageId> [options]
  [--format full|metadata|raw] [--headers ...]

# Download attachment
gog gmail attachment <messageId> <attachmentId> [--out PATH] [--name NAME]

# Get Gmail URLs
gog gmail url <threadIds...>
```

### Labels

```bash
gog gmail labels list
gog gmail labels get <labelIdOrName>
gog gmail labels create <name>
gog gmail labels modify <threadIds...> [--add ...] [--remove ...]
```

### Send

```bash
gog gmail send [options]
  --to a@b.com --subject S
  [--body B] [--body-html H]
  [--cc ...] [--bcc ...]
  [--reply-to-message-id ...]
  [--reply-to addr]
  [--attach <file>...]
  [--track]                        # Enable open tracking
  [--track-split]                  # Send tracked to multiple recipients
```

### Drafts

```bash
gog gmail drafts list [--max N] [--page TOKEN]
gog gmail drafts get <draftId> [--download]
gog gmail drafts create [--subject S] [--to ...] [options]
gog gmail drafts update <draftId> [--subject S] [options]
gog gmail drafts send <draftId>
gog gmail drafts delete <draftId>
```

### Settings

```bash
# Autoforward
gog gmail autoforward status
gog gmail autoforward enable <email>
gog gmail autoforward disable

# Delegates
gog gmail delegates list
gog gmail delegates add <email>
gog gmail delegates remove <email>

# Filters
gog gmail filters list
gog gmail filters get <filterId>
gog gmail filters create [options]
gog gmail filters delete <filterId>

# Forwarding addresses
gog gmail forwarding list
gog gmail forwarding add <email>
gog gmail forwarding remove <email>

# Vacation responder
gog gmail vacation status
gog gmail vacation enable [--subject S] [--body B] [--from DT] [--to DT]
gog gmail vacation disable

# Send-as addresses
gog gmail sendas list
gog gmail sendas get <email>
```

### Tracking

```bash
gog gmail track setup --worker-url <URL>
gog gmail track status
gog gmail track opens [--id ID] [--recipient EMAIL]
```

### Watch (Pub/Sub)

```bash
gog gmail watch start --topic <gcp-topic> [--label <idOrName>...]
gog gmail watch status
gog gmail watch renew
gog gmail watch stop
gog gmail watch serve --bind <ip> --port <num> --path <path>
  [--include-body] [--max-bytes N]
gog gmail history --since <historyId>
```

---

## Calendar Commands

```bash
# List calendars
gog calendar calendars

# List ACLs
gog calendar acl <calendarId>

# List events
gog calendar events <calendarId> [options]
  [--from RFC3339] [--to RFC3339]
  [--max N] [--page TOKEN]
  [--query Q] [--weekday]

# Get event
gog calendar event <calendarId> <eventId>
gog calendar get <calendarId> <eventId>

# Create event
gog calendar create <calendarId> [options]
  --summary S --from DT --to DT
  [--description D] [--location L]
  [--attendees a@b.com,c@d.com]
  [--all-day]
  [--event-type default|focusTime|outOfOffice|workingLocation]
  [--rrule RRULE]
  [--reminders 10m,1h]

# Update event
gog calendar update <calendarId> <eventId> [options]
  [--summary S] [--from DT] [--to DT]
  [--description D] [--location L]
  [--attendees ...] [--add-attendee ...]
  [--all-day]
  [--event-type TYPE]

# Delete event
gog calendar delete <calendarId> <eventId>

# Check availability
gog calendar freebusy <calendarIds> --from RFC3339 --to RFC3339

# Respond to event
gog calendar respond <calendarId> <eventId> [options]
  --status accepted|declined|tentative
  [--send-updates all|none|externalOnly]

# Propose alternative time
gog calendar propose-time <calendarId> <eventId> --from DT --to DT

# Calendar colours
gog calendar colors

# Team calendars
gog calendar team <groupEmail> [--from DT] [--to DT]

# Conflicts detection
gog calendar conflicts <calendarId> --from DT --to DT

# Workspace users
gog calendar users [--max N] [--page TOKEN]
```

### Special Event Types

```bash
# Focus time
gog calendar focus-time create <calendarId> --from DT --to DT
  [--summary S] [--auto-decline]

# Out of office
gog calendar ooo create <calendarId> --from DT --to DT
  [--summary S] [--decline-message M]

# Working location
gog calendar working-location create <calendarId> --from DT --to DT
  [--location office|home|custom] [--building ID] [--floor F] [--desk D]
```

---

## Drive Commands

```bash
# List files
gog drive ls [--parent ID] [--max N] [--page TOKEN] [--query Q]

# Search files
gog drive search <text> [--max N] [--page TOKEN]

# Get file metadata
gog drive get <fileId>

# Download file
gog drive download <fileId> [--out PATH]

# Upload file
gog drive upload <localPath> [--name N] [--parent ID]

# Create folder
gog drive mkdir <name> [--parent ID]

# Delete file
gog drive delete <fileId>

# Move file
gog drive move <fileId> --parent ID

# Copy file
gog drive copy <fileId> [--name N] [--parent ID]

# Rename file
gog drive rename <fileId> <newName>

# Share file
gog drive share <fileId> [options]
  [--anyone | --email addr]
  [--role reader|writer|commenter]
  [--discoverable]

# List permissions
gog drive permissions <fileId> [--max N] [--page TOKEN]

# Remove sharing
gog drive unshare <fileId> <permissionId>

# Get URLs
gog drive url <fileIds...>

# List shared drives
gog drive drives [--max N] [--page TOKEN] [--query Q]

# Comments
gog drive comments <fileId> [--max N] [--page TOKEN]
gog drive comments add <fileId> --content <text>
gog drive comments reply <fileId> <commentId> --content <text>
gog drive comments resolve <fileId> <commentId>
gog drive comments delete <fileId> <commentId>
```

---

## Sheets Commands

```bash
# Create spreadsheet
gog sheets create <title> [--sheet NAME]

# Get spreadsheet info
gog sheets get <spreadsheetId>

# Read cells
gog sheets read <spreadsheetId> <range>
  # range format: SheetName!A1:B10

# Write cells
gog sheets write <spreadsheetId> <range> --values '[[...],[...]]'
  # values: JSON array of arrays

# Update cells
gog sheets update <spreadsheetId> <range> --values '[[...],[...]]'

# Append rows
gog sheets append <spreadsheetId> <range> --values '[[...],[...]]'

# Clear cells
gog sheets clear <spreadsheetId> <range>

# Format cells
gog sheets format <spreadsheetId> <range> [options]
  [--bold] [--italic] [--underline]
  [--bg-color #RRGGBB] [--fg-color #RRGGBB]
  [--font-size N] [--font-family NAME]
  [--h-align left|center|right]
  [--v-align top|middle|bottom]
  [--number-format FORMAT]

# Spreadsheet metadata
gog sheets metadata <spreadsheetId>
```

---

## Docs Commands

```bash
# Create document
gog docs create <title>

# Get document info
gog docs get <documentId>

# Export document
gog docs export <documentId> [--format pdf|docx|txt|html|md] [--out PATH]
```

---

## Slides Commands

```bash
# Create presentation
gog slides create <title>

# Get presentation info
gog slides get <presentationId>

# Export presentation
gog slides export <presentationId> [--format pdf|pptx] [--out PATH]
```

---

## Classroom Commands

### Courses

```bash
gog classroom courses [--state ACTIVE|ARCHIVED|...] [--max N] [--page TOKEN]
gog classroom courses get <courseId>
gog classroom courses create --name NAME [--owner me] [--state ACTIVE|...]
gog classroom courses update <courseId> [--name ...] [--state ...]
gog classroom courses delete <courseId>
gog classroom courses archive <courseId>
gog classroom courses unarchive <courseId>
gog classroom courses join <courseId> [--role student|teacher] [--user me]
gog classroom courses leave <courseId> [--role student|teacher] [--user me]
gog classroom courses url <courseId...>
```

### Rosters

```bash
gog classroom students <courseId> [--max N] [--page TOKEN]
gog classroom students get <courseId> <userId>
gog classroom students add <courseId> <userId> [--enrollment-code CODE]
gog classroom students remove <courseId> <userId>

gog classroom teachers <courseId> [--max N] [--page TOKEN]
gog classroom teachers get <courseId> <userId>
gog classroom teachers add <courseId> <userId>
gog classroom teachers remove <courseId> <userId>

gog classroom roster <courseId> [--students] [--teachers]
```

### Coursework

```bash
gog classroom coursework <courseId> [--state ...] [--topic TOPIC_ID] [--scan-pages N] [--max N] [--page TOKEN]
gog classroom coursework get <courseId> <courseworkId>
gog classroom coursework create <courseId> [options]
  --title T [--description D] [--type ASSIGNMENT|SHORT_ANSWER_QUESTION|...]
  [--due DT] [--max-points N] [--topic TOPIC_ID]
gog classroom coursework update <courseId> <courseworkId> [options]
gog classroom coursework delete <courseId> <courseworkId>
gog classroom coursework assignees <courseId> <courseworkId>
  [--mode ALL_STUDENTS|INDIVIDUAL_STUDENTS]
  [--add-student ...]
```

### Materials

```bash
gog classroom materials <courseId> [--state ...] [--topic TOPIC_ID] [--max N] [--page TOKEN]
gog classroom materials get <courseId> <materialId>
gog classroom materials create <courseId> [options]
gog classroom materials update <courseId> <materialId> [options]
gog classroom materials delete <courseId> <materialId>
```

### Submissions

```bash
gog classroom submissions <courseId> <courseworkId> [--state ...] [--max N] [--page TOKEN]
gog classroom submissions get <courseId> <courseworkId> <submissionId>
gog classroom submissions turn-in <courseId> <courseworkId> <submissionId>
gog classroom submissions reclaim <courseId> <courseworkId> <submissionId>
gog classroom submissions return <courseId> <courseworkId> <submissionId>
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade N
```

### Announcements

```bash
gog classroom announcements <courseId> [--state ...] [--max N] [--page TOKEN]
gog classroom announcements get <courseId> <announcementId>
gog classroom announcements create <courseId> --text T [--state ...]
gog classroom announcements update <courseId> <announcementId> [options]
gog classroom announcements delete <courseId> <announcementId>
gog classroom announcements assignees <courseId> <announcementId> [--mode ...]
```

### Topics

```bash
gog classroom topics <courseId> [--max N] [--page TOKEN]
gog classroom topics get <courseId> <topicId>
gog classroom topics create <courseId> --name N
gog classroom topics update <courseId> <topicId> --name N
gog classroom topics delete <courseId> <topicId>
```

### Invitations & Guardians

```bash
gog classroom invitations [--course ID] [--user ID]
gog classroom invitations get <invitationId>
gog classroom invitations create --course ID --user EMAIL --role student|teacher
gog classroom invitations accept <invitationId>
gog classroom invitations delete <invitationId>

gog classroom guardians <studentId> [--max N] [--page TOKEN]
gog classroom guardians get <studentId> <guardianId>
gog classroom guardians delete <studentId> <guardianId>

gog classroom guardian-invitations <studentId> [--state ...] [--max N] [--page TOKEN]
gog classroom guardian-invitations get <studentId> <invitationId>
gog classroom guardian-invitations create <studentId> --email EMAIL
```

### Profile

```bash
gog classroom profile [userId]
```

---

## Chat Commands (Workspace)

```bash
# Spaces
gog chat spaces list [--max N] [--page TOKEN]
gog chat spaces find <displayName> [--max N]
gog chat spaces create <displayName> [--member email,...]

# Messages
gog chat messages list <space> [--max N] [--page TOKEN] [--order ORDER] [--thread THREAD] [--unread]
gog chat messages send <space> --text TEXT [--thread THREAD]

# Threads
gog chat threads list <space> [--max N] [--page TOKEN]

# Direct messages
gog chat dm space <email>
gog chat dm send <email> --text TEXT [--thread THREAD]
```

---

## Tasks Commands

```bash
# Task lists
gog tasks lists [--max N] [--page TOKEN]
gog tasks lists create <title>

# List tasks
gog tasks list <tasklistId> [--max N] [--page TOKEN]

# Get task
gog tasks get <tasklistId> <taskId>

# Add task
gog tasks add <tasklistId> [options]
  --title T [--notes N]
  [--due RFC3339|YYYY-MM-DD]
  [--repeat daily|weekly|monthly|yearly]
  [--repeat-count N]
  [--repeat-until DT]
  [--parent ID] [--previous ID]

# Update task
gog tasks update <tasklistId> <taskId> [options]
  [--title T] [--notes N] [--due ...]
  [--status needsAction|completed]

# Complete/uncomplete task
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>

# Delete task
gog tasks delete <tasklistId> <taskId>

# Clear completed tasks
gog tasks clear <tasklistId>
```

---

## Contacts Commands

```bash
# Search contacts
gog contacts search <query> [--max N]

# List contacts
gog contacts list [--max N] [--page TOKEN]

# Get contact
gog contacts get <people/...|email>

# Create contact
gog contacts create --given NAME [--family NAME] [--email addr] [--phone num]

# Update contact
gog contacts update <people/...> [--given NAME] [--family NAME] [--email addr] [--phone num]

# Delete contact
gog contacts delete <people/...>

# Directory (Workspace)
gog contacts directory list [--max N] [--page TOKEN]
gog contacts directory search <query> [--max N] [--page TOKEN]

# Other contacts
gog contacts other list [--max N] [--page TOKEN]
gog contacts other search <query> [--max N]
```

---

## People Commands

```bash
gog people me                                # Get own profile
gog people get <people/...|userId>           # Get profile
gog people search <query> [--max N] [--page TOKEN]
gog people relations [<people/...|userId>] [--type TYPE]
```

---

## Groups Commands (Workspace)

```bash
gog groups list [--max N] [--page TOKEN]
gog groups get <groupEmail>
gog groups members <groupEmail> [--max N] [--page TOKEN]
```

---

## Keep Commands (Workspace)

```bash
gog keep list [--max N] [--page TOKEN]
gog keep get <noteId>
gog keep create --title T [--text CONTENT] [--list "item1,item2,..."]
gog keep delete <noteId>
```

---

## Time Commands

```bash
gog time now [--timezone TZ]
```

---

## Completion Commands

```bash
gog completion bash
gog completion zsh
gog completion fish
gog completion powershell
```
