---
name: nano-banana-2
description: Generate and edit images using Nano Banana 2 through Google Gemini or the optional Atlas Cloud provider. This skill should be used when the user asks to create or modify images, especially when they need fast iteration, explicit aspect-ratio control, or resolution control from 512px to 4K.
---

# Nano Banana 2 Image Generation & Editing

Generate new images or edit existing images with Nano Banana 2. Google Gemini remains the default provider; Atlas Cloud is an explicit optional provider.

## Usage

Run the script using absolute or workspace-relative path (do NOT cd into the skill directory first):

**Generate new image:**
```bash
uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py --prompt "your image description" --filename "output-name.png" [--resolution 512px|1K|2K|4K] [--aspect-ratio RATIO] [--api-key KEY]
```

**Edit image(s) with references:**
```bash
uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input1.png" [--input-image "path/to/input2.png" ...] [--resolution 512px|1K|2K|4K] [--aspect-ratio RATIO] [--api-key KEY]
```

**Use Atlas Cloud:**
```bash
uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py --provider atlas --prompt "your image description" --filename "output-name.png" [--input-image "path/to/input.png"] [--resolution 1K|2K|4K] [--aspect-ratio RATIO] [--atlas-api-key KEY]
```

Always run from the user's current working directory so outputs are saved in the active project context.

## Model

Provider model routes:
- Google Gemini (default): `gemini-3.1-flash-image-preview`
- Atlas Cloud text generation: `google/nano-banana-2/text-to-image`
- Atlas Cloud image editing: `google/nano-banana-2/edit`

Do not use `gemini-3-pro-image-preview` in this skill.

## Resolution Options

Nano Banana 2 supports:
- `512px` (fastest, low-latency iteration)
- `1K` (default)
- `2K`
- `4K`

Map common user language:
- "quick draft", "thumbnail", "tiny", "512", "0.5K" → `512px`
- no resolution mention → `1K`
- "2K", "medium", "normal" → `2K`
- "4K", "high-res", "ultra", "print quality" → `4K`

Use uppercase `K` for `1K`, `2K`, `4K`.

Atlas Cloud supports `1K`, `2K`, and `4K` for these routes. It promotes an auto-detected 512px reference to 1K and rejects an explicitly requested `512px` resolution.

## Aspect Ratios

Supported aspect ratios:
- `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`

Map common requests:
- square post / icon → `1:1`
- phone wallpaper / vertical reel → `9:16`
- widescreen / slide / hero image → `16:9`
- cinematic wide → `21:9`
- portrait print → `2:3` or `3:4`
- panorama banner → `4:1` or `8:1`

If unspecified, let the model default behavior apply.

Atlas Cloud supports `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, and `21:9`. The script reports a validation error before submission for other ratios.

## Reference Images (New in Gemini 3 Image workflows)

Provide up to 14 reference images when needed by repeating `--input-image`:
- preserve character consistency
- preserve object fidelity
- combine multiple visual references into one output

Use one image for simple edits; use multiple images for composition or consistency-sensitive tasks.

## API Key

For the default Gemini provider, resolve the API key in this order:
1. `--api-key` argument
2. `GEMINI_API_KEY` environment variable

For Atlas Cloud, resolve the API key in this order:
1. `--atlas-api-key` argument
2. `ATLASCLOUD_API_KEY` environment variable

Atlas uploads local references, submits generation once, polls the returned prediction with bounded GET requests, and downloads only HTTPS media URLs from its allowed delivery domains. If no provider key is available, stop and report a clear error.

## Filename Generation

Generate filenames as: `yyyy-mm-dd-hh-mm-ss-name.png`

Examples:
- `2026-02-26-17-31-04-japanese-garden.png`
- `2026-02-26-17-31-59-social-banner.png`

## Prompt Handling

For generation, pass the user's request as-is unless critically underspecified.
For editing, include explicit transformation instructions in the prompt and preserve the original intent.

## Output

- Save PNG to the current directory (or to a provided path in `--filename`)
- Return the full saved path(s)
- Do not read the output image back unless explicitly requested

## Examples

**Create a 4K widescreen image:**
```bash
uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py --prompt "Futuristic city skyline at blue hour with neon reflections" --filename "2026-02-26-17-45-00-futuristic-skyline.png" --resolution 4K --aspect-ratio 16:9
```

**Edit with multiple references:**
```bash
uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py --prompt "Create a polished campaign image that keeps the exact logo details and character identity" --filename "2026-02-26-17-50-10-campaign-image.png" --input-image "logo.png" --input-image "character.png" --resolution 2K --aspect-ratio 4:5
```
