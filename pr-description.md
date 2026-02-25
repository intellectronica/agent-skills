Hullo @intellectronica 👋

I ran your skills through `tessl skill review` at work and found some targeted improvements. Here's the before/after:

| Skill | Before | After | Change |
|-------|--------|-------|--------|
| tavily | 75% | 96% | +21% |
| anki-connect | 76% | 89% | +13% |
| notion-api | 79% | 94% | +15% |
| beautiful-mermaid | 80% | 93% | +13% |
| mgrep-code-search | 81% | 96% | +15% |
| gpt-image-1-5 | 83% | 93% | +10% |
| nano-banana-pro | 86% | 100% | +14% |
| todoist-api | 88% | 100% | +12% |
| promptify | 88% | 95% | +7% |

<details><summary>Summary of changes</summary>

Key changes across 9 skills:

- **Expanded descriptions with concrete actions and natural trigger terms** — replaced generic category mentions with specific verbs (e.g., "CRUD operations" → "create tasks, list projects, update due dates") and added natural user phrases ("flashcards", "spaced repetition", "todo list", "look up online")
- **Removed content redundancy** — consolidated duplicate Purpose/When to Use sections in tavily, trimmed explanations of concepts Claude already knows (UUID format, ISO 8601, pagination basics) from notion-api, condensed verbose parameter mapping tables in gpt-image-1-5 and nano-banana-pro
- **Added error handling and validation steps** — gpt-image-1-5, nano-banana-pro, and mgrep-code-search now include troubleshooting guidance and explicit validation checkpoints
- **Improved workflow clarity** — added polling workflow with timing for tavily research endpoint, restructured nano-banana-pro into a clear 5-step workflow with validation
- **Added concrete before/after example** to promptify demonstrating the expected transformation
- 11 skills unchanged (already scoring 85%+)

</details>

Honest disclosure — I work at @tesslio where we build tooling around skills like these. Not a pitch, just saw room for improvement and wanted to contribute.

If you want to run evals yourself, click [here](https://tessl.io/registry/skills/submit).

Thanks in advance 🙏
