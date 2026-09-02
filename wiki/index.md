# Index

The catalog: every wiki page, one line each. Updated on every ingest.

## Meta

- [[overview]] — what this KB is and where to start

## Concepts

- [[Three-Layer Architecture]] — raw / wiki / schema, and why the ownership boundary matters
- [[Ingest Workflow]] — the write path: integrate, don't index; one source per session
- [[Subtractive Onboarding]] — ship with everything on, prune down deterministically
- [[Fractal Federation]] — nesting KBs: orchestrator as a feature, children as independent repos
- [[AI-Native Company]] — AI as the company's OS, not a tool; umbrella for the AI-native cluster
- [[Self-Improving AI Loop]] — closed-loop processes that fix themselves; loop anatomy
- [[Organizational Legibility]] — record everything; diarize down; the YC user manual example
- [[Company Brain]] — durable context at the center, humans at the edge, software ephemeral
- [[AI Software Factory]] — humans write specs and tests; agents write the code
- [[AI-Native Role Archetypes]] — Dorsey's IC/DRI/AI-founder × Claude Code's hiring profiles × the founder archetype
- [[AI-Native Startup Lifecycle]] — Idea/MVP/Launch/Scale remapped: exit criteria and AI-specific failure modes
- [[Founder as Orchestrator]] — founder as director of agents; the inverted failure modes of effortless building
- [[Verification Bottleneck]] — the constraint moves from writing code to judging it
- [[Just-in-Time Planning]] — prototypes replace design docs when building is cheap
- [[Everyone Ships]] — non-technical staff ship the 0→1 prototype; the mechanisms that make it systemic
- [[Fix the Principle, Not the Example]] — how a self-improving loop learns from corrections without overfitting; Cainex's back-tested loop
- [[Build for Rebuilding]] — software as disposable per model generation; a rebuild is done when the old path is gone
- [[Prototype, Dogfood, Productionize]] — internal agents that earn it become product; building with AI teaches harness design

## People

- [[Andrej Karpathy]] — author of the LLM Wiki gist this KB implements
- [[Diana Hu]] — YC GP; the founding AI-native-company talk
- [[Tom Blomfield]] — YC GP; self-improving loops, company brain, legibility
- [[Jack Dorsey]] — cited secondhand: intelligence-layer org, IC/DRI/AI-founder archetypes
- [[Kareem Amin]] — Clay CEO: hire tinkerers, build it four times, the moat is self-improvement
- [[Uriah Israel]] — Cainex CTO: the medical-coding loop behind fix-the-principle

## Syntheses

- [[Why LLM Wikis Beat RAG]] — compile-at-ingest vs retrieve-at-query, claims marked

## Raw sources

- [[2026-04-04 LLM Wiki (Karpathy)]] — the founding gist (article, 2026-04-04)
- [[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]] — Diana Hu talk (podcast, 2026-04-24)
- [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]] — Tom Blomfield talk (podcast, 2026-05-21)
- [[2026-05-06 The Founders Playbook (Anthropic)]] — Anthropic's AI-native startup lifecycle ebook (article/PDF, 2026-05-06)
- [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]] — Claude Code team's first-party account (article, 2026-06-03)
- [[2026-08-20 The Claude Code Guide For Startups]] — five rules from a dozen Claude Code startups (article/PDF, 2026-08-20)

<!-- sf:begin(product) -->
## Decisions

- [[ADR-001 Separate Repo with Product as Seam]] — KB and software live apart, bridged by MCP
- [[ADR-002 Fractal Federation for Nested KBs]] — orchestrator as a cuttable feature
- [[ADR-003 Copy-and-Own with Config-Code Split]] — vendored tooling, instance data in kb.toml
- [[ADR-004 Read-Only MCP in v1]] — search/read/index only; writes stay interactive
- [[ADR-005 Onboarding Archetypes as Presets]] — second-brain and playbook as /onboard presets, no new machinery
<!-- sf:end(product) -->
