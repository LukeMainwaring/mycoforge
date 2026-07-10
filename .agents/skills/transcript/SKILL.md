---
name: transcript
description: Fetch a YouTube or podcast transcript into raw/podcasts/ as a dated markdown file with timestamp anchors. Use when the user shares a video/podcast URL, or says "grab this podcast", "get the transcript", or "/transcript <url>". Capture only — never ingests into the wiki.
---

# Fetch a transcript into raw/

You are capturing a spoken-word source into this knowledge base's immutable raw
layer. The helper script does the mechanical work; you run it and report.

## Steps

1. Get the URL from the user (it's usually in their message). Anything yt-dlp
   understands is fine.
2. Run the helper:

   ```bash
   python3 .agents/skills/transcript/fetch.py "<url>"
   ```

   It fetches metadata + English (auto-)subtitles via yt-dlp and writes
   `raw/podcasts/YYYY-MM-DD <Title>.md` — publication-dated name, source
   frontmatter (title, channel, published, retrieved, url, duration), and the
   transcript as paragraphs anchored with `[MM:SS]` timestamps.
3. Report the file path and a one-line description of what was captured.

## Guardrails

- **Capture only.** This skill populates `raw/` and never creates or edits wiki
  pages. If the user wants the source *ingested*, that's the separate Ingest
  workflow in `AGENTS.md` — offer it, don't assume it.
- Don't edit the transcript content by hand; it's now an immutable raw source.
  (ASR errors get corrected later, at carve time, by `/snippet`'s glossary.)
- If yt-dlp is missing, tell the user to install it (`brew install yt-dlp` or
  `pipx install yt-dlp`) rather than improvising another fetch path.
