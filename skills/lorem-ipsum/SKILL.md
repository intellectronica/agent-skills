---
name: lorem-ipsum
description: Generate lorem ipsum placeholder text. This skill should be used when users ask to generate lorem ipsum content, placeholder text, dummy text, or filler text. Supports various structures including plain paragraphs, headings with sections, lists, and continuous text. Output can be saved to a file or used directly as requested by the user.
---

# Lorem Ipsum Generator

## Overview

Generate lorem ipsum placeholder text using the bundled generator script. **Always use the script** to generate content rather than writing lorem ipsum directly.

**Critical requirement**: ALL text in the generated output must be lorem ipsum, including headings, bullet points, list items, table cells, and any other textual elements.

## Generator Script

Use `scripts/generate.py` to produce lorem ipsum content. The script handles all text generation to ensure consistent, authentic lorem ipsum output.

### Basic Usage

```bash
# Generate 3 paragraphs (default)
uv run scripts/generate.py

# Generate 5 paragraphs with 4 sentences each
uv run scripts/generate.py --paragraphs 5 --sentences 4

# Generate approximately 500 words
uv run scripts/generate.py --words 500

# Generate exactly 1000 characters
uv run scripts/generate.py --characters 1000

# Generate approximately 200 LLM tokens (~800 characters)
uv run scripts/generate.py --tokens 200

# Continuous text without paragraph breaks
uv run scripts/generate.py --paragraphs 4 --continuous
```

### Structured Content

```bash
# 3 sections with headings and 2 paragraphs each
uv run scripts/generate.py --headings 3 --paragraphs 6

# 4 sections with bullet points (5 bullets each)
uv run scripts/generate.py --headings 4 --bullets 5

# Numbered lists instead of bullets
uv run scripts/generate.py --headings 3 --bullets 6 --numbered

# Realistic mixed document with 5 sections (varied content types)
uv run scripts/generate.py --mixed 5
```

The `--mixed` option generates realistic documents with varied structure per section:
- Some sections have paragraphs only
- Some have bullet or numbered lists
- Some have subheadings (h3) with nested content
- Some combine paragraphs with lists

### Output Options

```bash
# Write to file
uv run scripts/generate.py --paragraphs 3 --output ~/Desktop/placeholder.txt

# HTML format
uv run scripts/generate.py --headings 2 --format html --output page.html

# Plain text (no markdown formatting)
uv run scripts/generate.py --format text

# Copy to clipboard
uv run scripts/generate.py --words 200 | pbcopy
```

### All Options

| Option | Description |
|--------|-------------|
| `--paragraphs N` | Number of paragraphs (default: 3) |
| `--sentences N` | Sentences per paragraph (default: 5) |
| `--words N` | Approximate total word count |
| `--characters N` | Exact character count (truncates to match) |
| `--tokens N` | Estimated LLM token count (~4 chars/token) |
| `--continuous` | Output without paragraph breaks |
| `--headings N` | Number of sections with headings |
| `--bullets N` | Bullet points per section |
| `--numbered` | Use numbered lists instead of bullets |
| `--mixed N` | Realistic document with N sections, varied content types |
| `--output FILE` | Write to file instead of stdout |
| `--format FORMAT` | Output format: text, markdown, html (default: markdown) |

## Workflow

1. Interpret the user's request for length and structure
2. Run `scripts/generate.py` with appropriate options
3. If the user wants the output saved, use `--output` or redirect/pipe as needed
4. If the user wants it in clipboard, pipe to `pbcopy`
5. Display the result or confirm the file was written

## Examples

**"Generate 3 paragraphs of lorem ipsum"**
```bash
uv run scripts/generate.py --paragraphs 3
```

**"Create lorem ipsum with 3 headings and 2 paragraphs under each"**
```bash
uv run scripts/generate.py --headings 3 --paragraphs 6
```

**"Give me a document with bullet points"**
```bash
uv run scripts/generate.py --headings 3 --bullets 5
```

**"500 words of continuous lorem ipsum saved to ~/Desktop/placeholder.txt"**
```bash
uv run scripts/generate.py --words 500 --continuous --output ~/Desktop/placeholder.txt
```

**"Lorem ipsum with numbered lists in HTML format"**
```bash
uv run scripts/generate.py --headings 4 --bullets 5 --numbered --format html
```

**"Exactly 500 characters of lorem ipsum"**
```bash
uv run scripts/generate.py --characters 500
```

**"About 100 tokens worth of lorem ipsum with headings"**
```bash
uv run scripts/generate.py --tokens 100 --headings 2
```

**"A realistic document with mixed content"**
```bash
uv run scripts/generate.py --mixed 5
```
