---
type: architecture
kind: content
created: 2026-10-28
updated: 2026-10-28
commit: 4b7c704
watches:
  - wiki/concepts/AI Software Factory.md
  - wiki/concepts/AI-Native SDLC.md
  - wiki/concepts/Advisory and Deterministic Controls.md
  - wiki/concepts/Tiered Autonomy.md
  - wiki/concepts/Verification Bottleneck.md
  - wiki/concepts/Just-in-Time Planning.md
  - wiki/concepts/Token Efficiency.md
sources:
  - "[[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]"
  - "[[2026-05-06 The Founders Playbook (Anthropic)]]"
  - "[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-10-08 Building Effective Agent Automations (Anthropic)]]"
raw:
  - raw/podcasts/2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up.md
  - raw/articles/2026-05-06 The Founders Playbook (Anthropic).pdf
  - raw/articles/2026-06-03 Running an AI-native Engineering Org (Anthropic).md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md
related:
  - "[[The Knowledge Map]]"
  - "[[Verification Bottleneck]]"
  - "[[AI-Native SDLC]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Map - AI-Native Organizations]]"
tags: [architecture, content, ai-native, software-engineering]
---

# Map - AI-Native Software Engineering

## Summary

Seven pages on what happens to software engineering when agents write the code. [[Verification Bottleneck]] is the hub every other page links to: once building collapses, the constraint moves to judging what was built. The pages around it say where the judgment goes (controls, autonomy tiers, a rebuilt lifecycle), what planning becomes, and what the whole thing costs. The one idea to remember: speed is bought with verification infrastructure, not with more agents.

## Diagram

```mermaid
flowchart LR
    factory["AI Software Factory<br/>humans write specs and tests"]
    vb["Verification Bottleneck<br/>the constraint moves to judging"]
    sdlc["AI-Native SDLC<br/>six stages as a loop,<br/>committed artifacts"]
    adc["Advisory and Deterministic Controls<br/>skills advise, hooks enforce"]
    tiers["Tiered Autonomy<br/>earned, stops at the production gate"]
    jit["Just-in-Time Planning<br/>prototypes over design docs"]
    tokens["Token Efficiency<br/>cost per successful task"]

    factory -->|collapses build, so| vb
    vb -->|restructures into| sdlc
    vb -->|must-hold rules need| adc
    adc -->|maturity unlocks| tiers
    tiers -->|bounded by| sdlc
    jit -->|cheap building implies| vb
    sdlc -.->|"nothing without plan.md"| jit
    tokens -->|cost of the loop| factory
    vb -->|review cost is token cost| tokens
```

## How it works

[[AI Software Factory]] is the premise: humans write specs and tests, agents implement until the tests pass, and the spec is the asset while the code is disposable. [[Verification Bottleneck]] is the consequence and the hub: the engineering constraint shifts from writing code to verification, review and security, and the human/AI review boundary has to be recalibrated each model generation. Three pages say where verification lives. [[Advisory and Deterministic Controls]] splits rules into the kind an agent reads (skills, instructions) and the kind that holds regardless (hooks, sandboxes, PR review): a skill makes violations rare, only a hook makes them near impossible. [[Tiered Autonomy]] scales how much an agent may do by deviation, environment, change size and trust earned, and always stops at the production gate. [[AI-Native SDLC]] rebuilds the six-stage lifecycle as a loop chained by committed markdown artifacts that are both handoff and audit trail.

[[Just-in-Time Planning]] says cheap building turns feature design docs into prototypes while durable context documents matter more. [[Token Efficiency]] prices the loop: cost per successful task is the unit, a property of the whole architecture rather than of a router.

## Where the tensions are

- **Prototype or plan.** [[Just-in-Time Planning]] carries the cluster's only `contested` claim, that prototypes replace design docs; [[AI-Native SDLC]] says nothing is implemented without an accepted `plan.md`, checked by a hook. A source on a team that tried both would settle whether the difference is stage (startup vs regulated incumbent) or disagreement.
- **Spec as asset vs agents that drift.** [[AI Software Factory]] says humans only define and judge; [[Verification Bottleneck]] and [[Advisory and Deterministic Controls]] say agents drift from architecture plausibly and must not be able to weaken their own tests. The pages do not state this tension; it is implicit.
- **Spend tokens or save them.** [[Token Efficiency]] optimizes cost per task; [[AI Software Factory]] and [[Tiered Autonomy]] describe fleets and a burn-tokens posture. [[Token Efficiency]] calls these compatible but files no claim for it.
- **Sourcing.** The lowest-confidence claim is the factory's no-hand-written-code repo, secondhand and greenfield-only; nearly every other claim is `supported / medium` and rests on Anthropic or vendor-collected sources, with one consultant as the only outside corroboration.

## How to explain this

**In a few sentences:**

> Once agents write most of the code, the hard part is no longer building, it's knowing what you built is right. So the cluster is about verification: which rules merely advise an agent and which actually stop it, how much freedom an agent earns and where that stops, and how the lifecycle gets rebuilt around committed artifacts you can audit. Planning shifts toward prototypes, and the whole loop is priced per successful task rather than per seat.

**Likely follow-ups:**

- **Which page do I read first?** [[Verification Bottleneck]]; every other page is a consequence of it.
- **Where do the pages disagree?** On planning: prototypes-first against an enforced plan document.
- **How much of this is vendor material?** Most of it; the one non-Anthropic voice is a consultant's feature list, so treat `supported` as "no one has contested it yet".
