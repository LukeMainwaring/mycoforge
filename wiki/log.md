# Log

Append-only. Most recent at the bottom. Entry format:
`## [YYYY-MM-DD] <prefix> | <Title>` with prefixes
`ingest | query | lint | decision | schema | discovered`.

## [2026-07-10] schema | Initial schema established

Wrote `AGENTS.md`: three-layer architecture, frontmatter schema, claim callouts,
Ingest/Query/Lint workflows, log conventions, template contract.

## [2026-07-10] ingest | 2026-04-04 LLM Wiki (Karpathy)

Ingested the founding gist from `raw/articles/`. Created
[[Three-Layer Architecture]], [[Ingest Workflow]], [[Andrej Karpathy]], and the
synthesis [[Why LLM Wikis Beat RAG]] (three claims marked, all currently
supported). Seeded [[index]] and [[overview]].

## [2026-07-10] discovered | Template concepts are wiki-worthy

The template's own design ideas kept coming up while writing the schema, so they
became pages: [[Subtractive Onboarding]] and [[Fractal Federation]]. No raw
source behind them — provenance is the design session itself.

<!-- sf:begin(product) -->
## [2026-07-10] decision | Founding ADRs 001–004 accepted

Filed the four decisions from the template design session:
[[ADR-001 Separate Repo with Product as Seam]],
[[ADR-002 Fractal Federation for Nested KBs]],
[[ADR-003 Copy-and-Own with Config-Code Split]],
[[ADR-004 Read-Only MCP in v1]]. All `status: accepted`.
<!-- sf:end(product) -->

<!-- sf:begin(product) -->
## [2026-07-17] schema | Roadmap drops Now and Done sections

`roadmap.md` now holds Next / Later only — shipped items are removed rather
than archived (the log and git history are the record). Cleared the completed
v0.1–v0.3 items and updated the Roadmap-upkeep rule in AGENTS.md.
<!-- sf:end(product) -->

## [2026-07-23] ingest | Two YC talks on AI-native companies (paired)

