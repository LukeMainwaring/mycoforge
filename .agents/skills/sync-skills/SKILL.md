---
name: sync-skills
description: Port upstream changes to the skills vendored from mattpocock/skills and bump the pin in VENDORED.md.
disable-model-invocation: true
---

# Sync the vendored skills with upstream

`.agents/skills/VENDORED.md` is the manifest: the pinned upstream commit, which skills are
vendored (and which of those carry local edits), and which upstream skills were looked at and
skipped. This KB is the template, so changes land here first and reach instances through
`/sync-upstream`.

## Steps

1. **Run the check.**

   ```bash
   bash scripts/check-vendored-skills.sh
   ```

   It clones upstream, prints the upstream head, and lists **Changed since pin** and
   **New upstream skills**. `up to date` means stop here.
2. **Clone upstream at the head the check printed.** The check deletes its own clone on
   exit, so make one to copy from:

   ```bash
   tmp=$(mktemp -d) && git clone -q https://github.com/mattpocock/skills "$tmp" && git -C "$tmp" checkout -q <head>
   ```

3. **Port each changed skill.** Read the upstream commits the check listed. A skill without
   the `(customized)` suffix is copied whole from `$tmp/skills/<bucket>/<name>/` over
   `.agents/skills/<name>/`.
   A `(customized)` skill gets the upstream change applied by hand so the local edits named in
   the manifest survive; show the user the resulting diff.
4. **Decide each new skill.** Ask the user vendor or skip, one line each with the upstream
   description. Vendor: copy the directory in from `$tmp` and add it under **Vendored**. Skip: add it under
   **Not vendored**. Either way it never shows as new again.
5. **Audit invocation on everything touched.** A skill that only ever fires by hand carries
   `disable-model-invocation: true` in `SKILL.md`, `policy.allow_implicit_invocation: false` in
   `agents/openai.yaml`, and a one-line human-facing description. A model-invoked skill carries
   neither flag and a description with its triggers. Every skill has an `agents/openai.yaml`.
6. **Pin.** Set `Upstream commit:` in the manifest to the head the check printed. Rerun the
   check: it must print `up to date`.
7. **Verify.** `python3 scripts/lint.py` is clean. Remove `$tmp`.
8. **Record.** Append a `schema |` entry to `wiki/log.md` naming the skills ported, vendored,
   and skipped, and the new pin.

## Guardrails

- Native skills are out of scope (`connect`, `research`, `snippet`, `transcript`, `onboard`,
  `sync-upstream`, `sync-skills`): the check never lists them and this skill never edits them.
- A skill under **Not vendored** stays skipped unless the user asks for it by name.
- Upstream `engineering/research` is unrelated to this KB's `/research`; it stays skipped.
