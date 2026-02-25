---
name: todoist-api
description: Create tasks, list projects, update due dates, complete items, manage labels, and organise sections in Todoist using the td CLI tool. Use when the user wants to manage their todo list, add a task, check their to-dos, update reminders, or interact with Todoist data in any way. Requires confirmation before destructive actions.
---

# Todoist CLI Skill

This skill provides procedural guidance for working with Todoist using the `td` CLI tool.

## Prerequisites

The `td` CLI must be installed and authenticated. Verify with:

```bash
td auth status
```

If td is not installed or not authenticated:
- **Not installed**: Tell the user to install with `npm install -g @doist/todoist-cli`
- **Not authenticated**: Tell the user to run `td auth login` to authenticate via OAuth

## Output Formats for Agents

For machine-readable output, use these flags:
- `--json` - Output as JSON array
- `--ndjson` - Output as newline-delimited JSON (one object per line)
- `--full` - Include all fields in JSON output (default shows essential fields only)

## Confirmation Requirement

**Before executing any destructive action, always ask the user for confirmation using AskUserQuestion or similar tool.** A single confirmation suffices for a logical group of related actions.

Destructive actions include:
- Deleting tasks, projects, sections, labels, or comments
- Completing tasks
- Updating existing resources
- Archiving projects

Read-only operations do not require confirmation.

## Quick Commands

| Command | Description |
|---------|-------------|
| `td add "text"` | Quick add with natural language parsing |
| `td today` | Tasks due today and overdue |
| `td upcoming [days]` | Tasks due in next N days (default: 7) |
| `td inbox` | Tasks in Inbox |
| `td completed` | Recently completed tasks |

### Quick Add Examples

```bash
td add "Buy milk tomorrow p1 #Shopping"
td add "Call dentist every monday @health"
td add "Review PR #Work /Code Review"
```

The quick add parser supports:
- Due dates: `tomorrow`, `next monday`, `Jan 15`
- Priority: `p1` (urgent) through `p4` (normal)
- Project: `#ProjectName`
- Section: `/SectionName`
- Labels: `@label1 @label2`

## Tasks

### List Tasks

```bash
td task list [options]
```

**Filters:**
- `--project <name>` - Filter by project name or id:xxx
- `--label <name>` - Filter by label (comma-separated for multiple)
- `--priority <p1-p4>` - Filter by priority
- `--due <date>` - Filter by due date (today, overdue, or YYYY-MM-DD)
- `--filter <query>` - Raw Todoist filter query
- `--assignee <ref>` - Filter by assignee (me or id:xxx)
- `--workspace <name>` - Filter to workspace
- `--personal` - Filter to personal projects only

**Output:**
```bash
td task list --json                    # JSON array
td task list --project "Work" --json   # Filtered JSON
td task list --all --json              # All tasks (no limit)
```

### View Task Details

```bash
td task view <ref>              # Human-readable
td task view <ref> --json       # JSON output
```

The ref can be a task name, partial match, or `id:xxx`.

### Create Task

**Quick add (natural language):**
```bash
td add "Task text with #Project @label tomorrow p2"
```

**Explicit flags:**
```bash
td task add --content "Task text" \
  --project "Work" \
  --due "tomorrow" \
  --priority p2 \
  --labels "urgent,review" \
  --description "Additional details"
```

**Options:**
- `--content <text>` - Task content (required)
- `--due <date>` - Due date (natural language or YYYY-MM-DD)
- `--deadline <date>` - Deadline date (YYYY-MM-DD)
- `--priority <p1-p4>` - Priority level
- `--project <name>` - Project name or id:xxx
- `--section <id>` - Section ID
- `--labels <a,b>` - Comma-separated labels
- `--parent <ref>` - Parent task for subtask
- `--description <text>` - Task description
- `--assignee <ref>` - Assign to user (name, email, id:xxx, or "me")
- `--duration <time>` - Duration (e.g., 30m, 1h, 2h15m)

### Update Task

```bash
td task update <ref> --content "New content" --due "next week"
```

**Options:**
- `--content <text>` - New content
- `--due <date>` - New due date
- `--deadline <date>` - Deadline date
- `--no-deadline` - Remove deadline
- `--priority <p1-p4>` - New priority
- `--labels <a,b>` - Replace labels
- `--description <text>` - New description
- `--assignee <ref>` - Assign to user
- `--unassign` - Remove assignee
- `--duration <time>` - Duration

### Complete Task

