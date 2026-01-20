---
name: promptify
description: Transform user requests into detailed, precise prompts for AI models. Use when users say "promptify", "promptify this", or explicitly request prompt engineering or improvement of their request for better AI responses.
---

# Promptify

Transform user requests into detailed, precise prompts optimised for AI model consumption.

## Core Task

Rewrite the user's request as a clear, specific, and complete prompt that guides an AI model to produce the desired output without ambiguity. Treat the output as specification language, not casual natural language.

## Process

1. **Read and understand** - Read the user's request carefully to understand the full context, intent, and all details
2. **Plan the rewrite** - Consider what specific information, instructions, or context the AI model needs to fulfill the request effectively
3. **Rewrite as a detailed prompt** - Transform the request into a precise prompt with clarity, specificity, and completeness

## Writing Guidelines

### Structure

- Begin with a single short paragraph summarising the overall task
- Use headings (##, ###, ####) for sections only where appropriate (no first-level title)
- Use **bold**, _italics_, bullet points (`-`), and numbered lists (1., 2.) liberally for organisation
- Never use emojis
- Never use `*` for bullet points, always use `-`

### Language

- Use plain, straightforward, precise language
- Avoid embellishments, niceties, or creative flourishes
- Think of language as specification/code, not natural language
- Be clear and specific in all instructions

### Content

- Keep the prompt concise: 0.75X to 1.5X the length of the original request
- Do not add or invent information not present in the input
- Do not include unnecessary complexity or verbosity

## Output

Provide only the final prompt as markdown, without additional commentary or explanation.
