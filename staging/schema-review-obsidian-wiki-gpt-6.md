# Schema review (obsidian-wiki drift lint) — gpt-6, 2026-10-23

## Summary
Do not adopt a numeric drift lint now; the sample shows a real claim-coverage problem, not evidence for a useful threshold.
Choose (a): apply the existing callout convention to consequential unsupported inferences, with a small instruction clarification and no Python change.
First review the three sampled pages against their sources, removing overstatements and promoting substantive inferences into auditable callouts.

## Measurement
Estimates are by prose volume outside callouts, excluding frontmatter, headings and navigation-only text; lists count. They are rough readings of attribution and argumentative moves, not a source-by-source audit: the other cited raw sources were not read. Local schema descriptions are not automatically inference. These selected pages do not establish a vault-wide rate or growth over successive ingests.

- **Why LLM Wikis Beat RAG:** roughly **35–50%** inferred framing or evaluation. The opening largely restates the compilation rationale, but “why that trade wins” and the concluding “strictly worse than RAG” go beyond it. The denominator is small because most of this page lives inside callouts.
- **Progressive Disclosure:** roughly **40–55%** inferred application and synthesis. The connections to token efficiency and organizational legibility, “This KB is one,” the proposed graph-walking rule, and the payoff interpretation supply much of it; quotations and the reported experiment are mostly restatement. The KB section mixes checkable local description with inference, so it is not all counted as inference.
- **Three-Layer Architecture:** roughly **25–40%** inferred interpretation. The safety argument, mapping WikiSkill onto the layers, generalizing the ownership boundary without humans, and classifying memory/ledger machinery as properties of a layer are examples. The layer inventory and reported implementation details are mostly descriptive; the decision recap was read here but its linked decision pages were not opened.

## Real or local
Real, but narrower than Provenance Tags suggests. “Strictly worse than RAG” is a contestable comparison outside a callout, despite the schema already requiring contestable assertions to be inside one. Reading each ingest with a human reduces exposure; it does not ensure every inference is recognized or source-supported.

Inference is not synonymous with speculation. A sound deduction, a proposed architectural analogy and an unsupported performance claim should not receive identical epistemic treatment. Origin and evidential standing are separate dimensions. A high inference share can be appropriate for a synthesis; a single unsupported sentence can be consequential on an otherwise extracted page.

Batch ingestion and conversation capture plausibly increase the value of origin marks, but the README does not establish that nobody reads each page or demonstrate that its lint prevents drift. It supplies neither its algorithm nor a threshold. Our sample demonstrates unmarked inference, not an increasing drift rate or the effectiveness of the proposed remedy.

## Smallest change
**AGENTS.md, Claims:** clarify: “Apply this rule to contestable assertions in ordinary prose as well as summaries. Agent-derived claims must identify their inference and its premises in the evidence line; use `status: speculative` when those premises do not establish the conclusion. This applies during ingest and query filing as well as `/connect`.”

**AGENTS.md, Lint step 2:** add a judgment check for consequential assertions outside callouts and conclusions stronger than their cited evidence, including inside existing callouts. This is a clarification of the current contract, not a promise of automated semantic detection.

**scripts/lint.py:** no change. Existing `confidence`, `status` and `evidence` fields suffice; `check_claims` already checks their shape and an evidence wikilink's resolution. It cannot determine whether a sentence is an inference or whether evidence entails a conclusion. No new frontmatter field or `kb.toml` threshold is warranted. The closure is procedural; automated detection of omitted claims remains unsolved.

**Existing pages:** remove or qualify “strictly worse than RAG,” or preserve the comparison as a speculative callout with premises and limits. Review the causal assertion that compiling makes routing metadata trustworthy, and qualify the general safety claims in Three-Layer Architecture. Keep simple local descriptions and navigation prose compact. Any actual claim-title changes must follow the existing logging rule; none are made by this review.

Reject **(b)** for now: counting `^[inferred]` measures declared annotations, not missed inferences. An absolute threshold penalizes longer pages; a ratio needs a defined denominator and still confuses synthesis with unsupported speculation. Untagged claims remain invisible, and consistently marking sentence boundaries adds work. A future experiment could test its usefulness before setting policy.

