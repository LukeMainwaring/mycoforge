# Ingest queue

Sources captured in `raw/` that have not been ingested yet, in recommended
order. One source per session: run Ingest, tick the row once the `ingest |` log
entry exists. The "watch out" line is the question most likely to pull the session off
course, usually where the source argues with this KB's own conventions. It is a
prompt to evaluate, not a conclusion; per the Ingest workflow, if the answer
implies a schema change, note it in the log and do it on a branch. Plain markdown links only, so lint
leaves this file alone.

## From /scout 2026-10-22

- [x] `raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md` — cleanest statement of the thesis, so it goes first. Watch out: its three layers are raw logs → wiki → *executable skills*, with the wiki feeding skill updates. Does this KB need a path from `wiki/` back into `.agents/skills/`, and if so is that a page or a schema change? Also the first empirical source here: which existing claims does it actually support, and should their evidence line change from practitioner to paper?
- [x] `raw/articles/2026-10-15 gbrain Belief Ledger Design (Garry Tan).md` — long (1,700 lines); sections 1–4 and 13–15 carry the argument, 5–12 are DB mechanics. Watch out: it argues that `log.md` + git cannot record what a wiki believed and when. Does that argument hold for a markdown KB with claim callouts, or only for gbrain's database model? Decide whether any existing claim becomes contested before touching the Three-Layer Architecture page.
- [x] `raw/articles/2026-10-22 ar9av obsidian-wiki (repo).md` — same pattern, different conventions. Watch out: per-claim provenance tags, lint rules for speculative drift, and a locked writer for index/log. Which of these solve a problem this KB has, and which only matter for parallel agents? Compare in the wiki; any adoption is a branch.
- [x] `raw/articles/2026-10-22 langchain-ai openwiki (repo).md` — the vendor-scale comparator. Watch out: continuous connector-driven ingest with CI-opened PRs, against this KB's one-source-per-session rule; Grounded Claims pin evidence to versioned line ranges. Is the difference a design choice worth a claim, or just scale? Keep it to Ingest Workflow and Why LLM Wikis Beat RAG rather than a feature comparison page.
- [x] `raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md` — shortest, lowest conflict. Watch out: it is close to `/scout` (per-source bookmarks, append-only ledger, read-only prefs vs read-write state). Does it name a pattern worth a concept page, and does anything in it suggest a change to the scout skill? If so, log it and leave the skill for a branch.
