---
name: snippet
description: Carve the passages a user highlighted with ==marks== out of a transcript in raw/ into a structured clip file (Summary, Cleaned Transcript, Notes, Raw Transcript). Use when the user says "carve the highlights", "clip that transcript", or "/snippet <file>". Capture only — never ingests into the wiki.
---

# Carve highlights into a clip

The user has marked passages in a transcript (in `raw/`, usually from
`/transcript`) with Obsidian `==highlight==` syntax, and may have notes about
them in the conversation. You turn that into a structured clip file.

## Steps

1. Identify the source transcript (path in the user's message, or the most
   recently modified file in `raw/podcasts/`— confirm if ambiguous).
2. Run the helper:

   ```bash
   python3 .agents/skills/snippet/carve.py "raw/podcasts/<transcript>.md"
   ```

   It extracts every highlighted passage with its nearest `[MM:SS]` anchor and
   writes `<transcript> (Clip).md` beside the source with four sections:
   **Summary → Cleaned Transcript → Notes → Raw Transcript**. Raw is verbatim;
   Cleaned has the ASR-correction glossary from `kb.toml` `[snippet].glossary`
   already applied.
3. Now do your part in the clip file:
   - **Summary** — 2–4 sentences on why these passages were worth clipping.
   - **Cleaned Transcript** — polish lightly: fix remaining ASR errors, drop
     filler words, add punctuation. Keep meaning and phrasing; this is cleanup,
     not paraphrase. If you correct a *recurring* ASR error, add it to the
     glossary in `kb.toml` so future carves get it free.
   - **Notes** — the user's own commentary from the conversation, **verbatim**.
     If they gave none, delete the placeholder comment and leave the section empty.
4. Report the clip path and what you cleaned.

## Guardrails

- **Capture only.** The clip lives in `raw/`; never create or edit wiki pages
  here. Offer the Ingest workflow if the user wants it in the wiki.
- Never edit the source transcript itself (raw is immutable) — corrections go in
  the clip and the glossary.
- Glossary lives in `kb.toml [snippet]`, never hard-coded in the script.
