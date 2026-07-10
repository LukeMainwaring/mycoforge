---
type: concept
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[Fractal Federation]]"
confidence: high
tags: [template, design]
---

# Subtractive Onboarding

The template philosophy MycoForge inherits from its sibling **sporeforge** (the
full-stack app template): **ship with everything on, prune down.** A fresh clone
carries every feature — product layer, orchestrator, media capture, MCP server —
and onboarding is the act of *deleting* what you don't need, not assembling what
you do.

Why subtraction beats addition for templates:

- A deleted feature can't rot. Additive scaffolds accumulate half-wired options;
  a subtractive one is fully wired on day zero and only ever gets smaller.
- Pruning can be **deterministic**. Feature-owned paths and marked code blocks are
  removed by a script (`.template/onboard.py`), not by an LLM's judgment — so the
  result is reproducible and testable (`verify_matrix.sh` proves every feature
  combination still lints and passes its tests).
- The example content teaches by existing. You read a working wiki before you
  delete it and replace it with your domain.

The machinery deletes itself when done: `.template/` and the onboarding skill are
removed in the final onboarding phase, leaving a clean instance whose only
template residue is `kb.toml`'s pinned `template.version`.
