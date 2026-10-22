# Vendored skills

Skills copied from https://github.com/mattpocock/skills. `scripts/check-vendored-skills.sh` reads
this file and reports upstream changes since the pinned commit, plus upstream skills not listed
here. The `/sync-skills` skill runs it and ports what changed. Only the `engineering` and
`productivity` buckets are tracked.

Upstream commit: 5beb35b

## Vendored

Format: `<bucket>/<name>`. A `(customized)` suffix means the local copy carries intentional edits
(the wiki's own vocabulary sources in place of `GLOSSARY.md` in `pr`; a `learning/<topic>/`
workspace in `teach`); apply upstream changes to it by hand, never by copying.

- engineering/pr (customized)
- productivity/grill-me
- productivity/grilling
- productivity/handoff
- productivity/teach (customized)
- productivity/writing-for-agents

## Not vendored

Upstream skills looked at and skipped. The check does not report these as new. Upstream
`engineering/research` is a different skill from this KB's native `/research`.

- engineering/ask-matt
- engineering/code-review
- engineering/codebase-design
- engineering/diagnosing-bugs
- engineering/domain-modeling
- engineering/grill-with-docs
- engineering/implement
- engineering/implement-spec
- engineering/improve-codebase-architecture
- engineering/prototype
- engineering/research
- engineering/retro
- engineering/setup-matt-pocock-skills
- engineering/tdd
- engineering/to-spec
- engineering/to-tickets
- engineering/triage
- engineering/wayfinder
- engineering/wizard
- productivity/to-questionnaire
- productivity/wait-what
