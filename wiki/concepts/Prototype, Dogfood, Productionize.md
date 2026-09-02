---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[AI Software Factory]]"
  - "[[Everyone Ships]]"
  - "[[Why LLM Wikis Beat RAG]]"
  - "[[AI-Native Company]]"
confidence: medium
tags: [ai-native, product]
---

# Prototype, Dogfood, Productionize

Rule 5 of [[2026-08-20 The Claude Code Guide For Startups]], the flywheel
between how these startups build and what they build: build an internal agent
with Claude Code, use it internally, and promote the ones that earn it to
customer-facing product (via API, SDK, or managed agents). ClickHouse's
SQL-console agent and AI SRE, and Omni's packaged data analysis, started this
way; ClickHouse uses Claude Code to iterate on the product agents themselves.

The second-order effect is that practising agentic coding teaches harness
design. Omni: "We took inspiration from [Anthropic's] file vs embedding
approach, which emboldened us to keep things simple in our own product. We
avoided a lot of complexity that would have come from a RAG pipeline" (Chris
Merrick) — practitioner evidence for [[Why LLM Wikis Beat RAG]]. Emergent gets
faster triage because its app builder runs on the same models: "we can quickly
debug locally via Claude Code to tell whether it's model behavior or a harness
issue" (Mukund Jha).

Same shape as the relentless-dogfooding rollout principle in
[[AI-Native Company]]; here the dogfood is also the product pipeline, and the
prototypes come from anyone ([[Everyone Ships]]).
