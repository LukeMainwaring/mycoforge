---
type: concept
created: 2026-09-06
updated: 2026-10-23
sources:
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
raw:
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
related:
  - "[[Skill Evolution]]"
  - "[[AI-Native Company]]"
  - "[[Progressive Disclosure]]"
  - "[[AI Software Factory]]"
  - "[[Verification Bottleneck]]"
  - "[[Just-in-Time Planning]]"
  - "[[Company Brain]]"
confidence: medium
tags: [ai-native, cost]
---

# Token Efficiency

The cost discipline of an [[AI-Native Company]]: not spending fewer tokens,
but getting more successful work per token. Five of [[Alex Lieberman]]'s
thirty features are versions of it (features 4, 9, 11, 12 and 21 in
[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]).

> [!claim] Cost per successful task is the unit to optimize, and it is a property of the whole model architecture, not of a router
> confidence: medium · status: supported
> evidence: Lieberman: "use model routing to optimize cost per successful task
> across the business." The host's qualification: routing "is part and parcel
> of an overall model architecture that is designed to be adaptable and
> flexible to different types of tasks… matching task difficulty to model
> capability" — [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]].
> Consultant prescription plus commentator opinion; no cases.

The mechanisms the source lists:

- **Model routing** — match task difficulty to model capability (feature 4).
- **Plan with heavy models, execute with cheap ones** — divide work into
  planning and execution phases (feature 11); the host expects this to
  "naturally fall out" of a routing architecture. This is a different split
  from [[Just-in-Time Planning]], which is about *when* to plan, not which
  model plans.
- **Load only the slice you need** — [[Progressive Disclosure]] over the
  knowledge base (feature 12).
- **Cost per accepted PR** as a key software metric (feature 9). The host's
  caveat: the metrics of agentic delivery are unsettled, but they will need
  "some sense of completeness as well as cost per completeness" to compare
  model–harness combinations "in a more apples-to-apples kind of way." The
  Claude Code team's metrics in [[Verification Bottleneck]] (PR cycle time,
  AI-assisted commits) measure throughput; this adds cost per unit of
  accepted output, the [[AI Software Factory]]'s cost line.
- **Fine-tune open-weight models** for high-volume processes with an RL gym
  and first-party data (feature 21). The host's limit: only for organizations
  that already have the capability; most will lean on the labs' own cost
  measures.
- **Skills, not prompts** — a skills distribution system "improves token
  efficiency by triggering consistent skills throughout the workflow"
  (feature 7; the mechanism lives in [[Company Brain]]).

## Skills as a substitute for scale

[[Skill Evolution]] adds a measured version of the routing argument. In
WikiSkill ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]) Qwen-3.5-9B with evolved skills averages 47.4% over five
benchmarks against 39.4% for Qwen-3.6-27B without, and skills transfer
across model families, so an expensive model can do the discovery once and
a cheaper one can execute. The caveat cuts both ways: gains grow with model
size (+12.3, +17.5, +23.9 points for 4B, 9B, 27B), and skills evolved by a
small model can carry workarounds that hurt a large one
([[Fix the Principle, Not the Example]]). The proposer's on-demand reading
also makes the optimizer's cost constant in training-set size, the
[[Progressive Disclosure]] payoff with a number on it.

## Tension with token maxing

The YC talks say "burn tokens, not headcount" and run "an uncomfortably high
API bill" ([[AI-Native Company]]); Lieberman's features push cost per task
down. The two are compatible (spend a lot, waste little) and the sources
are looking at different stages: the YC advice is for startups substituting
tokens for hires, Lieberman's for incumbents running high-volume processes,
where a per-task cost is what gets budgeted. Noted as a reading, not a filed
synthesis.
