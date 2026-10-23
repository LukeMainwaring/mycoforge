# Schema review diff (obsidian-wiki drift lint) — opus-5.5 vs gpt-6, 2026-10-23

Comparison only. Quotes are verbatim.

## Summary lines
Agree: do not adopt a drift lint; take option (a); no change to `scripts/lint.py`, no new `kb.toml` field; reject (b) because counting `^[inferred]` "measures declared annotations, not missed inferences" (gpt-6) / "only counts inference the agent already admitted to" (opus); reject (c) as an unauditable number.
Agree on first step: fix the sampled pages. Opus: "promote or cut the roughly 5 sentences named above"; gpt-6: "review the three sampled pages against their sources, removing overstatements and promoting substantive inferences into auditable callouts."
Disagree on the AGENTS.md wording. Opus redefines `speculative` as "an inference the agent drew rather than a source stated, whether filed by `/connect` or written during ingest". GPT-6 keeps `speculative` for when "premises do not establish the conclusion" and asks that agent-derived claims "identify their inference and its premises in the evidence line". Turns on whether origin (inferred) and standing (unsupported) should share one status. GPT-6: "Origin and evidential standing are separate dimensions."

## Measurement
Agree on the three pages, within range: Why LLM Wikis Beat RAG ~50% / 35–50%; Progressive Disclosure ~45% / 40–55%; Three-Layer Architecture 25–30% / 25–40%. Both name "strictly worse than RAG" as the clearest contestable sentence outside a callout.
One only:
- Opus: 0 of 48 callouts in `wiki/` are `speculative`; the agent's inferences land as `supported` or as bare prose.
- GPT-6: inference "is not synonymous with speculation"; a synthesis page is inferred by design.

## Real or local
Agree: real but narrow; the failure is a single inference that skips the callout when written, not drift over several ingests; one source per session with a human reading each commit limits exposure. Both: the README gives no algorithm or threshold for its lint, so its efficacy is unknown.

## Missed
Agree: `undated_claims` appears only in the capturer's repo notes; capture `docs/` before proposing anything. Locked writer: defer until concurrent sessions exist. Manifest: no need under one-source-per-session. Session hooks: a start recap is harmless, an end-of-session capture nudge conflicts with user-invoked capture (opus) / with the deliberate ingest boundary (gpt-6).
One only:
- Opus: a deterministic lint warning for a `raw/` file cited by no wiki page ("captured, never ingested"); "challenge queries" are `/grill-me` grounded in the wiki; obsidian-wiki writes `extracted` bare, so extracted prose may be unmarked there too, which narrows the gap between the designs.
- GPT-6: the orphan check already excludes index/log; the benchmark does not prove constant query cost at 2,000 pages.

## Misread (both)
Agree: "from the tag mix" invents an algorithm; "every claim-shaped sentence" / "tagging every sentence" strengthens "every claim"; `undated_claims` attributed to the README in prose; "chosen to avoid" assigns an undocumented motive to the anti-padding rule; the claim's "cannot" is the KB's own position marked `supported`.
Opus only: the evidence line quotes `check_claims` with text that is in ADR-010, not `lint.py`; "three implementations in `raw/`" when this KB is not in `raw/`; Three-Layer Architecture's "page to the sentence" should be "claim to the sentence".
GPT-6 only: "only `/connect` files" `speculative` overstates the schema; `ambiguous` as "the source itself unclear" is an interpretation.
