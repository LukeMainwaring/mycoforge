<div align="center">
  <h1>MycoForge</h1>
  <p>A template for LLM knowledge bases — a Karpathy-pattern "LLM wiki" scaffold with a schema, deterministic lint and prune tooling, capture skills, and a read-only MCP feed. Create a repo from the template and grow a knowledge base that compounds.</p>
</div>

## What is MycoForge?

MycoForge is a starting point, not a product. It packages the
[LLM wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
— a persistent, compounding markdown knowledge base maintained by an LLM agent —
as a **template you instantiate per domain**: a research topic, a personal
project, a books library, a whole-vault orchestrator.

Three layers, one ownership rule:

- **`raw/`** — your curated sources (papers, articles, transcripts). Immutable;
  the LLM reads but never modifies them.
- **`wiki/`** — LLM-owned markdown: concept and entity pages, syntheses, an
  `index.md` catalog, an append-only `log.md`. Obsidian is the IDE; the LLM is
  the programmer; the wiki is the codebase.
- **`AGENTS.md`** — the schema: the contract that makes the LLM a disciplined
  wiki maintainer instead of a generic chatbot.

MycoForge is the KB sibling of
[sporeforge](https://github.com/LukeMainwaring/sporeforge), the full-stack
AI-app template. Where sporeforge grows fruiting bodies — software products —
MycoForge is the mycelial network that feeds them: products come and go as
separate sporeforge instances, while **the knowledge base is the part you always
keep**, feeding them over MCP.

## The example you replace, and the meta-layer you keep

The shipped wiki is **self-referential**: it documents the LLM-wiki pattern
itself, with Karpathy's gist as its one raw source, four concept pages, a
synthesis with its claims marked, and the template's own design decisions as
real ADRs. It exists to be the worked example — every page obeys the schema, so
CI has real content to lint and you learn the conventions by reading them.
Onboarding deletes it and seeds your domain in its place.

What you keep is the meta-layer:

- **The schema** (`AGENTS.md`, with `CLAUDE.md` symlinked) — conventions,
  frontmatter, claim callouts, and the Ingest / Query / Lint workflows. Works in
  Claude Code and Codex alike.
- **The linter** (`scripts/lint.py`, pure stdlib) — index audits, wikilink
  resolution, provenance checks, orphan/stale detection, concept-candidate
  promotion hints. Every knob reads from `kb.toml`.
- **Skills** (`.agents/skills/`) — `/transcript` and `/snippet` capture
  spoken-word sources into `raw/`; `/sync-upstream` ports template updates;
  `/onboard` runs the whole setup interview.
- **The MCP server** (`mcp/server.py`) — read-only `search_kb` / `read_page` /
  `get_index` so other repos' agent sessions can consult the KB.

## Quick start

No stack to install — the KB is markdown plus Python stdlib. You need
[uv](https://docs.astral.sh/uv/) only if you keep the MCP server, and
[yt-dlp](https://github.com/yt-dlp/yt-dlp) only if you keep media capture.

MycoForge is a GitHub template repository — create a new KB from it (a fresh
repo with its own history, not a fork):

```bash
gh repo create my-kb --template LukeMainwaring/mycoforge --private --clone
cd my-kb
```

Or click **Use this template → Create a new repository** on GitHub, then clone.

Then onboard. The guided way: open an agent session (Claude Code or Codex) and
say **"onboard"** — the `/onboard` skill interviews you for domain, identity,
features, and page-type taxonomy, runs the deterministic prune, seeds your wiki,
and cleans up after itself.

## Onboarding

The scaffold ships every feature on, then you **cut down** to what you want —
pruning is subtractive, deterministic, and verified. The four cuttable features
(the wiki core is the trunk and always stays):

| Feature | What it is |
|---|---|
| `product` | Spec pages, ADRs in `decisions/`, roadmap, Home dashboard — for KBs that feed software |
| `orchestrator` | Parent-KB federation: children manifest, routing workflow, child-aware lint |
| `media-capture` | `/transcript` + `/snippet` skills for podcast/video sources |
| `mcp-server` | The read-only MCP feed |

The raw CLI underneath the skill lives in [`.template/`](.template/README.md):

```bash
python3 .template/onboard.py --list                            # the cuttable features
python3 .template/onboard.py --keep orchestrator,media-capture,mcp-server
                                                               # preview: research-only KB
python3 .template/onboard.py --keep media-capture,mcp-server \
        --slug mykb --brand MyKB --apply                       # apply + rename
```

Feature-specific content is marked inline (HTML comments in markdown, hash
comments in code), so pruning is mechanical — and `.template/verify_matrix.sh`
proves every representative combo still lints clean with zero leftovers. Delete
`.template/` once you've onboarded (the `/onboard` skill does).

Instances **vendor** their tooling (copy-and-own). All per-instance data lives
in `kb.toml`, so the code stays byte-identical across instances and the
`/sync-upstream` skill can port template updates against the pinned
`template.version`.

## Feeding a product repo over MCP

This repo's `.mcp.json` already registers the server for sessions opened in the
KB. To attach the KB from a *product* repo (or anywhere else), add one entry to
that repo's `.mcp.json`, pointing at the KB by absolute path:

```json
{
  "mcpServers": {
    "my-kb": { "command": "uv", "args": ["run", "/absolute/path/to/my-kb/mcp/server.py"] }
  }
}
```

The product session can then `search_kb`, `read_page`, and `get_index` — and
never write: ingestion stays an interactive workflow inside the KB, by design
(see `decisions/ADR-004 Read-Only MCP in v1.md`).

## Operating the KB

Day to day, everything runs through the schema's workflows — drop a source in
`raw/` and say "ingest"; ask questions; say "lint" now and then. The linter is
also a plain command:

```bash
python3 scripts/lint.py
```

## Roadmap

Tracked in `roadmap.md` (instances that keep the `product` feature). For the
template itself: a vault-level orchestrator instance, retrofitting pre-template
KBs via `/sync-upstream`, a books-library instance, and — as graduations if the
simple thing stops sufficing — MCP write tools, embeddings, and an installable
`kb-lint` package.
