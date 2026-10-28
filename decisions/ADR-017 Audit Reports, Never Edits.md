---
type: decision
status: accepted
created: 2026-10-28
updated: 2026-10-28
sources:
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-08 Building Effective Agent Automations (Anthropic)]]"
raw:
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md
related:
  - "[[ADR-012 No Scheduled Capture Without a Decision]]"
  - "[[ADR-014 The Wiki Does Not Edit Skills]]"
  - "[[ADR-016 Architecture Guide for Machinery and Content]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Unattended Agent State]]"
tags: [adr, schema, skills, audit]
---

# ADR-017 Audit Reports, Never Edits

## Context

The KB's health checks are scattered: `scripts/lint.py`, the vendored-skill
check behind `/sync-skills`, `/architecture-guide check`, and `/scout`. Each
is run when someone remembers it. One umbrella run, eventually on a timer and
posting to a channel, is the obvious next step, and
[[ADR-012 No Scheduled Capture Without a Decision]] says the timer needs its
own ADR first.

The WikiSkill ingest (2026-10-23) left three constraints for that umbrella.
WikiSkill gates skill changes on a validation score; this KB has none, so a
run cannot judge its own proposals. The agent being audited should not write
the numbers it is judged by. And skill→wiki provenance, if ever wanted,
belongs in the harness, not inside each skill
([[ADR-014 The Wiki Does Not Edit Skills]]).

## Decision

A manual, user-invoked `/audit [quick]` skill backed by `scripts/audit.py`.

- **Reports, never edits.** Its one write is the run section `/scout` step 4
  appends to `staging/scout.md`, which is scout's bookmark: without it the
  window never moves. It never touches `wiki/`, `raw/`, `kb.toml`,
  `architecture/`, the skills or the log, and never commits. Each finding
  ends in a move naming the workflow that fixes it; the user starts it.
- **The script writes the numbers.** `audit.py` prints lint output, the
  vendored-skill check, architecture staleness, and the scout ledger's
  latest run with counts. The skill pastes that verbatim and writes only the
  summary and the moves.
- **One staleness check.** `/architecture-guide`'s stale-page and
  new-entries steps call `audit.py --architecture` rather than running the
  git diffs by hand, so the two cannot drift.
- **Capture stays with `/scout`.** Audit stages candidates and stops; `/scout`
  step 5 now also captures `approved` rows left from earlier runs.
- **`quick`** skips scout's search, the only part that spends sub-agents;
  the ledger is still read, so open and approved rows are still reported.
- **Incomplete is not current.** A check that could not run (a git error,
  a page with no `watches:`, a crashed part) is reported as such; the
  report is "all clear" only when every part ran.
- **Trunk, with marked parts.** Audit survives every onboarding cut; its
  scout steps carry `insight` markers and the architecture check carries
  `architecture` markers.

## Consequences

- One command answers "is the KB healthy", with numbers no summary can
  round off.
- A manual audit leaves an uncommitted ledger section for the user.
- `/architecture-guide` now depends on a trunk script, so a copy ported to
  another repo needs `audit.py` or its old inline diff.
- The scheduling ADR starts from a run whose write boundary is already one
  file.

## Alternatives

- **Audit fixes what it finds**: rejected. With no validation score, nothing
  but the user can accept a fix.
- **Agent runs the checks and reports the counts**: rejected. It is the
  agent being judged writing its own record.
- **Audit writes nothing, scout results only in the report**: rejected. The
  ledger would never advance, so every run would re-find the same candidates.
- **Skill→wiki provenance table now**: deferred. If added, it is a `kb.toml`
  table plus a lint check, which audit then reports with no change here.
- **Schedule and post to Slack in this change**: deferred to the ADR that
  ADR-012 requires.

## Implemented

2026-10-28, same PR: `.agents/skills/audit/`, `scripts/audit.py` with
`scripts/test_audit.py`, the `/scout` step 5 sentence, the
`/architecture-guide` steps, and the `/audit` row in `AGENTS.md`.
