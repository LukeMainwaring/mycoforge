---
type: concept
created: 2026-11-02
updated: 2026-11-02
sources:
  - "[[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]]"
  - "[[2026-10-31 The AI Daily Brief - Artificial Intelligence News - How the Most AI (clip - 15 -00-30 -35)]]"
raw:
  - raw/articles/2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn).md
  - raw/podcasts/2026-10-31 The AI Daily Brief - Artificial Intelligence News - How the Most AI (clip - 15 -00-30 -35).md
related:
  - "[[Verification Bottleneck]]"
  - "[[Tiered Autonomy]]"
  - "[[AI-Native SDLC]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Organizational Legibility]]"
  - "[[AI-Native Company]]"
  - "[[Nathaniel Whittemore]]"
confidence: medium
tags: [ai-native, software-engineering, coordination]
---

# Stigmergic Coordination

Agents coordinating through the thing they are changing (the code, the live
product, the database) instead of telling each other what they are about to
change. The term is from ant colonies: an ant leaves a trail and the others
read the trail, not a message. Spawn, a ten-person game-engine company whose
work is done by a persistent agent fleet, runs its engineering this way —
[[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]].

Spawn's starting problem: once the fleet ran, agents spent their time
announcing changes. An announcement touches every piece of work that depends
on the thing changed, so if every agent tells every other agent, "double the
agents and you roughly quadruple the chatter." The argument for dropping it:
human teams coordinate heavily because people specialize (one knows the
database, another knows how player data is used), and the pull request is
where the specialists meet. Agents that each understand the whole system can
each own a task end to end, so Spawn "killed PRs" earlier in 2026.

> [!claim] Agents that each understand the whole system can coordinate through the code instead of announcing changes, and drop PR review
> confidence: medium · status: supported
> evidence: "For our agents, the world is the code, the live product and the
> database, and each agent just works on that" — work built on an old
> structure no longer fits and cannot land until updated, and whichever agent
> lands second does the update —
> [[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]].
> One company's account of its own practice. The premise, that agents are not
> specialized the way people are, is asserted rather than shown.

## How it stays sound

Dropping the pre-merge gate moves verification after merge; it does not
remove it ([[Verification Bottleneck]]):

- **Converge on a clock, not per change.** Changes may land "not quite
  right"; everything must be in line once an hour. Janitor agents clean up
  the disorder in between.
- **Fix forward.** When something breaks, an agent is created on the spot to
  fix it with a new change on top, rather than undoing and redoing the
  original. Spawn's justification is that agents are fast and always on.
- **Test the latest, not each change.** An agent runs the code and uses the
  product before landing, but not the whole suite. The suite runs against
  the latest code every 15 minutes, and "it broke in the last 15 minutes" is
  enough to find the cause. At Spawn's scale that is about 5,000 vCPUs,
  17 TB of RAM and 150 GPUs.
- **Adversarial review inside the team.** Before a change lands, helper
  agents that did not write it try to break it.
- **Hard gates only where nothing can be undone.** Actions that touch the
  outside world irreversibly, like sending a payment, go through "a small set
  of dumb, hard-coded gates." This is where the gate moved to: from
  production to irreversibility ([[Tiered Autonomy]]).

> [!claim] Without pre-merge review, a codebase stays sound if checks run after merge on a fixed clock and every break spawns a fixer
> confidence: medium · status: supported
> evidence: "over the last year only 1,055 of our 123,548 changes were
> reverted, about 0.9%" —
> [[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]].
> Self-reported and unaudited; a revert rate also says nothing about breaks
> that were fixed forward rather than reverted, which is the method's default.

The medium is not code alone. Spawn has also kept every call since 2024 as
text in the repo, next to the code, so the trail agents read includes a
written record of why ([[Organizational Legibility]]). The loop that tells
an agent its change broke something is in [[Self-Improving AI Loop]], and
the counter-position, a chain of committed artifacts and PRs as the handoff,
is [[AI-Native SDLC]].

## How far it travels

[[Nathaniel Whittemore]] ([[2026-10-31 The AI Daily Brief - Artificial Intelligence News - How the Most AI (clip - 15 -00-30 -35)]]) doubts two things: that it can be retrofitted
onto an existing system rather than started in a new division or product,
and that it works without a product whose users' agents file bug reports as
they play, a feedback loop most categories lack. His portable version is
"letting the work carry the context": more agents create more coordination
overhead, and a shared, current record shows what changed, who owns the next
step and what is unresolved.
