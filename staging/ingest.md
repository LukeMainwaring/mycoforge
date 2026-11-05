# Ingest queue

Sources captured in `raw/` that have not been ingested yet, in recommended
order. One source per session: run Ingest, tick the row once the `ingest |` log
entry exists. The "watch out" line is the question most likely to pull the session off
course, usually where the source argues with this KB's own conventions. It is a
prompt to evaluate, not a conclusion; per the Ingest workflow, if the answer
implies a schema change, note it in the log and do it on a branch. Plain markdown links only, so lint
leaves this file alone.

- [x] `raw/articles/2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn).md` — Spawn CEO's own account of a ten-person company run by a persistent agent fleet. Watch out: a self-report with unaudited numbers, so medium at best. It contradicts the production-gate claim in Tiered Autonomy and the committed-artifact claim in AI-Native SDLC (no PRs, hourly ship to production): contest those two, cite both. One new page (Stigmergic Coordination); precedent judges go in Organizational Legibility; no person page, no Spawn page. Leave out the vendor model comparisons, which date fast.
- [x] `raw/podcasts/2026-10-31 The AI Daily Brief - How the Most AI Pilled Company in the World Works (clip - Spawn).md` — companion to the Spawn article; cite only host commentary from [27:51] on (the two "hard to copy" doubts, five takeaways) onto Nathaniel Whittemore and the claims they challenge. The retelling before that is not evidence — it misstates figures (4 hours vs 4 minutes, 60% surge, "trained" judges, "Sundays off"). No new pages.
- [x] `raw/podcasts/2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd.md` — Warp CEO on the factory as infrastructure: factory as code, the stack, scorers, benchmarks, cost per PR. Watch out: vendor demo, auto captions garble model and benchmark names; leave out model scores and subscription economics.
- [ ] `raw/podcasts/2026-11-02 Warp - How to build an agentic self improvement loop.md` — companion to the Latent Space episode: Warp's DevEx lead on how scorers are built (traces, 0–1 rubrics, failure isolation, a daily self-improvement agent, Skill Doctor). Watch out: most of it is new beside the podcast, and it lands on Self-Improving AI Loop and Skill Evolution, maybe a scorer page; the "Kent C. Dodds test pyramid" with end-to-end tests on top sounds like his Testing Trophy, so check before claiming it; the sample rubric and report were on screen only. Carries the held schema question: should this KB score its own agent sessions?
