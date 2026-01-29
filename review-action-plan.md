# Review Action Implementation Plan

A GitHub Actions workflow that runs the improvebot skill reviewer on a schedule and on-demand.

## Overview

The workflow will:
1. Run weekly on Friday at 16:00 CET (15:00 UTC)
2. Support manual dispatch via `workflow_dispatch`
3. Run on push to `main` or `reviewbot` branches
4. Install bun and GitHub Copilot CLI
5. Authenticate using repository secrets
6. Execute `improvebot/review.ts --limit 3`

## Workflow Triggers

```yaml
on:
  schedule:
    - cron: '0 15 * * 5'  # 15:00 UTC = 16:00 CET, every Friday
  workflow_dispatch:       # Manual trigger
  push:
    branches:
      - main
      - reviewbot
```

**Note:** GitHub Actions cron uses UTC. 16:00 CET = 15:00 UTC (during standard time). During CEST (summer), this will run at 17:00 local time.

## Required Secrets

| Secret | Purpose | How to Create |
|--------|---------|---------------|
| `COPILOT_PAT` | Authenticates Copilot CLI for API access | Create a [fine-grained PAT](https://github.com/settings/personal-access-tokens/new) with **Copilot Requests: Read** permission |
| `GH_PAT` | Authenticates `gh` CLI for issue creation | Create a PAT with **Issues: Read and write** permission for this repository |

These are existing repository secrets.

## Workflow Steps

### 1. Checkout Repository

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

### 2. Setup Node.js

Node.js 22+ is required for the Copilot CLI.

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 22
```

### 3. Setup Bun

Using the official [oven-sh/setup-bun](https://github.com/oven-sh/setup-bun) action.

```yaml
- name: Setup Bun
  uses: oven-sh/setup-bun@v2
```

### 4. Install GitHub Copilot CLI

```yaml
- name: Install GitHub Copilot CLI
  run: npm install -g @github/copilot
```

### 5. Run Improvebot Review Script

The Copilot CLI uses `GH_TOKEN` or `GITHUB_TOKEN` environment variables for authentication (in order of precedence). The `gh` CLI also uses `GH_TOKEN`.

```yaml
- name: Run skill review
  env:
    GH_TOKEN: ${{ secrets.COPILOT_PAT }}
    GH_PAT: ${{ secrets.GH_PAT }}
  run: bun run improvebot/review.ts --limit 3
```

**Note:** Two separate tokens are used:
- `COPILOT_PAT` → `GH_TOKEN` for Copilot CLI authentication
- `GH_PAT` for `gh` CLI issue creation (requires modification to `review.ts` to use this env var)

## Complete Workflow File

Save as `.github/workflows/skill-review.yml`:

```yaml
name: Skill Review

on:
  schedule:
    - cron: '0 15 * * 5'  # 16:00 CET every Friday
  workflow_dispatch:
  push:
    branches:
      - main
      - reviewbot

jobs:
  review-skills:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2

      - name: Install GitHub Copilot CLI
        run: npm install -g @github/copilot

      - name: Run skill review
        env:
          GH_TOKEN: ${{ secrets.COPILOT_PAT }}
          GH_PAT: ${{ secrets.GH_PAT }}
        run: bun run improvebot/review.ts --limit 3
```

## Script Modification Required

The `improvebot/review.ts` script currently uses `gh issue create` which reads `GH_TOKEN`. Since `GH_TOKEN` is set to the Copilot token, the script needs modification to use `GH_PAT` for issue creation:

```typescript
// In createGitHubIssue function, prefix the command with the env var:
execSync(
  `GH_TOKEN="${process.env.GH_PAT}" gh issue create --title "${title.replace(/"/g, '\\"')}" --body "$(cat <<'EOF'\n${body}\nEOF\n)"`,
  { stdio: "inherit" }
);
```

Alternatively, set `GITHUB_TOKEN` instead of `GH_TOKEN` for Copilot (lower precedence), but this may conflict with the auto-provided token.

## Secrets Summary

The repository should already have these secrets configured:

| Secret | Required Permissions |
|--------|---------------------|
| `COPILOT_PAT` | Account: Copilot Requests (Read) |
| `GH_PAT` | Repository: Issues (Read and write) |

## Considerations

### Rate Limits

- With `--limit 3`, each run reviews 3 skills
- Each skill review uses Copilot API (gpt-5.2-codex model)
- Premium model requests may consume quota depending on subscription tier

### Error Handling

The current script continues on individual skill failures. If the Copilot CLI or authentication fails, the entire workflow will fail.

### Dry Run Option

For testing, consider adding a workflow input:

```yaml
on:
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Run without creating issues'
        type: boolean
        default: false
```

Then modify the run step:
```yaml
run: |
  FLAGS="--limit 3"
  if [ "${{ inputs.dry_run }}" = "true" ]; then
    FLAGS="$FLAGS --dry-run"
  fi
  bun run improvebot/review.ts $FLAGS
```

## Implementation Checklist

- [ ] Modify `improvebot/review.ts` to use `GH_PAT` env var for `gh` CLI
- [ ] Create `.github/workflows/skill-review.yml`
- [ ] Test with manual dispatch and `--dry-run` first
- [ ] Remove `reviewbot` branch trigger once merged to main

## References

- [GitHub Copilot CLI Installation](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- [Copilot CLI Authentication Methods](https://deepwiki.com/github/copilot-cli/4.1-authentication-methods)
- [oven-sh/setup-bun Action](https://github.com/oven-sh/setup-bun)
- [Using Copilot CLI in GitHub Actions](https://dev.to/vevarunsharma/injecting-ai-agents-into-cicd-using-github-copilot-cli-in-github-actions-for-smart-failures-58m8)
