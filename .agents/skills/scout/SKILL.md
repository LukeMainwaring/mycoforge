---
name: scout
description: Standing watch for fresh sources on the KB's own topics. Searches the watch list and topics in kb.toml, stages candidates in staging/scout.md for review, captures only what the user approves. Capture only.
argument-hint: "[<N>d lookback override, e.g. 30d]"
disable-model-invocation: true
---

# Scout fresh sources into raw/

`/research` answers a question once. `/scout` asks the same question every run:
*what's new on the KB's own topics since last time?* Everything it needs is in
`kb.toml` `[scout]`; every run leaves a record in `staging/scout.md`, the
**ledger**. The ledger is the review stage, the skip list, and the "since when"
all at once, so there is no other state.

Capture only: this skill writes to `staging/scout.md`, `staging/ingest.md`
and `raw/`. It never touches `kb.toml`, `wiki/`, the index, or the log, and it
never commits. `kb.toml` is the user's: changes to it are proposed in the
ledger and the user applies them.

## Steps

1. **Set the window.** Read `[scout]` from `kb.toml` and the ledger. The window
   starts at the most recent `## [date]` run header in the ledger; on a first run,
   or when the user passed `<N>d`, it starts `lookback_days` / `N` days ago.
   A `watch` entry listed as `unreachable` in the latest run keeps its
   window open: for that entry alone, start at the most recent run header
   that does not list it. State the window in one line before searching,
   naming any entry with a longer window.

2. **Build the skip set.** From `raw/`: every filename and every `url:` in
   frontmatter. From the wiki: every `sources:` entry in `wiki/` frontmatter.
   From the ledger: every `captured` and `rejected` row, unless the source
   shows an update later than the row's run date. For a repo or a rolling page,
   "an update" means one that would change what the wiki says (a release, an
   architecture change), not commit count; a re-capture lands as a new dated
   snapshot, never an overwrite of the earlier raw file.

3. **Fan out.** Launch one background sub-agent per `watch` entry and one per
   `topics` entry, in parallel up to whatever concurrency the harness allows
   (queue the rest), each briefed with: the window, the freshness
   rules below, the skip set, and the KB description from `kb.toml` `[kb]`. Each
   returns at most three candidates as `url · title · kind · date · one line on
   what it adds that the wiki lacks`, plus any site or org it kept hitting that
   is not in `watch`. A sub-agent that could not read its `watch` entry (fetch
   failed, blocked, feed empty where it never is) returns `unreachable` with
   one line on what it saw, never an empty candidate list: an empty list
   means the source was read and had nothing new. Fresh means:
   - article / post / podcast: published or visibly updated within
     `max_age_days`
   - repo: a commit within `repo_active_days` and a real cadence, not one
     drive-by commit
   - anything older appears only as an explicit **evergreen** exception with a
     one-line reason
   Freshness is a filter, not a tiebreaker: stale candidates are dropped, not
   demoted.

4. **Merge and stage.** Dedupe across agents, drop anything in the skip set,
   rank by what it adds to the wiki, and keep **at most five**. Append a run
   section to the ledger (format below) with every kept candidate as a
   `candidate` row, and list any `candidate` rows still open from earlier runs
   under a `still awaiting review` line rather than searching them again.
   Entries that came back `unreachable` go on an `unreachable:` line under
   the run header, with the sub-agent's reason; their window stays open for
   the next run (step 1). Zero new candidates is a normal result: write the
   run header with `nothing new` and say so, but a run with unreachable
   entries is never `nothing new`, it is `nothing new from what was read`.
   Then stop and point the user at the ledger, with the candidates listed in
   conversation as clickable links and the unreachable entries named. Done
   when the user has answered, by editing status cells or by replying.

5. **Capture approved rows** following
   [`../research/capture.md`](../research/capture.md), including any
   `approved` rows left in earlier runs (an `/audit` run stages but never
   captures). Set each row to `captured` with its `raw/` path. Only a row the user explicitly declined
   becomes `rejected`; rows they didn't mention stay `candidate` and carry
   forward to the next run. If the
   sub-agents reported watch candidates, write them under a `proposed watch`
   line in the run section as ready-to-paste `{ url = …, why = … }` rows. The
   user pastes the ones they want into `[scout].watch` in `kb.toml`; the skill
   does not edit `kb.toml`. Each row ends in a status cell: `proposed`, which
   the user changes to `added` after pasting or `declined`; the next run
   also treats a URL already in `[scout].watch` as `added`. Only `proposed`
   rows carry forward, listed once under the next run's `proposed watch`.

6. **Hand off.** Append each captured source to `staging/ingest.md` as an
   unticked row, in the order you would ingest them, with one line on what to
   look out for. List what landed in `raw/`, then offer the Ingest workflow,
   one source per session. Do not ingest here.

## Ledger format

`staging/scout.md` is append-only at the run level (most recent run at the
bottom); status cells inside a run are edited in place:

```markdown
## [2026-10-22] window 2026-07-24 → 2026-10-22

| # | source | date | kind | adds | status |
|---|--------|------|------|------|--------|
| 1 | [Title](https://…) | 2026-10-18 | article | what the wiki lacks, one line | candidate |
| 2 | [org/repo](https://github.com/…) | 2026-10-20 | repo | … | captured → raw/articles/2026-10-22 Title.md |

unreachable: https://example.com/blog (fetch timed out twice); window stays open from 2026-07-24

proposed watch:
- `{ url = "https://example.org/notes", why = "turned up in two topic searches; posts on agent memory" }` · proposed
```

Statuses: `candidate` → `approved` → `captured → <raw path>`, or `rejected`.
Plain markdown links only, never wikilinks, so lint leaves the ledger alone.

## Guardrails

- The ledger is the only memory between runs. If it disagrees with the
  conversation, the ledger wins.
- A source that could not be read is reported as unreadable, never as a
  quiet source. Its bookmark does not move.
- `kb.toml` is read, never written. Proposals go in the ledger.
- Quality over volume: a run that stages two strong candidates beats one that
  stages five thin ones.
- A sub-agent reports; it never writes to `raw/`, the ledger, or `kb.toml`.
