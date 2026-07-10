---
name: snippet
description: Carve podcast snippets from Obsidian ==highlights== in a full-episode transcript, or regenerate the Summary + Cleaned Transcript of an existing snippet. Operates on raw/podcasts/ files; reads the [MM:SS] anchors emitted by /transcript to compute clip ranges.
---

# /snippet

Take a full podcast episode marked up with Obsidian `==highlights==` and turn each highlight into its own structured snippet file in `raw/podcasts/`. Or, run on an existing snippet to regenerate its Summary and Cleaned Transcript while preserving your Notes verbatim.

This skill complements `/transcript`. The intended end-to-end flow:

1. `/transcript <url>` — fetch the full episode (anchors emitted automatically).
2. Read the file in Obsidian; mark interesting passages with `==highlight==` (Cmd+Shift+H wraps the current selection).
3. `/snippet <path-to-full-episode.md>` — carve and process all highlights in one shot.

## Usage

- `/snippet <path>` — carve mode (full-episode input) or regen mode (snippet input). Mode is auto-detected from frontmatter.
- `/snippet <path> --force` — overwrite existing carved snippet files (carve mode only; ignored in regen mode).

## Mode detection

Inspect the input file's frontmatter:

- `clip:` field present **or** `podcast-clip` in `tags:` → **regen mode**.
- Otherwise → **carve mode**.

A fresh `/transcript --clip ... --topic "..."` output is technically a snippet (has `clip:` and `podcast-clip` tag) but has no Summary/Cleaned/Notes/Raw structure yet — regen mode handles that case by inserting the four sections for the first time.

## Carve mode workflow

1. **Run `carve.py plan <path>`.** The script scans for `==highlights==`, computes clip ranges from surrounding `[MM:SS]` anchors, and emits a JSON manifest to stdout. Read it.

2. **For each highlight, infer a 2-4 word kebab-case topic.** Use the highlight text plus the surrounding paragraph(s) as context. Aim for content-specific labels (`compounding-vs-rag`, `index-first-navigation`) — avoid generic ones (`interesting-bit`, `general-discussion`).

3. **Show the user a confirmation prompt** listing each highlight:
   ```
   Found N highlights in <stem>:
     1. [23:14-25:31]   compounding-vs-rag               (1 paragraph)
     2. [44:02-46:30]   index-first-navigation           (1 paragraph)
     3. [1:12:08-1:14:51] memex-lineage                  (2 paragraphs)
   Confirm, edit topic names, or 'skip N' to drop a highlight.
   ```
   Wait for the user's response. Update topics and drop skipped entries before proceeding.

4. **For each remaining highlight, generate `summary` and `cleaned_transcript`.** Apply the cleaning rules below.

5. **Pipe the filled plan back via stdin:** `python3 .agents/skills/snippet/carve.py write <path> --plan-stdin` (add `--force` only if the user explicitly asked).

6. **Report saved paths** and a one-line summary per file.

## Regen mode workflow

1. **Run `carve.py plan <path>`.** Returns a single-entry manifest with the existing Raw Transcript content (or, for a fresh `/transcript --clip` output without sections yet, the entire body).

2. **Generate fresh `summary` and `cleaned_transcript`** from the raw content and frontmatter context. Same cleaning rules as carve mode. Topic is preserved from the existing `clip_topic` frontmatter (or filled from the plan if unset).

3. **Pipe the filled plan back:** `python3 .agents/skills/snippet/carve.py write <path> --plan-stdin`.

4. The script preserves Notes byte-identical. If `==` markers appear in the existing Notes section, the script refuses — surface that error to the user.

## Cleaning rules

These define what `cleaned_transcript` should look like. Goal: a recognizable, de-cluttered version of Raw — *not* a paraphrase or rewrite.

### Speaker turns

- **Detect ground truth first.** If the Raw Transcript has paragraphs prefixed with `— ` (em-dash + space), those are explicit turn boundaries from `/transcript`'s `>>` marker handling. Use them directly — *no inference, no inference note*.
- **Paragraph 1 is special.** It never carries a `— ` prefix because it's the first turn (only turn-2+ get the prefix). When paragraph 1 obviously contains a speaker change — e.g., a brief host question followed by the guest's answer that the captioner rolled into one block — split it into two turns by inference. No inference note required as long as the rest of the cleaned transcript uses ground-truth boundaries.
- **If no `— ` prefixes appear anywhere** (auto-caption episodes), infer turns from conversational rhythm and add an italic note at the top of the Cleaned Transcript section: `_(speakers inferred from context)_`.

### Speaker labeling

Prefer named labels:
- `host` ← `show:` field, or text before `—` / `-` in the title
- `guest` ← text after `—` / `-` in the title

