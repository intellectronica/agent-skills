---
name: monologue-notes-api
description: >
  Use this skill when the user wants to read or search their Monologue notes through the
  Monologue Notes REST API. It covers authentication with the MONOLOGUE_API_KEY environment
  variable, safe token handling, listing notes, fetching a single note, pagination, filters,
  and error handling. The API is read-only and should be accessed with direct HTTP requests
  such as curl or any equivalent REST client.
---

# Monologue Notes API

This skill provides the information needed to call the Monologue Notes REST API directly.
Use it for read-only operations on the authenticated user's notes.

Use whatever HTTP client fits the task: `curl`, a short script, or another REST-capable tool.
Do not invent client libraries unless the user asks for one.

## Authentication

Use the environment variable `MONOLOGUE_API_KEY` as the bearer token.

- Required auth header: `Authorization: Bearer $MONOLOGUE_API_KEY`
- Required scope: `notes:read`
- Never print the token, echo it, log it, or include it in a response to the user
- Only pass it through the `Authorization` header as a shell variable expansion

Check whether the token is available without displaying it:

```bash
if [ -z "${MONOLOGUE_API_KEY:-}" ]; then
  echo "MONOLOGUE_API_KEY is not set"
fi
```

If `MONOLOGUE_API_KEY` is missing:

- Report that the environment variable is not present
- Ask the user whether they want to provide an API key
- Do not attempt authenticated API calls until a token is available

Avoid commands such as these because they would expose secrets:

```bash
echo "$MONOLOGUE_API_KEY"
env | grep MONOLOGUE_API_KEY
set | grep MONOLOGUE_API_KEY
```

## Base URL

- Base URL: `https://api.monologue.to`
- API shape: read-only Notes API
- Data format: JSON
- Timestamps: ISO 8601 date-time strings

## Request Pattern

For all requests:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/..."
```

If structured output is useful, pipe the response to `jq`.

## Endpoints

### List notes

`GET /v1/public-api/notes`

Returns a page of notes for the authenticated user.

Supported query parameters:

- `limit`: integer from `1` to `100`, default `20`
- `cursor`: opaque pagination cursor from a previous response
- `created_after`: ISO 8601 timestamp
- `created_before`: ISO 8601 timestamp
- `updated_after`: ISO 8601 timestamp
- `q`: full-text search across titles, summaries, and transcripts

Example:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes?limit=20&q=interview"
```

Example with `jq`:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes?limit=20" \
  | jq '{next_cursor, items: [.items[] | {note_id, title, summary, created_at, updated_at}]}'
```

Expected response fields:

- `items`: array of note summaries
- `next_cursor`: cursor for the next page, if any

Each list item may include:

- `note_id`
- `title`
- `summary`
- `created_at`
- `updated_at`

Possible errors:

- `400`: invalid filter or cursor
- `401`: missing or invalid token
- `403`: token lacks the required scope
- `422`: validation error

### Get a single note

`GET /v1/public-api/notes/{note_id}`

Returns the full details for one note belonging to the authenticated user.

Path parameters:

- `note_id`: note identifier returned by the list endpoint

Example:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes/NOTE_ID"
```

Example with `jq`:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes/NOTE_ID" \
  | jq '{note_id, title, summary, transcript, transcript_segments, created_at, updated_at}'
```

In addition to the list fields, the full note response may include:

- `transcript`
- `transcript_segments`

Notes:

- `transcript_segments` is loosely typed structured JSON and may be `null`
- `404` means the note was not found for the authenticated user

Possible errors:

- `401`: missing or invalid token
- `403`: token lacks the required scope
- `404`: note not found
- `422`: validation error

## Common Workflows

### Search notes by keyword

Use the `q` parameter:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes?q=meeting"
```

Search covers:

- note titles
- note summaries
- note transcripts

### Page through results

1. Call `GET /v1/public-api/notes`
2. Read `next_cursor` from the response
3. Pass that cursor back as the `cursor` query parameter
4. Stop when `next_cursor` is absent or `null`

Example:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes?limit=50&cursor=OPAQUE_CURSOR"
```

### Filter by time

Use ISO 8601 date-time values:

```bash
curl -sS \
  -H "Authorization: Bearer $MONOLOGUE_API_KEY" \
  "https://api.monologue.to/v1/public-api/notes?created_after=2026-01-01T00:00:00Z"
```

## Operating Rules

- Treat this API as read-only
- Do not claim write support; this skill only covers listing and reading notes
- Prefer `https://api.monologue.to` for requests
- When reporting failures, summarise the HTTP status and relevant response body without exposing the token
- If the user asks for a workflow that requires local post-processing, fetch the data first and then transform it separately

## Source Notes

This skill is based on:

- `/Users/eleanor/repos/obsidian/intellectronica/2026-04-21-20-10 Monologue API.md`
- Live OpenAPI checks against `https://api.monologue.to/public-openapi.json` on 2026-04-22
