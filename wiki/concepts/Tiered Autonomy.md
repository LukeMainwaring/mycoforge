---
type: concept
created: 2026-09-02
updated: 2026-09-06
sources:
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
raw:
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
related:
  - "[[AI-Native SDLC]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Verification Bottleneck]]"
  - "[[Founder as Orchestrator]]"
  - "[[Organizational Legibility]]"
confidence: medium
tags: [ai-native, governance, autonomy]
---

# Tiered Autonomy

How much an agent may do on its own is not a single switch in the
[[AI-Native SDLC]]. It scales along several axes at once, and every axis stops
at the same place: the production gate.

> [!claim] Agent autonomy is earned by guardrail maturity and bounded by the production gate, never switched on flat
> confidence: medium · status: supported
> evidence: auto-accept "becomes the default for routine work" only "as the
> guardrails from the later plays mature (a tuned CLAUDE.md, skills that
> encode policy, hooks that block unsafe actions, and a test suite Claude can
> run)"; and "the governing principle is that the agent may act up to the
> production gate and cannot pass it" —
> [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]].
> Practitioner corroboration: none of the dozen startups in
> [[2026-08-20 The Claude Code Guide For Startups]] "are having agents merge
> to main and hoping for the best." Both Anthropic. First non-Anthropic
> corroboration, as prescription: [[Alex Lieberman]]'s feature 29, "autonomy
> must be earned… not given full autonomy right away, but climb a ladder" —
> [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]].

## The axes

- **By deviation magnitude.** In the closing-the-loop play a deterministic,
  unit-tested detection script (rolling mean and standard deviation, Western
  Electric rules) watches a metric; "detection stays entirely deterministic,
  with no model involved." Response tiers live in version-controlled config:
  at 1σ log only, at 2σ invoke Claude read-only to diagnose, at 3σ Claude may
  act, "though only by opening a PR into the review gate or triggering a
  pre-approved runbook." The tier sets what the agent may do; the band sets
  when it is invoked at all.
- **By environment.** In development the agent deploys freely; staging sits
  in the middle; in production the agent prepares the release and a named
  release manager authorizes it, with a hook enforcing the gate. Deploy,
  status, and rollback are exposed as MCP tools scoped per environment, "so
  the agent's deployment powers are an allowlist rather than a shell script
  with credentials."
- **By change size.** A bounded finding (a scan result, an on-call fix, a
  flaky test) goes straight to a PR through the review gate; anything wider
  is written as `intent.md` and starts again at Plan. The same rule appears in
  the closing-the-loop, recurring-scan, and Claude Tag plays.
- **Over time.** The engineer's stance moves from watching each edit to
  reviewing artifacts after long autonomous sessions, and eventually "to
  building and monitoring loops." Auto mode plus worktrees is what makes
  parallel sessions and the fully autonomous maintenance stage possible.
- **By trust earned.** Lieberman's ladder for any agent, not just a coding
  one: observation, suggestion, acting with approval, acting alone, "until
  they can run whole workflows inside a defined boundary." The host: "we
  don't have to identify everything all at once… an ounce of prevention"
  ([[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]). The same
  rungs as the playbook's guardrail-maturity path, stated as a general policy.

## The human sandwich

Lieberman's feature 22 keeps "human touch and judgment at the first and final
mile of most processes." The host agrees "wholeheartedly" with the two ends
and is explicit that the middle is unsolved: "what I'm less sure is where
we'll find the right intervention points for humans in the middle of
processes… I don't think that we know exactly the right patterns"
([[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]). The
playbook's answer for the SDLC is the gates (ask-hooks at deploy, never in the
build); no source yet gives the general answer. The goal-plus-guardrails
framing of the ladder is also the host's alternative to automating a mapped
human process ([[Organizational Legibility]]).

## Separation of duties

The agent that wrote the code has no route to approve it, and the agent that
proposed a scan fix has no route to merge it. Each non-interactive run acts
under the agent's own identity, "so the pipeline log separates what the agent
did from what the engineer who triggered it did." Anything the agent writes
arrives as a PR behind branch protection. Between autonomous stages sits "an
independent confidence gate… a deterministic check or an adversarial reviewing
agent, deciding whether the previous stage's output continues or is escalated
to a human." The playbook's closing line: "The loop keeps running. Human
judgement stays above it."

This is the enterprise version of the human/AI review boundary in
[[Verification Bottleneck]], made explicit as tiers rather than recalibrated by
feel, and it is what the policy layer in a [[Self-Improving AI Loop]] looks
like when written down. The enforcement mechanics are in
[[Advisory and Deterministic Controls]]. At founder scale the same shift shows
up as [[Founder as Orchestrator]]: direct less, gate more.
