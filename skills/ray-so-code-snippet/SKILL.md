---
name: ray-so-code-snippet
description: Generate beautiful code snippet images using ray.so. This skill should be used when the user asks to create a code image, code screenshot, code snippet image, or wants to make their code look pretty for sharing. Saves images locally to the current working directory or a user-specified path.
---

# ray.so Code Snippet Image Generator

Generate beautiful code snippet images using [ray.so](https://ray.so/) and save them locally.

## Requirements

- The user MUST provide the code snippet, either directly or by pointing to a file/selection in context
- MUST ask the user for ALL styling parameters before generating, presenting ALL available options
- MUST use `agent-browser` for screenshot capture (check availability first)

## Workflow

### Step 1: Verify agent-browser Availability

Before proceeding, verify that `agent-browser` is available:

```bash
which agent-browser
```

If `agent-browser` is not found in the PATH, inform the user that this skill requires agent-browser and cannot proceed without it.

### Step 2: Fetch Available Options

Fetch the current themes and languages from ray.so's GitHub repository using curl:

```bash
# Fetch and parse available themes
curl -s "https://raw.githubusercontent.com/raycast/ray-so/main/app/(navigation)/(code)/store/themes.ts" | grep -oE 'id:\s*"[^"]+"' | sed 's/id:\s*"//;s/"//' | sort -u

# Fetch and parse available languages
curl -s "https://raw.githubusercontent.com/raycast/ray-so/main/app/(navigation)/(code)/util/languages.ts" | grep -oE '^[[:space:]]*"?[a-zA-Z0-9+#-]+"?\s*:\s*\{' | sed 's/[[:space:]]*"//g;s/".*//;s/:.*//' | sort -u
```

### Step 3: Ask User for ALL Parameters

MUST use AskUserQuestion to ask for EVERY parameter, presenting ALL available options. Ask for parameters in this order:

#### 3.1 Theme Selection

Present ALL available themes. In the question, list every theme fetched from step 2. Example:

```
Question: "Which theme would you like?"
Description: "Available themes: [list ALL themes from curl output]"
Options (pick 4 popular ones for quick select):
- breeze (default, purple gradient)
- midnight (cyan-blue)
- vercel (minimalist dark)
- sunset (warm orange)
Note: User can select "Other" to type any theme from the full list
```

#### 3.2 Language Selection

**Infer the language when possible.** Skip this question if:
- The user explicitly specified a language
- The code comes from a file with a clear extension (e.g., `.py` → python, `.js` → javascript, `.ts` → typescript, `.rs` → rust, `.go` → go, etc.)
- The syntax is unmistakably identifiable (e.g., `def`/`import` → python, `func`/`package` → go, `fn`/`let mut` → rust)

Only ask this question if the language cannot be confidently inferred:

```
Question: "Which language for syntax highlighting?"
Description: "Available languages: [list ALL languages from curl output]"
Options:
- auto (auto-detect)
- javascript
- python
- typescript
Note: User can select "Other" to type any language from the full list
```

#### 3.3 Dark/Light Mode

```
Question: "Dark or light mode?"
Options:
- Dark mode (default)
- Light mode
```

#### 3.4 Background

```
Question: "Show the gradient background?"
Options:
- Yes, show background (default)
- No, transparent/minimal background
```

#### 3.5 Padding

```
Question: "How much padding around the code?"
Options:
- 16 (compact)
- 32 (small)
- 64 (medium, default)
- 128 (large)
```

#### 3.6 Line Numbers

```
Question: "Show line numbers?"
Options:
- No (default)
- Yes
```

#### 3.7 Title

```
Question: "Add a title above the code? (e.g., filename)"
Options:
- No title (default)
- Yes, add title
If yes, ask for the title text.
```

Note: Do NOT ask about output path/filename. Save to the current working directory with a sensible filename (e.g., `rayso-snippet.png`, or based on the title if provided like `fibonacci.png`). Only use a different path if the user explicitly specifies one in their original request.

### Step 4: Build the ray.so URL

**CRITICAL: ALL parameters must be in the URL hash (after #), NOT in the query string.**

Build the URL using shell commands:

```bash
# 1. Base64 encode the code
CODE_BASE64=$(echo -n 'YOUR_CODE_HERE' | base64)

# 2. URL encode the base64 string
CODE_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CODE_BASE64'))")

# 3. Build the URL with ALL parameters in the hash
# Format: https://ray.so/#param1=value1&param2=value2&code=ENCODED_CODE
# Do NOT include width parameter - let ray.so auto-size to fit content
URL="https://ray.so/#theme=THEME&padding=PADDING&background=BACKGROUND&darkMode=DARKMODE&language=LANGUAGE&code=${CODE_ENCODED}"

# Add optional parameters if needed:
# If lineNumbers: add "&lineNumbers=true" before &code=
# If title: add "&title=URL_ENCODED_TITLE" before &code=
```

**URL Hash Parameters:**
| Parameter | Values | Default |
|-----------|--------|---------|
| theme | Any theme from list | breeze |
| padding | 16, 32, 64, 128 | 64 |
| background | true, false | true |
| darkMode | true, false | true |
| language | Any language from list, or "auto" | auto |
| lineNumbers | true, false | false |
| title | URL-encoded string | (none) |
| width | Number (pixels) | auto |
| code | Base64-encoded, then URL-encoded | (required) |

**Note on width:** Do NOT include the `width` parameter unless you specifically need a fixed width. Without it, ray.so auto-sizes the frame to fit the code content, avoiding unnecessary empty space.

**Example URL construction:**
```bash
# For code: for i in range(23):\n    print(i)
# Theme: midnight, Padding: 64, Dark mode: true, Background: true, Language: python, Title: test.py

CODE='for i in range(23):
    print(i)'
CODE_BASE64=$(echo -n "$CODE" | base64)
CODE_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CODE_BASE64'))")
TITLE_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('test.py'))")
URL="https://ray.so/#theme=midnight&padding=64&background=true&darkMode=true&language=python&title=${TITLE_ENCODED}&code=${CODE_ENCODED}"
echo "$URL"
```

### Step 5: Capture High-Quality Image with agent-browser

MUST use agent-browser (verified in Step 1). This approach uses the `html-to-image` library (same as ray.so's internal export) with high pixelRatio for crisp, sharp text rendering.

**IMPORTANT:** Always use a unique session name with `--session` to avoid stale session issues.

```bash
# Generate unique session name
SESSION="rayso-$(date +%s)"

# 1. Set viewport
agent-browser --session $SESSION set viewport 1400 900

# 2. Open the URL
agent-browser --session $SESSION open "$URL"

# 3. Wait for the page to fully render
agent-browser --session $SESSION wait --load networkidle
agent-browser --session $SESSION wait 3000

# 4. Load html-to-image library (same library ray.so uses internally)
agent-browser --session $SESSION eval 'new Promise((r,e)=>{const s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js";s.onload=r;s.onerror=e;document.head.appendChild(s)})'

# 5. Capture at 4x resolution using html-to-image (produces crisp text)
agent-browser --session $SESSION eval 'htmlToImage.toPng(document.querySelector("#frame > div"),{pixelRatio:4,skipAutoScale:true})' > /tmp/rayso-dataurl-$SESSION.txt

# 6. Close the browser
agent-browser --session $SESSION close

# 7. Convert data URL to PNG file
DATAURL=$(cat /tmp/rayso-dataurl-$SESSION.txt | tr -d '"' | tr -d '\n')
echo "$DATAURL" | sed 's/data:image\/png;base64,//' | base64 -d > /path/to/output.png

# 8. Clean up temp file
rm /tmp/rayso-dataurl-$SESSION.txt
```

**Critical notes:**
- Uses `html-to-image` library which is what ray.so uses for its own export feature
- `pixelRatio: 4` produces high-DPI images with crisp, sharp text (4x native resolution)
- The data URL is captured directly from the library, not from a screenshot
- No ImageMagick required - pure browser-based rendering at high resolution
- Output is correctly sized with no extra whitespace

### Step 6: Confirm Output and STOP

Report the saved file location to the user. **The task is complete - do not perform any additional checks, explorations, or verifications after the screenshot is saved.**

## Complete Example

User: "Create a code snippet image of this Python function"

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

1. Check `which agent-browser` - confirmed available

2. Fetch themes and languages:
```bash
curl -s "https://raw.githubusercontent.com/raycast/ray-so/main/app/(navigation)/(code)/store/themes.ts" | grep -oE 'id:\s*"[^"]+"' | sed 's/id:\s*"//;s/"//' | sort -u
```

3. Ask user for parameters via AskUserQuestion:
   - Theme: user selects "midnight"
   - Language: *inferred as python from `def` syntax - not asked*
   - Dark mode: user selects "Dark mode"
   - Background: user selects "Yes"
   - Padding: user selects "64"
   - Line numbers: user selects "No"
   - Title: user selects "No title"

4. Build URL (all params in hash, no width for auto-sizing):
```bash
CODE='def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)'
CODE_BASE64=$(echo -n "$CODE" | base64)
CODE_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CODE_BASE64'))")
URL="https://ray.so/#theme=midnight&padding=64&background=true&darkMode=true&language=python&code=${CODE_ENCODED}"
```

5. Capture high-quality image:
```bash
SESSION="rayso-$(date +%s)"

agent-browser --session $SESSION set viewport 1400 900
agent-browser --session $SESSION open "$URL"
agent-browser --session $SESSION wait --load networkidle
agent-browser --session $SESSION wait 3000

# Load html-to-image library
agent-browser --session $SESSION eval 'new Promise((r,e)=>{const s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js";s.onload=r;s.onerror=e;document.head.appendChild(s)})'

# Capture at 4x resolution
agent-browser --session $SESSION eval 'htmlToImage.toPng(document.querySelector("#frame > div"),{pixelRatio:4,skipAutoScale:true})' > /tmp/rayso-dataurl-$SESSION.txt
agent-browser --session $SESSION close

# Save as PNG
DATAURL=$(cat /tmp/rayso-dataurl-$SESSION.txt | tr -d '"' | tr -d '\n')
echo "$DATAURL" | sed 's/data:image\/png;base64,//' | base64 -d > ./fibonacci.png
rm /tmp/rayso-dataurl-$SESSION.txt
```

6. Report: "Saved code snippet image to ./fibonacci.png"

## Image Resolution and Quality

This skill uses the `html-to-image` library with `pixelRatio: 4` to produce high-quality images with crisp, sharp text. This is the same rendering approach that ray.so uses for its built-in export feature.

**Output quality:**
- Default: 4x native resolution (frame auto-sizes to content, then rendered at 4x)
- Text is rendered at high DPI, not upscaled from low resolution
- Gradient backgrounds and all CSS styling are preserved
- No unnecessary empty space (frame auto-sizes to fit code)

**Adjusting resolution:**
- For smaller files: Change `pixelRatio:4` to `pixelRatio:2` in the eval command
- For maximum quality: Use `pixelRatio:6` (same as ray.so's "6x" export option)

**Forcing a specific width:**
- Only add `&width=NUMBER` to the URL if you need a fixed width (e.g., for consistent sizing across multiple images)

## Troubleshooting

- **If agent-browser is not available:** Inform the user and do not proceed
- If curl fails to fetch themes/languages, use these common defaults:
  - Themes: breeze, midnight, candy, crimson, falcon, meadow, raindrop, sunset, vercel, supabase, tailwind
  - Languages: auto, javascript, typescript, python, rust, go, java, ruby, swift, kotlin, css, html, json, yaml, bash
- **If parameters aren't applied:** Ensure ALL parameters are in the URL hash (after #), not the query string
- **If title isn't showing:** The title parameter must be in the hash: `#title=filename.py&code=...`
- **If html-to-image fails to load:** Check network connectivity; the library loads from jsdelivr CDN
- **If capture returns empty:** The frame selector `#frame > div` may have changed; inspect the page structure
- For very long code snippets, ray.so may truncate; consider splitting into multiple images
- If the page doesn't load properly, increase the wait time (try 4000ms or more)
- **If you get a blank page:** Use a fresh unique session name with `--session` flag
- **If data URL is malformed:** Ensure quotes and newlines are stripped before base64 decoding
