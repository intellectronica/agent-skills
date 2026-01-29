# Calendar Operations Reference

Comprehensive guide to Google Calendar operations with `gog`.

## Listing Calendars

```bash
# List all calendars
gog calendar calendars

# JSON output
gog calendar calendars --json
```

## Listing Events

```bash
# List events from primary calendar
gog calendar events primary

# List from specific calendar
gog calendar events work@group.calendar.google.com

# Filter by date range
gog calendar events primary --from 2024-12-01T00:00:00Z --to 2024-12-31T23:59:59Z

# Natural date formats also work
gog calendar events primary --from "2024-12-01" --to "2024-12-31"

# Search events
gog calendar events primary --query "meeting"

# Show weekday
gog calendar events primary --weekday

# Limit results
gog calendar events primary --max 10

# Paginate
gog calendar events primary --page <nextPageToken>
```

---

## Getting Event Details

```bash
gog calendar event primary <eventId>
gog calendar get primary <eventId>
```

---

## Creating Events

### Basic Event

```bash
gog calendar create primary \
  --summary "Team Meeting" \
  --from "2024-12-20T14:00:00" \
  --to "2024-12-20T15:00:00"
```

### With Details

```bash
gog calendar create primary \
  --summary "Project Review" \
  --description "Quarterly review of project progress" \
  --location "Conference Room A" \
  --from "2024-12-20T14:00:00" \
  --to "2024-12-20T15:00:00"
```

### With Attendees

```bash
gog calendar create primary \
  --summary "Team Sync" \
  --from "2024-12-20T14:00:00" \
  --to "2024-12-20T15:00:00" \
  --attendees "alice@example.com,bob@example.com"
```

### All-Day Event

```bash
gog calendar create primary \
  --summary "Company Holiday" \
  --from "2024-12-25" \
  --to "2024-12-26" \
  --all-day
```

### With Recurrence

```bash
# Weekly meeting
gog calendar create primary \
  --summary "Weekly Standup" \
  --from "2024-12-20T09:00:00" \
  --to "2024-12-20T09:30:00" \
  --rrule "FREQ=WEEKLY;BYDAY=MO,WE,FR"

# Monthly meeting
gog calendar create primary \
  --summary "Monthly Review" \
  --from "2024-12-01T10:00:00" \
  --to "2024-12-01T11:00:00" \
  --rrule "FREQ=MONTHLY;BYMONTHDAY=1"
```

### With Reminders

```bash
gog calendar create primary \
  --summary "Important Meeting" \
  --from "2024-12-20T14:00:00" \
  --to "2024-12-20T15:00:00" \
  --reminders "10m,1h,1d"
```

---

## Updating Events

```bash
# Update summary
gog calendar update primary <eventId> --summary "Updated Title"

# Update time
gog calendar update primary <eventId> \
  --from "2024-12-20T15:00:00" \
  --to "2024-12-20T16:00:00"

# Update multiple fields
gog calendar update primary <eventId> \
  --summary "New Title" \
  --description "Updated description" \
  --location "New Location"

# Add attendee (preserves existing)
gog calendar update primary <eventId> --add-attendee "new@example.com"

# Replace all attendees
gog calendar update primary <eventId> --attendees "only@example.com"
```

---

## Deleting Events

```bash
gog calendar delete primary <eventId>
```

---

## Responding to Events

```bash
# Accept invitation
gog calendar respond primary <eventId> --status accepted

# Decline
gog calendar respond primary <eventId> --status declined

# Tentative
gog calendar respond primary <eventId> --status tentative

# Control notification sending
gog calendar respond primary <eventId> \
  --status accepted \
  --send-updates all          # all, none, externalOnly
```

---

## Checking Availability

```bash
# Check free/busy for calendars
gog calendar freebusy "primary,work@group.calendar.google.com" \
  --from "2024-12-20T08:00:00Z" \
  --to "2024-12-20T18:00:00Z"
```

---

## Proposing Alternative Times

```bash
gog calendar propose-time primary <eventId> \
  --from "2024-12-21T14:00:00" \
  --to "2024-12-21T15:00:00"
```

---

## Special Event Types

### Focus Time

```bash
gog calendar focus-time create primary \
  --from "2024-12-20T09:00:00" \
  --to "2024-12-20T12:00:00" \
  --summary "Deep Work" \
  --auto-decline
```

### Out of Office

```bash
gog calendar ooo create primary \
  --from "2024-12-20T00:00:00" \
  --to "2024-12-27T00:00:00" \
  --summary "Holiday" \
  --decline-message "I'm away until Dec 27"
```

### Working Location

```bash
# Office
gog calendar working-location create primary \
  --from "2024-12-20T09:00:00" \
  --to "2024-12-20T17:00:00" \
  --location office \
  --building "HQ" \
  --floor "3" \
  --desk "3-42"

# Home
gog calendar working-location create primary \
  --from "2024-12-20T09:00:00" \
  --to "2024-12-20T17:00:00" \
  --location home

# Custom
gog calendar working-location create primary \
  --from "2024-12-20T09:00:00" \
  --to "2024-12-20T17:00:00" \
  --location custom \
  --custom-location "Client Site"
```

---

## Calendar Colours

```bash
gog calendar colors
```

---

## Team Calendars

```bash
# View team calendar
gog calendar team team@group.calendar.google.com

# Filter by date range
gog calendar team team@group.calendar.google.com \
  --from "2024-12-01" \
  --to "2024-12-31"
```

---

## Conflict Detection

```bash
gog calendar conflicts primary \
  --from "2024-12-20T00:00:00Z" \
  --to "2024-12-27T00:00:00Z"
```

---

## Workspace Users

```bash
# List workspace users (for scheduling)
gog calendar users
gog calendar users --max 50
```

---

## Access Control

```bash
# List calendar ACLs
gog calendar acl primary
gog calendar acl work@group.calendar.google.com
```

---

## Time Formats

Commands accept various time formats:

| Format | Example |
|--------|---------|
| RFC3339 | `2024-12-20T14:00:00Z` |
| RFC3339 with offset | `2024-12-20T14:00:00-05:00` |
| Date only | `2024-12-20` |
| ISO datetime | `2024-12-20T14:00:00` |

The default timezone can be configured:

```bash
# Set default timezone
gog config set default_timezone America/New_York

# Or via environment
export GOG_TIMEZONE=Europe/London

# Or per-command
gog time now --timezone Asia/Tokyo
```

---

## Scripting Examples

### Find Available Slots

```bash
# Get free/busy and parse with jq
gog calendar freebusy "user1@example.com,user2@example.com" \
  --from "2024-12-20T08:00:00Z" \
  --to "2024-12-20T18:00:00Z" \
  --json | jq '.calendars'
```

### Batch Create Events

```bash
# Create events from a file
while IFS=$'\t' read -r summary from to; do
  gog calendar create primary \
    --summary "$summary" \
    --from "$from" \
    --to "$to"
done < events.tsv
```

### Export Events

```bash
# Export events to JSON
gog calendar events primary \
  --from "2024-12-01" \
  --to "2024-12-31" \
  --json > december-events.json
```
