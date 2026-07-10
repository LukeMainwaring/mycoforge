---
name: research
description: Deep-research a topic and land vetted web sources in raw/ with proper dated naming and provenance frontmatter. Use when the user says "research <topic>", "find sources on", "go deep on", or "/research <topic>". Capture only — sourcing ends where ingest begins.
---

# Research a topic into raw/

You are the sourcing arm of this knowledge base: turn a question into a small,
vetted set of raw sources, saved with full provenance. This closes the loop the
other capture skills leave open — `/transcript` and `/snippet` capture what the
user already found; this skill finds.

## Steps

1. **Scope the question.** Restate the research question in one sentence and, if
   the KB already covers adjacent ground, check `wiki/index.md` and skim the
   relevant pages first — the goal is sources that *add* to the wiki, not
   re-cover it. Confirm scope with the user if it's ambiguous.
2. **Search broadly.** Use whatever web search and page-fetch capability your
   harness provides. Cast wide first (surveys, primary sources, contrarian
   takes), then go deep on the strongest threads. Prefer primary sources and
   named authors over aggregators; note publication dates.
3. **Vet and shortlist.** Present 3–7 candidates in conversation, one line each:
   what it is, why it earns a place in `raw/`, and what it would add that the
   wiki lacks. Let the user cut the list.
4. **Capture the approved sources.** For each, save a markdown copy into the
   right `raw/` subfolder (`articles/`, `papers/`) following the schema's
   conventions:
   - filename `YYYY-MM-DD <Title>.md` — publication date if known, else
     retrieval date; never use `[ ] # ^ | : / \` in the name
   - frontmatter: `type` (article/paper), `title`, `author`, `published`,
     `retrieved`, `url`
   - body: the source content converted to clean markdown. If the full text
     isn't accessible (paywall, login), save the abstract/summary you *can*
     access plus the link, and say so in the frontmatter (`access: partial`).
5. **Report and hand off.** List what landed in `raw/`, then offer the Ingest
   workflow — **one source per session**, per the schema. Do not ingest as part
   of this skill.

## Guardrails

- **Capture only.** This skill populates `raw/` and never creates or edits wiki
  pages, the index, or the log. Ingestion is a separate, deliberate step.
- Provenance frontmatter is mandatory — a raw file without `url` and dates is a
  future mystery.
- Quality over volume: a run that lands two strong sources beats one that lands
  ten thin ones. Never pad the shortlist.
- If the user's question is really a *query against existing knowledge*, say so
  and run the Query workflow instead of fetching the web.
