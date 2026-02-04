# Todoist Filter Query Syntax

The `--filter` flag on `td task list` accepts Todoist's filter query language, enabling powerful task queries.

## Usage with td CLI

```bash
td task list --filter "today & p1"
td task list --filter "overdue | today" --json
td task list --filter "#Work & @urgent" --all
```

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

## Example Queries

### High-Priority Tasks Due Soon

```bash
td task list --filter "(today | overdue) & (p1 | p2)" --json
```

### Unassigned Tasks in Work Project

```bash
td task list --filter "#Work & !assigned" --json
```

### Tasks with Label Due This Week

```bash
td task list --filter "@waiting & 7 days" --json
```

### All Inbox Tasks Not Started

```bash
td task list --filter "#Inbox & no date" --json
```

### Urgent Tasks Assigned to Me

```bash
td task list --filter "assigned to: me & p1" --json
```

## Notes

- Filter queries are case-insensitive
- Project and label names with spaces should be quoted: `"#My Project"`
- Complex filters may require Premium/Business plans
- The CLI handles quoting and escaping automatically (unlike raw API calls)