Paired ingest of [[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]
(Diana Hu) and [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]
(Tom Blomfield) — deliberately together, as the second talk builds on the first.
Created concepts [[AI-Native Company]], [[Self-Improving AI Loop]],
[[Organizational Legibility]], [[Company Brain]], [[AI Software Factory]] and
people [[Diana Hu]], [[Tom Blomfield]], [[Jack Dorsey]] (stub, secondhand).
Updated [[Why LLM Wikis Beat RAG]]: Blomfield's diarization argument and the
regenerated YC user manual independently corroborate the compounding claim at
organizational scale. Two Anthropic articles remain captured-but-uningested in
raw/articles/.

## [2026-07-23] ingest | Running an AI-native Engineering Org (Anthropic)

Ingested [[2026-06-03 Running an AI-native Engineering Org (Anthropic)]] — the
AI-native cluster's first first-party practitioner source. Created
[[AI-Native Role Archetypes]] (anchor for the onboarding-archetypes plan;
Dorsey's accountability modes vs Claude Code's hiring filters),
[[Verification Bottleneck]], and [[Just-in-Time Planning]]. Updated
[[AI-Native Company]] (middleware claim low→medium on partial first-party
corroboration of the routing half; archetypes moved out; rollout/metrics
section added) and [[AI Software Factory]] (every-commit-Claude-assisted
evidence). One Anthropic PDF (The Founders Playbook) still awaits ingest.

## [2026-07-23] ingest | The Founders Playbook (Anthropic)

Ingested [[2026-05-06 The Founders Playbook (Anthropic)]] — Anthropic's vendor
prescription to founders (marketing ebook; provenance caveat noted on every
page). Created [[AI-Native Startup Lifecycle]] (four stages with exit criteria
and AI-specific failure modes) and [[Founder as Orchestrator]] (third axis for
the onboarding-archetypes plan). Updated [[AI-Native Role Archetypes]] (two
sets → three), [[Verification Bottleneck]] (founder-level analog: choose/
validate, not build), [[Company Brain]] (context-as-moat claim), and
[[AI-Native Company]] (lean-by-design corroboration). Marked the
prototypes-replace-design-docs claim in [[Just-in-Time Planning]] **contested**:
the playbook mandates architecture + scope docs before MVP code — reconciled
as durable context docs up front, feature planning JIT.

<!-- sf:begin(product) -->
## [2026-07-23] decision | ADR-005 Onboarding Archetypes as Presets
Filed [[ADR-005 Onboarding Archetypes as Presets]] (status: proposed): personal
second-brain and company playbook become `/onboard` interview presets (feature
keep-set + taxonomy + seed pages), no new template machinery; substrate framing
keeps the README lead. Implementation deferred — three Next items added to
[[roadmap]]. Planning handoff file deleted.
<!-- sf:end(product) -->

<!-- sf:begin(product) -->
## [2026-07-23] decision | ADR-005 accepted — archetype presets shipped
Implemented [[ADR-005 Onboarding Archetypes as Presets]] and flipped it to
accepted: archetype question + playbook seed scaffolding in the /onboard skill,
`[archetypes]` preset data in `.template/features.toml`, both preset combos in
`verify_matrix.sh`, and a "two archetypes" entry-paths section in the README
(substrate framing still leads). Shipped items removed from roadmap Next;
dogfooding the playbook preset remains.
<!-- sf:end(product) -->

## [2026-08-08] schema | Skill sync from sporeforge v1.2.3 upstream
Ported the sibling template's skill-pack conventions: vendored three new skills
(`writing-for-agents` + SKILL-MECHANICS, `grilling` rounds/frontier interview,
`wait-what`), added `disable-model-invocation: true` to `/onboard` and
`/sync-upstream`, gave every skill an `agents/openai.yaml` companion for
portability, and rewrote the onboard Phase 1 interview to the rounds format
with tool-agnostic phrasing. New skills are core (unmarked); no workflow-table
rows added — their descriptions are the context pointers.

## [2026-08-08] schema | Commit pinning + onboard rename fix, v0.4.0
Bumped the template to 0.4.0. `kb.toml` `[template]` gains a `commit` key so
instances pin the exact template SHA they synced from; `/sync-upstream` now reads
and records it. Fixed `do_rename` in `.template/onboard.py` to skip the
sync-upstream skill — its "MycoForge" references name the template, and
onboarding was rewriting them to the instance brand.

## [2026-08-28] schema | Skill sync from mattpocock/skills main (post-v1.2.3)
Audited the three vendored Pocock skills against upstream main at `6654f6b` (no new tag yet; sporeforge already ported the same in `951f011`). Ported: grilling round template now separates questions with `---`; `wait-what` description quoted (unquoted colon broke YAML discovery upstream); repo-wide em-dash removal in all three; grilling `openai.yaml` short description fixed to "a round of questions" (was stale). Kept our wiki-vocabulary rewrite of `wait-what`, so upstream's `CONTEXT-MAP.md` addition doesn't apply. `connect`, `research`, `snippet`, `transcript`, `onboard`, `sync-upstream` are MycoForge-native and weren't compared.

## [2026-09-02] ingest | The Claude Code Guide For Startups (Anthropic)

Ingested [[2026-08-20 The Claude Code Guide For Startups]] — Anthropic's
interviews with about a dozen Claude Code startups (Artemis, Cainex, Clay,
ClickHouse, Commure, Crosby, Emergent, Harvey, Heidi, Higgsfield, Omni,
Parahelp, Translucent, Zingage), distilled into five rules. First
multi-company practice source in the KB; vendor-selected testimonials, so
every claim it touches stays at medium. Created [[Everyone Ships]] (Rule 1),
[[Fix the Principle, Not the Example]] (Cainex's back-tested correction loop
and its overfitting failure), [[Build for Rebuilding]] (Rule 4), and
[[Prototype, Dogfood, Productionize]] (Rule 5); person pages for
[[Kareem Amin]] and [[Uriah Israel]]. Updated [[AI-Native Company]] (fifth
source, headline numbers, Artemis echo of the OS claim),
[[Self-Improving AI Loop]] (multi-company corroboration incl. ClickHouse agents
as #2/#3 contributors; learning-mechanism section), [[Verification Bottleneck]]
(new "what verification is made of" section: invariants, evals, hooks, review
agents; Higgsfield on per-model recalibration), [[AI Software Factory]]
(10x claim raised low→medium; mechanical-80% section), [[Just-in-Time Planning]]
(guide sits on both sides of the contested claim; Emergent's stale-context
tolerance rule; claim stays contested), [[AI-Native Role Archetypes]],
[[Company Brain]] (practitioner-brain section; moat claim echoes),
[[Why LLM Wikis Beat RAG]] (Omni chose files over a RAG pipeline),
[[Organizational Legibility]], and [[Founder as Orchestrator]]. Fixed a stale
line in [[overview]] that still said the Founders Playbook awaited ingest.

## [2026-09-02] ingest | The AI-Native SDLC playbook (Anthropic)

Ingested [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]] —
Anthropic's Applied AI team's stage-by-stage playbook for rebuilding the
six-stage SDLC around agents in a regulated enterprise. First incumbent-facing
source in the cluster; vendor prescription with no named cases, so every claim
it touches stays at medium. Created [[AI-Native SDLC]] (loop of stages, the
committed-artifact chain intent → spec → plan → diff → PR → incident, plays
table with indicators, legacy source-of-truth sidebar),
[[Advisory and Deterministic Controls]] (skills advise, hooks enforce; the five
control layers and placement rules), and [[Tiered Autonomy]] (autonomy by
σ-band, environment, change size, and guardrail maturity; production gate as
the ceiling). Updated [[Verification Bottleneck]] (enterprise restatement of the
bottleneck claim; "enterprise version" section: feedback loop, verifier
subagent, config-as-code evals; scans stale per model generation),
[[Just-in-Time Planning]] (fourth source on the contested claim: heaviest
write-it-down source yet but it kills the rituals; drift-tolerance divergence
startup vs enterprise; claim stays contested), [[Self-Improving AI Loop]]
(closing-the-loop mapped onto Blomfield's five layers), [[Company Brain]]
(CLAUDE.md/skills as owned institutional knowledge; under-a-page rule vs
Zingage's 567 lines noted as tension), [[Everyone Ships]] (plan and design
stages handed to non-engineers), [[AI-Native Company]] (sixth source; incumbent
side of the startup-advantage claim), [[Organizational Legibility]] (commit
chain and Slack channel as audit trail), [[Fix the Principle, Not the Example]]
(mistake-twice rule, review drift diagnostic), [[AI-Native Role Archetypes]]
(engineer → orchestrator → loop builder), [[overview]], and [[index]].
Source notes: the clipping's frontmatter says `published: 2001-08-21` (a
clipper typo; the URL and filename date it 2026-08-21), left as-is since
raw/ content is immutable. The clipper's filename carried a double space where
the "|" was stripped from the page title; renamed at the user's request to
`2026-08-21 The AI-Native SDLC Playbook (Anthropic).md` (rename only, content
untouched) and every link updated. Contributors credited (Jim Blackhurst,
Will Steuk, Jamal Arif) have no attributed content, so no person pages.

## [2026-09-06] ingest | The AI Daily Brief - How to Build an AI-Native Company Today
Podcast (24 min, YouTube captions labeled manual but reading as raw ASR): the
host walks [[Alex Lieberman]]'s "30 features of an AI native company" X post
one by one with qualifications. First non-Anthropic, non-YC source in the
cluster; an aggregator's checklist from a consultant who sells the
transformation, so it mostly corroborates existing pages as prescription and
every claim it touches stays at medium. Created [[Token Efficiency]] (cost per
successful task; routing, plan/execute model split, cost per accepted PR,
fine-tuned open models; tension with YC's token maxing noted),
[[Progressive Disclosure]] (metadata at the top of knowledge files so agents
load only a slice; the section "This KB is one" records that MycoForge's
frontmatter, index, and MCP split implement it), [[Alex Lieberman]], and
[[Nathaniel Whittemore]] (host; not named in the transcript, attributed from
the show byline, medium). Updated [[AI-Native Company]] (seventh source; full
30-feature table mapped to pages, numbering as heard skips 14; daily-driver
harness gloss; marketing-barbell aside), [[Company Brain]] (new contested
low-confidence claim: one intelligence layer vs the host's mesh of sources of
truth; context as code; skills not prompts), [[Organizational Legibility]]
(record-everything corroborated; new claim: a process map is context for
redesign, not a template for agents; feature 30 traceability),
[[Self-Improving AI Loop]] (loops need an objective success metric; SEO loop
example), [[Tiered Autonomy]] (first non-Anthropic corroboration; new
by-trust-earned axis: observe → suggest → act with approval → act alone; human
sandwich section with the middle left open),
[[Advisory and Deterministic Controls]] (governance-as-unlock section: permissions inherited and enforced
in the data layer, legal/HR/IT in lockstep), [[Everyone Ships]] (third source
on the claim; intent vs implementation, citizen-developer SDLC, Claude Tag
Slack anecdote), [[AI Software Factory]] (feature 10 as checklist; cost line),
[[Build for Rebuilding]] (every-three-months policy; disrupt yourself),
[[Just-in-Time Planning]] (fifth source on the contested claim, status
unchanged), [[Verification Bottleneck]] (evals as core infrastructure; "everyone
is in the eval business"), [[AI-Native SDLC]] (intent/implementation split and
traceability restated independently), [[AI-Native Role Archetypes]] (new claim:
every agent workflow needs a named owner, the DRI arrived at independently;
"everyone becomes a manager of agents"), [[Three-Layer Architecture]]
(cross-reference only), [[overview]], and [[index]]. Not filed: features 13,
17, 18, 20 (continuous finance, ROI framework, ad-creative swarms, agentic
cybersecurity) have no second source; listed in the table only. Source
notes: Lieberman's X post is not in `raw/` and would be the upstream
reference; the transcript's proper nouns are ASR-garbled ("Grockbot",
"codecs and GBT image 2", "Benti Jal" for the quoted commenter) and were not
relied on.

## [2026-10-22] schema | Skills audit: sync to mattpocock/skills v1.3.1, vendoring manifest, invocation pass
Synced `grilling` to upstream `5beb35b` ("Grill" description, "yes accepts the recommendation" line). Removed `wait-what` (unused). Vendored `grill-me`, `handoff`, `teach` (workspace scoped to `learning/<topic>/`), `pr` (wiki vocabulary in place of `GLOSSARY.md`). Added `.agents/skills/VENDORED.md` + `scripts/check-vendored-skills.sh` (from sporeforge) and a `/sync-skills` skill that runs them; upstream `engineering/research` deliberately skipped in favour of the native `/research`. Made `connect`, `research`, `transcript`, `snippet` user-invoked (`disable-model-invocation`, `allow_implicit_invocation: false`, argument hints) so the agent never reaches for capture or connection skills unprompted; `/research` now offers to run its search phase as a background agent. AGENTS.md: workflow table shows slash forms, new Version control section (content to `main`, tooling via branch + `pr`-skill PR), template contract names the manifest.


## [2026-10-22] schema | /scout skill, shared capture rules, staging ledger
Added `/scout` (user-invoked, `insight` feature): a standing watch that reads `[scout]` from `kb.toml` (topics, watch list, `max_age_days = 60`, `repo_active_days = 30`, `lookback_days = 90`), fans out background sub-agents, and stages at most five fresh candidates in a new `staging/scout.md` ledger that doubles as review stage, skip list, and run history. Factored `/research` step 4 into a `capture.md` beside it (adds `type: repo` and `updated:`), which both skills now point at. AGENTS.md: workflow-table row, insight section renamed "Research, Scout, and Connect". gbrain seeded as a watch target rather than a design input.

## [2026-10-22] schema | Ingest step 5 and the ingest queue
Ingest now ends by routing any implication for the KB's own schema, claims, lint, or skills to a branch instead of changing them mid-session. Added `staging/ingest.md` (ordered queue with watch-outs; /scout appends to it on hand-off) and seeded it with the five sources from today's scout run.

## [2026-10-23] ingest | WikiSkill (Google Research paper, 2026-08-27)
First paper in `raw/` and first source whose raw layer is machine-generated:
WikiSkill co-evolves agent skills with a persistent wiki (raw traces → wiki
patterns → skills; skills gated on a validation score and rolled back, wiki
never), citing Karpathy's gist. New: [[Skill Evolution]] (loop anatomy, four
claims, results table, limitations) and [[Tu Vu]] (corresponding author; also
on the EvoSkill baseline and the SealQA benchmark). Updated
[[Three-Layer Architecture]] (new claim: layers generalize to any immutable raw
record; executor denied wiki access), [[Why LLM Wikis Beat RAG]] (compounding
claim gets its first controlled evidence, 63.7% vs 48.7% ablation; index-first
claim gets a machine-scale data point), [[Progressive Disclosure]] (first
non-practitioner source on the metadata claim; cost model for index-first
reading), [[Self-Improving AI Loop]] (the anatomy benchmarked), [[Fix the Principle, Not the Example]]
(measured negative transfer from
workaround-encoding skills; maintainer rules as the Cainex fix written down),
[[Ingest Workflow]] (unattended maintainer; sampling instead of
one-source-per-session; "no mechanism to prune" vs Lint), [[Token Efficiency]]
(9B with skills beats 27B without), [[Andrej Karpathy]],
[[Advisory and Deterministic Controls]], [[overview]], [[index]]. No existing claim contested;
all confidences unchanged (single paper, authors' method vs a baseline one
author co-wrote). Schema implication, not acted on here: the paper's third
layer is executable skills fed by the wiki, with `PURPOSE.md` as per-skill
provenance back to wiki pages. Whether `wiki/` should feed `.agents/skills/`
here, and what would gate it given this KB has no validation score, is a
branch decision; also worth a look is its executor/maintainer read split for
the MCP server's readers.

