# Calendar Operations Reference

Use this for listing calendars, events, availability, scheduling, RSVP, calendar aliases, subscriptions, secondary calendars, team calendars, and Workspace scheduling helpers.

## Calendar discovery and aliases

```bash
gog calendar calendars
gog calendar calendars --json
gog calendar calendars --all-pages

gog calendar alias list
gog calendar alias set team team@group.calendar.google.com
gog calendar alias unset team
gog calendar events team --today
```

Subscribe to shared calendars:

```bash
gog calendar subscribe user@example.com
gog calendar subscribe team@group.calendar.google.com --color-id 9 --selected
```

Create secondary calendars:

```bash
gog calendar create-calendar "Project Calendar" \
  --description "Launch planning" \
  --timezone Europe/Zurich \
  --location "Zurich"
```

Access control:

```bash
gog calendar acl primary
gog calendar colors
```

## Listing events

```bash
gog calendar events primary
gog calendar events primary --today --weekday
gog calendar events primary --tomorrow
gog calendar events primary --week --week-start mon
gog calendar events primary --days 14
gog calendar events primary --from "2026-04-25T00:00:00+02:00" --to "2026-04-26T00:00:00+02:00"
gog calendar events --all --from today --to tomorrow
gog calendar events --cal primary --cal team --today
gog calendar events primary --query "planning"
gog calendar events primary --private-prop-filter "source=gog"
gog calendar events primary --fields "id,summary,start,end"
```

Pagination and failure handling:

```bash
gog --json calendar events primary --today --max 10
gog --json calendar events primary --today --all-pages
gog calendar events primary --query "unlikely query" --fail-empty
```

## Event details

```bash
gog calendar event primary <eventId>
gog calendar get primary <eventId>
gog calendar search "roadmap" --from today --days 30
```

## Create events

Prefer explicit RFC3339 timestamps with timezone offsets.

```bash
gog calendar create primary \
  --summary "Team Sync" \
  --from "2026-04-25T14:00:00+02:00" \
  --to "2026-04-25T14:30:00+02:00" \
  --attendees "alice@example.com,bob@example.com" \
  --with-meet \
  --send-updates all
```

Details:

```bash
gog calendar create primary \
  --summary "Project Review" \
  --description "Quarterly review" \
  --location "Room 3" \
  --from "2026-04-25T10:00:00+02:00" \
  --to "2026-04-25T11:00:00+02:00" \
  --event-color 2 \
  --visibility private \
  --transparency busy
```

All-day:

```bash
gog calendar create primary \
  --summary "Company Holiday" \
  --from "2026-05-01" \
  --to "2026-05-02" \
  --all-day
```

Recurrence and reminders:

```bash
gog calendar create primary \
  --summary "Weekly Standup" \
  --from "2026-04-27T09:00:00+02:00" \
  --to "2026-04-27T09:30:00+02:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR" \
  --reminder popup:10m \
  --reminder email:1d
```

Extended properties and attachments:

```bash
gog calendar create primary \
  --summary "Imported Event" \
  --from "2026-04-25T12:00:00+02:00" \
  --to "2026-04-25T13:00:00+02:00" \
  --source-url "https://example.com/event" \
  --source-title "Source" \
  --private-prop source=gog \
  --shared-prop project=alpha \
  --attachment "https://drive.google.com/file/d/<fileId>/view"
```

## Update, delete, RSVP

```bash
gog calendar update primary <eventId> --summary "Updated Title"
gog calendar update primary <eventId> --from "2026-04-25T15:00:00+02:00" --to "2026-04-25T16:00:00+02:00"
gog calendar update primary <eventId> --add-attendee new@example.com
gog calendar update primary <eventId> --attendees "only@example.com"
gog calendar delete primary <eventId>
```

Recurring-event updates/deletes can have scope flags in current builds. Check `gog calendar update --help` and `gog calendar delete --help` before altering a series.

Respond:

```bash
gog calendar respond primary <eventId> --status accepted --send-updates all
gog calendar respond primary <eventId> --status tentative
gog calendar respond primary <eventId> --status declined --send-updates none
```

Propose a time:

```bash
gog calendar propose-time primary <eventId> \
  --from "2026-04-26T14:00:00+02:00" \
  --to "2026-04-26T15:00:00+02:00"
```

## Availability and conflicts

```bash
gog calendar freebusy primary --from "2026-04-25T09:00:00+02:00" --to "2026-04-25T17:00:00+02:00"
gog calendar freebusy --cal primary --cal team --from "2026-04-25T09:00:00+02:00" --to "2026-04-25T17:00:00+02:00"
gog calendar freebusy --all --from "2026-04-25T09:00:00+02:00" --to "2026-04-25T17:00:00+02:00"

gog calendar conflicts --today --all
gog calendar conflicts --from today --to tomorrow --cal primary
```

Workspace helpers:

```bash
gog calendar users --max 50
gog calendar team engineering@example.com --from today --days 7
```

## Special event types

Focus Time:

```bash
gog calendar focus-time primary \
  --summary "Deep Work" \
  --from "2026-04-25T09:00:00+02:00" \
  --to "2026-04-25T12:00:00+02:00" \
  --auto-decline all \
  --decline-message "Focus block" \
  --chat-status doNotDisturb
```

Out of Office:

```bash
gog calendar out-of-office primary \
  --from "2026-05-01T00:00:00+02:00" \
  --to "2026-05-05T00:00:00+02:00" \
  --auto-decline all \
  --decline-message "Away until May 5"
```

Working Location:

```bash
gog calendar working-location primary --from "2026-04-25" --to "2026-04-26" --type home
gog calendar working-location primary --from "2026-04-25" --to "2026-04-26" --type office --office-label "HQ" --building-id HQ --floor-id 3 --desk-id 42
gog calendar working-location primary --from "2026-04-25" --to "2026-04-26" --type custom --custom-label "Client site"
```

Equivalent generic event creation is also available with `--event-type focus-time|out-of-office|working-location` and related `--focus-*`, `--ooo-*`, and `--working-*` flags.

## Time input

Accepted formats include:

| Kind | Example |
| --- | --- |
| RFC3339 | `2026-04-25T14:00:00Z` |
| RFC3339 with offset | `2026-04-25T14:00:00+02:00` |
| ISO offset without colon | `2026-04-25T14:00:00+0200` |
| Local datetime | `2026-04-25 14:00:00` |
| Date only | `2026-04-25` |
| Relative ranges | `today`, `tomorrow`, `monday`, `next friday` |

Generated automation should use RFC3339 with explicit timezone offsets.

