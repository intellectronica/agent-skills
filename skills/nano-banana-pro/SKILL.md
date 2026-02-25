---
name: nano-banana-pro
description: Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) API. Use when the user asks to generate, create, edit, modify, change, alter, or update images. Also use when user references an existing image file and asks to modify it in any way (e.g., "modify this image", "change the background", "replace X with Y"). Supports both text-to-image generation and image-to-image editing with configurable resolution (1K default, 2K, or 4K for high resolution). DO NOT read the image file first - use this skill directly with the --input-image parameter.
---

# Nano Banana Pro Image Generation & Editing

Generate new images or edit existing ones using Google's Nano Banana Pro API (Gemini 3 Pro Image).

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**Edit existing image:**
```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--resolution 1K|2K|4K] [--api-key KEY]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| `--resolution` | `1K` (~1024px), `2K` (~2048px), `4K` (~4096px) | `1K` |
| `--api-key` | API key string | Falls back to `GEMINI_API_KEY` env var |

## Filename Generation

Pattern: `yyyy-mm-dd-hh-mm-ss-descriptive-name.png`

Example: `2025-11-23-14-23-05-japanese-garden.png`. Keep the descriptive part concise (1–5 hyphenated words from the prompt). If unclear, use a random identifier.

## Workflow

1. **Determine mode**: generation (no input image) or editing (`--input-image` provided)
2. **Build command**: set `--prompt`, `--filename`, and optional `--resolution`/`--input-image`
3. **Execute**: run the script from the user's working directory
4. **Validate**: verify the output file exists (`ls` or `stat`) before confirming to the user
5. **Report**: inform the user of the saved file path — do not read the image back

**Prompt handling**: pass the user's description as-is to `--prompt`. For editing, use editing instructions (e.g., "make the sky more dramatic"). Preserve user intent.

## Error Handling

- **Missing API key**: script exits with an error — prompt the user to set `GEMINI_API_KEY`
- **Rate limit / 429**: wait and retry once after a few seconds
- **Invalid image format**: ensure input images are PNG or JPEG; convert if necessary
- **Script failure**: check stderr output and report the error message to the user

## Examples

**Generate new image:**
```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**Edit existing image:**
```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```
