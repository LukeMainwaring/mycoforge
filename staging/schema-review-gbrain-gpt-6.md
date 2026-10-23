# Schema review (gbrain belief ledger) — GPT-6, 2026-10-23

## Summary
Adopt the two-clock clarification; defer stable claim IDs and reject per-page coverage markers and source-tier scoring for now.
First define historical answers as committed wiki snapshots, with an explicit distinction between historical prose and explicitly recorded claim status.
Git already preserves this KB's published states; it does not provide semantic claim correspondence or record intermediate agent beliefs.
The source identifies useful limits, but its synchronized database's observation-time problem is not automatically this repository's problem.

## 1. Claim identity
Real or local: Real for reliable automated tracking across moves, splits and rewrites; not a loss of the historical text itself. A rename or title edit does not erase earlier Git snapshots. Rename detection is heuristic, and semantic correspondence can require human judgment, but “history is severed” overstates the gap. gbrain also does not preserve one claim key through arbitrary rewording: a changed fingerprint becomes a new assertion, linked to its predecessor (§§3–4).

Smallest change: No mandatory ID or lint change now. Add a Claims convention: retain the old proposition when superseding it, identify the successor by page and claim title, and distinguish wording-only edits from changed propositions. Existing pages need changes only when a substantive replacement occurs; do not retrofit IDs across the corpus. This closes ambiguous replacement reporting for a human reviewer, not machine identity.

If automated claim histories become a concrete requirement, use one opaque `id: claim-<uuid>` line inside each callout, unchanged across moves and wording-only edits; a different proposition receives a new ID and `supersedes: claim-<uuid>`. Lint would require one well-formed ID per claim, enforce repository-wide uniqueness, and resolve predecessor references against retained callouts. Existing callouts would need one baseline ID each, without asserting that the ID existed historically. Snapshot lint cannot prove an ID was preserved correctly; semantic review remains necessary.

Cost: The convention adds a short predecessor/successor reference only on substantive replacements. Universal IDs add a visible metadata line to every claim, migration work, copy-versus-move decisions, and split/merge bookkeeping on future ingests. That is a poor trade before there is a consumer for machine identity.

## 2. Coverage marker
Real or local: The epistemic distinction is real: old prose can be recovered without an explicitly recorded confidence/status. gbrain's certified interval completeness is a different requirement (§7): it instruments every publication, including transitions that later cancel out. This KB intentionally publishes only the end of each workflow; lack of a callout does not mean the old page or its assertions were unrecorded.

Smallest change: No page field and no lint check. State in Query that historical answers cite a commit and distinguish “the page stated X” from “a callout explicitly marked X supported”; absent historical metadata is unknown, never reconstructed as if recorded then. Record an actual convention rollout or completed audit once in the schema log, with its scope and commit reference. Do not invent a date D from current page dates or treat adoption as proof that all pages complied. Existing pages need no retrospective marker.

A future complete claim audit could warrant a documented baseline, but a `claims_since` date alone would not certify every intervening edit or every contestable sentence. No present check can establish that completeness by inspecting callout syntax.

Cost: No extra ingest fields or Obsidian noise; a historical query pays for inspecting the relevant revision. Page markers would require migration, ongoing audit discipline and exceptions for missed claims, while implying more assurance than they establish.

## 3. Two clocks
Real or local: Real and cheap to clarify. Source publication, capture, KB incorporation and the date an assertion applies to are not interchangeable. Even the raw filename is ambiguous by design: it can contain publication or capture date. The captured gbrain document itself has different `published`, `updated` and `retrieved` dates.

Smallest change: Add one paragraph to AGENTS.md: source dates describe the evidence; `created` and `updated` describe page maintenance at day precision; the content workflow's commit identifies the published KB snapshot. Never backdate page maintenance fields to source publication. For “known at T,” inspect the relevant main-history snapshot and cite its hash; for “true at T,” use the evidence's explicit applicability dates and disclose uncertainty. A commit timestamp is a practical publication-time convention, not proof of the agent's first observation or a trusted wall clock. Imported/rebased history and branch author dates require qualification.

No new fields or linter changes. Existing pages change only if their maintenance dates were actually copied from source dates; no such defect is established by this review. Do not add per-claim `recorded_at` timestamps that merely duplicate the workflow commit.

Cost: Negligible per ingest: keep existing dates honest. No page noise. Historical queries incur revision lookup; that is where this cost belongs.

## 4. Trust on sources
Real or local: Provenance quality matters, but gbrain's tiers are primarily write authority and derivation attribution, not a ranking of paper versus practitioner versus vendor (§6). Those categories overlap: a vendor can publish a primary experiment, and a practitioner can quote it secondhand. A curated source also does not make every inference from it owner-confirmed.

