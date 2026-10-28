---
name: audit
description: Health report across the KB's checks, ending in what to do next. Reports only.
argument-hint: "[quick]"
disable-model-invocation: true
---

# Audit the KB

One report on the KB's health. The numbers come from `scripts/audit.py`, pasted
exactly as printed; your part is the summary and the next moves. Audit
**reports**: the working tree ends as it started, and each fix is its own
workflow, started by the user.
<!-- sf:begin(insight) -->
The one exception is the run section `/scout` appends to `staging/scout.md`;
the user reviews and commits it.
<!-- sf:end(insight) -->

## Steps

1. **Run the checks.**

   ```bash
   python3 scripts/audit.py
   ```

   Keep the output exactly as printed. A part that failed to run (the
   vendored check needs the network) stays in the report with its error.
<!-- sf:begin(insight) -->
2. **Stage fresh sources**, unless the argument is `quick`. Follow
   [`/scout`](../scout/SKILL.md) steps 1–4, and stop once the run section is
   appended to the ledger: capture and `staging/ingest.md` belong to a later
   `/scout` run with the user.
3. **Read the ledger**, with or without `quick`:

   ```bash
   python3 scripts/audit.py --scout
   ```

   and add that output, exactly as printed, after the first.
<!-- sf:end(insight) -->
4. **Report** in the format below. Done when every part that ran has its
   output in the block and every part that found something has a move.

## Report

```text
Audit YYYY-MM-DD

<script output, verbatim>

<two or three lines interpreting the findings above: which matter most and why>

Your move:
- <one line per part that found something>
```

The moves, one per part that found something:

- lint errors or warnings: run Lint.
- `Changed since pin` or `New upstream skills`: run `/sync-skills`.
- a part that failed, crashed, or printed `incomplete`: name it and its error; the user decides whether to rerun.
- stale architecture pages or new entries: run `/architecture-guide`; a stale diagram alone: `/architecture-guide render <topic>`. <!-- sf:keep-if(architecture) -->
- new scout candidates: list each as a clickable link; the user marks rows `approved` or `rejected` in `staging/scout.md`, and the next `/scout` captures approved rows. Name each unreachable entry. <!-- sf:keep-if(insight) -->
- `approved` rows awaiting capture: run `/scout`. <!-- sf:keep-if(insight) -->

When every part ran to completion and none found anything, the report is
`Audit YYYY-MM-DD: all clear` followed by the script output, verbatim.

The summary quotes the block's numbers as printed.

## Scheduling (draft)

Manual only for now. A scheduled audit posting this report to a channel such as
Slack starts as its own ADR, per ADR-012 (`decisions/ADR-012 No Scheduled
Capture Without a Decision.md`): what the run may write, what it must never
touch, and what enforces that beyond this file (harness permissions, a spend
cap). ADR-017 (`decisions/ADR-017 Audit Reports, Never Edits.md`) is its
starting point.
