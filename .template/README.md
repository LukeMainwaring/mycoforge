# `.template/` — onboarding tooling

This directory turns the full MycoForge scaffold into *your* knowledge base.
It's the deterministic substrate the `/onboard` skill drives; you can also run
it by hand. **Delete this whole directory once you've onboarded.**

## Files

- **`features.toml`** — declares the cuttable features (`product`,
  `orchestrator`, `media-capture`, `insight`, `mcp-server`; all independent),
  the paths each wholly owns, and the `[archetypes]` onboarding presets
  (interview defaults the `/onboard` skill reads; `onboard.py` ignores them).
- **`onboard.py`** — deterministic prune + rename (pure stdlib, dry-run by
  default, idempotent).
- **`verify_matrix.sh`** — copies the tree, prunes it for representative
  feature combos, and asserts each still lints clean with zero leftover
  markers and consistent symlinks/references.
- **`test_onboard.py`** — pytest suite for marker processing, keep-set
  resolution, and the rename.

## Usage

```bash
python3 .template/onboard.py --list                            # show features
python3 .template/onboard.py --keep orchestrator,media-capture,mcp-server
                                                               # preview: research KB
python3 .template/onboard.py --keep media-capture,mcp-server \
        --slug mykb --brand MyKB --apply                       # apply + rename
python3 .template/onboard.py --keep "" --apply                 # minimal wiki core
```

After `--apply`, run `python3 scripts/lint.py` and regenerate the prose docs
(the `/onboard` skill owns that half).

## How pruning works

The scaffold marks feature-specific content inline so removal is mechanical.
Two comment styles, chosen by file type:

- **Code and config** (`.py`, `.toml`, `.sh`, `.gitignore`):
  `# sf:begin(<id>) … # sf:end(<id>)` blocks, and a trailing
  `# sf:keep-if(<id>)` on a single line.
- **Markdown** (`.md`): the same markers as HTML comments —
  `<!-- sf:begin(<id>) -->` … `<!-- sf:end(<id>) -->` and a trailing
  `<!-- sf:keep-if(<id>) -->`. HTML comments are invisible in both Obsidian
  reading view and GitHub rendering (Obsidian `%%` comments are not).
- JSON can't carry comments, so `.json` files are never marked — a feature owns
  them wholesale via `paths` (that's why `.mcp.json` is a listed path).

Semantics: if the feature is **dropped**, the block/line vanishes; if **kept**,
only the marker vanishes, leaving clean text. `onboard.py` deletes each disabled
feature's `paths`, processes the markers everywhere, verifies the symlinks and
skill references, and (with `--slug`) renames the identity tokens — preserving
the `[template]` repo pin in `kb.toml` so `/sync-upstream` keeps working.

When *documenting* markers in prose that survives onboarding, write the id as a
`<placeholder>` (as this file does) — the marker regexes require a literal
feature id, so placeholders are inert, and `verify_matrix.sh` greps the pruned
tree to prove no real marker survives.

## Adding a new cuttable feature

1. Add a `[features.<id>]` block to `features.toml` (paths + `requires`).
2. Wrap its code/prose in markers, or list the files it solely owns under
   `paths`. Instance data it needs goes in `kb.toml`, never in code.
3. Add or extend a case in `verify_matrix.sh`.
