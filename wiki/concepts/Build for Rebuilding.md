---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[Company Brain]]"
  - "[[Just-in-Time Planning]]"
  - "[[AI Software Factory]]"
  - "[[Self-Improving AI Loop]]"
confidence: medium
tags: [ai-native, software-engineering]
---

# Build for Rebuilding

Rule 4 of [[2026-08-20 The Claude Code Guide For Startups]]: model capability
keeps shifting underneath these teams, so very little is treated as permanent.
Features and scaffolding "were discarded the minute they became sunk costs,"
and the startups count the rebuilding itself as competitive advantage.

> [!claim] AI-native startups treat software as disposable and rebuild it per model generation
> confidence: medium · status: supported
> evidence: Clay: "you build it and then you build it again and then you build
> it again. And then the fourth time you build it, you know everything that's
> needed and you get it right" ([[Kareem Amin]]); Harvey re-architected its
> platform for each wave of model capability: "If we hadn't been willing to say
> 'Hey, we need to scrap this and go agent native' we simply could not have
> these capabilities" (Niko Grupen) —
> [[2026-08-20 The Claude Code Guide For Startups]]. Practitioner corroboration
> of [[Tom Blomfield]]'s ephemeral-software prescription in [[Company Brain]]:
> the durable asset is what you learned across the four builds, not the code.

Commure's completion rule, from Tanay Tandon: "A rebuild isn't done when the
new path ships. It's done when the old path is gone." Teardown "always lost the
prioritization fight" because it ships no features; now an engineer invokes a
skill ("for every feature flag already released to everyone, open a PR removing
it and the associated code"), reviews the fan-out, and migrations that ate dev
cycles are "a plan and a fan out, done in a couple of hours." The same
kill-obsolete-process discipline as [[Just-in-Time Planning]], applied to code
paths.

Tooling the guide attaches: git worktrees so v2 runs beside v1 and evals decide
which one merges ("what makes 'build it four times' cheap"), and plan mode for
any rewrite big enough to drift from the architecture.

Clay's moat argument follows from this: "the moat for any company right now is
that it needs to be self-improving" — see [[Self-Improving AI Loop]].