Smallest change: No raw tier, no derived confidence formula, no lint change. Keep claim-level confidence as a reasoned judgment about directness, methods, independence, scope and contrary evidence. Add a sentence to Claims distinguishing source provenance, confidence and conflict status. When contested, retain both propositions and their evidence and state what would resolve the conflict; `contested` alone neither enforces a write gate nor establishes an owner decision.

Existing examples already show the useful practice: “Why LLM Wikis Beat RAG” qualifies benchmark transfer, while “Advisory and Deterministic Controls” identifies two sources as coming from the same organization. Preserve or extend those evidence qualifications when necessary. Immutable raw files should not become mutable confidence records.

Cost: Some judgment on every new or conflicting claim, already part of ingest; usually one short qualification in evidence. A universal tier would add classification and dependency maintenance while concealing the judgment inside an unjustified confidence calculation.

## 5. Missed
- **The current claim contract is not linted.** `scripts/lint.py` checks links, raw references, index presence, orphans, configured terms and optional date staleness; it does not parse callouts or validate confidence/status/evidence. Before introducing new metadata, add a bounded claim-shape check: outside code fences, each claim needs exactly one recognized confidence and status plus nonempty evidence containing a resolving provenance link. Align the status vocabulary first: Claims lists supported/contested/superseded, while Connect explicitly permits speculative. Keep instance-specific vocabularies in `kb.toml`. Existing callouts need repairs only where fields are missing or invalid. This detects malformed records, not evidential truth or unmarked contestable prose.
- **Changes include more than status.** Revised proposition, evidence, scope and confidence can matter even when status remains supported (§§4, 15). A short ingest-log description should name material revisions; spelling and layout changes need no belief event. A net change report must say it nets changes, since an edit and revert can disappear from it while remaining in history.
- **Propagate evidence corrections deliberately.** The transferable part of §6.3 is to inspect claims and syntheses that depend on discredited evidence. Add that check to Ingest/Lint, using existing provenance and links, without automatic confidence downgrades. Copied reports are not independent corroboration. No additional fields are needed, but discovering indirect dependencies remains judgment work.
- **Historical answers need limits.** §§7, 14–15 distinguish unknown prior values from absence. Cite the recovered revision and disclose missing history, uncommitted work or ambiguous identity; never interpolate confidence into an old snapshot. Preserve content workflow history if it is to serve this role. A linter over today's files cannot certify its completeness.

## 6. Misread
- **“History is severed” is too strong in both pages.** Git retains the old paths and text. What is absent is an explicit stable semantic join, not recoverable history. Three-Layer Architecture acknowledges the local commit-time distinction but retains an overly general claim title and the identity overstatement.
- **The source does not establish a universal markdown-plus-git impossibility.** Its §1 concerns what gbrain observed from synced sources, including database-only state and held imports. Its row-churn measurements do not demonstrate that a directly committed wiki cannot reconstruct a historical published state. A textual diff is useful evidence from which semantic changes can be interpreted.
- **“The one thing ... not recomputable” is false.** Belief Ledger's opening says this about the ledger, but §1 explicitly puts it alongside the withdrawal ledger and mutation journal as database-only system-of-record state. The same paragraph's “cannot drift” needs the managed-write qualification; §7 describes unmanaged writes, drift detection and uncertified intervals.
- **The markdown analogue is narrower than the source.** Belief Ledger says the thing worth recording is which callouts changed status. The source also records assertion content, confidence, evidence-related fields and other canonical values (§4); status-only tracking would miss substantive changes.
- **Coverage cuts are per page.** Belief Ledger says reads before the source watermark refuse. Section 7.1 gives each page its own baseline cut, with source completion forming the aggregate watermark. Also, backfill does not literally “carry only source time”: it has a recorded timestamp for the backfill run (§5.4), which cannot establish historical observation time (§14.1).
- **Trust behavior is overgeneralized.** Not every event reads a post-trigger row tier: held events use writer attribution, deleted subjects use preimages, and baselines/backfills can be unknown (§6.1). Not every lower-tier operation inserts a new active challenger: §6.2 includes refused remote forget requests, held new rows, retained takes pending approval and page lowering. Derivation also applies caps, not merely the minimum evidence tier (§6.3). The analogy to `contested` is useful but is not equivalent enforcement.
- **“Fourth store” needs a gbrain-specific qualifier.** Its database audit store is not evidence of a necessary fourth layer in this KB. Three-Layer Architecture's closing distinction is sound; its opening should avoid implying the source redesigned this repository's three-layer model.
