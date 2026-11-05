---
type: concept
created: 2026-07-23
updated: 2026-11-05
sources:
  - "[[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]"
  - "[[2026-06-03 Running an AI-native Engineering Org (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]]"
  - "[[2026-11-02 Warp - How to build an agentic self improvement loop]]"
raw:
  - raw/podcasts/2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up.md
  - raw/articles/2026-06-03 Running an AI-native Engineering Org (Anthropic).md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/podcasts/2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd.md
  - raw/podcasts/2026-11-02 Warp - How to build an agentic self improvement loop.md
related:
  - "[[AI-Native Company]]"
  - "[[Company Brain]]"
  - "[[Verification Bottleneck]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Prototype, Dogfood, Productionize]]"
  - "[[Token Efficiency]]"
  - "[[Zach Lloyd]]"
  - "[[Skill Evolution]]"
  - "[[Stigmergic Coordination]]"
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
[[Alex Lieberman]]'s feature 10 is the factory as a checklist item: "letting
fleets of coding agents plan, write, test, review, and ship code while humans
define intent and acceptance criteria," which the host calls "a lot less
controversial than it would have been a year ago" and the feature most
organizations are furthest along with
([[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]). His feature
9 gives the factory a cost line, cost per accepted PR ([[Token Efficiency]]).

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

## The factory as infrastructure

[[Zach Lloyd]] of Warp turns the term from a division of labor into a system
a team operates ([[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]]).
His definition: an agentic system in the cloud that sets the roles of agents
across building software, with some autonomy, and that is "very measurable,
very close loop" so a team can tune, measure and benchmark it. The
misconception he argues against is a team calling its pile of automations
and interactive agents its factory.

> [!claim] A software factory should be a declared, versioned artifact, one per product surface, not a collection of automations
> confidence: medium · status: supported
> evidence: "you should define your factory in code… a concrete thing that
> you should be able to run at some point in time and measure how it's
> doing"; "you have one factory per product surface." The Terraform analogy:
> versioning, branches to test, revert, and "because it's in code, coding
> agents can suggest improvements to it" — [[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]].
> A vendor's prescription for its own product, though Warp runs its own
> engineering this way and reports results ([[Token Efficiency]]). Auto
> captions. Open: whether the declaration needs its own file or can be a
> repo's existing agent config.

Warp's declaration is a YAML file naming the repos, skills, MCPs and
integrations, plus a workflow that "roughly matches what… your team is
probably already doing": triage, spec, implementation. Ben, Warp's DevEx
lead, gives the whole inner loop
([[2026-11-02 Warp - How to build an agentic self improvement loop]]):
triage (research the task and check no other agent already has it); a
spec written with a person only when one needs to weigh in ("think 'grill
me,' but only tagging you in when you actually need a grill-me session"),
otherwise straight to implementation; verification, by the agent clicking
through what it built with computer use or by end-to-end tests in
Playwright; rounds of adversarial code review; ship; and a monitor such as
Sentry that files new issues and starts the cycle again. Improving that
loop is the outer loop in [[Self-Improving AI Loop]].

**Two kinds of engineering.** Product engineers put work in through tools
they already use (Slack, Linear or Jira, GitHub, an API or MCP call) and a
predefined workflow starts. The factory's controls are for engineering
managers, the CTO and above all the platform or DevEx team, not the
day-to-day engineer. Lloyd names the second job factory engineering: the
engineer is "engineering the system that builds the software and not just
building the software directly" — a role [[AI-Native Role Archetypes]] does
not yet list. Hu's spec-and-tests split above is what product engineers do
inside the factory; Lloyd's layer is what the factory engineers keep running.

**The stack**, bottom up, as Lloyd lists it for anyone building one, on Warp
or not:

1. **Declaration** — the factory as code, above.
2. **Trace and artifact store** — every agent conversation and artifact,
   following one piece of work from Slack through Linear and GitHub review to
   a production crash, so it can be diagnosed or replayed later.
3. **Integrations** — MCPs, with access scoped by team (what marketing may
   reach versus engineering).
4. **Compute** — a pluggable sandbox provider; Linux by default, a Mac VM
   when computer use has to drive an iOS simulator.
5. **Inference and harness** — bring your own provider (to burn down
   existing commitments) or your own harness.
6. **Improvement** — scorers and self-improvement agents
   ([[Self-Improving AI Loop]]).
7. **Orchestrator** — moves work through the stages, loading models and
   skills and firing automations; "a piece of it," not the platform.
8. **Access points** — headless, API- and MCP-driven. About 60% of Warp's
   own work starts in Slack; at Spawn the same share starts from production
   errors and reports ([[Stigmergic Coordination]]).

He places the whole stack "one level back from" CI/CD, a new layer of
developer infrastructure. Its metrics assume the PR as the unit of work
(cost per PR, human touches per PR, revert rate), the unit Spawn dropped.

> [!claim] A factory platform pays off from about five to ten engineers; smaller teams go faster on plain subscriptions
> confidence: low · status: supported
> evidence: "if you're like a few people honestly… this is overkill. Don't do
> this… you'll go faster"; "five to 10 engineers would maybe be the floor";
> self-serve for growth-stage startups on a common Slack/Linear/Jira stack;
> very large companies with bespoke infrastructure build their own —
> [[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]].
> One vendor's sales experience, no data. It argues against the vendor's
> interest at the low end, which is why it is filed as supported rather
> than speculative.

Warp's own throughput rose 40% in a month of tuning (detail in
[[Token Efficiency]]). That is a gain inside a running factory, not a
before-and-after against no factory, so it neither supports nor refutes the
order-of-magnitude claim above.
