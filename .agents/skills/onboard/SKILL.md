---
name: onboard
description: Turn this MycoForge template clone into your own knowledge base — interview for domain, identity, features, and page-type taxonomy; run the deterministic prune+rename; generate the seed pages; verify with lint. Use when starting a new KB from this template, or when the user says "onboard", "set up this KB", or "make this mine".
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
2. Run `python3 .template/onboard.py --list` to see the cuttable features
   (currently `product`, `orchestrator`, `media-capture`, `insight`,
   `mcp-server` — all independent). Read `.template/README.md` if you need the
   marker/prune details.
3. Confirm git state is clean (or warn the user) so onboarding is a reviewable diff.

## Phase 1 — Interview

Use **AskUserQuestion** for the discrete choices; ask free-text items
conversationally. Skip anything the user already answered.

1. **Archetype** (AskUserQuestion, single-select) — the first question:
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
4. **Feature keep-set** (AskUserQuestion, multi-select — one per feature, read
   from `--list`; with an archetype, present the preset's `keep` list as the
   pre-selected answer and ask its `optional` features individually):
   - `product` — spec pages, decisions/ADRs, roadmap, Home dashboard. Keep if
     this KB feeds software or accumulates formal decisions.
   - `orchestrator` — children manifest, routing workflow, child-aware lint.
     Keep only for a parent KB with nested child KBs.
   - `media-capture` — `/transcript` + `/snippet` for podcast/video sources.
   - `insight` — `/research` (web source discovery into `raw/`) + `/connect`
     (novel-connection syntheses). Keep for KBs that grow by exploration.
   - `mcp-server` — read-only search/read/index for other repos' agent sessions.
5. **Page-type taxonomy** (AskUserQuestion): propose domain-appropriate types —
   `concepts/people/syntheses` for a research KB, `books/authors/themes` for a
   reading library, `projects/experiments/notes` for a lab KB — plus "keep the
   default". The chosen types become the `wiki/` subfolders and the `type:`
   values in the frontmatter schema. Archetype pre-fills: second-brain proposes
   the default `concepts/people/syntheses`; playbook proposes
   `concepts/decisions/playbooks/roles` (decision pages live in the `product`
   feature's top-level `decisions/`; `playbooks/` and `roles/` are `wiki/`
   subfolders).

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
2. **Wiki reset**: delete the example wiki pages (`wiki/concepts/`, `wiki/people/`,
   `wiki/syntheses/` contents), the example raw source in `raw/articles/`, and —
   if `product` was kept — the example ADRs in `decisions/` and the example page
   in `product/software/`. Create the taxonomy's empty subfolders.
3. **Seed pages**: fresh `wiki/overview.md` (domain, purpose, where to start),
   `wiki/index.md` (empty catalog with the taxonomy's sections), `wiki/log.md`
   (one genuine `schema |` entry recording the onboarding), and — if `product`
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
4. **Config**: refresh `kb.toml` — `[kb]` description; `[lint]`
   `concept_candidate_terms` seeded with 3–5 terms likely to recur in this
   domain; `intentional_forward_links` for pages the user already knows they
   want; `[snippet].glossary` starters (domain jargon ASR will get wrong) if
   media-capture was kept.

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
- **The script owns pruning and renaming (never do it by hand); the skill owns
  interview, generation, and prose.**
- Everything you generate must pass `scripts/lint.py` — indexed, linked, logged.
