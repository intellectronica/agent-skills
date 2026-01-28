# Retrieving Completed Tasks

The REST API v2 `/tasks` endpoint returns only active (non-completed) tasks. To access completed task history, use the unified API v1 endpoints or the Sync API.

## API v1 Endpoints for Completed Tasks

### By Completion Date

Retrieve tasks based on when they were completed:

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_completion_date"
```

**Parameters:**
- `since` - Start date (ISO 8601 format)
- `until` - End date (ISO 8601 format)
- `project_id` - Filter by project
- `limit` - Results per page
- `cursor` - Pagination cursor

### By Due Date

Retrieve completed tasks based on their original due date:

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_due_date"
```

**Parameters:** Same as above.

## Sync API Approach

For comprehensive completed task data, use the Sync API:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'sync_token=*&resource_types=["completed_info"]' \
  "https://api.todoist.com/sync/v9/sync"
```

This returns completion counts per project and section, not individual completed items.

## Pagination for Completed Tasks

Completed task endpoints support cursor-based pagination:

```bash
# Initial request
response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_completion_date?limit=100")

# Extract cursor for next page
cursor=$(echo "$response" | jq -r '.next_cursor // empty')

# Fetch next page if cursor exists
if [ -n "$cursor" ]; then
  curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
    "https://api.todoist.com/api/v1/tasks/completed/by_completion_date?cursor=$cursor&limit=100"
fi
```

## Complete Retrieval Loop

To fetch all completed tasks within a date range:

```bash
all_completed="[]"
cursor=""
since="2024-01-01T00:00:00Z"
until="2024-12-31T23:59:59Z"

while true; do
  url="https://api.todoist.com/api/v1/tasks/completed/by_completion_date?since=$since&until=$until&limit=100"

  if [ -n "$cursor" ]; then
    url="$url&cursor=$cursor"
  fi

  response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" "$url")

  items=$(echo "$response" | jq '.items // []')
  all_completed=$(echo "$all_completed $items" | jq -s 'add')

  cursor=$(echo "$response" | jq -r '.next_cursor // empty')

  if [ -z "$cursor" ]; then
    break
  fi
done

echo "$all_completed" | jq '.'
```

## Response Structure

Completed task objects include:

```json
{
  "id": "123456789",
  "content": "Task content",
  "project_id": "987654321",
  "completed_at": "2024-06-15T14:30:00Z",
  "meta_data": null
}
```

## Important Notes

- Completed tasks are stored in history and may have limited retention based on user plan
- The `/tasks/{id}/reopen` endpoint can restore a completed task to active status
- Recurring tasks create new instances when completed; the original remains in history
