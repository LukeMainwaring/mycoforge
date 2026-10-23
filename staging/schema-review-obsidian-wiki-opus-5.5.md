# Schema review (obsidian-wiki drift lint) — opus-5.5, 2026-10-23

## Summary
Don't adopt the drift lint: no `^[inferred]` marks and no `inferred:` count. Take option (a), slightly widened.
The real gap is narrow. A few contestable inferences per page sit outside callouts, and the KB has no place for the agent's own claims because `speculative` is defined as what `/connect` files.
First change: one sentence in `AGENTS.md` Claims and one in the Lint judgment pass. No change to `lint.py`.

## Measurement
- **Why LLM Wikis Beat RAG**: about 50% of the ~10 prose lines outside callouts are inferred. The closing "honest caveat" is all inference and contestable ("strictly worse than RAG, which at least never pretends to remember"), and it has no mark.
- **Progressive Disclosure**: about 45% of ~40 lines. Most of it is "This KB is one" and the "/connect should skip them" prescription, i.e. the KB applying sources to itself, which can be checked against the repo rather than a source. Only the "same constraint as diarization" framing is world inference.
- **Three-Layer Architecture**: about 25–30% of ~55 lines. Three load-bearing inferences have no mark: "holds with no human in the loop at all", "the layering survives… not a fourth layer", and "precisely because it can never damage the sources".
- Across all three, inferred prose falls into three kinds. (1) Cross-links and framing, which is the wiki's job. (2) Application to this KB, which can be checked in git. (3) Contestable claims about the world that skipped a callout, about 1–3 sentences per page. Only (3) is a gap.
- Related finding: 0 of the 48 callouts in `wiki/` are `status: speculative` (42 are supported, 2 contested). The agent's own inferences end up either `supported` or in bare prose. Example: the claim in Provenance Tags.md has a second half that is the KB's own position, yet it is marked `supported`.

## Real or local
Real, but small, and a different shape from the one obsidian-wiki's lint targets. obsidian-wiki's setting produces drift: batch ingest of directories, `/wiki-capture` of conversations, mining whole agent session histories, and no human reading each page. Here there is one source per session, the takeaways are discussed with the user first, and each ingest is one reviewable commit. Pages do not "drift" over several ingests without a person seeing the diff.

The failure that does happen here is a single inference that bypasses the callout at the moment it is written. Per-sentence tags cannot catch that either. A lint counting `^[inferred]` only counts inference the agent already admitted to. An unmarked inferred sentence looks exactly like an unmarked extracted one, so the failure mode is invisible to the check. Whether obsidian-wiki's lint does anything smarter cannot be known from the README alone (its docs were not captured).

## Smallest change
Option (a), widened so it can be used during ingest:
- **AGENTS.md › Claims.** Redefine `speculative` as "an inference the agent drew rather than a source stated, whether filed by `/connect` or written during ingest; it names what would confirm or refute it." Then add: "If you would write a contestable sentence that no source states, put it in a `speculative` callout or cut it. Cross-links and statements about this KB itself stay as prose."
- **AGENTS.md › Lint step 2.** Add to the judgment list: "contestable inference in bare prose; supported claims whose evidence is the KB's own reasoning."
- **scripts/lint.py.** No change. `check_claims` already accepts `speculative` from `kb.toml`. No new `kb.toml` fields.
- **Existing pages.** No sweep. Fix on touch: during the next lint pass, promote or cut the roughly 5 sentences named above, and split the Provenance Tags claim (keep the sourced half `supported`, file the KB-position half as `speculative`). Name the split in the log entry, as the schema requires.

Rejected: **(b)**, for the reasons above and under Cost. **(c)**: a hand-maintained number that lint cannot check (it cannot count unmarked sentences), which goes stale on the first hand edit. That is bookkeeping with no audit value.

## Cost
- **(a)**: per ingest, about one more judgment per touched page and 0–2 extra callouts; this ingest touched 4 pages. Reader noise is low, because callouts are already the reading convention. The risk is callout inflation, a page that turns into a wall of boxes. The "or cut it" clause is the guard and matches the anti-padding rule.
- **(b)**: per ingest, a classification of every non-callout sentence on every touched page, plus a one-time retrofit of 40 wiki pages. At the measured rates, 25–50% of prose sentences would carry a mark. In Obsidian, `^[inferred]` is an inline footnote: reading view shows a superscript number after each tagged sentence and a "Footnotes" list at the bottom saying "inferred" over and over. That is pure page noise for a human reader. A threshold in `kb.toml` would also need to vary by type, because `type: synthesis` pages are inferred by design. That means more config to keep lint quiet on exactly the pages that are the KB's point.
- **(c)**: low effort, zero value, plus a frontmatter field that is wrong most of the time.

## Missed
- **`undated_claims`**: this appears only in the capturer's "Repo notes", not in the README, and its behavior is unknown. It overlaps ADR-006's two clocks in spirit. Before proposing anything, capture `docs/architecture.md` / the lint skill.
- **Locked atomic writer**: local to obsidian-wiki. It solves parallel agents writing `index.md`/`log.md`. This KB has one session per workflow run and commits through git, and a lost append would show in the diff. No change. If parallel agents ever arrive, git merge conflicts are the lock.
- **Ingest manifest**: `staging/ingest.md` plus `sources:`/`raw:` frontmatter already show what has been ingested. A delta manifest only pays off for batch re-runs over a directory, which this KB rules out. A cheap version of the same check would be a lint warning for a `raw/` file cited by no wiki page ("captured, never ingested"). It is deterministic and fits `lint.py` without per-instance data. Worth a separate proposal.
- **Session hooks**: the end-of-session capture nudge conflicts with the memory rule that capture skills are user-invoked. Reject. A start-of-session recap is already partly covered by the `git status` hand-edit check and `grep log.md | tail`.
- **Challenge queries** (arguing against a plan from the vault's own record): this is `/grill-me` grounded in the wiki. It is a possible Query variant, not a schema change.
- **Granularity**: the README writes `extracted` bare and the other two as `^[...]`. That suggests extracted is the unmarked default, so obsidian-wiki may also leave most prose unmarked. That narrows the gap between the two designs.

## Misread
- Provenance Tags.md says the lint flags drift "from the tag mix". The README does not say how drift is computed.
- It gives the unit as "every claim-shaped sentence". The README says "every claim", and its notation suggests `extracted` carries no mark (see Missed). The table overstates how much gets marked.
- It states `undated_claims` as part of the source ("beside it") in prose. Only the evidence line correctly attributes it to the repo notes.
- Its evidence line quotes `check_claims` as saying "does not try to find contestable prose that should have been a claim". That text is not in `scripts/lint.py`. The function's docstring says "Shape of the claim contract, not its truth". In git history, outside the off-limits `decisions/` folder, the quote first appears in the ingest commit d4e0b21.
- The claim is marked `supported`, but its second half ("marking only contestable claims cannot") is the KB's own reasoning, not the source's. By this review's rule it is `speculative`.
- "Three implementations in `raw/`": this KB is not in `raw/`.
- "The cost is tagging every sentence, which the anti-padding rule… [was] chosen to avoid": that motive is invented. The rule is about filler, not tagging.
- "A page's share of inferred prose can rise over several ingests and nothing here would notice" is itself an unmarked contestable inference, and the measurement above weakens it: each ingest is a reviewed single-source commit.
- Three-Layer Architecture says obsidian-wiki "moves provenance down a level, from the page to the sentence". This KB already has provenance below the page, at the callout, so the step is from the claim to the sentence.
