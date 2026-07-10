---
name: sync-upstream
description: Port MycoForge template updates into this KB instance — diff the vendored tooling against the template repo at HEAD, apply what's wanted, bump the pinned template version. Use when the user says "sync upstream", "update the template tooling", or "pull template updates".
---

# Sync this instance with the upstream template

This KB vendors full copies of the template's tooling (copy-and-own). Your job is
to port upstream improvements **selectively** into this instance, guided by the
config/code split: code should be byte-identical to the template; everything
instance-specific lives in `kb.toml`, so real conflicts are rare and usually mean
someone hard-coded instance data where it doesn't belong.

## Steps

1. **Read the pin.** From `kb.toml` `[template]`: the `repo` URL and the pinned
   `version` this instance last synced to.
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
4. **Present the plan.** Summarize each upstream change in a sentence and whether
   it applies here. Instance config in `kb.toml` is never overwritten; new config
   *keys* upstream introduced get added with their default values and a comment.
5. **Port what the user approves.** Copy upstream file contents over the vendored
   copies. If a vendored file has local edits (it shouldn't — that violates
   copy-and-own), show the conflict and let the user pick.
6. **Verify.** Run `python3 scripts/lint.py` and the tooling tests
   (`pytest scripts/` if pytest is available). Fix or revert anything red.
7. **Record it.** Bump `[template].version` in `kb.toml` to upstream's version,
   and append a `schema |` entry to `wiki/log.md` naming what was ported.

## Guardrails

- Never overwrite instance data: `kb.toml` values, wiki content, `raw/` —
  untouchable.
- Never re-add features this instance pruned at onboarding.
- If upstream and instance code genuinely diverged, prefer upstream and move the
  instance-specific part into `kb.toml` — that's the split reasserting itself.
