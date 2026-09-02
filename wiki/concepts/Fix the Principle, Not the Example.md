---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[Self-Improving AI Loop]]"
  - "[[Verification Bottleneck]]"
  - "[[Ingest Workflow]]"
  - "[[Organizational Legibility]]"
confidence: medium
tags: [ai-native, feedback-loops, evals]
---

# Fix the Principle, Not the Example

[[Uriah Israel]]'s rule for how a [[Self-Improving AI Loop]] learns from
corrections: a correction must change the *instruction* that produced the
mistake, not add the mistaken case as a patch. From Cainex's medical-coding
loop in [[2026-08-20 The Claude Code Guide For Startups]], where "a wrong code
isn't a typo. It's a billing and compliance event."

The loop as described:

1. An agent processes a batch; human auditors review the output **and the
   model's reasoning** in an internal app, commenting on both. Everything is
   versioned and auditable.
2. Claude Code reads the predictions plus every correction, each tagged by
   kind (diagnosis, procedure, …), and goes to the guidance governing that kind.
3. It finds the part of the agent's instructions that produced the mistake and
   revises it, or writes new guidance when the case is genuinely new. Every
   change is made against a versioned instruction set.
4. **Back-test**: the candidate change runs across a golden set plus random
   samples. A record can have more than one acceptable coding, so the check is
   semantic matching plus a judge asking "is this a real error or just a
   different valid path?"
5. The output is a short list: suggested edits, unresolved records, open
   questions. Engineers spend their time on the hard cases, not the
   "mechanical 80%."

> [!claim] Example-level fixes make a self-improving loop accumulate patches instead of getting smarter
> confidence: medium · status: supported
> evidence: "It didn't start this clean. Our first version overfitted. It would
> 'fix' things by encoding the specific case, and we were accumulating patches
> instead of getting smarter. We changed the approach to force general
> principles and to cap how many specifics can enter a change at all" —
> [[2026-08-20 The Claude Code Guide For Startups]]. Single company,
> first-party. The failure mode is overfitting and plausible on general
> grounds; the fix's effectiveness is asserted, not measured.

Two structural requirements fall out. Corrections must be **legible** — tagged,
versioned, reasoning visible — which is [[Organizational Legibility]] applied
to agent output. And there must be a **golden set** to back-test against,
which the guide generalizes to "every startup should maintain multiple sets of
evals for their key use cases, and update them regularly" (see
[[Verification Bottleneck]]).

It is also the [[Ingest Workflow]]'s rule restated: a new source updates the
general page and its claims rather than appending a one-off note, and lint
catches drift. Patch accumulation is what an unmaintained wiki looks like.
