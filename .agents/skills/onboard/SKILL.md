---
name: onboard
description: Turn this MycoForge template clone into your own knowledge base — interview for domain, identity, features, and page-type taxonomy; run the deterministic prune+rename; generate the seed pages; verify with lint. Use when starting a new KB from this template.
disable-model-invocation: true
---

# Onboard a MycoForge clone

You are turning this freshly-cloned MycoForge template into the user's own
knowledge base. This skill orchestrates an interview, then leans on the
**deterministic** helper `.template/onboard.py` for pruning + renaming, and on
**your generation** for the schema taxonomy, seed pages, and prose. Work through
the phases in order. Confirm before anything destructive. Never invent feature
lists — read them from the manifest.

## Phase 0 — Preflight

1. Check `.template/features.toml` exists. If `.template/` is gone, this repo is
   already onboarded — stop and tell the user.
2. Run `python3 .template/onboard.py --list` to see the cuttable features and
   their descriptions (all independent). Read `.template/README.md` if you need
   the marker/prune details.
3. Confirm git state is clean (or warn the user) so onboarding is a reviewable diff.

## Phase 1 — Interview

Run the interview in **rounds** (the `/grilling` format): each round, ask every
question whose prerequisites are already settled — numbered, each with your
recommended answer — then wait for the user's answers before recomputing what's
askable. Question 1 gates the pre-fills of questions 4–5, and question 3's
defaults derive from question 2, so a typical run is two rounds. Facts are your
job, never the user's: read the feature list and git state yourself. Skip
anything the user already answered (e.g. via an argument).

1. **Archetype** (single-select) — the first question:
   - **Personal second-brain** — an individual's compounding research/reading KB.
   - **Company playbook** — a venture's durable context layer: the decisions,
     playbooks, and roles that outlive any feature plan.
   - **Custom** — no preset; the rest of the interview runs as written.

   A preset pre-fills three later answers — the feature keep-set (read it from
   the `[archetypes]` block in `.template/features.toml`, never hardcode), the
   taxonomy proposal (question 5), and the Phase 4 seed-page set. Presets are
   defaults, not locks: still show each pre-filled answer and let the user
   override it. A preset's `optional` features are always asked explicitly.
2. **Domain + purpose** (free text): what is this KB about, and what feeds it —
   papers? articles? podcasts? a book? Use the answer everywhere below.
3. **Identity** (free text): slug (lowercase, `^[a-z][a-z0-9_]*$`) and display
   brand. Offer defaults derived from the domain; validate the slug.
4. **Feature keep-set** (multi-select — one per feature, read
   from `--list`; with an archetype, present the preset's `keep` list as the
   pre-selected answer and ask its `optional` features individually):
   Describe each from its `--list` line. When to recommend keeping it:
   - `product` — this KB feeds software.
   - `orchestrator` — only a parent KB with nested child KBs.
   - `media-capture` — podcast or video sources.
   - `insight` — the KB grows by exploration, not only by sources the user
     already has.
   - `architecture` — the user wants diagrams of the KB kept current, or will
     explain it to other people.
   - `mcp-server` — other repos' agent sessions will read this KB.
5. **Page-type taxonomy**: propose domain-appropriate types —
   `concepts/people/syntheses` for a research KB, `books/authors/themes` for a
   reading library, `projects/experiments/notes` for a lab KB — plus "keep the
   default". The chosen types become the `wiki/` subfolders and the `type:`
   values in the frontmatter schema. Archetype pre-fills: second-brain proposes
   the default `concepts/people/syntheses`; playbook proposes
   `concepts/decisions/playbooks/roles` (decision pages live in the top-level
   `decisions/`, which every instance keeps; `playbooks/` and `roles/` are
   `wiki/` subfolders).

## Phase 2 — Dry run + confirm

```bash
python3 .template/onboard.py --keep <kept-features> --slug <slug> --brand <Brand>
```

Show the plan: features kept/dropped, the rename, the taxonomy, and what you'll
generate in Phase 4. Get an explicit go-ahead before applying.

## Phase 3 — Prune + rename (deterministic)

```bash
python3 .template/onboard.py --keep <kept-features> --slug <slug> --brand <Brand> --apply
```

Do **not** hand-delete features or hand-rename — the script deletes disabled
features' paths, strips all `sf:` markers, verifies the symlinks and skill
references, and renames the identity tokens (preserving the `[template]` repo
pin in `kb.toml`).

## Phase 4 — Generate

Now your half. All of it must obey the schema in `AGENTS.md`:

1. **Schema**: update `AGENTS.md` for the chosen domain and taxonomy — the
   instance description, the `type:` list in the frontmatter section, any
   domain-specific workflow notes from the interview. Keep the template contract
   section intact (markers are gone, but the kb.toml discipline still applies).
