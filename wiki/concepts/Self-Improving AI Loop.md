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
  - "[[Organizational Legibility]]"
confidence: medium
tags: [ai-native, feedback-loops]
---

# Self-Improving AI Loop

The unit of the [[AI-Native Company]]: a company process wrapped in a feedback
loop that improves itself with minimal human intervention. [[Diana Hu]] frames it
in control-systems terms — pre-AI companies ran as **open loops** (decide,
execute, rarely measure); a **closed loop** continuously monitors output and
adjusts. [[Tom Blomfield]] calls the same thing "recursive self-improving AI
loops."

Blomfield's loop anatomy:

1. **Sensor layer** — customer emails, support tickets, code changes, churn
   events, telemetry
2. **Policy layer** — what the AI may do, what needs human permission, what must
   be logged
3. **Tool layer** — deterministic APIs (query the database, read the calendar)
4. **Quality gate** — evals, deterministic checks, safety filters, human review
   for high-risk actions
5. **Learning mechanism** — failures feed back to the top

> [!claim] A monitored agent loop can fix its own failures overnight, unattended
> confidence: medium · status: supported
> evidence: YC's internal query agent gained a monitoring agent that watches every
> failed query, diagnoses the gap (missing tool? stale skills file? new index?),
> writes the fix, opens a merge request, has an agent review, merge, and deploy it
> — "when a human comes the next day to ask the same query, it will now succeed"
> — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> Single first-party anecdote; no external replication cited.

Other proposed loops: a product loop (agent mines analytics for funnel friction,
researches fixes, runs an A/B test, deploys the winner, repeats) and a support
loop (agent triages suggestions against the roadmap, ships accepted ones
overnight). The precondition for all of them is [[Organizational Legibility]] —
a loop can only learn from what got recorded.

The sidekick-vs-loop distinction is the load-bearing idea: an agent that answers
questions is "last year's version… making me 20 or 30% more effective"; the loop
is what compounds. Kin to this KB's own thesis — see
[[Why LLM Wikis Beat RAG]] on compounding vs re-deriving.
