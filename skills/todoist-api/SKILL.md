---
name: todoist-api
description: This skill provides instructions for interacting with the Todoist REST API v2 using curl and jq. It covers authentication, CRUD operations for tasks/projects/sections/labels/comments, pagination handling, and requires confirmation before destructive actions. Use this skill when the user wants to read, create, update, or delete Todoist data via the API.
---

# Todoist API Skill

This skill provides procedural guidance for working with the Todoist REST API v2 via curl and jq.

## Authentication

### Token Resolution

Resolve the API token in this order:

1. Check environment variable `TODOIST_API_TOKEN`
2. Check if the user has provided a token in the conversation context
3. If neither is available, use AskUserQuestion (or similar tool) to request the token from the user

To verify a token exists in the environment:

```bash
[ -n "$TODOIST_API_TOKEN" ] && echo "Token available" || echo "Token not set"
```

### Making Authenticated Requests

All requests require the Authorization header with Bearer token:

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/ENDPOINT"
```

For POST requests with JSON body, include Content-Type:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  "https://api.todoist.com/rest/v2/ENDPOINT"
```

## Base URL

All REST API v2 endpoints use: `https://api.todoist.com/rest/v2/`

## Confirmation Requirement

**Before executing any destructive action (DELETE, close, update, archive), always ask the user for confirmation using AskUserQuestion or similar tool.** A single confirmation suffices for a logical group of related actions.

Destructive actions include:
- Deleting tasks, projects, sections, labels, or comments
- Closing (completing) tasks
- Updating existing resources
- Archiving projects

Read-only operations (GET requests) do not require confirmation.

## Endpoints Reference

### Tasks

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List active tasks | GET | `/tasks` |
| Get task | GET | `/tasks/{id}` |
| Create task | POST | `/tasks` |
| Update task | POST | `/tasks/{id}` |
| Close task | POST | `/tasks/{id}/close` |
| Reopen task | POST | `/tasks/{id}/reopen` |
| Delete task | DELETE | `/tasks/{id}` |

**Task filters** (query params for GET /tasks):
- `project_id` - Filter by project
- `section_id` - Filter by section
- `label` - Filter by label name
- `filter` - Todoist filter query (e.g., "today", "overdue")

**Task creation/update fields:**
- `content` (required for creation) - Task text
- `description` - Additional details
- `project_id`, `section_id`, `parent_id` - Organisation
- `priority` - 1 (normal) to 4 (urgent)
- `due_string` - Natural language ("tomorrow", "every monday")
- `due_date` - YYYY-MM-DD format
- `due_datetime` - RFC3339 format
- `labels` - Array of label names
- `assignee_id` - For shared projects
- `duration`, `duration_unit` - Estimated time

### Projects

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List projects | GET | `/projects` |
| Get project | GET | `/projects/{id}` |
| Create project | POST | `/projects` |
| Update project | POST | `/projects/{id}` |
| Archive project | POST | `/projects/{id}/archive` |
| Unarchive project | POST | `/projects/{id}/unarchive` |
| Delete project | DELETE | `/projects/{id}` |
| List collaborators | GET | `/projects/{id}/collaborators` |

**Project fields:**
- `name` (required for creation)
- `parent_id` - For nested projects
- `color` - Colour name (e.g., "berry_red", "blue")
- `is_favorite` - Boolean
- `view_style` - "list" or "board"

### Sections

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List sections | GET | `/sections` |
| Get section | GET | `/sections/{id}` |
| Create section | POST | `/sections` |
| Update section | POST | `/sections/{id}` |
| Delete section | DELETE | `/sections/{id}` |

**Section filters** (query params for GET):
- `project_id` - Filter by project (recommended)

**Section fields:**
- `name` (required)
- `project_id` (required for creation)
- `order` - Position within project

### Labels

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List personal labels | GET | `/labels` |
| Get label | GET | `/labels/{id}` |
| Create label | POST | `/labels` |
| Update label | POST | `/labels/{id}` |
| Delete label | DELETE | `/labels/{id}` |
| List shared labels | GET | `/shared_labels` |
| Rename shared label | POST | `/shared_labels/{name}/rename` |
| Remove shared label | DELETE | `/shared_labels/{name}` |

