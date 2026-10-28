# Page template

Each section stays within about one screen: a page is something to study. A page is a wiki page first: Title Case filename, frontmatter, wikilinks to the pages and sources it rests on.

## Frontmatter

```yaml
---
type: architecture
kind: machinery          # machinery | content
created: 2026-10-28
updated: 2026-10-28
commit: abc1234          # full or short sha the page was written at
watches:                 # repo paths the page rests on; `check` diffs commit..HEAD over these
  - scripts/lint.py
  - .agents/skills/research
related:                 # wikilinks to wiki pages the text cites
  - "[[Three-Layer Architecture]]"
tags: [architecture, machinery]
---
```

An overview adds `new_entries:`, the directories where an addition may mean a new topic (for machinery: `.agents/skills`, `scripts`, `mcp`; for content: `wiki/concepts`, `wiki/syntheses`, `raw`). A content page lists the raw files behind its claims under `raw:` as every wiki page does, and lint checks the paths.

## Topic page

````markdown
# <Topic>

## Summary

Two or three sentences: what this is and the one idea to remember.

## Diagram

```mermaid
<one diagram>
```

## How it works

Short prose on the main pieces and how they connect. Machinery: name files and
skills so the reader can find them; leave the line-by-line to the code.
Content: name the pages, by wikilink, and the claims that hold the cluster
together.

## Why it's built this way          ← machinery pages only

The trade-offs behind the shape, each linked to the ADR or `AGENTS.md`
section that states it.

## Where the tensions are            ← content pages only

Which claims in the cluster are contested or speculative, which pages pull
against each other, and what source or question would settle each.

## How to explain this

**In a few sentences:**

> First person, as you would say it to a colleague. Four or five plain
> sentences, one idea each, starting from what it does for its user.

**Likely follow-ups:**

- **<A question a colleague would plausibly ask>** One-sentence answer.
- at most three of these
````

### Diagram

When the topic has a rendered diagram, one line after the Mermaid block links it: `Rendered with archify: [diagrams/<slug>](diagrams/<slug>/<slug>.html) (open from a local checkout).`

Pick the Mermaid type from the topic: `sequenceDiagram` for a path a thing takes, `flowchart` for structure, data movement, or a map of related pages, `stateDiagram-v2` for phases. Keep it to what the summary claims, around fifteen nodes at most, with a verb on every arrow. A detail that needs a second diagram belongs in its own topic.

### Watches

List the files the page's claims rest on, repo-relative. Prefer a directory when the topic covers everything in it, so new files there mark the page stale. For a content page, watch the mapped wiki pages and the raw files they cite. Cite a broad document such as `AGENTS.md` in the prose only: it changes for unrelated reasons and would mark the page stale each time.

## Overview page

An overview uses the same sections with three differences:

- After the summary, a **Topics** section: one line per topic, linking its page and saying what question it answers. This list is the topic list the skill reads. The machinery overview may instead carry its subject as **focuses**, one H3 each under "How it works", and its Topics section then says that a focus becomes a page when it outgrows a screen or needs its own diagram.
- It states only what its own `watches:` or a topic page support, and leaves counts and other incidental details to the topic pages. Its `watches:` are the few files that change when the subject's shape changes, so ordinary work leaves the overview current.
- Its frontmatter carries `new_entries:`.
