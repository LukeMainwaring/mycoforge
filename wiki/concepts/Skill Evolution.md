---
type: concept
created: 2026-10-23
updated: 2026-10-23
sources:
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
raw:
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
related:
  - "[[Three-Layer Architecture]]"
  - "[[Why LLM Wikis Beat RAG]]"
  - "[[Self-Improving AI Loop]]"
  - "[[Fix the Principle, Not the Example]]"
  - "[[Progressive Disclosure]]"
  - "[[Ingest Workflow]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Token Efficiency]]"
  - "[[Tu Vu]]"
confidence: medium
tags: [skills, feedback-loops, architecture]
---

# Skill Evolution

Improving an agent's *skills* automatically. A skill is a filesystem module
of procedural knowledge (a `SKILL.md` with frontmatter, applicability
conditions and instructions, plus scripts); skill evolution runs the agent
on training tasks, analyzes the traces, proposes an edit to the skills, and
keeps the edit only if a validation score goes up. Prior methods (EvoSkill,
Trace2Skill, SkillOpt) keep what was learned inside the skill text or a flat
history of past proposals. WikiSkill, from [[Tu Vu]]'s group at Google
Research ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution|WikiSkill]]),
puts a persistent wiki between the raw traces and the skills, cites
[[Andrej Karpathy]]'s gist as the inspiration, and is the first controlled
evidence in this KB that a persistent wiki beats re-deriving from the latest
traces each time, the compounding half of [[Why LLM Wikis Beat RAG]]; the
paper has no retrieval arm, so it says nothing against RAG.

## The loop

A [[Three-Layer Architecture]] with a different third layer: `raw/` holds
immutable execution traces; `wiki/` holds `patterns/` pages (one per failure
mode or working strategy), `index.md`, `logs.md`, and a `skill-impact.md`
audit trail; `skills/` holds the active skills, each a `SKILL.md` plus a
`PURPOSE.md` that maps it back to the wiki patterns that motivated it. Each
iteration:

1. **Inference Agent** runs the training tasks with the current skills
   injected in full. Traces land in `raw/`. It is denied wiki access.
2. **Wiki Maintainer** reads a stratified sample of traces (at most 8: up to
   5 failing for root-cause analysis, 3 passing for what worked, each capped
   at 15k characters) plus the whole wiki, then creates or patch-edits
   pattern pages, rewrites `index.md`, and appends to `logs.md`. Its rules
   read like this KB's schema: no duplicate patterns, extend the existing
   page with new evidence; pages of 10–30 lines, "not essays"; only
   generalizable observations; index entries that state problem, root cause
   and fix so an agent can judge relevance without opening the page.
3. **Skill Proposer**, a ReAct agent, starts from `index.md`,
   `skill-impact.md` and a pass/fail summary, reads pattern pages and traces
   on demand (at least four traces), and emits one atomic proposal: create
   one skill or patch one. Rejected proposals are on file, so it must not
   re-propose them.
4. **Gating and rollback**: the candidate skill set runs on a validation
   split and is kept only if it beats the best score so far. The harness,
   not a model, appends proposal, diff, score and accept/reject to
   `skill-impact.md`.

The system state is the pair (skills, wiki). Skills roll back; the wiki never
does.

> [!claim] A persistent wiki between raw traces and skills beats evolving skills with no accumulated knowledge at all
> confidence: medium · status: supported
> evidence: WikiSkill has the highest average over five benchmarks for all
> five models, beating the strongest prior method by 3.3 to 12.0 points, and
> the ablation that removes the wiki (and with it the maintainer) drops
> Gemini-3.5-Flash from 63.7% to 48.7% average — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].
> Three runs per cell, paired bootstrap at p<0.05. Only the ablation
> isolates the wiki, and it compares against no memory, not against a flat
> proposal history; the cross-method lead is confounded by everything else
> that differs between methods. One paper, the authors' own method against
> baselines one of them co-wrote; moves to high on an independent
> reproduction.

> [!claim] During skill evolution, giving the executing agent the wiki lowers the final skill quality; the paper does not test wiki access at inference time
> confidence: medium · status: supported
> evidence: giving the Inference Agent wiki access during rollouts cuts the
> final average from 63.7% to 60.9% (LiveMath 72.6% to 64.8%); the authors'
> hypothesis is that an executor that solves tasks from the wiki leaves
> traces that say less about the skills — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].
> One model, four benchmarks, the mechanism explicitly "we hypothesize".
> The split protects a training signal, not a reader; it does not by itself
> say who should read a wiki that is not training anything.

> [!claim] Discovering a skill and executing it are different capabilities; evolved skills transfer across models and can beat self-evolved ones
> confidence: medium · status: supported
> evidence: Qwen-3.6-27B's ALFWorld skill lifts Qwen-3.5-9B to 70.2% against
> 63.4% with its own; its LiveMath skill lifts Gemma-4-31B to 73.7% against
> 56.7%; skills from the 4B model lift Gemma on LiveMath to 73.1%. Transfer
> fails when a skill encodes model-specific workarounds (see
> [[Fix the Principle, Not the Example]]) — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].

> [!claim] Skill gains grow with model scale, yet a small model with evolved skills can beat a larger one without
> confidence: medium · status: supported
> evidence: within the Qwen family WikiSkill adds +12.3, +17.5 and +23.9
> points for 4B, 9B and 27B; Qwen-3.5-9B with skills averages 47.4% against
> 39.4% for Qwen-3.6-27B without — [[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]].
> The cost reading is in [[Token Efficiency]].

## What the paper measured

| Result | Figure |
|---|---|
| Average lead over the best prior method, by model | 3.3 to 12.0 points |
| Ablation: proposer with vs without the wiki (Gemini-3.5-Flash) | 63.7% vs 48.7% |
| Ablation: executor given wiki access | 63.7% to 60.9% |
| Accepted skill updates landing in iterations 0–1 | 39–58%, the rest through iteration 7 |
| Optimizer LLM calls per iteration | 1 + ReAct turns (about 10–20), independent of training-set size |
| Wiki growth per run | 6–9 patterns created, 7–18 edits, pages of 18–48 lines |

## What this KB takes from it

The first source here whose `raw/` is machine-generated and whose wiki has
no human reader. The pattern survives: immutable raw, a model-owned wiki
that is only ever patched, bookkeeping in `index.md` and a log on every pass
([[Ingest Workflow]]). The loop is [[Tom Blomfield]]'s anatomy with a
number at the end ([[Self-Improving AI Loop]]), and its gate is the
deterministic layer under an advisory one
([[Advisory and Deterministic Controls]]): skills steer, the validation
score decides.

Three limitations the authors list matter here. No pruning: the wiki only
grows, and they flag that as future work (this KB's Lint is the manual
version). Strict gating: a proposal must *improve* validation, so neutral
groundwork that pays off later is thrown away. Skills are injected, not
retrieved, so nothing is known about triggering once the skill set grows.

The open question the paper raises for this KB's own structure, whether
`wiki/` should feed `.agents/skills/` the way WikiSkill's wiki feeds
`skills/`, is recorded in the log, not decided on this page. What the
paper's version needs that this KB lacks is an objective score to gate on.