Reject **(c)**: a hand-maintained `inferred:` count duplicates editorial bookkeeping without locating the sentences or letting lint verify the count. It can go stale while giving a reassuringly precise number.

## Cost
The chosen form adds a source-entailment check during every ingest, proportional to the changed assertions rather than all sentences on every touched page. Marginal effort should be smaller than full origin tagging because full-source reading and claim maintenance already belong to ingest, but this review does not measure minutes saved. Reviewing existing pages is a separate, bounded cleanup cost.

Callouts add visible lines in Obsidian, so first delete redundant or weak assertions; group closely related reasoning where it remains auditable. Do not turn every connective sentence into a callout. This serves the five-line-stub rule better than retaining filler and decorating it with provenance marks.

Sentence tags require classification and maintenance on every edit and add footnote markers to reading view. Counts avoid body noise but impose reconciliation work and hide the affected text. Neither cost is justified by the current evidence. The chosen approach retains a human/agent judgment dependency, which must be acknowledged rather than disguised as deterministic lint coverage.

## Missed
- **`undated_claims`:** mentioned only in the captured “Repo notes,” not explained by the README. Its scope, date semantics and implementation are unknown. Source publication, capture, page maintenance and a claim's temporal validity differ; the current raw-date check and `updated:` field do not establish claim validity. Consider dates for time-sensitive assertions, but inspect the upstream rule before proposing a mandatory field.
- **Locked writer:** the README explicitly describes locking and atomic writes for shared index/log/memory files. This is relevant if concurrent sessions write this KB: one source per session does not serialize separate sessions. A shared write path could prevent lost updates, but all writers must use it, and per-file atomicity alone does not establish a transaction across page, index and log. Defer until concurrent writing is supported or observed.
- **Ingest manifest:** delta processing could prevent redundant work. Here immutable curated sources and deliberate single-source ingest reduce its immediate benefit. A future manifest should distinguish capture from completed ingestion and identify source content/version plus the resulting workflow commit; the README does not specify those fields. Avoid maintaining another competing completion ledger without a demonstrated need.
- **Session hooks:** the end hook suggests capture; it does not automatically save everything. A read-only start recap could help continuity, but automatic wiki writes would change this KB's deliberate ingest and user-requested query-filing boundaries. The plugin installation also explicitly omits the hooks. Treat these as optional workflow proposals, not prerequisites for provenance.
- **Graph semantics:** the reported index-routing error supports distinguishing catalog links from semantic links in graph operations. The current orphan check already excludes index/log contributions. The small experiment does not prove broader retrieval superiority or constant query cost at 2,000 pages.

## Misread
- **“From the tag mix”** invents an implementation detail: the README says tags exist and lint flags speculation, without explaining the relationship algorithmically. The `undated_claims` mention should be attributed specifically to Repo notes.
- **“One question per sentence,” “every claim-shaped sentence,” and “tagging every sentence”** strengthen “every claim.” Claim granularity and mandatory sentence coverage are not specified. The precise meaning of `ambiguous`, especially “the source itself unclear,” is also an interpretation rather than a documented definition in this capture.
- **“Only `/connect` files” speculative status** overstates the schema's wording. `/connect` requires it, but neither Claims nor `check_claims` forbids other workflows from using it. The status is not equivalent to inferred origin.
- **The supported callout's “cannot”** confuses today's shape-only implementation with an inherent limitation of marking contestable claims. Inferred factual assertions can themselves be contestable and already fall under this KB's rule. Tagging also cannot catch omitted tags automatically. The source does not establish the comparative impossibility asserted in that title.
- **“Solves a problem this KB has”** skips both measurement and efficacy: this review finds examples of the gap, but neither the README nor a one-time sample shows drift over several ingests or proves the upstream lint solves it. “Nothing here would notice” overlooks the existing judgment pass and human review; “no deterministic check detects it” is defensible.
- **“Chosen to avoid” sentence tagging** assigns an undocumented motive to the anti-padding and callout rules. Their current wording does not establish that design history. The gbrain table is outside this review's evidence: its source was not read, so its accuracy remains unassessed.
