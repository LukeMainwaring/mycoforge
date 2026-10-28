# Rendering a topic with archify

Archify is a separately installed skill that draws a **rendered diagram** as standalone HTML. The guide is complete without it: if the `archify` skill is not available, say so and stop here.

For each topic the user picks:

1. **Choose the type** from the topic: `sequence` for a path a thing takes, `dataflow` for where data comes from and goes, `lifecycle` for phases and states, `architecture` for structure and for a map of related pages.
2. **Use one folder per topic**, `architecture/diagrams/<topic-slug>/`, and tell archify to use it, with the HTML named `<topic-slug>.html`. Keep only the spec and the HTML there; the receipts rule in step 4 says when to delete the rest.

   If the folder already has a `candidate.json`, this is a **re-render**. First rename `<topic-slug>.html` to `<topic-slug>-previous.html` in the same folder, so the user can open old and new side by side; `.gitignore` keeps it out of commits. Delete it when the user signs off, or when the render is dropped or redone. Then read the diff from the candidate's `meta.repository.revision` to `HEAD` over the page's `watches:` and edit that spec the way the update step edits a page. Change only the nodes, flows, cards, and source citations the diff touches, keep every position and route that still holds, and set the revision to `HEAD`'s full commit. Fix any path `finalize` reports missing at the new revision. Done when `finalize` passes and the spec's own diff shows only what changed in the subject.
3. **Invoke the archify skill** with a request built from the page:
   - the topic and the type you chose
   - the page's summary and "How it works" text, as the description of what to draw
   - the reader: a developer who cloned this template, learning it well enough to run one
   - that this is a real repository, so archify attaches source evidence: file paths, of whatever kind the page watches (`.py`, `.toml`, `.md` under `wiki/` or `raw/`), never line ranges ([[ADR-013 Evidence Stays at File Level]])
   - the page's Mermaid diagram as the statement of the topic's main claims: the rendered diagram must agree with it on what the pieces are, how they relate, and which boundaries they sit in. Layout is archify's choice, and it may add or leave out detail around those claims. For the machinery overview, one region per focus, so the render and the page's H3s match one to one.
4. **Apply these layout rules** while writing the request and editing the spec. Each one prevented a `finalize` or visual-check failure on an earlier render; tally any rule you add against a real failure before keeping it. Rules marked *unverified* are only exercised by sequence or dataflow diagrams and have not been re-tallied since they were written.

   **Before coordinates.** Pick the size from the content, then write positions.
   - An architecture diagram shows the whole graph at 1440 × 900 in the default view. A grid that has passed repeatedly: columns at x = 20 + 280n, rows at y = 40 + 150n, boxes 150 × 64, five columns by four rows (1290 × 620 before region pads). Fold detail into sublabels and cards rather than adding a row.
   - A region's default pad is 30px, so a region whose member sits at x = 20 overflows the canvas. Set `pad: 14` on a region that touches an edge. A region is the bounding box of what it wraps, so give each region its own columns.
   - A sequence diagram is 1080 × 696 at most. Wider fails the readability floor, because the 7px sublabels project below 6px once the canvas passes about 1085 (1180 failed); taller fails the desktop height check (760 failed). At that size it holds about 13 messages at 28px spacing with no notes, so choose the messages before writing coordinates. The legend needs the last segment's `to` at 590 or below.
   - *Unverified.* Dataflow geometry is fixed: stage centers at x = 100 + 215 × stage, so five stages need `viewBox` at least 1080 wide from the start. Showcase needs an aspect ratio of about 1.55 or more at 1440 × 900 (1080 × 680 passed; 1080 × 760 failed).

   **While editing.** Keep the layout compact.
   - Keep the canvas fixed and fix text by shortening labels or moving the fact to a card; a wider canvas fails the readability floor instead of helping. Budget with archify's own formula: a horizontal edge label takes 6.5px × characters + 21, a sublabel 5.4px × characters + 8. So a 130px gap takes 16 characters and a 150px box takes 26. Subtract a region's pad from any gap it borders: a 130px gap with a region border in it takes about 12. Where one label needs more, shrink the neighbouring boxes, not the canvas.
   - Let archify route forward flows; automatic port spread orders the ports correctly, including several edges into one side. Give a return flow explicit `via` points outside the rows plus `fromSide`/`toSide`; a return pinned to sides with no `via` runs along a region border. The `top-channel` and `bottom-channel` presets run between rows and cross the main path.
   - Put a per-node setting in `tag`; it shows on detail, not in the default view, so the sublabel carries the role. A region label or `tag` can replace an edge where it conveys the same fact, which keeps hubs from crossing.
   - The architecture schema caps `sources` at 3 per component; pick the three that prove the box's claims and leave the rest for a card. Its legend is keyed by node type, so relabel the types for the reader there.
   - In a sequence diagram, put explanation in cards, not in message notes. Since archify 3.1.0 a note renders wrapped in the default view and the next message must clear it, so a note costs a row the canvas does not have; a step that was its own arrow in the Mermaid becomes a card item instead. A segment label is drawn 22px above its frame at the left edge, and archify rejects one that would land on a message label, so keep segment labels short and start a segment at least 30px below the previous message. Messages that share horizontal space need 28px between them.
   - *Unverified.* In a dataflow or sequence diagram, set `meta.legend.entries` whenever a variant means something other than archify's default, such as dashed for a retry rather than "async batch".

   **Before finishing.** Clean the folder and look at the render.
   - `finalize` refuses to overwrite `<topic-slug>.browser-check.json`, so delete it by name between runs (a glob with no match aborts the line in zsh). Delete every receipt (`.finalize.json`, `.finalize-summary.json`, `.browser-check.json`, `.delivery.json`) before commit so the folder holds the spec and the HTML only.
   - Run `visual-check <html> --summary --require-provenance --out-dir <scratch>` and read the 1440 × 900 PNG yourself. It is the only check of the whole-graph rule and it catches what `finalize` passes: an oversized graph, a label hidden behind the next one, a label past the right edge or touching a region border.
5. **Finish** when archify's `finalize` passes and the 1440 × 900 capture shows the whole graph, readable labels, and nothing hidden. Passing `finalize` does not establish that. If the capture could not be produced or viewed, say so plainly instead of claiming visual quality.

Add the diagram to the table in `architecture/diagrams/README.md` (create it on the first render: one row per diagram with the topic, the type, and the HTML path) and a "Rendered with archify" link under the topic page's Diagram section, if not already there, and check the link resolves. `.archify/` is ignored and is only for scratch runs.

Then commit on a branch and open a draft PR as `AGENTS.md` (Version control) describes, titled `architecture: render the <topic-slug> diagram` (`re-render` for a re-render), or push to the PR this run already has. Stop and give the user the absolute path of the new HTML, of the `-previous` file if there is one, and the PR link, with the viewport you checked at and anything archify's visual review recommendation flagged. Wait for their visual check.
