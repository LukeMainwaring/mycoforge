# Log

Append-only. Most recent at the bottom. Entry format:
`## [YYYY-MM-DD] <prefix> | <Title>` with prefixes
`ingest | query | lint | decision | schema | discovered`.

## [2026-07-10] schema | Initial schema established

Wrote `AGENTS.md`: three-layer architecture, frontmatter schema, claim callouts,
Ingest/Query/Lint workflows, log conventions, template contract.

## [2026-07-10] ingest | 2026-04-04 LLM Wiki (Karpathy)

Ingested the founding gist from `raw/articles/`. Created
[[Three-Layer Architecture]], [[Ingest Workflow]], [[Andrej Karpathy]], and the
synthesis [[Why LLM Wikis Beat RAG]] (three claims marked, all currently
supported). Seeded [[index]] and [[overview]].

## [2026-07-10] discovered | Template concepts are wiki-worthy

The template's own design ideas kept coming up while writing the schema, so they
became pages: [[Subtractive Onboarding]] and [[Fractal Federation]]. No raw
source behind them — provenance is the design session itself.

<!-- sf:begin(product) -->
## [2026-07-10] decision | Founding ADRs 001–004 accepted

Filed the four decisions from the template design session:
[[ADR-001 Separate Repo with Product as Seam]],
[[ADR-002 Fractal Federation for Nested KBs]],
[[ADR-003 Copy-and-Own with Config-Code Split]],
[[ADR-004 Read-Only MCP in v1]]. All `status: accepted`.
<!-- sf:end(product) -->

<!-- sf:begin(product) -->
## [2026-07-17] schema | Roadmap drops Now and Done sections

`roadmap.md` now holds Next / Later only — shipped items are removed rather
than archived (the log and git history are the record). Cleared the completed
v0.1–v0.3 items and updated the Roadmap-upkeep rule in AGENTS.md.
<!-- sf:end(product) -->

## [2026-07-23] ingest | Two YC talks on AI-native companies (paired)

Paired ingest of [[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]
(Diana Hu) and [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]
(Tom Blomfield) — deliberately together, as the second talk builds on the first.
Created concepts [[AI-Native Company]], [[Self-Improving AI Loop]],
[[Organizational Legibility]], [[Company Brain]], [[AI Software Factory]] and
people [[Diana Hu]], [[Tom Blomfield]], [[Jack Dorsey]] (stub, secondhand).
Updated [[Why LLM Wikis Beat RAG]]: Blomfield's diarization argument and the
regenerated YC user manual independently corroborate the compounding claim at
organizational scale. Two Anthropic articles remain captured-but-uningested in
raw/articles/.

## [2026-07-23] ingest | Running an AI-native Engineering Org (Anthropic)

Ingested [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]] — the
AI-native cluster's first first-party practitioner source. Created
[[AI-Native Role Archetypes]] (anchor for the onboarding-archetypes plan;
Dorsey's accountability modes vs Claude Code's hiring filters),
[[Verification Bottleneck]], and [[Just-in-Time Planning]]. Updated
[[AI-Native Company]] (middleware claim low→medium on partial first-party
corroboration of the routing half; archetypes moved out; rollout/metrics
section added) and [[AI Software Factory]] (every-commit-Claude-assisted
evidence). One Anthropic PDF (The Founders Playbook) still awaits ingest.

## [2026-07-23] ingest | The Founders Playbook (Anthropic)

Ingested [[2026-05-06 The Founders Playbook (Anthropic)]] — Anthropic's vendor
prescription to founders (marketing ebook; provenance caveat noted on every
page). Created [[AI-Native Startup Lifecycle]] (four stages with exit criteria
and AI-specific failure modes) and [[Founder as Orchestrator]] (third axis for
the onboarding-archetypes plan). Updated [[AI-Native Role Archetypes]] (two
sets → three), [[Verification Bottleneck]] (founder-level analog: choose/
validate, not build), [[Company Brain]] (context-as-moat claim), and
[[AI-Native Company]] (lean-by-design corroboration). Marked the
prototypes-replace-design-docs claim in [[Just-in-Time Planning]] **contested**:
the playbook mandates architecture + scope docs before MVP code — reconciled
as durable context docs up front, feature planning JIT.

<!-- sf:begin(product) -->
## [2026-07-23] decision | ADR-005 Onboarding Archetypes as Presets
Filed [[ADR-005 Onboarding Archetypes as Presets]] (status: proposed): personal
second-brain and company playbook become `/onboard` interview presets (feature
keep-set + taxonomy + seed pages), no new template machinery; substrate framing
keeps the README lead. Implementation deferred — three Next items added to
[[roadmap]]. Planning handoff file deleted.
<!-- sf:end(product) -->

<!-- sf:begin(product) -->
## [2026-07-23] decision | ADR-005 accepted — archetype presets shipped
Implemented [[ADR-005 Onboarding Archetypes as Presets]] and flipped it to
accepted: archetype question + playbook seed scaffolding in the /onboard skill,
`[archetypes]` preset data in `.template/features.toml`, both preset combos in
`verify_matrix.sh`, and a "two archetypes" entry-paths section in the README
(substrate framing still leads). Shipped items removed from roadmap Next;
dogfooding the playbook preset remains.
<!-- sf:end(product) -->
