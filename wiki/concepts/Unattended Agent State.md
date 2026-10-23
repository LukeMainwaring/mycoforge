---
type: concept
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-10-08 Building Effective Agent Automations (Anthropic)]]"
raw:
  - raw/articles/2026-10-08 Building Effective Agent Automations (Anthropic).md
related:
  - "[[Belief Ledger]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Ingest Workflow]]"
  - "[[Three-Layer Architecture]]"
  - "[[Lance Martin]]"
  - "[[CJ Avilla]]"
confidence: medium
tags: [memory, workflow, guardrails]
---

# Unattended Agent State

The memory discipline for an agent that runs on a schedule with nobody
watching, from Anthropic's daily-brief reference implementation
([[2026-10-08 Building Effective Agent Automations (Anthropic)]]). Each run
"starts in a fresh sandbox with no memory of the last one", so everything the
agent carries between runs is files; four of the article's six rules are
about which files, who may write them, and when, and the other two are a
live re-check before posting and read-only access with a spending cap. It is
the closest published
sibling to this KB's `/scout` ledger, and the pattern an LLM wiki would need
before any of its capture ran on a timer.

## Two stores, two writers

The agent mounts two folders. **Preferences** belong to the reader and are
read-only to the agent: which sources to read, what to leave out, the length
cap, the destination, when to stop. **State** belongs to the agent and is
read-write: a bookmark per source, a ledger of what it has reported, one
record per run, changes it proposes to the preferences, and notes on how each
source behaves ("returns only the newest 50 items"). The split is enforced by
the platform, not by instruction, and the agent re-reads the preferences file
at the start of every run; a copy baked into the prompt "keeps applying rules
you've already changed". If it cannot read the file it stops and says so
instead of running on defaults. Proposed preference changes go into state for
the reader to accept, so the agent's learning about the reader never
rewrites the reader's rules directly.

This is the [[Three-Layer Architecture]] ownership boundary applied to a
different object: the reader owns the rules, the agent owns the working
record, and the thing the agent learns about the rules is filed as a
proposal. `/scout` already has the shape. `kb.toml` `[scout]` is the
preferences store, re-read every run; `staging/scout.md` is the state store,
and its run header is the bookmark. Until 2026-10-23 one thing leaked:
`/scout` appended approved `watch` entries to `kb.toml` itself, with the
user's approval in conversation; it now writes `proposed watch` rows in the
ledger and the user pastes them. The remaining difference is the source's
"from a store the agent can't edit": here `kb.toml` is read-only by
instruction, not by the harness.

## Bookmarks, not windows

> [!claim] A scheduled reader should read each source from a per-source bookmark, never from a fixed time window
> confidence: medium · status: supported
> evidence: "A common mistake is asking the agent to read a fixed window like
> 'the last 24 hours.' A late run leaves a gap and an early run repeats
> items." The bookmark is the timestamp of the newest item read per source,
> written at the end of each run, so the next window "stretches or shrinks
> to cover everything since the last run" —
> [[2026-10-08 Building Effective Agent Automations (Anthropic)]]. A
> reasoned rule from one reference implementation, no measurement; medium.

