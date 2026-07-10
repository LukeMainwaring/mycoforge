---
type: decision
status: accepted
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[Fractal Federation]]"
tags: [adr, architecture]
---

# ADR-002 Fractal Federation for Nested KBs

## Context

KBs will nest: an Obsidian vault-level orchestrator above per-project KBs, each of
which may in turn contain sub-KBs. Does nesting require a second kind of repo (a
dedicated "orchestrator template"), and how do nested KBs share links without
losing independence?

## Decision

**One template; "orchestrator" is a cuttable feature** (see [[Fractal Federation]]
for the concept). A parent KB is a normal KB that kept the feature: a
`[[orchestrator.children]]` manifest in `kb.toml`, a routing workflow in its
schema, a roll-up view, and child-aware lint. Children remain **independent git
repos** physically nested inside the vault folder tree; the parent gitignores
child directories. Cross-KB wikilinks (which Obsidian resolves vault-wide) are
**warn-only** in lint.

## Consequences

- The structure recurses with zero new machinery — any KB can become a parent by
  keeping one feature.
- Every KB stays portable as a standalone folder: clone it alone and all hard
  links still resolve; only warn-level cross-KB links go dark.
- The parent never writes into children — routing descends and reads, writes
  happen in a session opened in the child.
- Lint must know about children (existence + own `kb.toml`) — accepted cost,
  implemented behind the feature's markers.

## Alternatives

- **A distinct orchestrator template** — rejected: two templates to keep in sync,
  and "parent" turns out to be a small feature, not a different species.
- **One mono-repo vault** — rejected: destroys per-KB portability and git
  history isolation.
- **Hard-error cross-KB links** — rejected: punishes the vault-wide linking that
  makes Obsidian useful; warn preserves portability pressure without banning it.
