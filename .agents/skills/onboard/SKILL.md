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
   (currently `product`, `orchestrator`, `media-capture`, `mcp-server` — all
   independent). Read `.template/README.md` if you need the marker/prune details.
3. Confirm git state is clean (or warn the user) so onboarding is a reviewable diff.

## Phase 1 — Interview

Use **AskUserQuestion** for the discrete choices; ask free-text items
conversationally. Skip anything the user already answered.

1. **Domain + purpose** (free text): what is this KB about, and what feeds it —
   papers? articles? podcasts? a book? Use the answer everywhere below.
2. **Identity** (free text): slug (lowercase, `^[a-z][a-z0-9_]*$`) and display
   brand. Offer defaults derived from the domain; validate the slug.
3. **Feature keep-set** (AskUserQuestion, multi-select — one per feature, read
   from `--list`):
   - `product` — spec pages, decisions/ADRs, roadmap, Home dashboard. Keep if
     this KB feeds software or accumulates formal decisions.
   - `orchestrator` — children manifest, routing workflow, child-aware lint.
     Keep only for a parent KB with nested child KBs.
   - `media-capture` — `/transcript` + `/snippet` for podcast/video sources.
   - `mcp-server` — read-only search/read/index for other repos' agent sessions.
4. **Page-type taxonomy** (AskUserQuestion): propose domain-appropriate types —
   `concepts/people/syntheses` for a research KB, `books/authors/themes` for a
   reading library, `projects/experiments/notes` for a lab KB — plus "keep the
   default". The chosen types become the `wiki/` subfolders and the `type:`
   values in the frontmatter schema.

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
