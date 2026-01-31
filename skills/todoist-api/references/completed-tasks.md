# Retrieving Completed Tasks

REST v2 `/tasks` returns only active tasks. Use the API v1 endpoints for completed task history.

## Endpoints

### By Completion Date

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_completion_date"
```

### By Due Date

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_due_date"
```

**Parameters (both endpoints):**
- `since` — start date (ISO 8601)
- `until` — end date (ISO 8601)
- `project_id` — filter by project
- `limit` — results per page
- `cursor` — pagination cursor

## Cursor-Based Pagination

These endpoints (unlike REST v2) use cursor pagination:

```bash
all_completed="[]"
cursor=""
since="2024-01-01T00:00:00Z"
until="2024-12-31T23:59:59Z"

while true; do
  url="https://api.todoist.com/api/v1/tasks/completed/by_completion_date?since=$since&until=$until&limit=100"
  [ -n "$cursor" ] && url="$url&cursor=$cursor"

  response=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" "$url")

  items=$(echo "$response" | jq '.items // []')
  all_completed=$(echo "$all_completed $items" | jq -s 'add')

  cursor=$(echo "$response" | jq -r '.next_cursor // empty')
  [ -z "$cursor" ] && break
done

echo "$all_completed" | jq '.'
```

## Response Structure

```json
{
  "id": "123456789",
  "content": "Task content",
  "project_id": "987654321",
  "completed_at": "2024-06-15T14:30:00Z",
  "meta_data": null
}
```

## Notes

- Completed task retention may be limited by user plan
- `/tasks/{id}/reopen` restores a completed task to active
- Recurring tasks create new instances on completion; the original stays in history
