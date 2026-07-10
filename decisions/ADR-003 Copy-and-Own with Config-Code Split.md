---
type: decision
status: accepted
created: 2026-07-10
updated: 2026-07-10
related:
  - "[[Subtractive Onboarding]]"
tags: [adr, tooling]
---

# ADR-003 Copy-and-Own with Config-Code Split

## Context

Every KB instance needs the tooling (linter, skills, schema boilerplate). The two
hand-built KBs that preceded this template had **diverged**: each had its own
`lint.py` with instance data (heuristic terms, allowlists, glossaries) hard-coded
in Python, so improvements in one never reached the other. How should instances
get tooling, and how do template updates propagate?

## Decision

**Copy-and-own**: instances vendor full copies of all tooling. Combined with a
strict **config/code split**: every piece of per-instance data lives in `kb.toml`
(lint heuristic terms, link allowlists, ASR glossary, children manifest), so the
*code* stays byte-identical across instances. A `/sync-upstream` skill ports
template updates by diffing the vendored copies against the template repo at
HEAD, guided by the pinned `template.version` in `kb.toml`.

## Consequences

- Instances work offline and never break because upstream changed — they update
  when asked.
- Because code is byte-identical, `/sync-upstream` diffs are clean; conflicts can
  only come from someone violating the split.
- The discipline cost: **no per-instance data ever lives in Python code.** The
  linter reads everything from `kb.toml`; so do the skills.
- Retrofitting the two pre-template KBs is a roadmap item: adopt `kb.toml`,
  replace their diverged tooling with template copies.

## Alternatives

- **Installable package (`kb-lint` on PyPI)** — rejected for now: release
  ceremony without payoff at this scale. Documented as a graduation path if
  `/sync-upstream` proves insufficient.
- **Git submodule / subtree for tooling** — rejected: couples every instance to
  upstream's history and makes local patches painful; vendoring plus
  [[Subtractive Onboarding|subtractive]] pruning is simpler.
