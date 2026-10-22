# Capture rules for raw/

How a web source becomes a file in `raw/`. Shared by `/research` and `/scout`;
this file is the single source of truth, so edit it here rather than in either
skill.

## Where

- Articles, blog posts, release notes, repo snapshots → `raw/articles/`
- Papers → `raw/papers/`
- Transcripts belong to `/transcript`, not here.

## Filename

`YYYY-MM-DD <Title>.md` — the **publication** date if known, else the retrieval
date. Repos take the retrieval date. Never use `[ ] # ^ | : / \` in the name;
parentheses, hyphens, apostrophes, and spaces are fine.

## Frontmatter

Every file carries, in this order:

```yaml
---
type: article          # article | paper | repo
title:
author:                # person or org
published: YYYY-MM-DD
updated: YYYY-MM-DD    # only when the page shows a later revision date
retrieved: YYYY-MM-DD
url:
access: full           # full | partial — partial when the body is a summary/abstract only
---
```

`type: repo` adds, after `url`:

```yaml
commit:       # full sha the snapshot was taken at
last_commit: YYYY-MM-DD
stars:
license:
```

Provenance is mandatory: a raw file without `url` and dates is a future mystery.

## Body

The source converted to clean markdown. For a repo, the README at `commit`
followed by a `## Repo notes` section: what it does in two lines, how active it
is, and anything the README hides (architecture docs worth reading, license
caveats). If the full text isn't reachable (paywall, login), save the
abstract or summary you can reach plus the link, and set `access: partial`.

## Done when

Each approved source is one file under `raw/` with every frontmatter field above
filled or deliberately omitted, and nothing under `wiki/` has changed.
