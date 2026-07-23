---
type: concept
created: 2026-07-23
updated: 2026-07-23
sources:
  - "[[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]"
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
raw:
  - raw/podcasts/2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up.md
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
related:
  - "[[AI-Native Company]]"
  - "[[Company Brain]]"
  - "[[Ingest Workflow]]"
  - "[[Why LLM Wikis Beat RAG]]"
confidence: medium
tags: [ai-native, knowledge-capture]
---

# Organizational Legibility

Making the whole organization readable by AI: every important action produces an
artifact the intelligence layer can learn from. The precondition for every
[[Self-Improving AI Loop]] and the input to the [[Company Brain]].

> [!claim] If it wasn't recorded, it didn't happen — to the AI
> confidence: high · status: supported
> evidence: "if it is recorded, it happened to the AI. If it did not get
> recorded, it did not happen to your intelligence" — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> Practices from both talks: AI note-takers in every meeting, minimize DMs and
> email (they're illegible silos), record office hours and sales calls, pipe
> everything into one queryable store.

## Diarization: raw capture is necessary but not sufficient

> [!claim] Raw recordings must be synthesized down — context windows can't hold an org's history
> confidence: high · status: supported
> evidence: "you cannot pump in 100,000 hours worth of recordings into a context
> window… aggregate it down, synthesize it into the important parts, and give the
> AI breadcrumbs" — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> This is compile-at-ingest at organizational scale — the same argument as
> [[Why LLM Wikis Beat RAG]], arrived at independently.

## Worked example: the self-improving YC user manual

From ~2,000 hours of recorded office hours, YC regenerated its 5–10-year-old
user manual in a weekend: diarize, categorize (fundraising, hiring, co-founder
disputes…), rewrite — yielding a 150-page manual that can now be refreshed
monthly, each new piece of partner advice "compared with the existing manual and
either incorporated or thrown away." Structurally, that *is* this KB's
[[Ingest Workflow]]: new source → integrate into persistent pages → keep
current. The regenerated manual then becomes agent context — "the combined
wisdom of 16 YC partners in one."

[[Diana Hu]]'s version of the payoff: sprint planning where an agent with access
to tickets, Slack, customer feedback, and plans replaces lossy status roll-ups —
"what used to require constant coordination becomes legible and queryable by
default."
