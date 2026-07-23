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
  - "[[AI Software Factory]]"
  - "[[AI-Native Role Archetypes]]"
  - "[[Just-in-Time Planning]]"
  - "[[Founder as Orchestrator]]"
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
> First-party from the Claude Code team; single org so far.

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