```bash
td task complete <ref>
```

### Reopen Task

```bash
td task uncomplete id:xxx
```

Note: Uncomplete requires the task ID (id:xxx format).

### Delete Task

```bash
td task delete <ref>
```

### Move Task

```bash
td task move <ref> --project "New Project"
td task move <ref> --section <section-id>
td task move <ref> --parent <task-ref>
```

### Open in Browser

```bash
td task browse <ref>
```

## Projects

### List Projects

```bash
td project list                     # Human-readable tree
td project list --json              # JSON array
td project list --personal --json   # Personal projects only
```

### View Project

```bash
td project view <ref>
td project view <ref> --json
```

### Create Project

```bash
td project create --name "Project Name" \
  --color "blue" \
  --parent "Parent Project" \
  --view-style board \
  --favorite
```

**Options:**
- `--name <name>` - Project name (required)
- `--color <color>` - Colour name
- `--parent <ref>` - Parent project for nesting
- `--view-style <style>` - "list" or "board"
- `--favorite` - Mark as favourite

### Update Project

```bash
td project update <ref> --name "New Name" --color "red"
```

### Archive/Unarchive Project

```bash
td project archive <ref>
td project unarchive <ref>
```

### Delete Project

```bash
td project delete <ref>
```

Note: Project must have no uncompleted tasks.

### List Collaborators

```bash
td project collaborators <ref>
```

## Sections

### List Sections

```bash
td section list <project>           # Human-readable
td section list <project> --json    # JSON array
```

### Create Section

```bash
td section create --name "Section Name" --project "Project Name"
```

### Update Section

```bash
td section update <id> --name "New Name"
```

### Delete Section

```bash
td section delete <id>
```

## Labels

### List Labels

```bash
td label list              # Human-readable
td label list --json       # JSON array
```

### Create Label

```bash
td label create --name "label-name" --color "green" --favorite
```

### Update Label

```bash
td label update <ref> --name "new-name" --color "blue"
```

### Delete Label

```bash
td label delete <name>
```

## Comments

### List Comments

```bash
td comment list <task-ref>                    # Comments on task
td comment list <project-ref> --project       # Comments on project
```

### Add Comment

```bash
td comment add <task-ref> --content "Comment text"
td comment add <project-ref> --project --content "Comment text"
```

### Update Comment

```bash
td comment update <id> --content "Updated text"
```

### Delete Comment

```bash
td comment delete <id>
```

## Reminders

### List Reminders

```bash
td reminder list <task-ref>
```

### Add Reminder

```bash
td reminder add <task-ref> --due "tomorrow 9am"
```

### Delete Reminder

```bash
td reminder delete <id>
```

## Filters

### List Saved Filters

```bash
td filter list --json
```

### Show Tasks Matching Filter

```bash
td filter show <filter-ref> --json
```

### Create Filter

```bash
td filter create --name "My Filter" --query "today & p1"
```

## Completed Tasks

```bash
td completed                              # Today's completed tasks
td completed --since 2024-01-01           # Since specific date
td completed --project "Work" --json      # Filtered JSON output
td completed --all --json                 # All completed (no limit)
```

**Options:**
- `--since <date>` - Start date (YYYY-MM-DD), default: today
- `--until <date>` - End date (YYYY-MM-DD), default: tomorrow
- `--project <name>` - Filter by project

## Activity and Stats

```bash
td activity                  # Recent activity
td stats                     # Productivity stats and karma
```

## Pagination

For large result sets, use `--all` to fetch everything, or handle pagination with cursors:

```bash
# First page
result=$(td task list --json --limit 50)

# If there's a next_cursor in the response, continue
cursor=$(echo "$result" | jq -r '.[-1].id // empty')
td task list --json --limit 50 --cursor "$cursor"
```

## Reference Resolution

The `<ref>` parameter in commands accepts:
- Task/project/label name (partial match supported)
- `id:xxx` for exact ID match
- Numeric ID (interpreted as id:xxx)

## Additional Reference

For detailed information on specific topics, consult:
- `references/completed-tasks.md` - Alternative methods for completed task history via API
- `references/filters.md` - Todoist filter query syntax for `--filter` flag

## Workflow Summary

1. **Verify authentication** - `td auth status`
2. **Read operations** - Execute directly without confirmation
3. **Write operations** - Ask for confirmation before executing
4. **Use JSON output** - Add `--json` flag for machine-readable data
5. **Handle large datasets** - Use `--all` or pagination with `--cursor`