**Label fields:**
- `name` (required)
- `color` - Colour name
- `order` - Display order
- `is_favorite` - Boolean

### Comments

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List comments | GET | `/comments` |
| Get comment | GET | `/comments/{id}` |
| Create comment | POST | `/comments` |
| Update comment | POST | `/comments/{id}` |
| Delete comment | DELETE | `/comments/{id}` |

**Comment filters** (query params for GET):
- `task_id` - Comments on a task (required if no project_id)
- `project_id` - Comments on a project (required if no task_id)

**Comment fields:**
- `content` (required) - Markdown supported
- `task_id` or `project_id` (one required for creation)

## Pagination

Some endpoints return paginated results. Handle pagination by checking for a `next_cursor` field in the response and making subsequent requests with the `cursor` parameter.

### Pagination Pattern

```bash
# Initial request
response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/ENDPOINT")

# Check for more results
next_cursor=$(echo "$response" | jq -r '.next_cursor // empty')

# If cursor exists, fetch next page
if [ -n "$next_cursor" ]; then
  curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
    "https://api.todoist.com/rest/v2/ENDPOINT?cursor=$next_cursor"
fi
```

### Complete Data Retrieval Loop

To retrieve all data when pagination is involved:

```bash
all_results="[]"
cursor=""

while true; do
  if [ -z "$cursor" ]; then
    response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
      "https://api.todoist.com/rest/v2/ENDPOINT")
  else
    response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
      "https://api.todoist.com/rest/v2/ENDPOINT?cursor=$cursor")
  fi

  # Merge results (adjust .items or root array based on endpoint)
  items=$(echo "$response" | jq '.items // .')
  all_results=$(echo "$all_results $items" | jq -s 'add')

  # Check for next page
  cursor=$(echo "$response" | jq -r '.next_cursor // empty')
  has_more=$(echo "$response" | jq -r '.has_more // false')

  if [ "$has_more" != "true" ] || [ -z "$cursor" ]; then
    break
  fi
done

echo "$all_results"
```

## Common Patterns

### List All Tasks in a Project

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?project_id=PROJECT_ID" | jq '.'
```

### Create a Task with Due Date

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Task name", "due_string": "tomorrow", "priority": 2}' \
  "https://api.todoist.com/rest/v2/tasks"
```

### Complete a Task

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks/TASK_ID/close"
```

### Get Today's Tasks

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=today" | jq '.'
```

### Get Overdue Tasks

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=overdue" | jq '.'
```

## Error Handling

Check HTTP status codes and handle errors appropriately:

- `200` - Success with response body
- `204` - Success, no content
- `400` - Bad request (check parameters)
- `401` - Authentication failed (check token)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `429` - Rate limited (wait and retry)
- `5xx` - Server error (safe to retry)

### Example with Error Handling

```bash
response=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  echo "$body" | jq '.'
else
  echo "Error: HTTP $http_code"
  echo "$body"
fi
```

## Idempotency

For safe retries on write operations, include the `X-Request-Id` header (max 36 characters):

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Request-Id: $(uuidgen)" \
  -d '{"content": "New task"}' \
  "https://api.todoist.com/rest/v2/tasks"
```

Duplicate requests with the same X-Request-Id are discarded by the server.

## Completed Tasks

The REST API v2 `/tasks` endpoint returns only active tasks. For completed tasks, use the Sync API or the newer unified API v1 endpoints:

- `GET /tasks/completed/by_completion_date` - Retrieve by completion date
- `GET /tasks/completed/by_due_date` - Retrieve by original due date

See `references/completed-tasks.md` for details on retrieving completed task history.

## Additional Reference

For detailed information on specific topics, consult:
- `references/completed-tasks.md` - Retrieving completed task history
- `references/filters.md` - Todoist filter query syntax

## Workflow Summary

1. **Resolve token** - Environment, context, or ask user
2. **Verify authentication** - Test with a simple GET request
3. **Read operations** - Execute directly without confirmation
4. **Write operations** - Ask for confirmation before executing
5. **Handle pagination** - Loop with cursor for complete data
6. **Parse responses** - Use jq to extract and format data
