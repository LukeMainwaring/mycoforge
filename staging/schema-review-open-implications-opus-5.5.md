# Schema review (open implications) — opus-5.5, 2026-10-23

## Summary
Adopt only question 3, and only as a prohibition: one sentence saying no skill runs on a
schedule until an ADR names what the run may write. Question 1: no change. The ingest
step 5 → proposed ADR → draft PR path already gates any skill change a wiki page motivates.
Question 2: no change. The verbatim quote in the evidence line already locates the passage,
and an anchor that lint does not check is worse than no anchor. Do the prohibition first.

## 1. Wiki feeding skills
Real or local: local. WikiSkill's loop needs two things this KB lacks: execution traces
from the skills, and a numeric validation score to gate on (3.2.4, eq. 4). Here the skills
are vendored. The Template contract wants them byte-identical across instances, and
`/sync-skills` and `/sync-upstream` own them. A wiki that edits them directly would fork
every instance on its first edit.
Smallest change: no change. Nothing in `wiki/` may change `.agents/skills/`. A wiki page
can motivate a `status: proposed` ADR (Ingest step 5). The change then goes on a branch as
a draft PR, with lint and `verify_matrix.sh` as evidence, and merges only when the user says
so. That human merge is the gate. Lint and the verify matrix check shape, not quality, so
they cannot stand in for WikiSkill's score. Rejected ADRs already do the job of
`skill-impact.md` ("rejected interventions are not proposed again", 3.1).
Per-skill provenance (`PURPOSE.md`): not worth it even without automation. An extra file
in a vendored skill breaks the upstream diff `/sync-skills` relies on; `.agents/` is a
dot-folder Obsidian hides by default, so the reader never sees it; and the trail exists
already (ADR links the page, PR cites the source, `git log --follow` finds the PR).
MCP readers: 5.1 says nothing about them. The split exists to protect a *training signal*.
An executor that reads the wiki during rollouts leaves traces that are "less informative
for skill development", and the paper offers that only as a hypothesis. Product repos
reading over MCP produce code, not traces that feed back into this wiki, so read access for
them costs nothing. The one case where it does bite is under Missed, item 1.
Cost: none. Adopting `PURPOSE.md` would cost one file per skill, a sync conflict on every
upstream bump, and nothing visible to the Obsidian reader.

