# Other Services Reference

Guide to Classroom, Chat, Contacts, Tasks, People, Groups, and Keep.

## Google Classroom

### Courses

```bash
# List courses
gog classroom courses
gog classroom courses --state ACTIVE
gog classroom courses --state ARCHIVED

# Get course details
gog classroom courses get <courseId>

# Create course
gog classroom courses create --name "Physics 101"
gog classroom courses create --name "Physics 101" --owner me --state ACTIVE

# Update course
gog classroom courses update <courseId> --name "Physics 102"
gog classroom courses update <courseId> --state ARCHIVED

# Delete course
gog classroom courses delete <courseId>

# Archive/unarchive
gog classroom courses archive <courseId>
gog classroom courses unarchive <courseId>

# Join/leave course
gog classroom courses join <courseId> --role student
gog classroom courses leave <courseId>

# Get course URLs
gog classroom courses url <courseId1> <courseId2>
```

### Students & Teachers

```bash
# List students
gog classroom students <courseId>

# Get student
gog classroom students get <courseId> <userId>

# Add student
gog classroom students add <courseId> user@example.com
gog classroom students add <courseId> user@example.com --enrollment-code CODE

# Remove student
gog classroom students remove <courseId> <userId>

# List teachers
gog classroom teachers <courseId>

# Add/remove teachers
gog classroom teachers add <courseId> teacher@example.com
gog classroom teachers remove <courseId> <userId>

# Full roster
gog classroom roster <courseId>
gog classroom roster <courseId> --students
gog classroom roster <courseId> --teachers
```

### Coursework

```bash
# List coursework
gog classroom coursework <courseId>
gog classroom coursework <courseId> --state PUBLISHED
gog classroom coursework <courseId> --topic <topicId>

# Get coursework
gog classroom coursework get <courseId> <courseworkId>

# Create assignment
gog classroom coursework create <courseId> \
  --title "Homework 1" \
  --description "Complete exercises 1-10" \
  --type ASSIGNMENT \
  --due "2024-12-31T23:59:59Z" \
  --max-points 100

# Update coursework
gog classroom coursework update <courseId> <courseworkId> --title "Updated Title"

# Delete coursework
gog classroom coursework delete <courseId> <courseworkId>

# Manage assignees
gog classroom coursework assignees <courseId> <courseworkId> --mode ALL_STUDENTS
gog classroom coursework assignees <courseId> <courseworkId> \
  --mode INDIVIDUAL_STUDENTS \
  --add-student user1@example.com
```

### Submissions

```bash
# List submissions
gog classroom submissions <courseId> <courseworkId>
gog classroom submissions <courseId> <courseworkId> --state TURNED_IN

# Get submission
gog classroom submissions get <courseId> <courseworkId> <submissionId>

# Turn in submission
gog classroom submissions turn-in <courseId> <courseworkId> <submissionId>

# Reclaim submission
gog classroom submissions reclaim <courseId> <courseworkId> <submissionId>

# Return submission
gog classroom submissions return <courseId> <courseworkId> <submissionId>

# Grade submission
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 95
```

### Materials

```bash
# List materials
gog classroom materials <courseId>

# Create/update/delete materials
gog classroom materials create <courseId> --title "Lecture Notes"
gog classroom materials update <courseId> <materialId> --title "Updated Notes"
gog classroom materials delete <courseId> <materialId>
```

### Announcements

```bash
# List announcements
gog classroom announcements <courseId>

# Create announcement
gog classroom announcements create <courseId> --text "Class cancelled tomorrow"

# Update/delete
gog classroom announcements update <courseId> <announcementId> --text "Updated text"
gog classroom announcements delete <courseId> <announcementId>
```

### Topics

```bash
# List topics
gog classroom topics <courseId>

# Create topic
gog classroom topics create <courseId> --name "Unit 1"

# Update/delete
gog classroom topics update <courseId> <topicId> --name "Unit 1: Introduction"
gog classroom topics delete <courseId> <topicId>
```

### Guardians

```bash
# List guardians
gog classroom guardians <studentId>

# List guardian invitations
gog classroom guardian-invitations <studentId>

# Invite guardian
gog classroom guardian-invitations create <studentId> --email parent@example.com
```

### Profile

```bash
gog classroom profile
gog classroom profile <userId>
```

---

## Google Chat (Workspace)

### Spaces

```bash
# List spaces
gog chat spaces list

# Find space by name
gog chat spaces find "Team Chat"

# Create space
gog chat spaces create "Project Discussion"
gog chat spaces create "Project Discussion" --member user1@example.com --member user2@example.com
```

