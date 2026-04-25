# Other Services Reference

Use this for Chat, Classroom, Contacts, Tasks, People, Groups, Admin, Keep, and local time helpers.

## Chat (Workspace)

Chat commands require Google Workspace; consumer Gmail accounts are not supported.

Spaces:

```bash
gog chat spaces list
gog chat spaces find "Engineering"
gog chat spaces find "Engineering" --exact
gog chat spaces create "Project Room" --member alice@example.com --member bob@example.com
```

Messages and threads:

```bash
gog chat messages list spaces/<spaceId> --max 50
gog chat messages list spaces/<spaceId> --thread spaces/<spaceId>/threads/<threadId>
gog chat messages list spaces/<spaceId> --unread
gog chat messages send spaces/<spaceId> --text "Build complete"
gog chat messages send spaces/<spaceId> --text "Reply" --thread spaces/<spaceId>/threads/<threadId>
gog chat threads list spaces/<spaceId>
```

Reactions:

```bash
gog chat messages reactions list spaces/<spaceId>/messages/<messageId>
gog chat messages react spaces/<spaceId>/messages/<messageId> <emoji>
gog chat messages reactions create spaces/<spaceId>/messages/<messageId> <emoji>
gog chat messages reactions delete spaces/<spaceId>/messages/<messageId>/reactions/<reactionId>
```

Direct messages:

```bash
gog chat dm space user@example.com
gog chat dm send user@example.com --text "Ping"
gog chat dm send user@example.com --text "Reply" --thread spaces/<spaceId>/threads/<threadId>
```

## Classroom

Classroom commands generally require Google Workspace for Education. Personal accounts have limited support.

Courses:

```bash
gog classroom courses list
gog classroom courses list --role teacher
gog classroom courses get <courseId>
gog classroom courses create --name "Physics 101" --owner me --state ACTIVE
gog classroom courses update <courseId> --name "Physics 102"
gog classroom courses archive <courseId>
gog classroom courses unarchive <courseId>
gog classroom courses delete <courseId>
gog classroom courses url <courseId>
```

Roster:

```bash
gog classroom roster <courseId>
gog classroom roster <courseId> --students
gog classroom roster <courseId> --teachers
gog classroom students list <courseId>
gog classroom students get <courseId> <userId>
gog classroom students add <courseId> <userId>
gog classroom students remove <courseId> <userId>
gog classroom teachers list <courseId>
gog classroom teachers add <courseId> <userId>
gog classroom teachers remove <courseId> <userId>
```

Coursework and materials:

```bash
gog classroom coursework list <courseId>
gog classroom coursework list <courseId> --state PUBLISHED --topic <topicId>
gog classroom coursework get <courseId> <courseworkId>
gog classroom coursework create <courseId> --title "Homework 1" --type ASSIGNMENT --state PUBLISHED --due "2026-05-01T23:59:59Z" --max-points 100
gog classroom coursework update <courseId> <courseworkId> --title "Updated"
gog classroom coursework assignees <courseId> <courseworkId> --mode INDIVIDUAL_STUDENTS --add-student <studentId>
gog classroom coursework delete <courseId> <courseworkId>

gog classroom materials list <courseId>
gog classroom materials get <courseId> <materialId>
gog classroom materials create <courseId> --title "Syllabus" --state PUBLISHED
gog classroom materials update <courseId> <materialId> --title "Updated"
gog classroom materials delete <courseId> <materialId>
```

Submissions:

```bash
gog classroom submissions list <courseId> <courseworkId>
gog classroom submissions list <courseId> <courseworkId> --state TURNED_IN
gog classroom submissions get <courseId> <courseworkId> <submissionId>
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 95
gog classroom submissions return <courseId> <courseworkId> <submissionId>
gog classroom submissions turn-in <courseId> <courseworkId> <submissionId>
gog classroom submissions reclaim <courseId> <courseworkId> <submissionId>
```

Announcements, topics, invitations, guardians, profile:

```bash
gog classroom announcements list <courseId>
gog classroom announcements create <courseId> --text "Welcome"
gog classroom announcements update <courseId> <announcementId> --text "Updated"
gog classroom announcements assignees <courseId> <announcementId> --mode INDIVIDUAL_STUDENTS --add-student <studentId>
gog classroom announcements delete <courseId> <announcementId>

gog classroom topics list <courseId>
gog classroom topics create <courseId> --name "Unit 1"
gog classroom topics update <courseId> <topicId> --name "Unit 2"
gog classroom topics delete <courseId> <topicId>

gog classroom invitations list
gog classroom invitations create <courseId> <userId> --role student
gog classroom invitations accept <invitationId>
gog classroom invitations delete <invitationId>

gog classroom guardians list <studentId>
gog classroom guardians get <studentId> <guardianId>
gog classroom guardians delete <studentId> <guardianId>
gog classroom guardian-invitations list <studentId>
gog classroom guardian-invitations create <studentId> --email parent@example.com

gog classroom profile get
gog classroom profile get <userId>
```

