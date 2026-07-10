---
type: decision
status: accepted
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[ADR-004 Read-Only MCP in v1]]"
tags: [adr, architecture]
---

# ADR-001 Separate Repo with Product as Seam

## Context

MycoForge is the KB analog of sporeforge (the software template). A KB often
exists to feed a product: research becomes specs becomes software. Where should
the software live, and what does "product" mean inside a knowledge base?

## Decision

MycoForge is an **independent repo/template**, and the "product" inside a KB
instance is **spec pages only** — vision, features, decisions, embedded prompt
artifacts — never application code. Real software lives in a separate
sporeforge-derived repo; the KB feeds it through the read-only MCP server (see
[[ADR-004 Read-Only MCP in v1]]). The `product/` layer is itself a cuttable
feature for KBs that are pure research.

## Consequences

- The KB persists while products come and go — *"the knowledge base is the part
  you always keep."*
- Specs and decisions live next to the knowledge that motivated them, with
  wikilinks into the wiki proper.
- The seam is explicit: `product/software/` pages carry the full build prompt for
  each external artifact (the embedded-prompt convention), plus a link to its repo.
- Two repos to manage per product — accepted; the MCP bridge keeps the coupling
  one-directional.

## Alternatives

- **KB and app in one repo** — rejected: entangles the always-kept layer with the
  most disposable one, and breaks the template symmetry (one template each).
- **No product layer at all** — rejected as the default; kept as a prune option.
