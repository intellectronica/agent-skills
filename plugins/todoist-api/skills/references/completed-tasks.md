# Retrieving Completed Tasks

The `td completed` command is the primary way to retrieve completed tasks.

## CLI Usage

### Basic Usage

```bash
td completed                    # Today's completed tasks
td completed --json             # JSON output
td completed --all --json       # All completed (no limit)
```

### Date Range

```bash
td completed --since 2024-01-01 --until 2024-01-31
td completed --since 2024-01-01 --json
```

### Filter by Project

```bash
td completed --project "Work" --json
```

### Options

- `--since <date>` - Start date (YYYY-MM-DD), default: today
- `--until <date>` - End date (YYYY-MM-DD), default: tomorrow
- `--project <name>` - Filter by project name
- `--limit <n>` - Limit number of results (default: 300)
- `--all` - Fetch all results (no limit)
- `--json` - Output as JSON
- `--ndjson` - Output as newline-delimited JSON
- `--full` - Include all fields in JSON output

## Alternative: Direct API Access

If you need more control or the CLI doesn't provide the required functionality, you can use the API directly.

### API v1 Endpoints

**By Completion Date:**
```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_completion_date?since=2024-01-01T00:00:00Z&until=2024-01-31T23:59:59Z"
```

**By Due Date:**
```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/api/v1/tasks/completed/by_due_date?since=2024-01-01T00:00:00Z"
```

### API Parameters

- `since` - Start date (ISO 8601 format)
- `until` - End date (ISO 8601 format)
- `project_id` - Filter by project ID
- `limit` - Results per page
- `cursor` - Pagination cursor

### Response Structure

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

## Notes

- Completed tasks are stored in history and may have limited retention based on user plan
- Use `td task uncomplete id:xxx` to reopen a completed task
- Recurring tasks create new instances when completed; the original remains in history
