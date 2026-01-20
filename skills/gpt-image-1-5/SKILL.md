---
name: gpt-image-1-5
description: Generate and edit images using OpenAI's GPT Image 1.5 model. Use when the user asks to generate, create, edit, modify, change, alter, or update images. Also use when user references an existing image file and asks to modify it in any way (e.g., "modify this image", "change the background", "replace X with Y"). Supports text-to-image generation and image editing with optional mask. DO NOT read the image file first - use this skill directly with the --input-image parameter.
---

# GPT Image 1.5 - Image Generation & Editing

Generate new images or edit existing ones using OpenAI's GPT Image 1.5 model.

- **Generation**: Uses the Responses API with image_generation tool
- **Editing**: Uses the Image API for reliable mask-based inpainting

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--quality low|medium|high] [--size 1024x1024|1024x1536|1536x1024|auto] [--background transparent|opaque|auto] [--api-key KEY]
```

**Edit existing image (without mask - full image edit):**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png" [--size 1024x1024|1024x1536|1536x1024|auto] [--api-key KEY]
```

**Edit existing image (with mask - precise inpainting):**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "what to put in masked area" --filename "output-name.png" --input-image "path/to/input.png" --mask "path/to/mask.png" [--size 1024x1024|1024x1536|1536x1024|auto] [--api-key KEY]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Parameters

### Quality Options
- **low** - Fastest generation, lower quality
- **medium** (default) - Balanced quality and speed
- **high** - Best quality, slower generation

Map user requests:
- No mention of quality -> `medium`
- "quick", "fast", "draft" -> `low`
- "high quality", "best", "detailed", "high-res" -> `high`

### Size Options
- **1024x1024** (default) - Square format
- **1024x1536** - Portrait format
- **1536x1024** - Landscape format
- **auto** - Let the model decide based on prompt

Map user requests:
- No mention of size -> `1024x1024`
- "square" -> `1024x1024`
- "portrait", "vertical", "tall" -> `1024x1536`
- "landscape", "horizontal", "wide" -> `1536x1024`

### Background Options (generation only)
- **auto** (default) - Model decides
- **transparent** - Transparent background (PNG/WebP output)
- **opaque** - Solid background

## API Key

The script checks for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `OPENAI_API_KEY` environment variable

If neither is available, the script exits with an error message.

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

**Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens
- Keep the descriptive part concise (1-5 words typically)
- Use context from user's prompt or conversation
- If unclear, use random identifier (e.g., `x9k2`, `a7b3`)

Examples:
- Prompt "A serene Japanese garden" -> `2025-12-17-14-23-05-japanese-garden.png`
- Prompt "sunset over mountains" -> `2025-12-17-15-30-12-sunset-mountains.png`
- Prompt "create an image of a robot" -> `2025-12-17-16-45-33-robot.png`
- Unclear context -> `2025-12-17-17-12-48-x9k2.png`

## Image Editing

Both editing modes use the Image API (images.edit endpoint) with gpt-image-1.5 for reliable results.

### Without Mask (Full Image Edit)
When the user wants to modify an existing image without specifying exact regions:
1. Use `--input-image` parameter with the path to the image
2. The prompt should contain editing instructions (e.g., "make the sky more dramatic", "change to cartoon style")
3. A fully transparent mask is auto-generated, allowing the model to edit the entire image

### With Mask (Precise Inpainting)
When the user wants to edit specific regions:
1. Use `--input-image` parameter with the path to the image
2. Use `--mask` parameter with a PNG mask file
3. The mask should have transparent areas (alpha=0) where edits should occur
4. The prompt describes what should appear in the masked region

Common editing tasks: add/remove elements, change style, adjust colors, replace backgrounds, etc.

## Prompt Handling

**For generation:** Pass user's image description as-is to `--prompt`. Only rework if clearly insufficient.

**For editing:** Pass editing instructions in `--prompt` (e.g., "add a rainbow in the sky", "make it look like a watercolor painting")

Preserve user's creative intent in both cases.

## Output

- Saves PNG to current directory (or specified path if filename includes directory)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path

## Examples

**Generate new image:**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-12-17-14-23-05-japanese-garden.png" --quality high --size 1536x1024
```

**Generate with transparent background:**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "A cute cartoon cat mascot" --filename "2025-12-17-14-25-30-cat-mascot.png" --background transparent --quality high
```

**Edit existing image (full image):**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-12-17-14-27-00-dramatic-sky.png" --input-image "original-photo.jpg"
```

**Edit with mask (inpainting):**
```bash
uv run ~/.claude/skills/gpt-image-1-5/scripts/generate_image.py --prompt "a flamingo swimming" --filename "2025-12-17-14-30-00-lounge-flamingo.png" --input-image "lounge.png" --mask "mask.png"
```
