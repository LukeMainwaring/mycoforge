---
name: audit
description: Health report on the KB (lint, vendored-skill drift, stale architecture pages, fresh sources) ending in what to do next. Reports only.
argument-hint: "[quick]"
disable-model-invocation: true
---

# Audit the KB

One report on the KB's health. The numbers come from `scripts/audit.py`, pasted
exactly as printed; your part is the summary and the next moves. Audit
**reports**: its one write is the run section `/scout` appends to
`staging/scout.md`. Each fix is its own workflow, started by the user.

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
   `/scout` run with the user. Then:

   ```bash
   python3 scripts/audit.py --scout
   ```

   and add that output, exactly as printed, after the first.
<!-- sf:end(insight) -->
3. **Report** in the format below. Done when every part that ran has its
   output in the block and every part that found something has a move.

## Report

```text
Audit YYYY-MM-DD

<script output, verbatim>

<two or three lines: what changed since the KB was last healthy, what matters most>

Your move:
- <one line per part that found something>
```

The moves, one per part that found something:

- lint errors or warnings: run Lint.
- `Changed since pin` or `New upstream skills`: run `/sync-skills`.
- stale architecture pages or new entries: run `/architecture-guide`; a stale diagram alone: `/architecture-guide render <topic>`. <!-- sf:keep-if(architecture) -->
- new scout candidates: list each as a clickable link, then mark rows `approved` or `rejected` in `staging/scout.md`; the next `/scout` captures approved rows. Name each unreachable entry. <!-- sf:keep-if(insight) -->
- `approved` rows awaiting capture: run `/scout`. <!-- sf:keep-if(insight) -->

When no part found anything, the whole report is one line:
`Audit YYYY-MM-DD: all clear`, followed by the script's summary lines.

The summary interprets the block and quotes its numbers as printed. Leave the
working tree as you found it apart from the ledger section; the user reviews and
commits it.

## Scheduling (draft)

Manual only for now. A scheduled audit posting this report to a channel such as
Slack starts as its own ADR, per ADR-012 (`decisions/ADR-012 No Scheduled
Capture Without a Decision.md`): what the run may write, what it must never
touch, and what enforces that beyond this file (harness permissions, a spend
cap). ADR-017 (`decisions/ADR-017 Audit Reports, Never Edits.md`) is its
starting point.
