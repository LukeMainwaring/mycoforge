---
type: spec
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[Vision]]"
tags: [product]
---

# MVP

What v0.1 of the template ships (this repo):

- **The wiki core** (never cuttable): `raw/` + `wiki/` + `AGENTS.md` schema,
  self-referential example content, `scripts/lint.py` with its checks driven from
  `kb.toml`.
- **Four cuttable features**: `product` (this layer), `orchestrator` (federation),
  `media-capture` (`/transcript` + `/snippet`), `mcp-server` (read-only
  search/read/index).
- **Template machinery**: `.template/features.toml`, deterministic
  `onboard.py` prune+rename, `verify_matrix.sh` proving all four representative
  combos stay green, and the `/onboard` interview skill.
- **Drift control**: copy-and-own tooling, all instance data in `kb.toml`,
  `/sync-upstream` against a pinned template version (see
  [[ADR-003 Copy-and-Own with Config-Code Split]]).

Out of scope for v0.1 — see `roadmap.md`: the vault parent instance, retrofitting
the two pre-template KBs, the books KB, MCP write tools, embeddings.