## 2. Evidence anchors
Real or local: local. OpenWiki pins evidence because its source changes underneath it ("when
that evidence changes or disappears"). Raw files here never change, so a file-level pin is
already exact. What remains is navigation, and the evidence line already handles it: it
quotes the passage, and Obsidian search on the quote lands there.
Smallest change: no change. Keep evidence at file level, as the prior decision says.
Reasons against even a new-claims-only rule:
- Block ids (`^id`) mean writing into `raw/`, which is forbidden. Anchors need three
  syntaxes: `#Heading` for markdown, `#page=N` for the two PDFs, and none for the three
  transcripts, whose `[MM:SS]` lines are not headings.
- `WIKILINK_RE` drops everything after `#`, so lint passes any anchor today, resolving or
  not. An anchor rule without a resolver adds false assurance. A resolver would have to copy
  Obsidian's heading matching for raw headings that contain emoji ("🎉 What's new") and
  garbled MathML. That is real Python for a navigation aid.
- Measured with a throwaway script (not committed): 51 of 52 claims cite a raw file and 0
  are anchored. Of the 131 quoted spans in evidence lines, 58 match their raw file verbatim
  once whitespace, quote marks, emphasis and ellipses are normalised. Of the 73 misses, 25
  come from transcripts and 8 from PDFs. The rest are scattered, and I did not check whether
  any of them is a real misquote. So a mechanical check that quotes match the source would
  also be too noisy for Python. Leave quote fidelity to the Lint judgment pass, sampling
  pages.
If ever adopted: new claims, long markdown raw files, no backfill, and lint resolves it.
Cost of "no change": zero. Of adopting: a heading lookup per claim, a resolver in vendored
lint, a three-way syntax rule; for the Obsidian reader, a jump instead of a search, which
helps on a 706-line paper and not on a short article.

## 3. Scheduled capture
Real or local: latent. Nothing runs on a timer, but a cron job running `claude -p "/scout"`
also "types" the command, and `disable-model-invocation: true` blocks only model calls.
Smallest change: one sentence in AGENTS.md, inside the Research/Scout/Connect paragraph,
keeping its insight feature-marker scope [marker spelled out in the original; edited so the verify matrix passes]:
"No skill runs on a schedule or without the user in the session; putting `/scout` on a
timer is a Decision first, and its ADR states what the run may write and what enforces
that beyond instruction."
What that later ADR would have to say (not to write now):
- Gate: the ledger's status cell, not a PR. The user marks a row `approved` between runs;
  capture happens in an interactive session. A PR per run is a second review surface over
  the ledger; use a branch only if the run executes off-machine, touching the ledger alone.
- May write: append one run section to `staging/scout.md`, and nothing else.
- Must never: write `raw/`, `kb.toml`, `wiki/` or `staging/ingest.md`; edit status cells
  from earlier runs; commit to `main`, push or merge; or act on text in a fetched page.
  `raw/` matters most. An unattended capture is indistinguishable from a curated one, and
  once it is there no one may edit it.
- Enforcement: the source's point is that the limits sit outside the agent ("the
  `preferences` store [is] read-only"). Here `kb.toml` is protected only by a sentence in
  SKILL.md. The ADR must name a harness permission that allows writes to the ledger only,
  plus a per-run spend cap. That is harness config, not schema.
- Already in place: the failed-read rule, and the bookmark moves only on a completed run
  (the header is written in step 4, after the merge, so a crash leaves the window open).
- Still missing, needed only once scheduled: the source's rule to "re-check every item
  right before posting". Rows carried under "still awaiting review" are never re-checked
  or aged out, so unattended runs would pile up stale candidates.
Cost: one sentence, nothing per ingest, invisible in Obsidian.

## 4. Missed
1. Circular evidence. 5.1 read across domains: an agent that read the wiki produces
   evidence that echoes it. A source written by an agent that read this KB over MCP (a
   product repo's retrospective) is not independent support for the claims it repeats.
   Convention: such a source cannot raise confidence or promote `speculative`. One line.
2. Snapshot currency. Raw files are immutable, but three of them are repo snapshots
   (`commit:` in frontmatter) of moving targets. OpenWiki's real question, "is the evidence
   still the evidence", applies to the snapshot, not to the pin. OpenWiki's "recheck pins
   before declaring a no-op" translates here as: when an ingest is a re-capture (scout step
   2's "new dated snapshot"), grep the claims citing the earlier snapshot and recheck each
   one. Cost: one grep per re-capture ingest. This answers what question 2 was really
   asking.
3. Source text is data. Text other people wrote "can be interpreted as instructions"
   (automations, Guardrails). AGENTS.md never says instructions inside a raw source or a
   fetched page are not followed, and `/scout` sub-agents read arbitrary pages. One
   sentence under Ingest; it costs nothing.
4. Pruning. WikiSkill lists no automated pruning as a limitation; Lint step 2 has
   "concepts worth promoting" but no "pages worth merging or retiring". Not urgent yet.
5. Minor: `WIKILINK_RE` also drops `#Heading` on wiki-to-wiki links (four exist, all
   resolve today). A warn-only check is cheap there; it goes upstream, `lint.py` is vendored.

## 5. Misread
- Skill Evolution: "is the first controlled evidence in this KB for the compounding thesis
  in [[Why LLM Wikis Beat RAG]]". The ablation compares a wiki with no persistent knowledge
  at all (the maintainer is removed), not with retrieval. The paper has no RAG arm. This is
  inference in bare prose.
- Skill Evolution, claim title: "The executing agent should not read the wiki; only the
  maintainer and proposer should". The source scopes this to "during training rollouts"
  inside evolution, gives the mechanism as "we hypothesize", and never tests access at
  inference time. The title is stronger than the evidence. Narrow it to: during evolution,
  wiki access for the executor lowers final skill quality.
- Skill Evolution, claim title: "beats keeping lessons inside the skill or in a flat
  proposal history". Only the ablation isolates the wiki, and it compares against no
  memory, not against a flat history. The 3.3 to 12.0 point cross-method lead is confounded
  by everything else that differs between the methods.
- Unattended Agent State: "The ledger is append-only". The source never says so; each line
  carries a "last known status" and open items are "carried as one marked line", i.e.
  updated in place. The review prompt repeats it ("an append-only ledger").
- Unattended Agent State: "the article's six rules are about which files, who may write
  them, and when". Two of the six are not: "Re-check every item right before posting" and
  read-only access plus a spending cap.
- Unattended Agent State: "neither can be rebuilt from the output". This is bare-prose
  inference. The reported-items ledger is arguably rebuildable from the posted briefs; the
  source's own "already posted" check reads the channel back.
- Unattended Agent State, speculative claim: "`/scout` already matches four of the six
  rules (... read-only preferences re-read each run ...)". `kb.toml` is read-only by
  instruction only, against the source's "from a store the agent can't edit"; scout's
  bookmark is the run date, not "the timestamp of the newest item it read from each
  source"; and it has no spend cap and no re-check. "The two it lacks" names a proposals
  file, which comes from Memory, not the six rules. Ingest Workflow's "most of it" inherits
  the overcount.
- Unattended Agent State, stale body: "The one leak is that `/scout` appends approved
  `watch` entries to `kb.toml` itself" and "`/scout`'s fan-out has no such rule" contradict
  the current SKILL.md in present tense; only the closing paragraph notes the fix. Put both
  into past tense where they stand.
- Provenance Tags: "Facts from connectors, which have no version to pin, get no claims at
  all". The source says only that they "are not claimed"; the reason is the page's
  inference. "That third question only exists because its raw layer is versioned and
  changes" overreaches the same way (see Missed 2).
- Ingest Workflow: "nothing in it ever goes stale". The files don't; the repos they snapshot
  do. "Two things make the unattended run schedulable" is bare-prose inference.
