---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
raw:
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
related:
  - "[[AI-Native Company]]"
  - "[[Verification Bottleneck]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Tiered Autonomy]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Just-in-Time Planning]]"
  - "[[Everyone Ships]]"
  - "[[Organizational Legibility]]"
  - "[[Three-Layer Architecture]]"
confidence: medium
tags: [ai-native, software-engineering, governance]
---

# AI-Native SDLC

Anthropic's Applied AI team's playbook for rebuilding the six-stage software
development lifecycle (plan, design, build, test, deploy, maintain) around
agents — [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]].
Unlike the startup-facing sources in the [[AI-Native Company]] cluster, it is
written for incumbents, regulated ones especially: the question is how to keep
the old control objectives while changing the enforcement. The premise is that
code is no longer the bottleneck, but the process around code was designed
when it was.

> [!claim] When build collapses, the bottleneck moves to the human-speed stages on either side of it, and per-line controls stop matching reality
> confidence: medium · status: supported
> evidence: "The bottleneck moves to the steps to the left and right of the
> build phase. This is mainly plan, review/test, and deploy, which still run at
> human speed… Reviewing each line by hand made sense when a person had written
> it, but it can't keep up once agents write most of the diff… exceptions still
> route through meetings and committees that meet weekly or monthly" —
> [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]. Vendor
> prescription distilled from customer work, no named cases. The enterprise
> restatement of [[Verification Bottleneck]], with governance cost added as a
> third consequence.

The shape of the answer: the linear pipeline becomes a loop, AI sits at every
stage, and each stage ends by committing an artifact that triggers the next.
Humans stay accountable for every judgment call, but their attention moves to
the artifacts and the gates.

## The artifact chain

| Stage | Artifact committed | What fires next |
|---|---|---|
| Plan | `intent.md` — problem, proposed outcome, affected users and systems, constraints, open questions, in the originator's own words | product owner accepts → Design |
| Design | `spec.md` — agent-written from `intent.md` under the org's brand/security/compliance/UX skills, with concerns flagged | product owner accepts → Build |
| Build | `plan.md` from plan mode (files, order of work, risks, proof), then the diff and its tests | merged PR → pipeline |
| Test | the literal test/build/screenshot output the session pasted; eval results | attached to the PR |
| Deploy | the PR with its review findings, fixes, and human approval | merge → deploy through the production gate |
| Maintain | the incident record, written as a new `intent.md` | → Plan |

> [!claim] Committed markdown artifacts are both the handoff mechanism and the audit trail
> confidence: medium · status: supported
> evidence: "The thread running through the right-hand column is the committed
> artifact… The chain of commits is also the audit trail: who asked for what,
> what the agent produced, and who approved it." Markdown is the early-stage
> format "because a product owner and an agent can both read and act on the
> same file" — [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]].
> Every play's metric is read from git or PR history (time from first
> conversation to a committed `intent.md`, `spec.md` commits dated after the
> first `plan.md`, share of merged diffs that still match `plan.md`), so the
> chain is also the instrumentation. Vendor design, not observed practice.

Adoption order: prompt each step by hand first; the end state is a loop in
which each accepted artifact fires the next gate and "human attention
concentrates at the gates, reviewing what the agent flagged rather than
starting each stage from scratch." Plays carry prerequisites. `intent.md`,
`CLAUDE.md`, the feedback loop, and hooks-as-gates need nothing and are the
starting points; CI/CD automation needs PR review and approval gates first,
"because the gates must exist before automation accelerates anything through
them"; closing the loop needs all of it.

## The plays

| Stage | Play | What changes | Leading → lagging indicator |
|---|---|---|---|
| Plan | Capture as `intent.md` | idea → proto-spec in the originator's words; replaces backlog entries, user stories, story points, refinement meetings | time to committed intent (weeks → hours) → share accepted into Design |
| Design | Requirements and design | one agent session with org skills as constraints; product owner reviews but doesn't write; front-end via Claude Design mock → Claude Code | intent→spec commit gap → spec changes after the first `plan.md` |
| Build | Plan mode by default | nothing implemented without an accepted `plan.md`; interrogate what could break, riskiest step, options not taken; update the plan in the same commit when the diff departs | first-pass merge share → rework cycles, diff still matches plan |
| Build | `CLAUDE.md` | institutional knowledge as a file; mistake twice → into the file; keep under a page | repeated mistakes → new joiner's time to first merged PR |
| Build | Skills as institutional knowledge | one policy, one named owner, one written source of truth; org-wide via plugins | policy change → skill merge time → review findings citing the policy fall to zero |
| Build | Hooks as guardrails | deterministic: block protected paths, run formatter after edits, keep credentials out ([[Advisory and Deterministic Controls]]) | — |
| Build | Parallel sessions and subagents | one worktree per task; two or three sessions to start; ceiling is review capacity; recurring jobs become subagents | concurrent sessions while review holds → merges per engineer against rework |
| Test | Give Claude a feedback loop | one-command test/build; failing test first for bug fixes; verification is part of "done"; a hook blocks test edits during a fix | first-pass CI success → review time per PR, change failure rate |
| Test | Continuous evals in CI | 20–50 real tasks; run on any change to `CLAUDE.md`, skills, or hooks; every incident becomes an eval | pass rate over time → regressions caught in CI vs production |
| Deploy | AI in the PR review loop | `REVIEW.md` passes (bugs, security, compliance against `spec.md` and `plan.md`); findings never approve or block; `@claude` fixes comments; findings feed `CLAUDE.md` | time to first review (minutes) → escaped defects |
| Deploy | Hooks as approval gates | ask-hooks for release authorization; non-negotiable ones in managed settings | wait per gate → gate violations reaching production |
| Deploy | CI/CD integration | `claude -p` for read-only judgment steps first; writes arrive as PRs; deploy and rollback as per-environment MCP tools; rollback the most rehearsed path | failures triaged without paging → DORA measures |
| Maintain | Closing the loop | deterministic detection, σ-tiered response ([[Tiered Autonomy]]), diagnosis written as `intent.md` | breach → intent in triage queue → findings that become merged fixes, repeat incidents |
| Maintain | Recurring codebase scans | scheduled Claude Security scans; finding → PR or `intent.md`; each fixed class → eval | repos on schedule → scan-found vs production-found |
| Maintain | Claude on call (Claude Tag) | channel as first responder and audit trail; post-mortem to a version-controlled lessons file | — |

## Fitting around legacy systems

Jira, ServiceNow, requirements tools, Figma, and change boards "are hard to
displace because auditors and regulators already accept them," so the playbook
fits around them: for every artifact, name one source of truth. Three
configurations — the repo as source of truth (legacy records link to commits),
the legacy system as source of truth (Claude reads the record at session start
and writes the outcome back over MCP in the same session), or **linkage as the
minimum bar** (record ID in every artifact, commit SHA in every record, two
sources of truth accepted). This is the incumbent path that the
startup-advantage claim in [[AI-Native Company]] says is slow: unwinding is
replaced by wrapping.

## Rhyme with this KB

The chain is a [[Three-Layer Architecture]] with different names: `intent.md`
is the curated input the agent drafts but the human corrects and owns;
`spec.md`, `plan.md`, and the diff are agent-owned derived artifacts;
`CLAUDE.md` and skills are the schema. The commit history plays the role of
`log.md`. Noted as an observation, not a filed synthesis.
