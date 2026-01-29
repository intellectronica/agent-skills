---
name: copilot-sdk
description: This skill provides guidance for creating agents and applications with the GitHub Copilot SDK. ⚠️ IMPORTANT: When using the SDK with TypeScript/Node.js, the project MUST use ESM (ECMAScript Modules). CommonJS (require/module.exports) is NOT supported. It should be used when the user wants to create, modify, or work on software that uses the GitHub Copilot SDK in TypeScript (ESM only), Python, Go, or .NET. The skill covers SDK usage patterns, ESM-based project configuration, CLI configuration, custom tools, MCP servers, and custom agents.
---

# GitHub Copilot SDK

## Overview

The GitHub Copilot SDK is a multi-platform agent runtime that embeds Copilot's agentic workflows into applications. It exposes the same engine behind Copilot CLI, enabling programmatic invocation without requiring custom orchestration development.

**Critical Constraint (TypeScript / Node.js):**
- The Copilot SDK for Node.js is **ESM-only**
- Projects **MUST** use ECMAScript Modules
- CommonJS (`require`, `module.exports`) is **not supported**

**Status:** Technical Preview (suitable for development and testing)

**Supported Languages:** TypeScript/Node.js (ESM only), Python, Go, .NET

## Primary Documentation

- [GitHub Copilot SDK Repository](https://github.com/github/copilot-sdk)
- [Getting Started Guide](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md)
- [Cookbook with Recipes](https://github.com/github/copilot-sdk/blob/main/cookbook/README.md)

### Language-Specific SDK Docs

- [Node.js/TypeScript SDK](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md)
- [Python SDK](https://github.com/github/copilot-sdk/blob/main/python/README.md)
- [Go SDK](https://github.com/github/copilot-sdk/tree/main/go)
- [.NET SDK](https://github.com/github/copilot-sdk/tree/main/dotnet)

### CLI and Configuration Docs

- [About GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
- [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [Creating Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Custom Agents Configuration Reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Enhancing Agent Mode with MCP](https://docs.github.com/en/copilot/tutorials/enhance-agent-mode-with-mcp)
- [Supported AI Models](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

---

## Prerequisites

1. **GitHub Copilot Subscription** - Pro, Pro+, Business, or Enterprise
2. **GitHub Copilot CLI** - Installed and authenticated (`copilot --version`)
3. **Runtime:**
   - **Node.js 18+ (ESM required)**
   - Python 3.8+
   - Go 1.21+
   - .NET 8.0+

4. **TypeScript / Node.js Project Requirements**
   - `package.json` MUST include:
     ```json
     {
       "type": "module"
     }
     ```
   - Use `import` / `export`
   - Do NOT use `require()` or `module.exports`

## Installation

| Language | Command |
|----------|---------|
| TypeScript/Node.js (ESM) | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |

## Architecture

```
Application (ESM) → SDK Client → JSON-RPC → Copilot CLI (server mode)
```

The SDK manages CLI lifecycle automatically. External server connections supported via `cliUrl` / `cli_url`.

---

## Quick Start (TypeScript – ESM REQUIRED)

```typescript
// package.json MUST include: { "type": "module" }

import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({ model: "gpt-5" });

// Register handler BEFORE send()
session.on((event) => {
  if (event.type === "assistant.message") {
    console.log(event.data.content);
  }
});

await session.send({ prompt: "What is 2 + 2?" });

await session.destroy();
await client.stop();
```

**Critical:**
- ESM only (`import`)
- No CommonJS
- Register event handlers **before** calling `send()`

For complete examples in all languages, see `references/working-examples.md`.

---

## Core Concepts

### Client

Main entry point. Manages CLI server lifecycle and session creation.

**Operations:** `start()`, `stop()`, `createSession()`, `resumeSession()`

**Config:** `cliPath`, `cliUrl`, `port`, `useStdio`, `autoStart`, `autoRestart`

### Session

Individual conversation context with message history.

**Operations:** `send()`, `sendAndWait()`, `on()`, `abort()`, `getMessages()`, `destroy()`

**Config:** `model`, `streaming`, `tools`, `systemMessage`

### Events

Key events during processing:

| Event | Purpose |
|-------|---------|
| `assistant.message` | Complete response |
| `assistant.message_delta` | Streaming chunk |
| `session.idle` | Ready for next prompt |
| `tool.execution_start/end` | Tool invocations |

For full event lifecycle and SessionEvent structure, see `references/event-system.md`.

### Streaming

- `streaming: false` (default) - Content arrives all at once
- `streaming: true` - Content arrives incrementally via `assistant.message_delta`

Final `assistant.message` **always fires** regardless of streaming setting.

---

## Available Models

See [Supported AI Models](https://docs.github.com/en/copilot/reference/ai-models/supported-models) for full list.

| Provider | Model ID | Notes |
|----------|----------|-------|
| OpenAI | `gpt-4.1`, `gpt-5`, `gpt-5-mini` | Included |
| OpenAI | `gpt-5.1`, `gpt-5.1-codex`, `gpt-5.2` | Premium |
| Anthropic | `claude-sonnet-4.5` | Premium (CLI default) |
| Anthropic | `claude-opus-4.5` | Premium (3× multiplier) |
| Google | `gemini-3-pro-preview` | Premium |

---

## Custom Tools

**TypeScript (ESM + Zod):**
```typescript
const tool = defineTool("lookup_issue", {
  description: "Fetch issue details",
  parameters: z.object({ id: z.string() }),
  handler: async ({ id }) => fetchIssue(id),
});
```

**Python (Pydantic):**
```python
@define_tool(description="Fetch issue details")
async def lookup_issue(params: IssueParams) -> dict:
    return fetch_issue(params.id)
```

For complete tool examples in all languages, see `references/working-examples.md`.

---

## Language Conventions

| Concept | TypeScript (ESM) | Python | Go | .NET |
|---------|------------------|--------|----|----|
| Create session | `createSession()` | `create_session()` | `CreateSession()` | `CreateSessionAsync()` |
| Delta content | `deltaContent` | `delta_content` | `DeltaContent` | `DeltaContent` |

For full conventions table, see `references/event-system.md`.

---

## CLI Configuration

Config stored in `~/.copilot/`:
- `config.json` - General configuration
- `mcp-config.json` - MCP server definitions

For custom agents and MCP setup, see `references/cli-agents-mcp.md`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Ensure ESM (`"type": "module"`) |
| Events fire but content empty | Use `event.data.content`, not `event.content` |
| Handler never fires | Register **before** `send()` |
| Python enum issues | Use `event.type.value` |
| Go nil pointer | Check `!= nil` before dereferencing |

For debugging techniques, see `references/troubleshooting.md`.

---

## Skill References

Detailed documentation in this skill:

- `references/working-examples.md` - Complete examples for all languages, custom tools
- `references/event-system.md` - Event lifecycle, SessionEvent structure, language conventions
- `references/troubleshooting.md` - Common issues, debugging techniques
- `references/cli-agents-mcp.md` - CLI configuration, custom agents, MCP server setup

---

## Additional Resources

- [SDK Samples](https://github.com/github/copilot-sdk/blob/main/samples/README.md)
- [SDK Releases](https://github.com/github/copilot-sdk/releases)
- [Cookbook](https://github.com/github/copilot-sdk/blob/main/cookbook/README.md)
- [awesome-copilot](https://github.com/github/awesome-copilot)
