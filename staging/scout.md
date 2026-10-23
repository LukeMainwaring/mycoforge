# Scout ledger

Every `/scout` run appends a section here: the candidates it found, and what
happened to each. Statuses: `candidate` → `approved` → `captured → <raw path>`,
or `rejected`. Edit a status cell to review, or tell the agent in conversation; rows you
don't mention stay `candidate` and carry forward.
The latest run header is where the next run's window starts.

## [2026-10-22] window 2026-07-24 → 2026-10-22

| # | source | date | kind | adds | status |
|---|--------|------|------|------|--------|
| 1 | [WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution](https://arxiv.org/abs/2608.27454) | 2026-08-27 | paper | Empirical three-layer analogue (raw logs → compiled wiki → skills); ablations show the persistent wiki is what makes skill evolution work. First academic citation for Three-Layer Architecture and Why LLM Wikis Beat RAG | captured → raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md |
| 2 | [gbrain: Belief ledger design](https://github.com/garrytan/gbrain/blob/master/docs/designs/BELIEF_LEDGER.md) | 2026-10-16 | repo | Append-only event log of claim/page transitions with observation time; argues git + markdown cannot carry "what did we believe when". Direct challenge to log.md-as-provenance and an extension of the claim status lifecycle | captured → raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md |
| 3 | [langchain-ai/openwiki](https://github.com/langchain-ai/openwiki) | 2026-10-21 | repo | Major-vendor reference implementation (17k stars, weekly cadence): continuous connector-driven ingest of code and outside sources into local markdown. Comparator for Ingest Workflow's one-source-per-session rule | captured → raw/articles/2026-10-22 langchain-ai openwiki (repo).md |
| 4 | [Building effective agent automations (Anthropic)](https://claude.dev/blog/building-effective-agent-automations/) | 2026-10-08 | article | First-party pattern for unattended recurring agents whose only continuity is markdown state: read-only prefs vs read-write state, per-source bookmarks, append-only ledger, re-verify before posting. Closest published sibling to this KB's /scout ledger and log.md | captured → raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md |
| 5 | [The State of AI Harness Engineering 2026 (marmelab)](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html) | 2026-09-24 | article | Audit of 246 repos and 481 CLAUDE.md files: 4.4% of prose security rules had an enforcing control; AGENTS.md as table of contents of the rule tree. Numbers for Advisory and Deterministic Controls and Progressive Disclosure | rejected |
| 6 | [ar9av/obsidian-wiki](https://github.com/ar9av/obsidian-wiki) | 2026-10-21 | repo | 3.6k stars, dated monthly releases: locked atomic writer for index/log so parallel agents don't clobber, claim provenance tags (extracted / inferred / ambiguous) with lint for speculative drift, incremental-ingest manifest. Direct input to the Claims and Lint conventions | captured → raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md |
