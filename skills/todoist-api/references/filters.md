# Todoist Filter Query Syntax

The `filter` parameter on `/tasks` accepts Todoist's filter query language, enabling powerful task queries.

## Basic Filters

| Filter | Description |
|--------|-------------|
| `today` | Tasks due today |
| `tomorrow` | Tasks due tomorrow |
| `overdue` | Overdue tasks |
| `no date` | Tasks without a due date |
| `7 days` | Tasks due within the next 7 days |
| `next week` | Tasks due next week |
| `recurring` | Recurring tasks only |

## Date Filters

| Filter | Description |
|--------|-------------|
| `due before: Jan 1` | Due before specific date |
| `due after: Jan 1` | Due after specific date |
| `due: Jan 1` | Due on specific date |
| `created: today` | Created today |
| `created before: -7 days` | Created more than 7 days ago |

## Priority Filters

| Filter | Description |
|--------|-------------|
| `p1` | Priority 1 (urgent) |
| `p2` | Priority 2 (high) |
| `p3` | Priority 3 (medium) |
| `p4` or `no priority` | Priority 4 (normal) |

## Label Filters

| Filter | Description |
|--------|-------------|
| `@label_name` | Tasks with specific label |
| `no labels` | Tasks without any labels |

## Project and Section Filters

| Filter | Description |
|--------|-------------|
| `#Project Name` | Tasks in specific project |
| `##Project Name` | Tasks in project and subprojects |
| `/Section Name` | Tasks in specific section |

## Assignment Filters

| Filter | Description |
|--------|-------------|
| `assigned to: me` | Tasks assigned to you |
| `assigned to: John` | Tasks assigned to John |
| `assigned by: me` | Tasks you assigned |
| `assigned` | All assigned tasks |

## Combining Filters

Use logical operators to combine filters:

| Operator | Description | Example |
|----------|-------------|---------|
| `&` | AND | `today & p1` |
| `\|` | OR | `today \| overdue` |
| `!` | NOT | `!#Inbox` |
| `()` | Grouping | `(today \| overdue) & p1` |

## URL Encoding

When using filters in curl requests, URL-encode special characters:

```bash
# today & p1
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=today%20%26%20p1"

# today | overdue
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=today%20%7C%20overdue"

# @urgent
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=%40urgent"
```

## Common Encoding Reference

| Character | Encoded |
|-----------|---------|
| space | `%20` |
| `&` | `%26` |
| `\|` | `%7C` |
| `@` | `%40` |
| `#` | `%23` |
| `:` | `%3A` |
| `(` | `%28` |
| `)` | `%29` |

## Example Queries

### High-Priority Tasks Due Soon

```bash
# (today | overdue) & (p1 | p2)
filter="(today%20%7C%20overdue)%20%26%20(p1%20%7C%20p2)"
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=$filter"
```

### Unassigned Tasks in Work Project

```bash
# #Work & !assigned
filter="%23Work%20%26%20!assigned"
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=$filter"
```

### Tasks with Label Due This Week

```bash
# @waiting & 7 days
filter="%40waiting%20%26%207%20days"
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=$filter"
```

## Notes

- Filter queries are case-insensitive
- Project and label names with spaces should be quoted or URL-encoded
- The filter parameter only works with the GET `/tasks` endpoint
- Complex filters may require Premium/Business plans