### Messages

```bash
# List messages in space
gog chat messages list <spaceId>
gog chat messages list <spaceId> --max 50
gog chat messages list <spaceId> --unread

# List messages in thread
gog chat messages list <spaceId> --thread <threadId>

# Send message
gog chat messages send <spaceId> --text "Hello team!"

# Reply to thread
gog chat messages send <spaceId> --text "Reply" --thread <threadId>
```

### Threads

```bash
gog chat threads list <spaceId>
```

### Direct Messages

```bash
# Get/create DM space with user
gog chat dm space user@example.com

# Send DM
gog chat dm send user@example.com --text "Hi there!"

# Reply to DM thread
gog chat dm send user@example.com --text "Reply" --thread <threadId>
```

---

## Google Tasks

### Task Lists

```bash
# List task lists
gog tasks lists

# Create task list
gog tasks lists create "Personal"
```

### Tasks

```bash
# List tasks in list
gog tasks list <tasklistId>

# Get task
gog tasks get <tasklistId> <taskId>

# Add task
gog tasks add <tasklistId> --title "Buy groceries"

# Add task with details
gog tasks add <tasklistId> \
  --title "Project deadline" \
  --notes "Submit final report" \
  --due "2024-12-31"

# Add repeating task
gog tasks add <tasklistId> \
  --title "Weekly review" \
  --due "2024-12-20" \
  --repeat weekly

# Repeat options: daily, weekly, monthly, yearly
gog tasks add <tasklistId> \
  --title "Monthly report" \
  --due "2024-12-01" \
  --repeat monthly \
  --repeat-count 12                # Repeat 12 times

gog tasks add <tasklistId> \
  --title "Daily standup" \
  --due "2024-12-01" \
  --repeat daily \
  --repeat-until "2024-12-31"      # Repeat until date

# Update task
gog tasks update <tasklistId> <taskId> --title "Updated title"
gog tasks update <tasklistId> <taskId> --notes "Updated notes"
gog tasks update <tasklistId> <taskId> --due "2024-12-25"

# Complete task
gog tasks done <tasklistId> <taskId>

# Uncomplete task
gog tasks undo <tasklistId> <taskId>

# Delete task
gog tasks delete <tasklistId> <taskId>

# Clear completed tasks from list
gog tasks clear <tasklistId>
```

### Subtasks

```bash
# Add subtask
gog tasks add <tasklistId> --title "Subtask" --parent <parentTaskId>

# Add after specific task
gog tasks add <tasklistId> --title "Task" --previous <previousTaskId>
```

---

## Google Contacts

### Search & List

```bash
# Search contacts
gog contacts search "john"

# List all contacts
gog contacts list
gog contacts list --max 100
```

### CRUD Operations

```bash
# Get contact
gog contacts get people/c1234567890
gog contacts get john@example.com

# Create contact
gog contacts create --given "John" --family "Doe"
gog contacts create --given "John" --email "john@example.com" --phone "+1234567890"

# Update contact
gog contacts update people/c1234567890 --given "Jonathan"
gog contacts update people/c1234567890 --email "new@example.com"

# Delete contact
gog contacts delete people/c1234567890
```

### Workspace Directory

```bash
# List directory
gog contacts directory list

# Search directory
gog contacts directory search "smith"
```

### Other Contacts

```bash
# List "other contacts" (auto-added from interactions)
gog contacts other list

# Search other contacts
gog contacts other search "jane"
```

---

## Google People

```bash
# Get own profile
gog people me

# Get user profile
gog people get people/c1234567890
gog people get user@example.com

# Search people
gog people search "john smith"

# Get relations
gog people relations
gog people relations people/c1234567890 --type manager
```

---

## Google Groups (Workspace)

```bash
# List groups
gog groups list

# Get group info
gog groups get group@example.com

# List group members
gog groups members group@example.com
```

---

## Google Keep (Workspace Only)

Requires service account authentication.

```bash
# List notes
gog keep list

# Get note
gog keep get <noteId>

# Create text note
gog keep create --title "Shopping List" --text "Milk, Eggs, Bread"

# Create checklist note
gog keep create --title "Todo" --list "Task 1,Task 2,Task 3"

# Delete note
gog keep delete <noteId>
```

---

## Time Utilities

```bash
# Get current time
gog time now

# Get time in specific timezone
gog time now --timezone America/New_York
gog time now --timezone Europe/London
gog time now --timezone Asia/Tokyo
```
