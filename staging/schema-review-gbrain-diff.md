# Schema review diff (gbrain belief ledger) — opus-5.5 vs GPT-6, 2026-10-23

Comparison only. No recommendation, no merge. Quotes are verbatim.

## Summary lines
Agree: adopt 3 (two clocks), don't adopt 2 (coverage marker), no stable claim ids now, no source-genre tier.
Disagree on 4: Opus adopts a narrowed form ("trust tiers are about *who wrote*... hand edits are kept apart from agent edits"); GPT-6 rejects it outright ("reject ... source-tier scoring for now") and adds only a sentence distinguishing provenance from confidence. Turns on a judgment about what counts as "adopting 4".
Disagree on "do first": Opus: "the raw date check, since it is cheap and already finds a bug." GPT-6: "define historical answers as committed wiki snapshots". Turns on judgment about cost and value.

## 1. Claim identity
Agree: no ids now, no lint; a reworded title does not actually lose git history; if ids ever come, don't retrofit the corpus.
Disagree:
- Real or local. Opus: "mostly local." GPT-6: "Real for reliable automated tracking across moves, splits and rewrites; not a loss of the historical text itself." Turns on judgment: both agree the text survives and only machine identity is missing; they weigh that differently.
- Future id form. Opus: "give that one claim an Obsidian block id (`^short-slug`) and link it as `[[Page#^short-slug]]`" only when a link needs it. GPT-6: "one opaque `id: claim-<uuid>` line inside each callout ... a different proposition receives a new ID and `supersedes: claim-<uuid>`" with repo-wide uniqueness lint. Turns on judgment: Obsidian-native link target vs. opaque machine key.
One only:
- Opus: history is lost only when a claim "**moves between pages** (a split or merge)"; a universal id rewrite would hit "~45 callouts on ~22 pages" and is itself the §2/§9 churn the source warns about.
- GPT-6: gbrain itself does not keep one key through rewording ("a changed fingerprint becomes a new assertion, linked to its predecessor (§§3–4)"); proposes distinguishing "wording-only edits from changed propositions" and retaining the old proposition on supersede.

## 2. Coverage marker
Agree: no page marker, no lint, no new field; markers would be Obsidian noise and would imply more assurance than they give; any record belongs in the log.
Disagree:
- Whether the gap exists here. Opus: "no page here was written before the convention" because the Claims section dates from "the scaffold commit (`2833df0`, 2026-07-10)". GPT-6: "The epistemic distinction is real: old prose can be recovered without an explicitly recorded confidence/status." Turns on a fact about the KB (whether the convention predates all content) and on a judgment (whether "prose without a callout" counts as unrecorded belief).
One only:
- Opus: the gap is real for "an instance that **imports an existing vault**"; suggests one onboarding log line.
- GPT-6: put the rule in Query: historical answers cite a commit and separate "the page stated X" from "a callout explicitly marked X supported"; never invent a date D; a `claims_since` date would not certify intervening edits.

## 3. Two clocks
Agree: real, cheap, worth text in AGENTS.md; wiki `created`/`updated` are maintenance time and must never be backdated to source time; no new wiki fields.
Disagree:
- Lint. Opus: add "a **warning** ... when a raw `.md` file's filename date matches none of `published`, `retrieved` or `created`", ~15 lines. GPT-6: "No new fields or linter changes." Turns on a fact: Opus says drift already exists in raw/; GPT-6 says "no such defect is established by this review" (though GPT-6 is talking about wiki pages copying source dates, not raw filename drift).
- Length. Opus: "not a paragraph, one sentence under File naming". GPT-6: "Add one paragraph to AGENTS.md". Turns on judgment about scope: GPT-6's paragraph also covers "known at T" vs "true at T" and commit-hash citation.
One only:
- Opus: three concrete raw defects: SDLC Playbook `published: 2001-08-21`; gbrain file named by `updated:` (2026-10-16) not `published:` (2026-10-15); mixed `retrieved:`/`created:`/none across raw files, PDFs have no frontmatter.
- GPT-6: a commit timestamp "is a practical publication-time convention, not proof of the agent's first observation or a trusted wall clock"; "Imported/rebased history and branch author dates require qualification"; don't add per-claim `recorded_at`.

## 4. Trust on sources
Agree: the question misreads gbrain, whose tiers are about who wrote, not source genre (§6); no raw tier; confidence stays hand-set and claim-level, not derived; raw files should not carry mutable grading; `contested` is a looser thing than gbrain's gate.
Disagree:
- What to add. Opus: "A claim the user wrote or edited by hand is never superseded by you: set `status: contested`, cite both, and ask." GPT-6: "Add a sentence to Claims distinguishing source provenance, confidence and conflict status. When contested, retain both propositions ... and state what would resolve the conflict". Turns on judgment: Opus carries the writer-tier idea over to hand edits; GPT-6 drops the tier idea and tightens the contested convention instead.
One only:
- Opus: the same source is first-hand on one claim and second-hand on another; `/connect`'s `status: speculative` already follows gbrain's cap rule.
- GPT-6: "`contested` alone neither enforces a write gate nor establishes an owner decision"; cites "Advisory and Deterministic Controls" flagging two sources from one organization as the existing good practice.

