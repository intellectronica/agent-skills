---
name: tavily
description: Search the web, extract page content, map site URLs, crawl websites, and run multi-step research via Tavily’s REST API. Use when the user asks to look up, find online, search the internet, browse the web, scrape a page, or gather information from URLs — and no built-in web search tool is available, or when Tavily’s LLM-friendly output (summaries, citations, structured chunks) is beneficial.
---

# Tavily

## When to Use

- A task needs live web information, site extraction, URL mapping, or crawling
- No built-in web search tool is available, or Tavily’s LLM-friendly output (summaries, chunks, sources, citations) is preferred
- The user needs structured search results, page content extraction, or site discovery

## Required Environment

- Require `TAVILY_API_KEY` in the environment.
- If `TAVILY_API_KEY` is missing, prompt the user to provide the API key before proceeding.

## Base URL and Auth

- Base URL: `https://api.tavily.com`
- Authentication: `Authorization: Bearer $TAVILY_API_KEY`
- Content type: `Content-Type: application/json`
- Optional project tracking: add `X-Project-ID: <project-id>` if project attribution is needed.

## Tool Mapping (Tavily REST)

### 1) search → POST /search

Use for web search with optional answer and content extraction.

Recommended minimal request:

```bash
curl -sS -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "query": "<query>",
    "search_depth": "basic",
    "max_results": 5,
    "include_answer": true,
    "include_raw_content": false,
    "include_images": false
  }'
```

Key parameters:
- `query` (required): search text
- `search_depth`: `basic` | `advanced` | `fast` | `ultra-fast`
- `max_results`: 0–20
- `topic`: `general` | `news` | `finance`
- `time_range`: `day|week|month|year|d|w|m|y`
- `include_answer`: `false` | `true` | `basic` | `advanced`
- `include_raw_content`: `false` | `true` | `markdown` | `text`
- `include_domains`, `exclude_domains`: string arrays

Response: `answer` (if requested), `results[]` with `title`, `url`, `content`, `score`

### 2) extract → POST /extract

Use for extracting content from specific URLs.

```bash
curl -sS -X POST "https://api.tavily.com/extract" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "urls": ["https://example.com/article"],
    "query": "<optional intent for reranking>",
    "chunks_per_source": 3,
    "extract_depth": "basic",
    "format": "markdown",
    "include_images": false,
    "include_favicon": false
  }'
```

Key parameters:
- `urls` (required): array of URLs
- `query`: rerank chunks by intent
- `extract_depth`: `basic` | `advanced`
- `format`: `markdown` | `text`

Response: `results[]` with `url`, `raw_content`; `failed_results[]` for URLs that could not be extracted

### 3) map → POST /map

Use for generating a site map (URL discovery only).

```bash
curl -sS -X POST "https://api.tavily.com/map" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "url": "https://docs.tavily.com",
    "max_depth": 1,
    "max_breadth": 20,
    "limit": 50,
    "allow_external": true
  }'
```

Key parameters:
- `url` (required)
- `instructions`: natural language guidance (raises cost)
- `max_depth`: 1–5, `max_breadth`: 1+, `limit`: 1+
- `select_paths`, `exclude_paths`, `select_domains`, `exclude_domains`: regex arrays
- `allow_external`: boolean

Response: `base_url`, `results[]` (list of discovered URLs)

### 4) crawl → POST /crawl

Use for site traversal with built-in extraction.

```bash
curl -sS -X POST "https://api.tavily.com/crawl" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "url": "https://docs.tavily.com",
    "instructions": "Find all pages about the Python SDK",
    "max_depth": 1,
    "max_breadth": 20,
    "limit": 50,
    "extract_depth": "basic",
    "format": "markdown",
    "include_images": false
  }'
```

Key parameters:
- `url` (required)
- `instructions`: natural language guidance (enables `chunks_per_source`)
- `max_depth`, `max_breadth`, `limit`: same as map
- `extract_depth`: `basic` | `advanced`
- `format`: `markdown` | `text`

Response: `base_url`, `results[]` with `url`, `raw_content`

## Optional Research Workflow (Deep Investigation)

Use when a query needs multi-step analysis and citations.

### create research task → POST /research

```bash
curl -sS -X POST "https://api.tavily.com/research" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "input": "<research question>",
    "model": "auto",
    "stream": false,
    "citation_format": "numbered"
  }'
```

Response: `request_id`, `status` (initially `pending`)

### get research status → GET /research/{request_id}

Poll until `status` is `completed`:

```bash
curl -sS -X GET "https://api.tavily.com/research/<request_id>" \
  -H "Authorization: Bearer $TAVILY_API_KEY"
```

Polling workflow: wait 5 seconds after creation, then poll every 10 seconds. If `status` is still `pending` after 2 minutes, inform the user and stop polling.

Response when complete: `status: "completed"`, `content` (report text), `sources[]` with `title`, `url`

### streaming research (SSE)

Set `"stream": true` and use curl with `-N`:

```bash
curl -N -X POST "https://api.tavily.com/research" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"input":"<question>","stream":true,"model":"pro"}'
```

## Usage Notes

- Default to conservative parameters (`search_depth: basic`, `max_results: 5`) unless deeper recall is needed.
- Return structured results with URLs, titles, and summaries for downstream use.

## Error Handling

- 401/403: prompt for or re-check `TAVILY_API_KEY`
- Timeouts: reduce `max_depth`/`limit` or use `search_depth: basic`
- Oversized responses: lower `max_results` or `chunks_per_source`
