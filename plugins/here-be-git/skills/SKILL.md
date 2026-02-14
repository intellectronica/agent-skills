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
## Git Workflow — CRITICAL, MANDATORY, NO EXCEPTIONS

> **THIS IS NOT OPTIONAL.** Every agent operating in this repository MUST follow this workflow after every change, no matter how small. There are ZERO exceptions to this rule. Skipping a commit is never acceptable. If you have made any change to any file, you MUST commit before moving on.

### Rules

1. **ALWAYS commit your changes immediately after completing a task or reaching any logical stopping point.** Do not defer. Do not batch. Do not skip.
2. **ALWAYS commit before ending your session.** The working directory MUST be clean (all changes committed) when you finish. Leaving uncommitted changes is a failure state.
3. **Use clear, descriptive commit messages** that explain what was done and why.
4. **If in doubt, commit.** It is always better to have one commit too many than one too few.

### To be absolutely clear

- "I'll commit later" — **No. Commit now.**
- "It's just a small change" — **Commit it.**
- "I'm about to make another change" — **Commit the current one first.**
- "The user didn't ask me to commit" — **Irrelevant. Commit anyway.**
```

After creating or updating `AGENTS.md`, commit it with an appropriate message.

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
