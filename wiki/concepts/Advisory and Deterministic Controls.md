---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
raw:
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
related:
  - "[[AI-Native SDLC]]"
  - "[[Verification Bottleneck]]"
  - "[[Tiered Autonomy]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Company Brain]]"
  - "[[Fix the Principle, Not the Example]]"
confidence: medium
tags: [ai-native, governance, guardrails]
---

# Advisory and Deterministic Controls

The control model underneath the [[AI-Native SDLC]]: an instruction the agent
reads is an advisory control, and any policy that must always hold needs a
deterministic layer behind it that fires regardless of what the model decides.

> [!claim] A skill makes violations rare; only a hook makes them close to impossible
> confidence: medium · status: supported
> evidence: "A skill is a control, though an advisory one. It makes Claude
> likely to apply the policy while the code is written, and nothing forces a
> session to comply with it. A policy that must always hold needs something
> deterministic behind the skill, such as a hook that blocks the action or a
> review pass that re-checks the policy at the PR. The skill makes violations
> rare and the hook makes them close to impossible" —
> [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]].
> Corroborated by the practitioner framing in
> [[2026-08-20 The Claude Code Guide For Startups]]: "AI agents are not
> deterministic, but a lot of highly regulated work requires processes to be
> done the same way every time," hooks fire "regardless of what the model
> decides." Both Anthropic, one prescriptive and one collected from customers.

## The layers

Each layer closes a gap the one above leaves open:

1. **`CLAUDE.md` and skills** — advisory. The agent is likely to comply.
   Skill invocations show up in session traces, so non-compliance is at least
   visible.
2. **Hooks** — deterministic scripts that run before an action and can
   *allow*, *ask*, or *block*. Build-phase hooks block edits to protected
   paths, run the formatter after edits, keep credentials out of the diff,
   stop the agent editing test files during a fix. Every decision is logged
   with a timestamp to the OpenTelemetry export.
3. **Review pass at the PR** — re-checks the policy on the finished diff
   (`REVIEW.md` passes for bugs, security, compliance against `spec.md` and
   `plan.md`). Findings never approve or block on their own; branch protection
   keeps approval human.
4. **Permissions and managed settings** — who may override what. Team hooks
   live in `.claude/settings.json` and are reviewed like code; non-negotiable
   ones live in managed settings owned by the platform or IT admin, where
   `allowManagedHooksOnly` and `allowManagedPermissionRulesOnly` mean "no
   engineer, project file or command-line flag can widen the rules."
5. **Sandbox** — closes what permissions cannot: "A tool-level deny on
   WebFetch doesn't stop a shell command reaching the network; the OS-level
   domain allowlist blocks egress outright." Credential rules deny reads of
   `~/.ssh` and `~/.aws/credentials` and strip named secrets from every
   sandboxed command's environment; `failIfUnavailable` refuses to start
   without the sandbox.

The playbook's managed-settings example is offered as "a starting point to
tailor, rather than a recommendation to copy. Every deny trades against
capability."

## Placement rules

- **Build hooks are fast and scoped to the file that changed.** Heavier
  checks such as the full test suite belong at the commit or the PR.
- **Ask-hooks belong at the deploy gates, not in the build.** "An approval
  prompt during the build puts a person back on the critical path of all the
  sessions running in parallel." The human sits at the gate, not in the loop
  — see [[Tiered Autonomy]].
- **A block explains itself.** The reason and the route to approval appear in
  the agent's output.
- **Protect the feedback loop with a hook.** "An agent fixing code must not be
  able to weaken the check on that code," so a fix task cannot edit test
  files; the fallback is rejecting any review diff that touches a test
  ([[Verification Bottleneck]]).

## Diagnosing drift between the layers

The playbook's lagging indicator for a skill is review findings that cite its
policy, which should fall toward zero. When they don't, "either the skill isn't
triggering or its text has drifted from the official policy." That is a
measurable version of the drift check in
[[Fix the Principle, Not the Example]]: the review layer audits the advisory
layer. In [[Tom Blomfield]]'s loop anatomy ([[Self-Improving AI Loop]]) the
advisory controls are the policy layer and the deterministic ones are the
quality gate; the playbook is the first source to say which is which and where
each runs. The advisory layer is also where institutional knowledge lives — the
[[Company Brain]] as files the agent reads.
