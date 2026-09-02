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
  - "[[AI Software Factory]]"
  - "[[AI-Native Role Archetypes]]"
  - "[[Just-in-Time Planning]]"
  - "[[Founder as Orchestrator]]"
  - "[[Fix the Principle, Not the Example]]"
  - "[[Build for Rebuilding]]"
confidence: medium
tags: [ai-native, software-engineering]
---

# Verification Bottleneck

When agents write the code, the constraint moves downstream.

> [!claim] Agentic coding shifts the engineering bottleneck from writing code to verification, review, and security
> confidence: medium · status: supported
> evidence: "writing code, writing tests, and refactoring rarely slows us down
> anymore. But the bottlenecks didn't go away… Verification, code review, and
> security took their place" — [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]].
> First-party from the Claude Code team. Multi-company corroboration:
> [[2026-08-20 The Claude Code Guide For Startups]] makes "Trust, but verify" its
> Rule 3, "the necessary corollary" to automation — "You can't automate a
> process unless you have a reliable means of monitoring and verifying the
> outcome" — and states that none of the dozen startups "are having agents
> merge to main and hoping for the best." Vendor-collected testimonials.

The team's response is **trust-but-verify review**: Claude handles style,
linting, bug-catching, and tests; humans review only where domain expertise
matters — legal partners for risk tolerance, security experts for trust
boundaries, PMs/designers for product taste. This is the review-side complement
of the [[AI Software Factory]]: humans judge output rather than produce it.

> [!claim] The human/AI review boundary is unstable and must be recalibrated per model generation
> confidence: medium · status: supported
> evidence: "the right balance of trust vs. verify will keep changing as the
> models improve. What you need humans for today might look different with the
> next model" — [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]].
> Corroborated by Higgsfield, where each new video/image model "requires new
> skills, evaluations, routing logic, and production testing before
> deployment" and Claude Code "compressed that cycle from days to hours"
> (Alex Mashrabov); the guide's eval advice is explicitly to "prevent drift
> and evaluate future models" — [[2026-08-20 The Claude Code Guide For Startups]].

## What verification is made of

The startup guide is the first source to itemize the verification layer.
Four components recur:

- **Written invariants.** Zingage gave Claude full autonomy early and "it
  shipped plausible code fast. The problem was it drifted from our
  architecture in ways that looked right but weren't." The fix was "567 lines
  of how this team thinks": every invariant, how problems are framed, "how to
  prove something works instead of trusting a confident answer" (Victor Hunt).
  The guide's rule: put what can't change in the root CLAUDE.md — the
  durable-context half of [[Just-in-Time Planning]].
- **Evals and golden sets.** The failure mode is "flying blind": teams get
  far on manual testing and intuition until users report the agent feels
  worse and nobody can separate regressions from noise. Prescription:
  multiple eval sets per key use case, updated regularly. Cainex's back-test
  is the worked example — [[Fix the Principle, Not the Example]].
- **Deterministic gates.** "AI agents are not deterministic, but a lot of
  highly regulated work requires processes to be done the same way every
  time." Hooks fire at fixed lifecycle points "regardless of what the model
  decides" — block a write that fails lint, require a test pass before commit,
  strip secrets. Cainex combines agents with deterministic checks for hospital
  billing.
- **Review agents.** Translucent's reviewer "fans out across a change,
  reviews it from multiple angles, and synthesizes the results"; Heidi runs
  automated reviews against compliance frameworks and routes findings to the
  right human reviewers. Same trust-but-verify split as above: agents do
  breadth, humans do domain judgment.

Artemis Security's framing makes the causal direction explicit: deployment
speed "only works… because we've invested deeply in testing infrastructure,
codebase organization, and team knowledge systems that let agents ship end to
end… structure your codebase, knowledge base, and team the right way, and
every contribution compounds" (Dan Shiebler). Verification infrastructure is
the precondition for speed, not a tax on it — which is also why rebuilding is
cheap for these teams ([[Build for Rebuilding]]: run evals against v1 and v2,
merge the winner).

## The founder-level analog

The same displacement recurs one level up in
[[2026-05-06 The Founders Playbook (Anthropic)]]: when building is effortless,
the constraint moves from *writing code* to *choosing and validating what to
build* — "The bottlenecks are no longer what you can build, but what you choose
to build"; the prime directive is "keeping your sense-making ahead of your
building." Same pattern, different altitude: engineers verify agent output,
founders verify the premise (see [[Founder as Orchestrator]] for the failure
modes). Both sources are Anthropic, so this is intra-org corroboration, not
independent replication.

The article's suggested health metrics track this bottleneck: PR cycle time
down (and watch for CI/build systems becoming the *next* bottleneck as code
volume grows), onboarding ramp time down, AI-assisted commits up — with the
caveat that throughput is not success; measure the problem you're solving.
