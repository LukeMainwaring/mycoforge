# Ingest queue

Sources captured in `raw/` that have not been ingested yet, in recommended
order. One source per session: run Ingest, tick the row once the `ingest |` log
entry exists. The "watch out" column is the thing most likely to pull the
session off course, usually a point where the source argues with this KB's own
conventions; per the Ingest workflow, note that in the log and change the
schema on its own branch, not mid-ingest. Plain markdown links only, so lint
leaves this file alone.

## From /scout 2026-10-22

- [ ] `raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md` — cleanest statement of the thesis, so it goes first. Watch out: its three layers are raw logs → wiki → *executable skills*, with the wiki feeding skill updates. This KB has no path from `wiki/` back into `.agents/skills/`; that is a structural gap, not a page edit. Also: this is the first empirical source, so claims it supports should move from practitioner-backed to paper-backed, not just gain a citation.
- [ ] `raw/articles/2026-10-16 gbrain Belief Ledger Design (Garry Tan).md` — long (1,700 lines); sections 1–4 and 13–15 carry the argument, 5–12 are DB mechanics. Watch out: it directly contests the assumption that `log.md` + git is a sufficient record of what the wiki believed and when. Expect a contested claim and a schema implication about claim-status history, not a rewrite of the Three-Layer Architecture page.
- [ ] `raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md` — same pattern, different conventions. Watch out: per-claim provenance tags, lint rules for speculative drift, and a locked writer for index/log are all proposals against this KB's Claims and Lint sections. Compare, don't adopt in-session.
- [ ] `raw/articles/2026-10-22 langchain-ai openwiki (repo).md` — the vendor-scale comparator. Watch out: continuous connector-driven ingest with CI-opened PRs vs. this KB's one-source-per-session rule; Grounded Claims pin evidence to versioned line ranges. Good material for Ingest Workflow and Why LLM Wikis Beat RAG; resist turning the ingest into a feature comparison page.
- [ ] `raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md` — shortest, lowest conflict. Watch out: it is the published sibling of `/scout` (per-source bookmarks, append-only ledger, read-only prefs vs read-write state). The temptation is to edit the scout skill; instead file the pattern as a concept page and note any skill change for a branch.
