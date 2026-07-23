---
type: concept
created: 2026-07-23
updated: 2026-07-23
sources:
  - "[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]"
  - "[[2026-05-06 The Founders Playbook (Anthropic)]]"
raw:
  - raw/articles/2026-06-03 Running an AI-native Engineering Org (Anthropic).md
  - raw/articles/2026-05-06 The Founders Playbook (Anthropic).pdf
related:
  - "[[AI-Native Company]]"
  - "[[Verification Bottleneck]]"
  - "[[AI Software Factory]]"
confidence: medium
tags: [ai-native, planning]
---

# Just-in-Time Planning

Heavy pre-planning existed because coding time was expensive; agentic coding
removes the premise. The Claude Code team's six-month roadmap was "out of date
by month three" *because of* the product it described — so planning shifted to
JIT, by analogy with JIT compilation: just the right amount, at the right time.

> [!claim] When building is cheap, prototypes replace design docs as the planning artifact
> confidence: medium · status: contested
> evidence: "Our planning ritual shifted away from design docs toward
> discussions in PRs or prototypes… let's prototype, get a lot of internal
> users on it, and start acting on their feedback" —
> [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]].
> counter-evidence: "Founders who skip specs, architectural decisions, and
> context files (like CLAUDE.md) hit a predictable wall where every new session
> requires re-explaining the codebase and AI-generated changes drift from the
> original vision" — [[2026-05-06 The Founders Playbook (Anthropic)]], which
> prescribes a written architecture doc *and* scope definition before Claude
> Code writes a line of MVP code.

The two Anthropic sources pull in opposite directions, and the reconciliation
is probably about *which* documents die: feature-level design docs give way to
prototypes (the engineering-org account), while **durable context documents**
— architecture constraints, scope boundaries, CLAUDE.md — become *more*
necessary, because without them each agent session re-derives foundational
decisions from scratch ("agentic technical debt",
[[AI-Native Startup Lifecycle]]). Plan the frame up front; plan the features
just in time.

The companion discipline is killing obsolete process: team members have
explicit permission to question and kill rituals that no longer close a gap
("pick your noisiest workflow… is it still serving its purpose?"). Processes
built for expensive engineering time don't dissolve on their own.