2. **Example reset**: the template ships its author's live KB as the example.
   Delete all of it that survived the prune, leaving each folder in place:
   - every page under `wiki/concepts/`, `wiki/people/`, `wiki/syntheses/`
   - every source under `raw/articles/`, `raw/papers/`, `raw/podcasts/`
   - every ADR in `decisions/` that no surviving file cites. List the cited
     ones with
     `grep -rhoE 'ADR-[0-9]{3}' AGENTS.md .agents/skills scripts mcp kb.toml 2>/dev/null | sort -u`
     and keep those: they hold the reasons for rules this instance inherits. In
     each kept ADR, turn wikilinks to deleted pages into plain text and drop
     the `sources:` / `raw:` entries for deleted sources.
   - `product/MVP.md` and the example page in `product/software/` (if `product`
     was kept)
   - `images/mycoforge-logo.png`
   - every page under `architecture/` and every folder under
     `architecture/diagrams/` (if `architecture` was kept; the first
     `/architecture-guide` run rebuilds them for the new wiki)
   - the rows in `staging/ingest.md` and the run sections in `staging/scout.md`
     (if `insight` was kept)

   Then create the taxonomy's empty subfolders.
3. **Seed pages**: fresh `wiki/overview.md` (domain, purpose, where to start),
   `wiki/index.md` (empty catalog with the taxonomy's sections), `wiki/log.md`
   (one genuine `schema |` entry recording the onboarding; if the user brings
   existing pages into `wiki/` instead of starting empty, the entry also says
   `imported N pages; beliefs before <date> not recorded as claims`, so the
   coverage gap is on record in the log and never on the pages), and — if `product`
   was kept — a thin `Home.md`, `roadmap.md`, `product/Vision.md` for the new
   domain.

   **Playbook archetype scaffolding** — if the archetype is *company playbook*,
   additionally seed these three pages. Moderately opinionated: real frames the
   venture localizes, not blank stubs — but the anti-padding rule still applies,
   so each is a dense skeleton, not an essay. Self-contained prose only (the
   template's own wiki pages are gone by now). Index and cross-link all three;
   `confidence: low` until the venture has filled them in.

   - **`wiki/concepts/Venture Lifecycle.md`** — the stage frame. A four-stage
     table (Idea → MVP → Launch → Scale), one row per stage with its **exit
     criterion** and known failure modes. Pre-fill the generic criteria —
     problem-solution fit from real conversations before building (Idea);
     product-market-fit evidence in retention, revenue, or referral from an
     identifiable group (MVP); repeatable channel-driven growth with operations
     that don't route through the founder (Launch); a threshold event the org
     withstands external scrutiny for (Scale) — then mark the venture's current
     stage and localize its failure modes. State the operating rule: evidence
     gates building; no stage advances until its exit criterion is met.
   - **`wiki/playbooks/Playbook Template.md`** — the loop-anatomy shape every
     playbook page follows. One company process per page, documented as a
     closed loop in five parts: **sensors** (what the process observes —
     tickets, telemetry, churn events), **policy** (what the AI may do alone,
     what needs human permission, what must be logged), **tools** (the
     deterministic actions available), **quality gate** (evals, checks, human
     review for high-risk actions), **learning mechanism** (how failures feed
     back to the top). Each playbook names a single owner (the DRI) and its
     current automation level, from manual-with-checklist to closed-loop.
   - **`wiki/roles/Role Template.md`** — the role scaffold; one page per role,
     structured on three axes: **what it owns** (the DRI outcome — one person,
     one outcome, no hiding), **why a human** (the judgment or expertise the
     models don't supply — hire for that, not throughput), **how it reshapes**
     (what the role becomes as orchestration of agents rather than direct
     production).

   The second-brain archetype adds nothing here — it uses the standard seed set
   with the default taxonomy.
4. **Config**: refresh `kb.toml` — `[kb]` description; `[scout]` `topics` and
   `watch` replaced with the new domain's (if `insight` was kept). Replace,
   never append to, the template's own values in `[lint]`
   `concept_candidate_terms` (3–5 terms likely to recur in this domain),
   `intentional_forward_links` (pages the user already knows they want, or
   empty) and, if media-capture was kept, `[snippet].glossary` (domain jargon
   ASR will get wrong, or empty).
5. **README**: rewrite `README.md` for the instance — what this KB is about,
   the three layers, the workflows and skills that survived the prune, and how
   to attach it over MCP if `mcp-server` was kept. Every path and command it
   names exists in the pruned tree.

Phase 4 is done when every file `find raw wiki decisions product architecture
staging images -type f 2>/dev/null` lists is one this phase wrote or emptied, a kept ADR,
or a `.gitkeep`.

## Phase 5 — Lint

Run `python3 scripts/lint.py` and fix every error (a fresh KB should also have
zero warnings). Run the tooling tests if pytest is available: `pytest scripts/`.

## Phase 6 — Cleanup

- Confirm with the user, then remove the machinery: `rm -rf .template/` and this
  skill's directory (`.agents/skills/onboard/`).
- Offer a fresh start: commit the onboarding as one commit, or re-init history
  (`rm -rf .git && git init`) for a clean slate.

## Phase 7 — Report

Summarize: identity, features kept/dropped, taxonomy, what was generated, and
the next steps (drop a first source into `raw/` and say "ingest"). Keep it short.

## Guardrails

- Read feature names from `python3 .template/onboard.py --list`; never hardcode.
- Always dry-run and show the plan before `--apply`.
- **The script owns feature pruning and renaming (never do it by hand); the skill owns
  interview, generation, and prose.**
- Everything you generate must pass `scripts/lint.py` — indexed, linked, logged.