## Contacts

Search/list/get:

```bash
gog contacts search "Ada"
gog contacts list --max 100
gog contacts get people/c1234567890
gog contacts get ada@example.com
```

Create/update:

```bash
gog contacts create --given "Ada" --family "Lovelace" --email ada@example.com --phone "+41441234567"
gog contacts create --given "Ada" --org "Analytical Engines Ltd" --title "Programmer" --url https://example.com --custom source=gog
gog contacts create --given "Ada" --address "street=1 Main St;city=Zurich;country=CH" --relation manager=Grace

gog contacts update people/c1234567890 --given "Ada" --email ada@new.example
gog contacts update people/c1234567890 --birthday "1815-12-10"
gog contacts update people/c1234567890 --from-file contact.json
gog contacts update people/c1234567890 --from-file - --ignore-etag
gog contacts delete people/c1234567890
```

Workspace directory and other contacts:

```bash
gog contacts directory list
gog contacts directory search "smith"
gog contacts other list
gog contacts other search "jane"
gog contacts other delete people/other...
```

For bulk or precise People API payload updates, prefer `contacts update --from-file` after inspecting `contacts get --json`.

## Tasks

Task lists:

```bash
gog tasks lists
gog tasks lists create "Personal"
```

Tasks:

```bash
gog tasks list <tasklistId>
gog tasks get <tasklistId> <taskId>
gog tasks add <tasklistId> --title "Buy groceries"
gog tasks add <tasklistId> --title "Project deadline" --notes "Submit final report" --due "2026-05-01"
gog tasks update <tasklistId> <taskId> --title "Updated title"
gog tasks update <tasklistId> <taskId> --due ""
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>
```

Repeating tasks materialize occurrences:

```bash
gog tasks add <tasklistId> --title "Weekly review" --due "2026-04-27" --repeat weekly
gog tasks add <tasklistId> --title "Monthly report" --due "2026-05-01" --repeat monthly --repeat-count 12
gog tasks add <tasklistId> --title "Daily standup" --due "2026-04-25" --repeat daily --repeat-until "2026-05-01"
gog tasks add <tasklistId> --title "Every other week" --due "2026-04-27" --recur-rrule "FREQ=WEEKLY;INTERVAL=2"
```

Subtasks/order:

```bash
gog tasks add <tasklistId> --title "Subtask" --parent <parentTaskId>
gog tasks add <tasklistId> --title "Next task" --previous <previousTaskId>
```

## People

```bash
gog people me
gog people get people/<userId>
gog people get user@example.com
gog people search "Ada Lovelace" --max 5
gog people relations
gog people relations people/<userId> --type manager
```

`people search` is for Workspace directory/profile-style lookup; use `contacts search` for personal contacts.

## Groups

Groups commands use Cloud Identity and require Workspace scopes.

```bash
gog groups list
gog groups members engineering@example.com
```

If scopes are missing:

```bash
gog auth add you@example.com --services groups --force-consent
```

## Admin (Workspace)

Admin commands require a Workspace service account with domain-wide delegation and Admin SDK scopes.

Users:

```bash
gog admin users list --domain example.com
gog admin users get user@example.com
gog admin users create user@example.com --given Ada --family Lovelace --password 'TempPass123!'
gog admin users suspend user@example.com
```

Groups:

```bash
gog admin groups list --domain example.com
gog admin groups members list engineering@example.com
gog admin groups members add engineering@example.com user@example.com --role MEMBER
gog admin groups members remove engineering@example.com user@example.com
```

Treat Admin writes as high impact. Use `--dry-run` when supported and require explicit user intent.

## Keep (Workspace)

Google Keep requires Workspace service-account access/domain-wide delegation.

```bash
gog keep --service-account ~/service-account.json --impersonate user@example.com list
gog keep --service-account ~/service-account.json --impersonate user@example.com search "receipt"
gog keep --service-account ~/service-account.json --impersonate user@example.com get <noteId>
gog keep --service-account ~/service-account.json --impersonate user@example.com create --title "Shopping" --text "Milk\nEggs"
gog keep --service-account ~/service-account.json --impersonate user@example.com create --title "Todo" --item "Task 1" --item "Task 2"
gog keep --service-account ~/service-account.json --impersonate user@example.com attachment <attachmentName> --out ./file.bin
gog keep --service-account ~/service-account.json --impersonate user@example.com delete <noteId>
```

If a service account is configured for the impersonated account, normal account selection can be enough:

```bash
gog auth service-account set user@example.com --key ~/service-account.json
gog --account user@example.com keep list
```

## Time utilities

```bash
gog time now
gog time now --timezone UTC
gog time now --timezone Europe/Zurich
gog time now --timezone America/New_York
```

Use this for quick local/UTC conversions in scripts.