## [2026-10-23] ingest | gbrain Belief Ledger design (Garry Tan, 2026-10-16)
First database-backed brain in `raw/` and first gbrain document: an
append-only ledger of canonical belief transitions (page, fact, take, link)
keyed on logical identity, with recorded time kept apart from source time,
trust tier on every event, contested-not-refused supersession, baseline and
watermark coverage that refuses rather than guesses, and a measured weekly
belief diff. New: [[Belief Ledger]] (four portable rules, two claims: diff
beliefs not rows, measured 0 beliefs per 27 to 258 row writes; cited change
diff costs about the same tokens as an uncited list) and [[Garry Tan]].
Updated [[Three-Layer Architecture]] (new section and claim: markdown plus
git records file history, not belief history; assessed as holding for
identity but mostly not for time in this KB, since one commit per workflow
run makes commit time recorded time), [[Company Brain]] (a brain that knows
when it knew; trust per write; disclosed coverage), [[Organizational Legibility]]
(the strict form of record-everything; the design doc as a legible
decision log), [[overview]], [[index]]. No existing claim contested. Sections
5 to 12 of the source (DB mechanics, purge sweeps, backup contract) read but
not filed. Schema implications, not acted on here: (1) `[!claim]` callouts
have no stable identity, so a rename or title edit severs a claim's history;
a short claim id in the callout would fix it and let lint track status
changes over time. (2) The KB has no coverage marker: pages written before
callouts existed carry no "beliefs before this date unrecorded" note. (3)
This KB is already bitemporal in a loose way (raw filename date is source
time, frontmatter `created`/`updated` and commit time are recorded time);
worth naming in AGENTS.md. (4) gbrain's contested-not-refused rule is
`status: contested` made mechanical; `raw/` has no trust tier, and whether
sources should carry one (paper vs practitioner vs vendor) is a branch
question. Each is a branch decision with this source as the PR citation.

