---
type: concept
created: 2026-07-23
updated: 2026-09-02
sources:
  - "[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]"
  - "[[2026-05-06 The Founders Playbook (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/articles/2026-06-03 Running an AI-native Engineering Org (Anthropic).md
  - raw/articles/2026-05-06 The Founders Playbook (Anthropic).pdf
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[AI-Native Company]]"
  - "[[Verification Bottleneck]]"
  - "[[AI Software Factory]]"
  - "[[Build for Rebuilding]]"
  - "[[Everyone Ships]]"
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
> third source: [[2026-08-20 The Claude Code Guide For Startups]] sits on both
> sides at once — 0→1 prototypes from anyone ([[Everyone Ships]]) and plan
> mode for "non-trivial rewrites" on one side; Zingage's "567 lines of how
> this team thinks" and the rule "put what can't change in CLAUDE.md at the
> root of your repo" on the other.

The two Anthropic sources pull in opposite directions, and the reconciliation
is probably about *which* documents die: feature-level design docs give way to
prototypes (the engineering-org account), while **durable context documents**
— architecture constraints, scope boundaries, CLAUDE.md — become *more*
necessary, because without them each agent session re-derives foundational
decisions from scratch ("agentic technical debt",
[[AI-Native Startup Lifecycle]]). Plan the frame up front; plan the features
just in time.

The startup guide's practice matches that reconciliation, and adds a
tolerance rule for the durable half: Emergent's Mukund Jha says "instead of
trying to be perfect here, it is ok to live with slightly outdated context
files as long as the agent can quickly verify and course correct." The
invariants must be written; the rest of the context can lag. Zingage's
drift story ([[Verification Bottleneck]]) is what happens when the invariants
aren't written.

The companion discipline is killing obsolete process: team members have
explicit permission to question and kill rituals that no longer close a gap
("pick your noisiest workflow… is it still serving its purpose?"). Processes
built for expensive engineering time don't dissolve on their own. Neither do
old code paths: Commure's "a rebuild isn't done… until the old path is gone"
extends the same discipline to code ([[Build for Rebuilding]]).
