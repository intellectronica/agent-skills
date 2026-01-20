---
name: here-be-git
description: Initialise a git repository with optional agent commit instructions and .gitignore. Use when users say "here be git", "init git", "initialise git", or otherwise indicate they want to set up version control in the current directory.
---

# Here Be Git

Initialise a git repository with optional configuration for agent workflows.

## Workflow

### Step 1: Initialise Git Repository

Run `git init` in the current working directory. Confirm to the user that the repository has been initialised.

### Step 2: Agent Commit Instructions

Ask the user:

> Would you like me to add instructions for the agent to always commit when it's done with a task?

If the user confirms:

1. Check if `AGENTS.md` exists in the current directory
2. If it exists, append the commit instructions to it
3. If it doesn't exist, create it with the commit instructions

The commit instructions to add:

```markdown
## Git Workflow

- Always commit your changes when you have completed a task or reached a logical stopping point
- Use clear, descriptive commit messages that explain what was done and why
- Ensure the working directory is clean (all changes committed) before ending your session
```

After creating or updating `AGENTS.md`:

1. Check if `CLAUDE.md` exists in the current directory
2. If it doesn't exist, create it with just `@AGENTS.md` followed by a newline
3. If it exists but doesn't already have `@AGENTS.md` at the top, prepend `@AGENTS.md` followed by a newline to the existing content
4. Commit both files together with an appropriate message

### Step 3: Gitignore Configuration

Ask the user:

> Would you like me to create a .gitignore? If so, what flavour or patterns should I include? (e.g., Node.js, Python, macOS, IDE files, or specific files/patterns)

If the user provides a flavour or patterns:

1. Generate an appropriate `.gitignore` based on their input
2. For common flavours, include standard patterns:
   - **Node.js**: `node_modules/`, `dist/`, `.env`, `*.log`, etc.
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.env`, `*.egg-info/`, etc.
   - **macOS**: `.DS_Store`, `.AppleDouble`, `.LSOverride`, `._*`
   - **IDE files**: `.idea/`, `.vscode/`, `*.swp`, `*.swo`, `*.sublime-*`
3. Include any specific files or patterns the user mentions
4. Commit the `.gitignore` with an appropriate message

If the user declines, skip this step.

## Notes

- If git is already initialised in the directory, inform the user and skip to Step 2
- Use the AskUserQuestion tool for the confirmation prompts
- Keep commits atomic and well-described