## [2026-10-23] schema | Decisions become trunk; Decision workflow; schema-review prompt
`decisions/` leaves the `product` feature: removed from `.template/features.toml` paths, Decisions section in [[index]] unwrapped, `README.md` feature table and the ADR-001 keep-if in [[Company Brain]] adjusted. New **Decision** workflow in AGENTS.md (own table row; Product ops keeps roadmap and embedded prompts): Ingest step-5 schema implications become `status: proposed` ADRs on a branch, and later ingests add evidence to the ADR rather than the log. Added `staging/schema-review-prompt.md`, a shared prompt for two independent external reviews of the four gbrain implications (output to `staging/schema-review-gbrain-<model>.md`); the ADRs come after those reviews are read. verify_matrix all cases pass, lint clean.

## [2026-10-23] decision | ADR-006 to ADR-010 proposed from the gbrain schema review
Two independent reviews (Opus 5.5, GPT-6; `staging/schema-review-gbrain-*.md`) ran `staging/schema-review-prompt.md` on the four gbrain implications; a third session wrote the agree/disagree diff (`staging/schema-review-gbrain-diff.md`). Factual splits checked here: the claim convention predates all content (scaffold commit `2833df0`); raw date drift is real (SDLC `published: 2001-08-21`, gbrain file named by `updated:`, `retrieved:` vs `created:` mixed, PDFs bare); lint never parses callouts; `/connect`'s `speculative` is missing from the Claims vocabulary. Filed as proposed: [[ADR-006 Two Clocks in Frontmatter]], [[ADR-007 No Stable Claim Identity]], [[ADR-008 No Coverage Marker]], [[ADR-009 Hand Edits Are the Unmanaged Writer]], [[ADR-010 Lint the Claim Contract]]. Corrected the misreads both reviews found in [[Belief Ledger]] (ledger is one of several DB-only stores, not "the one"; per-page coverage cuts; backfill keeps a run time; trust rules narrowed to the common case; "diff beliefs" claim dropped to medium, scratch bench), [[Three-Layer Architecture]] (claim retitled; "severs" softened; time half narrowed to agent writes) and [[Company Brain]]. None of the five is implemented yet; acceptance is the user's.

