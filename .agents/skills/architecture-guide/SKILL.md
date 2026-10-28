---
name: architecture-guide
description: Write or update the architecture guide under architecture/ — one overview per kind (machinery, content) plus topic pages — and optionally render a topic with archify.
argument-hint: "[check | full | render <topic>]"
disable-model-invocation: true
---

The **architecture guide** lives in `architecture/`. It has two **kinds** of page, each with its own overview:

- `kind: machinery` — how this KB works: the loop, the layers, the write and read paths, lint. Its sources are `AGENTS.md`, `kb.toml`, `scripts/`, `mcp/`, and the skills. The overview is `The Machinery.md`.
- `kind: content` — what the wiki knows: how its pages and claims relate, one topic per cluster. Its sources are wiki pages and raw files. The overview is `The Knowledge Map.md`.

Each overview holds its kind's topic list; a **topic** (one way of looking at the subject, such as "the write path" or "the AI-native org cluster") is one page beside it. `diagrams/` holds rendered diagrams and is not a page. The reader is a developer who cloned this template: technical, new to LLM wikis, here to understand a closed-loop system well enough to run one. Every page follows [`page-template.md`](page-template.md), and every page is a wiki page: frontmatter, an `index.md` entry, wikilinks, `updated:` bumped on every edit, lint clean at the end of a run.

Read a page's `watches:` paths before writing or changing it, and write only what they show. A machinery page's reasons come from ADRs and `AGENTS.md`; a content page's claims come from the pages it maps and their raw sources, cited by wikilink. Where no reason or source is written down, say so.

## Pick the run

- A kind with no overview page: **first run** for that kind.
- Argument `check`: **find stale pages** (and stale diagrams), **find new entries**, report both, and stop.
- Argument `full`: rewrite every page in both topic lists from its sources, **find new entries**, then **report**.
- Argument `render <topic>`: re-render that topic's diagram by following [`archify.md`](archify.md), then stop. Nothing else is read or changed.
- Otherwise: **find stale pages**, **update** them, **find new entries**, then **report**.

The guide describes committed state: every comparison runs from a page's `commit:` to `HEAD`. When the working tree has uncommitted changes under a page's `watches:`, say in the report that they will be picked up once committed.

## First run

1. For machinery, read `AGENTS.md`, `kb.toml`, the ADRs, and the skills' `SKILL.md` files. For content, read `wiki/index.md` and `wiki/overview.md`, then the concept and synthesis pages, grouping them by tags and by which pages link each other most. Propose the overview and the few topics that carry the subject. For machinery, favor focuses inside the overview over topic pages: a focus becomes a page only when it outgrows a screen or needs its own diagram. For content, one topic per cluster.
2. Wait for the user to confirm or change the list.
3. Write the overview and each topic page, add each to `index.md`, and link both overviews from `Home.md`. Done when every confirmed topic has a page with all template sections and `commit:` and `watches:` set, and `python3 scripts/lint.py` passes.

## Find stale pages

```bash
python3 scripts/audit.py --architecture
```

For every page, overviews included, it diffs the page's `watches:` from its `commit:` to `HEAD`; a page is **stale** when any watched file changed or the commit no longer exists. A page whose Diagram section has a "Rendered with archify" link also has a rendered diagram, whose `candidate.json` records the commit it was drawn at in `meta.repository.revision`; the script runs the same diff from that commit, so a **stale diagram** is caught even when its page is current. It also lists uncommitted changes under each page's watches and, for each overview, the files added under its `new_entries:`.

Done when every page and every rendered diagram is marked stale or current, with the changed files listed for each stale one. A page the script marks `incomplete` (no `watches:`, or a git error) is reported as such, never as current.

## Update

For each stale page:

1. Read the diff of its changed files and the page.
2. Edit the sentences, diagram nodes, and explanation the change touches. Leave the rest of the page exactly as it is, so the page's own diff shows what changed in the subject. A content page whose mapped claim changed status cites the new source and updates "Where the tensions are".
3. Set `commit:` to `HEAD`'s commit and `updated:` to today, and add or drop `watches:` paths if the topic's files moved. A change that leaves the page's story intact still gets the new commit. An overview is the exception: edit its text here, but its `commit:` is set at the end of **find new entries**, since that step uses the old commit.

When any topic page changed, re-read its overview and fix whatever no longer matches it.

## Find new entries

Each overview's frontmatter has a `new_entries:` list of directories. Run `python3 scripts/audit.py --architecture`, unless this run already has its output; its `new under <overview>'s new_entries` lines list what was added there since the overview's commit.

For each addition (a new skill or script for machinery; a new concept, synthesis, or raw source for content), read enough to judge whether an existing page already explains it. A page listing the directory in `watches:` is not the same as explaining what was added. Report the ones no page explains as possible new topics, additions to an existing page, or, for machinery, a focus grown enough to become its own page.

Outside `check`, wait for the user's decision on each, then set the overview's `commit:` to `HEAD`'s so settled entries are not raised again. Adding or removing a page is the user's call.

## Report

List each page touched, the changed files that triggered it, and one line on what you edited. List current pages as a count, then any new entries and what was decided. List each stale diagram with the files that made it stale. Run `python3 scripts/lint.py` and fix what it reports. Append an `architecture |` entry to `wiki/log.md` naming the pages touched. Then offer to render: each stale diagram, and any topic with no rendering yet. For each the user accepts, follow [`archify.md`](archify.md). A declined stale diagram stays stale and is listed again next run; `render <topic>` picks it up later.
