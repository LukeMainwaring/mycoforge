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