## [2026-10-23] decision | ADR-006 to ADR-010 accepted and implemented
All five accepted by the user. `scripts/lint.py`: `check_claims` (hard error; one confidence, one status from `kb.toml` `[lint].claim_statuses`, evidence with a resolving wikilink; 42 callouts pass) and `check_raw_dates` (warn-only; flags the SDLC Playbook's `published: 2001-08-21` and the gbrain file named by `updated:`, both for the user to fix in `raw/`). `kb.toml`: `claim_statuses` adds `speculative`. AGENTS.md: two-clocks sentence under File naming; historical-answer rule under Query; Claims gains the vocabulary, the supersede/reword/move rules and the hand-edited-claim rule; Version control gains `hand-edit:` commits at session start. `/onboard` logs an import coverage line. ADR statuses set to accepted; [[index]] updated.

## [2026-10-23] ingest | obsidian-wiki (ar9av, repo README + notes, 2026-10-22)
First open-source implementation of the Karpathy gist in `raw/`: 39 markdown skills, optional Python CLI, 3,609 stars at capture. New: [[Provenance Tags]] (extracted / inferred / ambiguous on every claim, lint for speculative drift and undated claims; compared as origin vs standing with this KB's callouts and gbrain's trust tiers; one claim, medium). Updated [[Three-Layer Architecture]] (third raw type, conversations and mined session histories, added to the generalization claim's evidence; memory surface and locked writer as wiki-layer properties), [[Ingest Workflow]] (new section: batch ingest with a manifest vs one source per session; the locked writer only matters for parallel agents, points at ADR-009), [[Why LLM Wikis Beat RAG]] (index-first claim: second no-embeddings implementation, QMD search as graduation path, 2000-page figure asserted not shown), [[Progressive Disclosure]] (new section and claim: bookkeeping files must stay out of the link graph, from the 38-page benchmark where the plain agent routed every path through `index.md`; n=2 per cell, so medium), [[Andrej Karpathy]], [[overview]], [[index]]. Later-evidence notes on [[ADR-004 Read-Only MCP in v1]] (read-write Memory API and HTTP/MCP service, the opposite choice), [[ADR-009 Hand Edits Are the Unmanaged Writer]] (a lock solves agent-vs-agent, not user-vs-agent), [[ADR-010 Lint the Claim Contract]] (drift lint is the check the ADR declined). No existing claim contested. Only the README and repo notes are in `raw/`; `docs/architecture.md` and `docs/memory.md` were not captured, so the four ingest stages and the hook mechanics are cited from the README's summary. No person page for the author, who appears only as a handle. Schema implications, not acted on here: (1) a lighter form of the speculative-drift lint, such as `^[inferred]` on prose sentences counted per page, or a page-level inferred count, as a `proposed` ADR; (2) whether `/connect` and any future graph tooling should exclude `index.md` and `log.md` explicitly, likely one line in the connect skill and `kb.toml`; (3) a session-start recap (overview, open ADRs, last log entries) is what obsidian-wiki's hook injects and this KB's Query step approximates by hand; worth deciding whether to name it in AGENTS.md. Also noted for later: "challenge queries" that argue against a plan from the wiki's own record, which this KB has no counterpart for.

## [2026-10-23] decision | ADR-011 Speculative Drift Lint proposed from the obsidian-wiki review
Two independent reviews (Opus 5.5, GPT-6; `staging/schema-review-obsidian-wiki-*.md`, diff in `-diff.md`) ran `staging/schema-review-obsidian-wiki-prompt.md` on the one real implication from the obsidian-wiki ingest. Both: no drift lint, no field; widen `speculative` to the agent's own inferences and add the check to the lint judgment pass. Filed as proposed: [[ADR-011 Speculative Drift Lint]]. Misreads both reviews found fixed in [[Provenance Tags]]: no "tag mix" algorithm in the README, "every claim" not "every sentence", `undated_claims` attributed to the repo notes, the `check_claims` quote re-attributed to ADR-010, the invented anti-padding motive dropped; claim "Marking the origin of every claim lets lint catch a page drifting into speculation; marking only contestable claims cannot" split into "obsidian-wiki marks the origin of every claim and lints pages for drift into speculation" (supported) and "A lint over origin marks can only count inference the agent already admitted to..." (speculative, first non-connect use of the status). [[Three-Layer Architecture]]: "page to the sentence" corrected to "contestable claim to every claim". `/connect` skill step 1 now leaves `index.md`, `log.md` and `overview.md` out of the link map (implication 2 from the ingest, no ADR needed). Implication 3, a session-start recap in AGENTS.md, rejected: Query already reads the index first and session start already runs `git status`; both reviews agree an end-of-session capture nudge would break user-invoked capture. The sentences the reviews named ("strictly worse than RAG" and the Three-Layer safety generalisations) are left for the PR that accepts the ADR.

## [2026-10-23] decision | ADR-011 accepted and implemented
Accepted by the user. AGENTS.md Claims: `speculative` is an inference the agent drew rather than a source stated, during ingest or query filing as well as `/connect`, with premises and a confirm/refute line in its evidence; a contestable sentence no source states goes in a `speculative` callout or is cut. Lint step 2 gains "contestable inference in bare prose and claims whose conclusion is stronger than the evidence cited". The sentences both reviews flagged: [[Why LLM Wikis Beat RAG]] "strictly worse than RAG" is now the speculative claim "A wiki whose bookkeeping lapses is worse than RAG..." (low); [[Three-Layer Architecture]] "not a fourth layer" is now the speculative claim "A belief ledger is a property of the wiki layer, not a fourth layer" (medium), "precisely because it can never damage" attributed to Karpathy's framing, "no human in the loop at all" narrowed to WikiSkill's setting; [[Progressive Disclosure]] "trustworthy enough to route on" softened. No `scripts/lint.py` change. [[index]] updated.

## [2026-10-23] ingest | openwiki (langchain-ai, repo README + notes, 2026-10-22)
The vendor-scale comparator: LangChain's repository-to-wiki tool, 17,335 stars, 70 commits in the 30 days before capture, Deep Agents underneath. Code mode documents a repo with Grounded Claims and scheduled CI runs that open docs PRs; personal mode synthesizes nine connectors with no claims. No new concept page: the staging watch-out held and the material went to existing pages. Updated [[Ingest Workflow]] (new section: continuous ingest, the gate moves to the PR; one speculative claim, "One source per session is a choice of gate, not of scale", drawn across WikiSkill, obsidian-wiki and OpenWiki with confirm/refute lines), [[Why LLM Wikis Beat RAG]] (maintenance claim gains the no-op-run design; index-first claim notes the search mechanism is unstated, so not a data point on embeddings), [[Provenance Tags]] (table gains an OpenWiki column, origin / standing / currency framing, one supported claim on versioned evidence ranges rechecked before no-op; medium, README only), [[Three-Layer Architecture]] (the generalization claim's evidence gains the limit that OpenWiki's raw layer is mutable and holds only via per-claim evidence versions; schema layer split by owner, `INSTRUCTIONS.md` vs the managed `AGENTS.md` block), [[Progressive Disclosure]] (OKF v0.2 reserves `index.md` and `log.md` as non-concepts), [[overview]], [[index]]. Later-evidence notes on [[ADR-004 Read-Only MCP in v1]] (read-only search plus a validated MCP write lifecycle, the shape to copy if writes ever come), [[ADR-006 Two Clocks in Frontmatter]] (`generated` vs `verified` as two maintenance clocks) and [[ADR-007 No Stable Claim Identity]] (the consumer exists there, staleness against versioned evidence, and still not here). No existing claim contested. Only the README and repo notes are in `raw/`; `src/`, the OKF spec and the CI example workflows were not captured, so claim mechanics are cited from README prose. No person page: the author is an organization. Schema implications, not acted on here: (1) claim evidence here is a wikilink to a raw file, never a location in it; with raw immutable a pinned range buys only reader auditability, so whether `[[raw#heading]]` anchors are worth the write cost is a `proposed` ADR question, not a lint change. (2) If `/scout` capture is ever scheduled, the one-source rule's gate moves from the ingest session to PR review, as OpenWiki's does; AGENTS.md should say so before any scheduling, not after. (3) This KB's frontmatter is close to OKF v0.2 (`type`, `sources`; `status` on ADRs); emitting or validating OKF is a product-layer question for the MCP server, not a wiki change. (4) The MCP write lifecycle is the graduation path ADR-004 named, now with a worked shape; no change until a writer other than this session exists.

## [2026-10-23] ingest | Building Effective Agent Automations (Anthropic, Lance Martin and CJ Avilla, 2026-10-08)
Anthropic's daily-brief reference implementation on Managed Agents: a scheduled agent whose only continuity is two mounted folders, reader-owned read-only preferences and agent-owned read-write state (per-source bookmarks, an append-only ledger of reported items, a run record, proposed preference changes, source notes). The staging watch-out asked whether it names a pattern worth a page; it does. New [[Unattended Agent State]] with two supported claims (bookmarks not windows; record only after confirmation, duplicate over silent loss) and one speculative claim on what a scheduled `/scout` would need first, with confirm/refute lines. Updated [[Advisory and Deterministic Controls]] (new section: unattended runs lean on layers 4 and 5 alone; read-only token behind `always_allow` MCP tools; the authors' stated residual that a planted instruction can change the brief through the agent's own notes), [[Belief Ledger]] (the reported-items ledger as a second, smaller kind: what was told vs what is believed), [[Ingest Workflow]] (continuous-ingest section points at the pattern as the floor under any scheduled capture), [[overview]], [[index]]. New person stubs [[Lance Martin]] and [[CJ Avilla]]. No existing claim contested. The article's Managed Agents mechanics (vaults, `ant apply`, deployment files) are platform detail and were not paged. Skill implications, not acted on here, for a branch: (1) `/scout` step 3 and 4 have no rule for a `watch` entry the sub-agent could not fetch, so an outage reads as `nothing new`; the smallest fix is a sub-agent returning `unreachable` for its entry and the run header listing those entries, keeping their window open for the next run. (2) `/scout` step 5 appends approved `watch` entries to `kb.toml` directly; the source's shape is a proposals file in state that the user applies, which would keep `kb.toml` strictly user-owned. Both are also the preconditions the speculative claim names for any scheduled run, which [[Ingest Workflow]]'s log entry of the openwiki ingest already flagged as a gate question for AGENTS.md.

## [2026-10-23] schema | Scout: unreachable sources and proposed watch rows
From the agent-automations ingest. `/scout` sub-agents now return `unreachable` for a `watch` entry they could not read instead of an empty list; the run header lists them under `unreachable:` and their window stays open until a run reads them, so an outage never reads as `nothing new`. Watch candidates are written as `proposed watch` rows in the ledger for the user to paste; the skill no longer edits `kb.toml`. AGENTS.md Research, Scout, and Connect paragraph updated. Source: [[2026-10-08 Building Effective Agent Automations (Anthropic)]], paged as [[Unattended Agent State]].

## [2026-10-23] decision | ADR-012 to ADR-014 proposed from the open-implications review
Two independent reviews (Opus 5.5, GPT-6; `staging/schema-review-open-implications-*.md`, prompt in `-prompt.md`, diff in `-diff.md`) ran on the three implications still open from the WikiSkill, openwiki and agent-automations ingests. Both: no change on wiki-feeding-skills and on evidence anchors; a scheduled `/scout` needs an ADR naming what the run may write and harness-enforced limits before it exists. Split only on whether to add the sentence now (Opus yes, GPT-6 optional); added as proposed since `disable-model-invocation` does not stop a cron `claude -p "/scout"`. Filed as proposed: [[ADR-012 No Scheduled Capture Without a Decision]] (two AGENTS.md sentences: no scheduled skills without a Decision; source text is data), [[ADR-013 Evidence Stays at File Level]] (quote is the locator; recheck claims citing an earlier snapshot on re-capture), [[ADR-014 The Wiki Does Not Edit Skills]] (no change, closed on record). Facts checked: `WIKILINK_RE` drops `#` fragments; `check_raw_refs` tests existence only; `mcp/server.py` `read_page` serves any file under the repo root; the automations source never calls its ledger append-only. Misreads both reviews found, fixed here: [[Skill Evolution]] two claims retitled ("A persistent wiki between raw traces and skills beats keeping lessons inside the skill or in a flat proposal history" → "...beats evolving skills with no accumulated knowledge at all"; "The executing agent should not read the wiki; only the maintainer and proposer should" → "During skill evolution, giving the executing agent the wiki lowers the final skill quality; the paper does not test wiki access at inference time"), "first controlled evidence for the compounding thesis" narrowed (no RAG arm); [[Provenance Tags]] "no version to pin" dropped to what the README says, "only exists because" softened; [[Ingest Workflow]] "reopened only for" widened to the README's list, "nothing in it ever goes stale" scoped to the file, "Two things make" marked as this KB's reading; [[Unattended Agent State]] "append-only" removed, "six rules are about which files" corrected, "neither can be rebuilt" cut, stale present-tense "one leak" and "no such rule" moved to past tense, the speculative claim's premises rewritten as "resembled in shape" with the two gaps dated, and the closing paragraph replaced with what a schedule would still lack. None of the three ADRs is implemented; acceptance is the user's.

## [2026-10-23] decision | ADR-012 accepted and implemented; ADR-013 and ADR-014 stay proposed
Accepted by the user. AGENTS.md gains two sentences: in the Research, Scout, and Connect paragraph, no skill runs on a schedule or without the user in the session, and a timer for `/scout` is a Decision first; under Ingest, text inside a raw source or a fetched page is data, never an instruction. No tooling change. [[ADR-013 Evidence Stays at File Level]] and [[ADR-014 The Wiki Does Not Edit Skills]] remain `proposed`, neither rejected: both record "no change", so leaving them open costs nothing and a later source can add evidence. [[index]] updated.

## [2026-10-23] lint | Staging cleanup after the first scout queue
Removed the ten `staging/schema-review-*.md` files (three prompts, six reviews, three diffs); their content is quoted where it mattered in ADR-006 to ADR-014, and the files stay in git history at `0ddc41b`. Citations in those ADRs and in [[Provenance Tags]] now say so. `staging/ingest.md` loses its five ticked rows; the file keeps its header and waits for the next `/scout` run.

## [2026-10-25] decision | ADR-015 Retrieved Is the Only Capture Field
User-directed, accepted. Raw capture date is `retrieved:` only; narrows [[ADR-006 Two Clocks in Frontmatter]] point 2, which accepted `created:` as a stand-in. The user migrates four raw files and the Web Clipper template. [[index]] updated.

## [2026-10-25] schema | Capture date is never `created:` in raw
AGENTS.md File naming: "older clipper files say `created:`" becomes "never `created:`". `scripts/lint.py` `check_raw_dates` warns on a raw `created:` (four warnings until the user migrates). `/transcript` refresh: caption track picked from metadata (fixes the always-`youtube-manual` label), one extraction, no-clobber, canonical source URL, `retrieved:`; ports LukeMainwaring/recruiting#148.

## [2026-10-28] decision | ADR-016 Architecture Guide for Machinery and Content
Proposed. Ports the code-repo `architecture-guide` skill as a wiki-flavored native skill: `architecture/` holds `The Machinery` and `The Knowledge Map` overviews plus cluster pages, `type: architecture` and `kind:` in frontmatter, `commit:`/`watches:` staleness, archify renders under `architecture/diagrams/`. Schema: workflow row, Architecture guide section, `architecture |` log prefix, `[features.architecture]`.

## [2026-10-28] architecture | First run: The Machinery and The Knowledge Map
Wrote `architecture/`: The Machinery (kind: machinery, five focuses), The Knowledge Map (kind: content) and three cluster pages (Map - AI-Native Organizations, Map - AI-Native Software Engineering, Map - The Knowledge Layer), each with a Mermaid diagram, `commit: 4b7c704` and `watches:`. Indexed under a new Architecture section; linked from Home. Renders of the two overviews follow.

## [2026-10-28] decision | ADR-016 accepted and implemented
Status proposed → accepted, same PR. Skill, five `architecture/` pages, two archify renders and the `architecture` feature are in; the three cluster renders are queued as their own PRs.

## [2026-10-28] architecture | Render Map - AI-Native Organizations
First archify rendering of the AI-native organizations cluster at `architecture/diagrams/map-ai-native-organizations/` (type architecture, revision 4bb66ef). Page gets its "Rendered with archify" link; README table gets a row. No page text changed.

## [2026-10-28] architecture | Render Map - AI-Native Software Engineering
First archify rendering of the AI-native software engineering cluster at `architecture/diagrams/map-ai-native-software-engineering/` (type architecture, revision cb850c4). Page gets its "Rendered with archify" link; README table gets a row. No page text changed.

## [2026-10-28] architecture | Render Map - The Knowledge Layer
First archify rendering of the knowledge-layer cluster at `architecture/diagrams/map-the-knowledge-layer/` (type architecture, revision e3226d0). Page gets its "Rendered with archify" link; README table gets a row. No page text changed.

## [2026-10-28] architecture | Re-render Map - AI-Native Organizations (model comparison)
Fresh archify rendering of the AI-native organizations cluster at `architecture/diagrams/map-ai-native-organizations/` (type architecture, revision c82d295), drawn from scratch by a second model for a side-by-side comparison with the earlier render; the old spec and HTML were deleted first so the layout is independent. Page link and README row unchanged. No page text changed.

## [2026-10-28] architecture | The Knowledge Map watches its topic pages, not index.md
`check` flagged The Knowledge Map stale on every `index.md` edit, which the page template says not to watch. `watches:` now lists `overview.md` and the three cluster pages; `commit:` and the render's pinned revision bumped to HEAD (layout unchanged). All five pages and renders read current.

## [2026-10-28] schema | /audit: one health report that never edits
New user-invoked `/audit [quick]` skill and `scripts/audit.py` (with `scripts/test_audit.py`): the script prints lint output, the vendored-skill check, architecture staleness and the scout ledger's latest run with counts; the skill pastes them verbatim, summarizes, and names the fixing workflow per finding. Its one write is the scout run section; `quick` skips scout. `/scout` step 5 now also captures `approved` rows left from earlier runs; `/architecture-guide`'s stale-page and new-entries steps call `audit.py --architecture`. Decision in [[ADR-017 Audit Reports, Never Edits]]; scheduling and a Slack channel wait on the ADR that [[ADR-012 No Scheduled Capture Without a Decision]] requires. AGENTS.md gains the `/audit` row and an Audit section. A second-model review before merge found six bugs (malformed diagram metadata crashing the report, git errors and scalar `watches:` reading as current, a first-run ledger going unseen, `--root` checking the wrong manifest, `quick` hiding ledger state, insight-pruned prose keeping the write exception); all fixed with tests.

## [2026-10-28] architecture | The Machinery gains /audit
`check` flagged [[The Machinery]] stale after the `/audit` merge. The "Keeping it honest" focus gains a paragraph on `/audit` and `scripts/audit.py`, the diagram an Audit node (lint counts in, findings and next moves out to you), and "Why it's built this way" a bullet citing [[ADR-017 Audit Reports, Never Edits]]. `watches:` adds `scripts/audit.py`; `commit:` to `0ed9182`, which settles the new entries (the audit skill and script, now explained on the page). The rendered diagram stays stale until re-rendered. Other four pages current.
