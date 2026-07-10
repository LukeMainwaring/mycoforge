---
type: software
status: example
created: 2026-07-10
updated: 2026-07-10
repo: (not created — this page exists to demonstrate the convention)
related:
  - "[[ADR-001 Separate Repo with Product as Seam]]"
tags: [product, software, example]
---

# KB Stats Dashboard (Example)

**This is the worked example of the embedded-prompt convention** — delete it (or
let `/onboard` delete it) along with the rest of the example content.

The convention: each external software artifact gets one page here. The page *is*
the spec — a prose summary, a link to the repo once it exists, and the full build
prompt in a fenced block, ready to paste into a coding agent in a fresh
sporeforge-derived repo. Keep the prompt current as decisions change; the repo
link makes the seam auditable (see
[[ADR-001 Separate Repo with Product as Seam]]).

## What it would be

A tiny local web dashboard that reads this KB over its MCP server and charts wiki
health: pages per type over time, ingest cadence from the log, orphan/stale
counts from lint runs.

## Build prompt

```text
Create a repo from the sporeforge template. Build a single-page dashboard called
"KB Stats" that connects to a MycoForge knowledge base over MCP (stdio, see the
KB's .mcp.json for the server command).

Data sources, all read-only:
- get_index() for the page catalog; parse section headings for per-type counts
- read_page("log") for the append-only history; parse `## [YYYY-MM-DD] prefix |`
  entries into an activity timeline
- search_kb() spot-queries to power a search box

Charts: pages by type (bar), log entries per week by prefix (stacked area),
last-lint summary (stat tiles). No database — recompute on load. No writes to
the KB, ever.
```