## 5. Missed
Agree: both note (differently) that cosmetic/format changes should not count as belief events, and that "what changed" is a question of git history plus the log, not schema.
Disagree: none direct; the lists barely overlap.
One only:
- Opus: hand edits in Obsidian are the unmanaged writer (§5.1, §7); proposes a session-start `git status` check and a separate `hand-edit: <pages>` commit, and calls this "the most useful idea from the source for this KB". Lint's stale check compares mtime to `updated:` and a format migration would trip it everywhere. "What changed this week" is `git log -p --since=7.days -- wiki` filtered to claim lines. Withdrawal is not erasure (§6.5): deleted raw stays in git history.
- GPT-6: the claim contract is not linted at all; proposes a claim-shape check (one confidence, one status, nonempty evidence with a resolving link) and aligning the status vocabulary, since Connect allows `speculative` but Claims lists only supported/contested/superseded. Propagate evidence corrections to dependent claims (§6.3) without auto-downgrades. Historical answers must cite the revision and disclose gaps.

## 6. Misread
Agree: "the one thing ... not recomputable" is wrong, §1 lists it alongside the withdrawal ledger and mutation journal; the commit-time-is-recorded-time line holds only for managed/agent writes; the `contested` analogy overstates equivalence with gbrain's tier gate.
Disagree:
- "History is severed". GPT-6: "too strong in both pages. Git retains the old paths and text." Opus does not call this a misread; it argues the same point in Q1 but does not list it under Misread. Turns on what counts as a page-level error vs. a question-level overstatement.
One only:
- Opus: "a fence format change produces held files" is gbrain-parser-specific, not a markdown property; "nothing marks the beliefs a page held before callouts existed" is hypothetical here; the "diff beliefs, not storage" claim is `confidence: high` on "a free local bench (scratch test, not committed)" (§9).
- GPT-6: markdown analogue is too narrow (status-only; §4 records content, confidence, evidence); coverage cuts are per page (§7.1), not one source watermark; backfill has a recorded run timestamp (§5.4) so does not "carry only source time"; trust behavior overgeneralized (§6.1, §6.2, §6.3); "fourth store" needs a gbrain-specific qualifier.

## Checkable
- Convention predates all content (Q2): `git show 2833df0 --stat` and whether `AGENTS.md` had a Claims section there; compare to the earliest `wiki/` page `created:` dates.
- Raw date drift (Q3): frontmatter of `raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md` (`published:` line) and of `raw/articles/2026-10-16 gbrain Belief Ledger Design (Garry Tan).md` (`published:` vs `updated:`); `grep -L "retrieved:" raw/**/*.md` for the mixed-field claim.
- Lint parses callouts or not (Q5, GPT-6): `scripts/lint.py`, search for `[!claim]`.
- Status vocabulary mismatch (Q5, GPT-6): `AGENTS.md` Claims section vs. the Connect paragraph under Research, Scout, and Connect.
- `/connect` cap rule (Q4, Opus): `.agents/skills/connect/` for how `speculative` is promoted.
- Callout count "~45 on ~22 pages" (Q1, Opus): `grep -rl "\[!claim\]" wiki | wc -l` and `grep -rc "\[!claim\]" wiki`.
- gbrain tier semantics (Q4, both): source §6.1–6.3. Per-page coverage cuts: source §7.1. Backfill timestamp: §5.4. "Scratch test, not committed": §9.
- "diff beliefs, not storage" confidence (Q6, Opus): `wiki/concepts/Belief Ledger.md`, that claim's callout.

## Odd
- The prompt restricts recommended reading to source sections 1–4, 5.4, 6, 7, 13–15. GPT-6 cites §§3–4 fingerprint behavior and §6.1–6.3 event-tier details at a level of detail that may rely on the skimmable sections; Opus cites §9 twice, which the prompt listed as skimmable.
- GPT-6's Q3 says "no such defect is established by this review" while Opus lists three raw-file date defects. GPT-6 appears not to have inspected raw frontmatter beyond the gbrain file; Opus did.
- Opus's Q4 opens with "the question as asked is mostly a misreading", then adopts a change under Q4 anyway and counts it as adopting 4 in the Summary. GPT-6 answers the same question and counts it as a rejection. Same analysis, opposite ledger entry.
- GPT-6's Q2 reasons as if the KB might have pages predating the convention, but never checks; Opus checks and says none do. If Opus is right, GPT-6's Q2 answer addresses a hypothetical.
- Opus's Summary says "Adopt the part of 4 that gbrain actually means" but the change it proposes (hand-edit commits) is filed under Missed, not under Q4's Smallest change; Q4's sentence depends on it.
- GPT-6's Misread list goes beyond the two pages the prompt named into "both pages" generically and into gbrain §6 event mechanics that the wiki pages may not actually assert; worth checking that each item maps to a sentence in `Belief Ledger.md` or `Three-Layer Architecture.md`.
