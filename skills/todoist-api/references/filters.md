# Todoist Filter Query Syntax

The `filter` parameter on `GET /tasks` accepts Todoist's filter query language.

## ⚠️ Priority Note

Filter syntax uses **UI labels** (p1 = urgent), not API field values (priority 4 = urgent).
See the Priority Mapping table in SKILL.md.

## Basic Filters

| Filter | Description |
|--------|-------------|
| `today` | Tasks due today |
| `tomorrow` | Tasks due tomorrow |
| `overdue` | Overdue tasks |
| `no date` | Tasks without a due date |
| `7 days` | Due within next 7 days |
| `next week` | Due next week |
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

| Filter | UI meaning | API `priority` value |
|--------|-----------|---------------------|
| `p1` | Urgent (red) | 4 |
| `p2` | High (orange) | 3 |
| `p3` | Medium (blue) | 2 |
| `p4` / `no priority` | Normal | 1 |

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

| Operator | Description | Example |
|----------|-------------|---------|
| `&` | AND | `today & p1` |
| `\|` | OR | `today \| overdue` |
| `!` | NOT | `!#Inbox` |
| `()` | Grouping | `(today \| overdue) & p1` |

## URL Encoding

URL-encode special characters in curl:

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

### Examples

```bash
# High-priority tasks due soon: (today | overdue) & (p1 | p2)
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=(today%20%7C%20overdue)%20%26%20(p1%20%7C%20p2)"

# Tasks with @waiting label due this week
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=%40waiting%20%26%207%20days"
```

## Notes

- Filter queries are case-insensitive
- Complex filters may require Premium/Business plans
- The `filter` param only works with `GET /tasks`
