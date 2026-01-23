# `intellectronica/agent-skills`

**[`@intellectronica`](https://intellectronica.net/)'s agent skills**

<table border="0" cellspacing="0" cellpadding="10">
<tr>
<td valign="top" width="50%">

### [Mastering Agent Skills](https://agentic-ventures.com/mastering-agent-skills)

Join a hands-on workshop for AI power users to use and create Agent Skills.

<a href="https://agentic-ventures.com/mastering-agent-skills"><img src="https://agentic-ventures.com/skills/mastering-agent-skills/opengraph-image?847390cc6f31fc75" width="100%" alt="Mastering Agent Skills"></a>

</td>
<td valign="top" width="50%">

### [Introduction to Agent Skills](https://agentic-ventures.com/introduction-to-agent-skills)

Discover how Agent Skills can customise AI agents in these free tutorials.

<a href="https://agentic-ventures.com/introduction-to-agent-skills"><img src="https://agentic-ventures.com/skills/introduction-to-agent-skills/opengraph-image?7fad56ec884473fb" width="100%" alt="Introduction to Agent Skills"></a>

</td>
</tr>
</table>

---

| Skill | Description |
|-------|-------------|
| [anki-connect](https://github.com/intellectronica/agent-skills/tree/main/skills/anki-connect) | This skill is for interacting with Anki through AnkiConnect, and should be used whenever a user asks to interact with Anki, including to read or modify decks, notes, cards, models, media, or sync operations. |
| | ```npx skills add intellectronica/agent-skills --skill "anki-connect"``` |
| [context7](https://github.com/intellectronica/agent-skills/tree/main/skills/context7) | Retrieve up-to-date documentation for software libraries, frameworks, and components via the Context7 API. This skill should be used when looking up documentation for any programming library or framework, finding code examples for specific APIs or features, verifying correct usage of library functions, or obtaining current information about library APIs that may have changed since training. |
| | ```npx skills add intellectronica/agent-skills --skill "context7"``` |
| [copilot-sdk](https://github.com/intellectronica/agent-skills/tree/main/skills/copilot-sdk) | This skill provides guidance for creating agents and applications with the GitHub Copilot SDK. It should be used when the user wants to create, modify, or work on software that uses the GitHub Copilot SDK in TypeScript, Python, Go, or .NET. The skill covers SDK usage patterns, CLI configuration, custom tools, MCP servers, and custom agents. |
| | ```npx skills add intellectronica/agent-skills --skill "copilot-sdk"``` |
| [gpt-image-1-5](https://github.com/intellectronica/agent-skills/tree/main/skills/gpt-image-1-5) | Generate and edit images using OpenAI's GPT Image 1.5 model. Use when the user asks to generate, create, edit, modify, change, alter, or update images. Also use when user references an existing image file and asks to modify it in any way (e.g., "modify this image", "change the background", "replace X with Y"). Supports text-to-image generation and image editing with optional mask. DO NOT read the image file first - use this skill directly with the --input-image parameter. |
| | ```npx skills add intellectronica/agent-skills --skill "gpt-image-1-5"``` |
| [here-be-git](https://github.com/intellectronica/agent-skills/tree/main/skills/here-be-git) | Initialise a git repository with optional agent commit instructions and .gitignore. Use when users say "here be git", "init git", "initialise git", or otherwise indicate they want to set up version control in the current directory. |
| | ```npx skills add intellectronica/agent-skills --skill "here-be-git"``` |
| [lorem-ipsum](https://github.com/intellectronica/agent-skills/tree/main/skills/lorem-ipsum) | Generate lorem ipsum placeholder text. This skill should be used when users ask to generate lorem ipsum content, placeholder text, dummy text, or filler text. Supports various structures including plain paragraphs, headings with sections, lists, and continuous text. Output can be saved to a file or used directly as requested by the user. |
| | ```npx skills add intellectronica/agent-skills --skill "lorem-ipsum"``` |
| [markdown-converter](https://github.com/intellectronica/agent-skills/tree/main/skills/markdown-converter) | Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis. |
| | ```npx skills add intellectronica/agent-skills --skill "markdown-converter"``` |
| [mgrep-code-search](https://github.com/intellectronica/agent-skills/tree/main/skills/mgrep-code-search) | Semantic code search using mgrep for efficient codebase exploration. This skill should be used when searching or exploring codebases with more than 30 non-gitignored files and/or nested directory structures. It provides natural language semantic search that complements traditional grep/ripgrep for finding features, understanding intent, and exploring unfamiliar code. |
| | ```npx skills add intellectronica/agent-skills --skill "mgrep-code-search"``` |
| [nano-banana-pro](https://github.com/intellectronica/agent-skills/tree/main/skills/nano-banana-pro) | Generate and edit images using Google's Nano Banana Pro (Gemini 3 Pro Image) API. Use when the user asks to generate, create, edit, modify, change, alter, or update images. Also use when user references an existing image file and asks to modify it in any way (e.g., "modify this image", "change the background", "replace X with Y"). Supports both text-to-image generation and image-to-image editing with configurable resolution (1K default, 2K, or 4K for high resolution). DO NOT read the image file first - use this skill directly with the --input-image parameter. |
| | ```npx skills add intellectronica/agent-skills --skill "nano-banana-pro"``` |
| [promptify](https://github.com/intellectronica/agent-skills/tree/main/skills/promptify) | Transform user requests into detailed, precise prompts for AI models. Use when users say "promptify", "promptify this", or explicitly request prompt engineering or improvement of their request for better AI responses. |
| | ```npx skills add intellectronica/agent-skills --skill "promptify"``` |
| [ray-so-code-snippet](https://github.com/intellectronica/agent-skills/tree/main/skills/ray-so-code-snippet) | Generate beautiful code snippet images using ray.so. This skill should be used when the user asks to create a code image, code screenshot, code snippet image, or wants to make their code look pretty for sharing. Saves images locally to the current working directory or a user-specified path. |
| | ```npx skills add intellectronica/agent-skills --skill "ray-so-code-snippet"``` |
| [tavily](https://github.com/intellectronica/agent-skills/tree/main/skills/tavily) | Use this skill for web search, extraction, mapping, crawling, and research via Tavily’s REST API when web searches are needed and no built-in tool is available, or when Tavily’s LLM-friendly format is beneficial. |
| | ```npx skills add intellectronica/agent-skills --skill "tavily"``` |
| [ultrathink](https://github.com/intellectronica/agent-skills/tree/main/skills/ultrathink) | Display colorful ANSI art of the word "ultrathink". Use when the user says "ultrathink" or invokes /ultrathink. |
| | ```npx skills add intellectronica/agent-skills --skill "ultrathink"``` |
| [youtube-transcript](https://github.com/intellectronica/agent-skills/tree/main/skills/youtube-transcript) | Extract transcripts from YouTube videos. Use when the user asks for a transcript, subtitles, or captions of a YouTube video and provides a YouTube URL (youtube.com/watch?v=, youtu.be/, or similar). Supports output with or without timestamps. |
| | ```npx skills add intellectronica/agent-skills --skill "youtube-transcript"``` |

---