A bookmark only moves when the read succeeded and the output landed. When a
source fails (an MCP server down, an expired token), the run still starts
without that source's tools and the agent sees nothing from it. The rule:
keep that source's bookmark where it is, write the brief from the others, and
end with one line naming what could not be read ("pull requests unavailable
this run"). Otherwise a failed read is reported as a quiet day. `/scout`'s
fan-out lacked this rule until 2026-10-23: a sub-agent that could not reach
its `watch` entry returned no candidates, and the merge step could not tell
that from nothing new. It now returns `unreachable` and the run header
carries it. Scout's bookmark is still the run date, not the newest item
read per source, so a source that returns a bounded page is not necessarily
read in full.

## The ledger and the run record

The **ledger** holds one line per item ever reported: when it was reported,
where it came from, an id that does not change (a Slack message timestamp, a
pull request number) and its last known status, which is updated in place as
an open item is carried forward; the source never calls it append-only. It is what
stops the brief repeating itself and what lets an open item be carried as
one marked line ("still waiting, day 3") rather than re-reported. The **run
record** (`runs/<date>.md`) is the per-run state machine: "posting" before
the post, then "posted" with the message id, or "maybe posted".

This ledger is a different object from gbrain's [[Belief Ledger]]. gbrain
records what the brain *believes* and when it came to believe it; this one
records what the agent *told the reader* and when. Both key on a stable id
the source supplies and both are the working memory the next run reads
first. The scout ledger is the second kind: runs append, status cells change
in place, and the skill treats it as "the only memory between runs."

## Verify, then confirm, then record

Two rules order the end of a run. Before posting, every item is re-checked
against its live source: resolved since the read, drop it; changed, fix the
line; cannot confirm, drop it and list it in the run record's cuts. "One
stale 'still waiting on you' costs more trust than ten missing items, so
never hedge an item's status: assert it or drop it." Links are copied from
the source's own link field, never assembled by hand. Then the post counts as
sent only when Slack returns `"ok": true` and a message timestamp, the agent
has first checked that today's edition is not already in the channel, and the
ledger and bookmarks move only after that confirmation. An unclear result is
marked "maybe posted" and nothing else changes, so a lost post costs a
duplicate at worst, never a silently skipped item.

> [!claim] Recording an output before it is confirmed loses items silently; recording it only after confirmation costs at most a duplicate
> confidence: medium · status: supported
> evidence: "If the agent records a post that never landed, the bookmarks
> move on and those items are never reported. If it posts again because it
> isn't sure the first post landed, readers get the same brief twice" —
> [[2026-10-08 Building Effective Agent Automations (Anthropic)]]. The
> asymmetry is argued, not measured, and the duplicate is bounded by the
> "already posted" check.

## Guardrails for a run nobody is watching

The sources are text other people wrote, which "can be interpreted as
instructions", so the limit is on what following them could do: the GitHub
token and the preferences store are read-only, the sandbox reaches only
allowlisted hosts, and the authors concede that a planted instruction "can
still change what the brief says, including through the notes the agent
keeps between runs". That last clause names the exposure of any agent whose
memory is files it writes itself. A per-run spending cap starts at three to
five times a normal run and tightens with real numbers; a run that hits it
pauses rather than fails, so "a cap set too low looks like a brief that went
quiet", the same silent-failure shape as the unread source. Where these sit
in the control model is in
[[Advisory and Deterministic Controls#Unattended runs]].

## Relation to this KB

> [!claim] A scheduled `/scout` would need the failed-read rule and a proposals file before the schedule, not after
> confidence: medium · status: speculative
> evidence: this KB's inference, written when `/scout` lacked both. Premises
> at the time: scout resembled four of the six rules in shape (a window from
> the last run header, the ledger as the only state, `kb.toml` re-read each
> run and unwritten by instruction, capture only after the user confirms),
> and lacked a way to tell an unreachable `watch` entry from nothing new and
> a proposals path for its own `watch` additions —
> [[2026-10-08 Building Effective Agent Automations (Anthropic)]]. Both were
> added on 2026-10-23 (log, `schema |` entry), which leaves the claim's
> necessity half untested rather than confirmed: nothing is scheduled.
> Confirm: a scheduled run before these rules that reports "nothing new" on
> a window where a watch site was down. Refute: a scheduled run that holds
> quality without them.

What a schedule would still lack, in the source's terms: a bookmark that is
the newest item read per source rather than the run date, a re-check of
carried-forward candidates before they are shown again, a spend cap, and
limits enforced by the harness rather than by SKILL.md prose. Whether any of
that is ever built is [[ADR-012 No Scheduled Capture Without a Decision]].
