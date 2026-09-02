---
type: concept
created: 2026-07-23
updated: 2026-09-02
sources:
  - "[[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]"
  - "[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/podcasts/2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up.md
  - raw/articles/2026-06-03 Running an AI-native Engineering Org (Anthropic).md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[AI-Native Company]]"
  - "[[Company Brain]]"
  - "[[Verification Bottleneck]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Prototype, Dogfood, Productionize]]"
confidence: medium
tags: [ai-native, software-engineering]
---

# AI Software Factory

[[Diana Hu]]'s term for the emerging build paradigm: humans write the **spec and
the tests that define success**; agents generate the implementation and iterate
until the tests pass. "The human defines what to build and judges the output.
The actual code is the agent's job." She frames it as the next evolution of
test-driven development.

> [!claim] Repos can consist entirely of specs and test harnesses, with no hand-written code
> confidence: low · status: supported
> evidence: "Some companies have already pushed this to the point where the repos
> contain no hand-written code, just specs and test harnesses" — cited example:
> StrongDM's AI team, where "specs and scenario-based validations drive agents to
> write, test, and iterate on code until it meets a probabilistic satisfaction
> threshold" — [[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]].
> Marked low: secondhand, no counts, and generalizability beyond greenfield
> internal systems is untested.

> [!claim] Factory-equipped individuals reach order-of-magnitude productivity gains
> confidence: medium · status: supported
> evidence: "teams that do this cut their engineering sprint time in half and get
> close to 10x more done"; the "1000x engineer" (attribution: Steve Yegge) as one
> engineer "surrounded by a system of agents" — [[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]].
> Anecdotal multipliers from a VC talk, no methodology given. Raised to
> medium on [[2026-08-20 The Claude Code Guide For Startups]], whose
> subtitle is "ship like teams 10x their size": Commure reports one engineer
> running "a ~13-ticket initiative with Claude subagents in parallel, each
> owning a ticket and its PR" (Tanay Tandon); Higgsfield describes competing
> "against companies with 10x the headcount." Still self-reported and
> vendor-selected, so not high.

First-party corroboration that agent-written code is now the default, not an
experiment: on the Claude Code team "by default, every commit is
Claude-assisted. I don't think I've seen a non-Claude-assisted commit in the
last four months" — [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]].
The same source supplies the factory's missing half: when generation is free,
the constraint moves to judging output — see [[Verification Bottleneck]].

## The mechanical 80%

The startup guide states the factory's division of labor as a ratio: agents
"own the mechanical 80% so engineers spend their time on the cases that
actually need judgment" (Rule 2, "Automate the tedium"). The strongest data
point is ClickHouse, where two purpose-built agents are the #2 and #3
contributors to the repo (detail in [[Self-Improving AI Loop]]). The guide's
six workflow patterns — classify-and-act, fan-out-and-synthesize, adversarial
verification, generate-and-filter, tournament, loop-until-done — are the
factory's floor plan; Commure's parallel-tickets initiative is fan-out.

The same factory runs outside the SDLC. Nearly every company in the guide
has self-service data analytics on Claude (Clay's internal analytics agent,
Heidi categorizing clinician feedback against usage data, Crosby summarizing
thousands of legal documents with subagents, Commure sweeping claims data for
anomalies, Translucent mining hospital finances for warning signs). Internal
agents that earn it become product — [[Prototype, Dogfood, Productionize]].

The complement is [[Tom Blomfield]]'s ephemeral-software point (see
[[Company Brain]]): if agents regenerate implementations cheaply, the spec is
the asset and the code is disposable.
<!-- sf:begin(product) -->
This KB's embedded-prompt convention —
product spec pages holding a full build prompt, per
[[ADR-001 Separate Repo with Product as Seam]] — is a small-scale instance of
the same inversion.
<!-- sf:end(product) -->
