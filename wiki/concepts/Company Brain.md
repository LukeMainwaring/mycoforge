---
type: concept
created: 2026-07-23
updated: 2026-07-23
sources:
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
  - "[[2026-05-06 The Founders Playbook (Anthropic)]]"
raw:
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
  - raw/articles/2026-05-06 The Founders Playbook (Anthropic).pdf
related:
  - "[[AI-Native Company]]"
  - "[[Organizational Legibility]]"
  - "[[Three-Layer Architecture]]"
confidence: medium
tags: [ai-native, knowledge-capture]
---

# Company Brain

[[Tom Blomfield]]'s name for the durable center of an [[AI-Native Company]]: all
the data, emails, DMs, skills, and know-how — the extracted domain knowledge
that defines how the company works — with humans arranged **around the edge**,
where the intelligence makes contact with reality.

> [!claim] Business context and skills are the durable asset; software on top is ephemeral
> confidence: medium · status: supported
> evidence: "very preciously store all the data… treat the software as ephemeral.
> The models get smarter in a month or two — throw the software away, give it
> your original set of instructions, and regenerate it" — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> Internal dashboards and workflow tools become on-demand, one-shot,
> regenerable; the instructions that produce them are what you keep. See
> [[AI Software Factory]] for the same inversion applied to product code.

## From efficiency asset to moat

[[2026-05-06 The Founders Playbook (Anthropic)]] corroborates the pattern from
the vendor side and extends it: "investing in persistent context from day one
is what keeps AI a force multiplier instead of a source of entropy."

> [!claim] Accumulated AI context compounds into a defensible moat
> confidence: medium · status: supported
> evidence: domain expertise externalized into structured context and skills
> becomes "a proprietary knowledge substrate that no generalist AI can match";
> compounding user-behavior data is "time-locked, context-specific, and
> impossible for a copycat to recreate" — [[2026-05-06 The Founders Playbook (Anthropic)]].
> Vendor prescription, no independent case data yet — but note it inverts the
> usual moat story: the durable asset is the context layer, not the software
> (Blomfield's ephemeral-software point, above, from the other direction).

## Where humans still matter

Humans reach where models can't: novel situations, ethical considerations,
high-stakes and high-emotion moments (the co-founder-breakup conversation),
in-person contexts like conferences — and sales, which Blomfield puts at "a
human being in the room for the next 20 years."

The structural rhyme with this KB: the brain/edge split mirrors the
[[Three-Layer Architecture]] — durable curated knowledge at the center
(`raw/` + wiki), regenerable consumers at the edge (product repos reading over
MCP, per [[ADR-001 Separate Repo with Product as Seam]]). A MycoForge instance
is a candidate implementation of a company brain; noted here as an observation,
not yet a filed synthesis.
