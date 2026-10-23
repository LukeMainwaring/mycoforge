# Schema review (gbrain belief ledger) — opus-5.5, 2026-10-23

## Summary
Adopt 3 in a small form: one sentence and a warn-only lint check on raw dates,
which already finds a real error. Adopt the part of 4 that gbrain actually
means: trust tiers are about *who wrote*, not what genre the source is. Here
that means hand edits are kept apart from agent edits. Don't adopt 1 (use a
log-line convention) or 2 (no change; no page here predates the claim
convention). Do first: the raw date check, since it is cheap and already finds a bug.

## 1. Claim identity
Real or local: mostly local. gbrain needs logical keys because rows churn
(new ids on edit, renumbering, engine copies, cascades) and many writers touch
one subject. Here a claim changes only in an agent commit, one per workflow
run, and `log.md` names the pages. A reworded title shows up as a `-`/`+` pair
in one commit's diff, and `git log --follow` survives a page rename. History
is only truly lost when a claim **moves between pages** (a split or merge), and
nothing reads claim history by identity today: lint does not parse callouts,
and no page links to a claim.
Smallest change: no id. Add one sentence to Claims: "When you reword, move or
split a claim, name the old and new title in the log entry." No lint. If a page
ever needs to link to a claim on another page, give that one claim an
Obsidian block id (`^short-slug`) and link it as `[[Page#^short-slug]]`. That
should be done when a link needs it, not added to every claim.
Cost: the convention costs one clause in a log line, a few times a month. Ids on
every claim would cost a lot more: minting and keeping them unique on every
ingest, a lint uniqueness check, and a one-time rewrite of ~45 callouts on ~22
pages. That rewrite is the "format change rewrites everything, zero beliefs
change" churn the source warns about (§2, §9).

## 2. Coverage marker
Real or local: local to this instance. The Claims section was in `AGENTS.md`
from the scaffold commit (`2833df0`, 2026-07-10). That is the same day as the
first content, so no page here was written before the convention. Git
has recorded every write since then, so the repo's first commit already works as
the watermark. The thing the question gestures at, beliefs stated in prose
and never put in a callout, is by design: only contestable assertions become
claims. A marker would not change that.
The gap is real only for an instance that **imports an existing vault**. Its
pages carry beliefs from before the import that git never saw.
Smallest change: none here. For the template, onboarding could write one log
line on import (`discovered | imported N pages; beliefs before <date>
unrecorded`). That puts the marker in the log, never on pages. No lint.
Cost: zero per ingest. A marker on each page would be permanent clutter in
Obsidian and would say nothing that `created:` and git don't already say.

## 3. Two clocks
Real or local: real, already mostly followed, but nothing checks it, and it has
already drifted:
- `raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md` says
  `published: 2001-08-21` (a web-clipper error; the filename says 2026).
- The gbrain source is named `2026-10-16`, which is its `updated:` date. Its
  `published:` is 2026-10-15. The naming rule says publication date.
- Raw files use two frontmatter styles for the capture date: `retrieved:`
  (capture skills) and `created:` (Obsidian clipper and transcripts). Some have
  neither, and the PDFs have no frontmatter at all.

The wiki side is fine. `created`/`updated` and commit time are recorded time,
and no page copies a source date into them.
Smallest change: not a paragraph, one sentence under File naming: "Raw
frontmatter keeps source time (`published:`) apart from capture time
(`retrieved:`); the filename date is `published`, else `retrieved`; never copy
either into a wiki page's `created`/`updated`." Lint: a **warning** (raw is
immutable to the agent, so the user makes the fix) when a raw `.md` file's
filename date matches none of `published`, `retrieved` or `created`. That is about 15
lines in `check_raw_dates`, using the existing `parse_frontmatter`. It flags the
SDLC file today. Accept `created` as a stand-in for `retrieved` instead of
migrating old files.
Cost: none per ingest, because the capture skills already write both fields. One
warning to clear now. A caveat goes in Missed: commit time equals recorded time
only for agent writes.

