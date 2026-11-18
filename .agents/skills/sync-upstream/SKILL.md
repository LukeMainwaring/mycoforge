---
name: sync-upstream
description: Port MycoForge template updates into this KB instance — diff the vendored tooling against the template repo at HEAD, apply what's wanted, bump the pinned template version. Use when the user says "sync upstream", "update the template tooling", or "pull template updates".
disable-model-invocation: true
---

# Sync this instance with the upstream template

This KB vendors full copies of the template's tooling (copy-and-own). Your job is
to port upstream improvements **selectively** into this instance, guided by the
config/code split: code should be byte-identical to the template; everything
instance-specific lives in `kb.toml`, so real conflicts are rare and usually mean
someone hard-coded instance data where it doesn't belong.

## Steps

1. **Read the pin.** From `kb.toml` `[template]`: the `repo` URL, the pinned
   `version`, and the `commit` SHA this instance last synced to (the SHA is the
   diff base; if it's empty, this instance predates commit pinning — diff
   against upstream HEAD and note it).
2. **Fetch upstream.** Clone the template repo at HEAD into a temp directory
   (`git clone --depth 1 <repo> <tmpdir>`). If the clone fails, stop and tell
   the user.
3. **Diff the vendored surfaces**, instance vs upstream:
   - `scripts/` (the linter and its tests)
   - `.agents/skills/` (each skill this instance kept — skip ones that were
     pruned at onboarding; do not resurrect them)
   - the schema boilerplate sections of `AGENTS.md` (template contract, workflow
     scaffolding — *not* the instance's domain-specific prose)
   - `.mcp.json` + `mcp/` if this instance kept the MCP server

   Also list every file a kept surface holds here that upstream no longer has:
   those are **upstream deletions**, unless the user says the file is their own.
4. **Present the plan.** Summarize each upstream change in a sentence and whether
   it applies here, and list the upstream deletions. Instance config in `kb.toml`
   is never overwritten; new config *keys* upstream introduced get added with a
   comment. A key whose upstream value is the template KB's own data (`[scout]`
   `topics` and `watch`, a glossary, lint terms) is added empty for the user to
   fill.
5. **Port what the user approves.** Copy upstream file contents over the vendored
   copies. If a vendored file has local edits (it shouldn't — that violates
   copy-and-own), show the conflict and let the user pick. Three kinds of file
   are not a plain copy:
   - **Upstream deletions**: delete the ones the user approved.
   - **Ledgers** (`staging/ingest.md`, `staging/scout.md`): a new one gets the
     upstream header only, down to the first row or run section; an existing
     one keeps its rows and takes the new header.
   - **Identity** (`.mcp.json`, `.codex/config.toml`): after copying, replace
     the upstream `kb.toml` `[kb].slug` with this instance's.
6. **Verify.** Run `python3 scripts/lint.py` and the tooling tests:
   `uvx --with pytest pytest -q scripts`. With `mcp/` present the tests import
   the server's dependencies, so run
   `uv export --script mcp/server.py --no-hashes --quiet > "$TMPDIR/mcp-reqs.txt" && uvx --with pytest --with-requirements "$TMPDIR/mcp-reqs.txt" pytest -q scripts`.
   Fix or revert anything red.
7. **Record it.** In `kb.toml`, bump `[template].version` to upstream's version
   and set `[template].commit` to the upstream HEAD SHA you synced from, then
   append a `schema |` entry to `wiki/log.md` naming what was ported.

## Guardrails

- Never overwrite instance data: `kb.toml` values, wiki content, `raw/` —
  untouchable.
- Never re-add features this instance pruned at onboarding.
- If upstream and instance code genuinely diverged, prefer upstream and move the
  instance-specific part into `kb.toml` — that's the split reasserting itself.