The frontmatter `title` is canonical for proper nouns (yt-dlp pulls it from clean metadata). **Do not trust the body for guest names** — even with `captions_source: youtube-manual`, ASR errors leak through (a guest's name or a domain term often arrives garbled). Cross-reference the title and the `kb.toml` glossary.

Fall back to `**Speaker A:** / **Speaker B:**` when host/guest aren't derivable.

### Filler removal

Drop these inline: `um`, `uh`, `like` (when filler), `you know` (when filler), `I mean` (when filler), repeated false starts ("the the the").

### ASR error correction (domain glossary)

Even `youtube-manual` files often contain auto-transcribed text uploaded as if hand-edited, so proper nouns and domain jargon arrive mangled. Two references:

- The frontmatter `title` (yt-dlp pulls it from clean metadata) is canonical for the show/guest proper nouns — cross-reference it rather than trusting the body.
- The KB's **domain glossary** lives in `kb.toml` under `[snippet].glossary` as `"what ASR heard" = "what was actually said"` pairs. Read it and apply every correction aggressively. Example shape:

  ```toml
  [snippet]
  glossary = { "carpathy" = "Karpathy", "my co forge" = "MycoForge" }
  ```

The glossary is instance-specific and non-exhaustive — when a domain-relevant word looks ASR-mangled and isn't yet covered, fix it anyway, and add the recurring ones to `kb.toml` so future carves get them for free.

### Anchors and time references

- **Strip inline `[MM:SS]` / `[H:MM:SS]` anchors** from the Cleaned Transcript. They're noise when reading. The clip range (`clip: "MM:SS-MM:SS"` in frontmatter) is the canonical place for time bounds — don't duplicate it in the body.
- The Raw Transcript section keeps anchors verbatim for provenance.

### Cleaned Transcript scope

The cleaned transcript covers **all paragraphs touched by the highlight** — i.e., it mirrors `raw_text` in the plan, not just the substring inside the `==…==` markers. Clips are anchor-bounded at paragraph granularity, so any unhighlighted text within a touched paragraph is part of the clip's audio range and belongs in the cleaned version.

Practical implication: if the user marked only `==Now the only constant is change…==` mid-paragraph, the clip starts at that paragraph's anchor — which may include a setup sentence or two before the highlighted text. Include that setup in the cleaned transcript. The `==…==` markers are a record of what caught the user's eye, not an instruction to crop.

### Interruption artifacts (mid-sentence `>>` turns)

YouTube captioners sometimes mark `>>` speaker changes mid-utterance — when the other speaker briefly interjects ("um and the", "yeah", "right") while the primary speaker is talking, or when two speakers' words overlap and the captioner picks a `>>` boundary inside a continuous sentence. In the source these become tiny filler-only turns and awkwardly chopped sentences:

```
— [1:11:41] um and the

— [1:11:43] and there'll be even even greater cases of it. I actually kind of think that LLMs right now...
```

In the Cleaned Transcript:

- **Drop filler-only / single-interjection turns** entirely (`um and the`, `yeah`, `right`, `mhm`, `uh-huh`, lone confirmations). They're conversational noise, not content. Don't attribute them to anyone.
- **Smooth cross-turn sentence interruptions.** When turn N ends without terminal punctuation AND turn N+1 grammatically continues N (the `>>` was mid-utterance), reattach the continuation to the primary speaker's flow. Use a light em-dash or natural punctuation if a brief interjection from the other speaker was meaningful; otherwise just merge.

  Example raw:
  ```
  — [12:24] Like 5 years like the people that are working

  — [12:24] three or four times the entire R&D spend of the US on like non-defense.

  — [12:28] Yeah. And so it's like...
  ```

  Cleaned:
  ```
  **Guest:** Five years ago, the people working on this were three or four
  times the entire R&D spend of the US on non-defense.

  **Host:** Yeah. And so it's like...
  ```
  (The middle "three or four times..." is the host completing/correcting the
  guest's thought; merge into the sentence as the actual speaker meant it. If
  you can tell from context it was the *other* speaker who finished it,
  attribute the whole continuous thought to whichever speaker the surrounding
  paragraphs attribute it to.)
- **Preserve substantive back-and-forth** — real questions and answers, distinct points. Don't over-merge.

### What not to do

- **No paraphrase.** Cleaned should preserve the speaker's actual phrasing. If you're tempted to rewrite a sentence, you've gone too far.
- **Don't merge full speaker exchanges.** A real question + real answer stays as two turns. Only merge when one turn is clearly a fragment of the other speaker's incomplete sentence (the `>>`-mid-utterance case).
- **Don't edit the Raw Transcript section** — that's verbatim provenance, anchors and all (including the `==…==` markers, which double as a record of what was carved).

## Summary section

3-5 sentences. Cover:
- Who's talking (named speakers)
- What context the moment sits in (the broader episode arc, the topic being discussed)
- The substantive claim or insight, in the speaker's own framing

Avoid hedge phrases ("the speakers discuss"). Lead with the substance.

## Topic naming rubric

- 2-4 words, kebab-case
- Content-specific (`compounding-vs-rag`, not `interesting-bit`)
- Use the domain's own vocabulary precisely, drawing on the highlight's subject matter
- Lowercase except established proper nouns where appropriate

## Multi-paragraph highlights

Obsidian's "toggle highlight" hotkey (Cmd+Shift+H by default) wraps each paragraph in its own `==…==` markers when applied to a multi-paragraph selection — that's a Markdown-spec quirk, not user error. `carve.py` handles this transparently:

- **Auto-merge rule**: consecutive `==…==` runs separated *only* by paragraph breaks (whitespace + `\n\n`, no intervening prose) are treated as a single logical highlight. The user's intent ("highlight this whole passage") is honored without manual cleanup.
- **Independent highlights still work**: if there's any non-highlighted prose between two `==…==` runs, they parse as separate highlights → separate snippet files.
- **Anchors inside `==` wrappers are still detected**: when the user's selection started at the very beginning of a paragraph, the leading `[H:MM:SS]` anchor ends up inside the `==` markers (`==[1:09:53] Like, what went wrong?==`). `carve.py` looks past leading `==` / `— ` decoration to find the anchor, so clip ranges stay precise.

## Edge cases

- **No highlights found** (carve mode): `carve.py plan` exits non-zero with a message. Tell the user to add `==highlights==` first.
- **Highlight spans multiple paragraphs**: clip range expands to include all touched paragraphs (whether the user typed one big `==…==` block or relied on the auto-merge of consecutive paragraph wraps). The plan's `spans_paragraphs` count flags this; surface it in the confirmation prompt so the user can adjust their highlight if the wider window isn't what they wanted.
- **Highlight contains nested `==` markers**: carve.py prints a warning. Ask the user to fix the source markup.
- **Highlight before the first anchor or after the last paragraph**: clip range defaults to `0:00` / episode duration respectively.
- **Highlight ends mid-paragraph (substantively before the next anchor)**: the auto-computed `clip_range` end uses the *next* paragraph's anchor — a conservative upper bound, since paragraph anchors are the only ground truth. When the substantive content clearly ends well before that anchor (e.g., the user marked only the first word of a long final paragraph to complete a thought), override `clip_range` in the filled plan before piping to `write`. Use the touched paragraph's own anchor plus a small offset (~1–5s) as a closer approximation. The Cleaned Transcript should still trim the unhighlighted tail of that paragraph if it's a topic transition; otherwise include it per the [Cleaned Transcript scope](#cleaned-transcript-scope) rule.
- **Same topic for two different highlights in one run**: each highlight produces a distinct file; the second-with-same-topic overwrite collision is rare and handled by `--force` semantics.
- **Long source filenames**: `safe_stem` caps the source's stem at 80 chars when `/transcript` saves the episode. `carve.py` then composes the snippet's target stem as `<source_stem> (clip - <topic>)` — without re-truncating the combined string, since that would drop the suffix and collide with the source filename. The topic itself is sanitized separately (capped at 60 chars). Practical effect: snippet filenames can exceed 80 chars, which is fine on every modern filesystem but worth noting.

## Idempotency

- Running `/snippet` twice in carve mode on the same source: existing snippet files are skipped with a notice. Use `--force` to regenerate.
- Highlights stay in the source file after carving — they're a record of what was extracted. Re-running is therefore a no-op unless the user added new highlights.
- Regen mode always overwrites Summary + Cleaned (that's the point); Notes and Raw are preserved byte-identical.

## Out of scope

- Does **not** auto-ingest into `wiki/`. After carving, the user can say "ingest this" or "ingest these" to run the standard ingest workflow on each snippet.
- Does **not** modify the source full-episode file. Highlights stay where they were marked.
- Does **not** strip `==…==` from the source after carving. (A future `--clean-highlights` flag could; not in v1.)
- Does **not** log to `wiki/log.md`. Snippet creation is a `raw/`-layer operation; the chat-side report is sufficient.

## Dependencies

- Python 3.9+ (uses `tuple[float, str]` style type hints; no third-party packages).
- The sibling `/transcript` skill must be installed at `.agents/skills/transcript/` — `carve.py` imports `safe_stem` and `yaml_dq` from `fetch.py` for naming and frontmatter consistency.