## 4. Trust on sources
Real or local: the question as asked is mostly a misreading. gbrain's tiers
(`user_confirmed`, `operator_curated`, `agent_written`; §6.1, §6.3) record
**who made the write**. A model derivation is capped at `agent_written`, and
only the owner can raise it. They do not grade how reliable the external
evidence is. A source-genre tier (paper / practitioner / vendor /
secondhand) is a different idea, and I would not add it:
- Genre is already visible from the `raw/` folder, `type:` and `author:`.
- Reliability depends on the claim, not the source. The same Anthropic article
  is first-hand about Claude Code and second-hand when it quotes Omni. The
  evidence lines already make this call in prose ("Synthetic data, the
  authors' own probe, one brain"), and that is the right level of detail.
- Deriving `confidence` from it would be false precision. Confidence here comes
  from corroboration and fit. "Compounding beats re-derivation" is `high` from
  a gist, a talk and a paper, and none of them is a top-tier source alone.

What does carry over is gbrain's writer tier. Hand edits are the
owner tier. `AGENTS.md` says to "respect them and fold them in" but says
nothing about a new source contradicting a claim the user wrote or edited.
gbrain's rule is that a lower tier contests and the owner decides; it never
overwrites (§6.2).
Smallest change: one sentence in Claims: "A claim the user wrote or edited
by hand is never superseded by you: set `status: contested`, cite both, and
ask." This only works if hand edits can be identified, which is the
`hand-edit:` commit in Missed. No lint. `/connect`'s `status: speculative`
already follows the cap rule (agent-derived claims never become `supported`
without a source), so nothing changes there.
Cost: about zero per ingest, since it only applies when a hand-edited claim
is challenged. No new fields, no page noise.

## 5. Missed
- **Hand edits are this KB's unmanaged writer (§5.1, §7).** gbrain certifies
  coverage only where every write goes through a coordinated path, because
  unrecorded writers break interval completeness. Here, edits made in
  Obsidian between sessions are picked up by the next agent commit. They get
  that run's time and its `ingest:`/`lint:` prefix, so both the recorded
  clock and the authorship are wrong. Smallest fix, one sentence in Version
  control: "At session start, if `git status` shows uncommitted changes under
  `wiki/`, ask the user, then commit them on their own as `hand-edit: <pages>`
  before the workflow run." Cost: one `git status` per session and an
  occasional extra commit. This is the most useful idea from the
  source for this KB, and it is what makes the rule in 4 enforceable.
- **Storage clock policing the belief clock.** Lint's stale check compares
  file mtime (storage time) with `updated:` (belief time). A cosmetic or
  format-wide rewrite moves mtime without changing any belief, which is the
  §4 "projection refresh emits no event" case. It is warn-only, so no change, but
  any format migration (like the one 1 would need) will set it off everywhere.
- **"What changed this week" is answerable already** (gbrain's W4, §15):
  `git log -p --since=7.days -- wiki` filtered to `> [!claim]` lines, each
  status change timed by its commit. A query recipe, not schema.
- **Withdrawal is not erasure (§6.5).** A source the user deletes from `raw/`
  stays in git history. Worth a README line if the repo goes public; nothing more.

## 6. Misread
- *Three-Layer Architecture* says "the time half mostly does not [hold]"
  because "commit time *is* recorded time". That is true for agent writes only
  (see Missed). The page should say so instead of calling the time half closed.
- The same section lists "a fence format change produces held files" among
  three failures of markdown plus git. That one is specific to gbrain's fence
  parser holding files it can't parse, not a property of markdown. The nearest
  equivalent here is a callout format migration, a reason against 1, not
  evidence of a gap.
- It also says "nothing marks the beliefs a page held before callouts
  existed." No page here predates callouts (see 2), so the gap is hypothetical
  for this instance.
- *Belief Ledger* calls the ledger "the one thing in the system that is not
  recomputable from the markdown." §1 puts it in a DB-only category "next to
  the withdrawal ledger and the mutation journal", so it is one of several.
- *Belief Ledger* §4 says gbrain's contested write is "the same move as this
  KB's claim `status: contested`". The shape matches (keep both, the human
  decides) but the trigger is different. gbrain contests between writer tiers
  on one subject, and this KB contests between sources. Question 4 above
  carries the same mix-up.
- The "diff beliefs, not storage" claim is `confidence: high` and calls the
  measurement "direct", but §9 says it is "a free local bench (scratch test,
  not committed)". Better: lean on the §2 code-reading argument, or drop to `medium`.
