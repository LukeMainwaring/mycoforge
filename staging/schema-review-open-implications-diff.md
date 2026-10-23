# Schema review diff (open implications) — 2026-10-23

Two reviews of `staging/schema-review-open-implications-prompt.md`: Opus 5.5
(`-opus-5.5.md`) and GPT-6 (`-gpt-6.md`). Quotes verbatim. Facts the reviews
asserted about the repo were checked here and are marked.

## Agree

**1. Wiki feeding skills: no change, the ADR → branch → PR path is the gate.**
- Opus: "no change. Nothing in `wiki/` may change `.agents/skills/`. A wiki page can motivate a `status: proposed` ADR (Ingest step 5)... That human merge is the gate."
- GPT-6: "No schema or skill change. Let wiki findings motivate a separately reviewed skill patch through the existing workflow and vendoring owner."
- Both reject `PURPOSE.md`: Opus "breaks the upstream diff `/sync-skills` relies on; `.agents/` is a dot-folder Obsidian hides"; GPT-6 "Instance-specific wiki links inside portable skills would add local dependencies and upstream divergence."
- Both reject an MCP-reader restriction from section 5.1: Opus "The split exists to protect a *training signal*"; GPT-6 "It does not test whether ordinary knowledge consumers answer better with the wiki."

**2. Evidence anchors: no mandatory anchor, no backfill, no lint today.**
- Opus: "no change. Keep evidence at file level... An anchor rule without a resolver adds false assurance."
- GPT-6: "Do not add anchor lint now... No blanket backfill."
- Both note `WIKILINK_RE` drops the fragment, so any anchor passes lint. Checked: `scripts/lint.py:43`, the `(?:#[^\[\]|]*)?` group is non-capturing.
- Both reframe the real question as snapshot currency: Opus "Raw files are immutable, but three of them are repo snapshots... of moving targets"; GPT-6 "immutable captures can become outdated accounts of the world. Distinguish evidence-byte currency from claim currency."

**3. Scheduled capture: not authorized now; if ever, the ledger row is the gate, not a PR; the run may append one run section and nothing else.**
- Opus: "Gate: the ledger's status cell, not a PR... May write: append one run section to `staging/scout.md`, and nothing else."
- GPT-6: "The scheduled run may append a completed candidate/failure run section only to staging/scout.md... No PR is needed for each candidate: the ledger is already the review surface."
- Both: enforcement must sit outside the agent. Opus "The ADR must name a harness permission that allows writes to the ledger only, plus a per-run spend cap. That is harness config, not schema." GPT-6 "Prose alone cannot supply those controls."
- Both: scout's bookmark is the run date, not the newest item read per source, and carried-forward rows are never re-checked.

**Misreads both found** (fixed in this PR): Skill Evolution's executor claim title "universalizes a training ablation"; Provenance Tags' "no version to pin" is "the page's inference"; Unattended Agent State's present-tense "one leak" and "no such rule" were stale against the current skill; "four of the six rules" overcounts; Ingest Workflow's "nothing in it ever goes stale" and "Two things make the unattended run schedulable" are bare inference.

## Disagree

- **Add a sentence now?** Opus: yes, "one sentence in AGENTS.md... No skill runs on a schedule or without the user in the session; putting `/scout` on a timer is a Decision first." GPT-6: "No change is required" since slash workflows are already user-invoked, though it offers the same sentence as optional. Opus's reason for adding it is checked and holds: `disable-model-invocation: true` stops the model calling the skill; a cron job running `claude -p "/scout"` is the user typing it. Resolution: ADR-012 proposes the sentence.
- **Optional heading anchors.** GPT-6 would allow "optionally link to an existing source heading when it materially narrows the evidence." Opus: no, three syntaxes (markdown heading, PDF page, transcript timestamp) and no resolver. Resolution: ADR-013 proposes file level stays the rule and names the quote as the locator; the optional heading is listed as the rejected alternative, reopenable if lint grows a resolver upstream.
- **Append-only.** Opus: the source "never says so; each line carries a 'last known status'". GPT-6 did not object to the word but noted scout's status cells change in place. Checked: the source does not say append-only. Fixed on the page.

## Missed items, each one line, not decided

- Circular evidence (Opus): a source written by an agent that read this KB over MCP cannot raise confidence or promote `speculative`. One line under Claims if ever raised.
- Source text is data (Opus; GPT-6 "Memory does not enforce authority"): AGENTS.md never says instructions inside a raw file or fetched page are not followed. Folded into ADR-012.
- Re-capture recheck (Opus; GPT-6 "completion must mean durable output" is adjacent): on a new dated snapshot of a repo, grep the claims citing the earlier snapshot and recheck each. Folded into ADR-013.
- Lint gaps (GPT-6, checked): `check_claims` accepts any resolving wikilink as evidence, not necessarily a raw file; `check_raw_refs` checks existence, not that the path is under `raw/`; wiki-to-wiki `#Heading` anchors are never resolved (Opus). All upstream, `lint.py` is vendored.
- MCP read scope (GPT-6, checked at `mcp/server.py:108`): `read_page` serves any file under the repo root, not only `wiki/` and `raw/`. Separate from any reader policy; a product-layer question.
- Pruning (Opus): Lint step 2 has "concepts worth promoting" but no "pages worth merging or retiring".
