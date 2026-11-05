---
type: concept
created: 2026-07-23
updated: 2026-11-05
sources:
  - "[[2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up]]"
  - "[[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]]"
  - "[[2026-08-20 The Claude Code Guide For Startups]]"
  - "[[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]"
  - "[[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]"
  - "[[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]"
  - "[[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]]"
  - "[[2026-10-31 The AI Daily Brief - How the Most AI Pilled Company in the World Works (clip - Spawn)]]"
  - "[[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]]"
  - "[[2026-11-02 Warp - How to build an agentic self improvement loop]]"
raw:
  - raw/podcasts/2026-04-24 Y Combinator - How To Build A Company With AI From The Ground Up.md
  - raw/podcasts/2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI.md
  - raw/articles/2026-08-20 The Claude Code Guide For Startups.pdf
  - raw/articles/2026-08-21 The AI-Native SDLC Playbook (Anthropic).md
  - raw/podcasts/2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today.md
  - raw/papers/2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution.md
  - raw/articles/2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn).md
  - raw/podcasts/2026-10-31 The AI Daily Brief - How the Most AI Pilled Company in the World Works (clip - Spawn).md
  - raw/podcasts/2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd.md
  - raw/podcasts/2026-11-02 Warp - How to build an agentic self improvement loop.md
related:
  - "[[Skill Evolution]]"
  - "[[AI-Native Company]]"
  - "[[Organizational Legibility]]"
  - "[[Fix the Principle, Not the Example]]"
  - "[[Build for Rebuilding]]"
  - "[[AI-Native SDLC]]"
  - "[[Tiered Autonomy]]"
  - "[[Advisory and Deterministic Controls]]"
  - "[[Stigmergic Coordination]]"
  - "[[AI Software Factory]]"
  - "[[Zach Lloyd]]"
confidence: medium
tags: [ai-native, feedback-loops]
---

# Self-Improving AI Loop

The unit of the [[AI-Native Company]]: a company process wrapped in a feedback
loop that improves itself with minimal human intervention. [[Diana Hu]] frames it
in control-systems terms — pre-AI companies ran as **open loops** (decide,
execute, rarely measure); a **closed loop** continuously monitors output and
adjusts. [[Tom Blomfield]] calls the same thing "recursive self-improving AI
loops."

Blomfield's loop anatomy:

1. **Sensor layer** — customer emails, support tickets, code changes, churn
   events, telemetry
2. **Policy layer** — what the AI may do, what needs human permission, what must
   be logged
3. **Tool layer** — deterministic APIs (query the database, read the calendar)
4. **Quality gate** — evals, deterministic checks, safety filters, human review
   for high-risk actions
5. **Learning mechanism** — failures feed back to the top

> [!claim] A monitored agent loop can fix its own failures overnight, unattended
> confidence: medium · status: supported
> evidence: YC's internal query agent gained a monitoring agent that watches every
> failed query, diagnoses the gap (missing tool? stale skills file? new index?),
> writes the fix, opens a merge request, has an agent review, merge, and deploy it
> — "when a human comes the next day to ask the same query, it will now succeed"
> — [[2026-05-21 Y Combinator - How to Build a Self-Improving Company with AI]].
> Corroborated across companies in [[2026-08-20 The Claude Code Guide For Startups]]:
> ClickHouse turned "nearly every SDLC stage into an autonomous loop", and two
> purpose-built agents that fix flaky tests and find missing coverage are the
> #2 and #3 contributors to its repo; Clay automated bug triage "from first
> pass to suggesting code changes"; Emergent's onboarding doc is self-healing
> ("If Claude hits anything broken or out of date during onboarding, it
> updates that file"); at Anthropic, Claude Tag is the CI/CD first responder
> and "authored the first situation report in every recent incident", usually
> within 15 minutes. Still vendor-collected, but the contributor ranking is the
> first quantitative signal. First non-vendor source: Spawn, where a break
> spawns a fixer agent on the spot and "if the code breaks at 2am on
> Christmas, nobody gets woken up" —
> [[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]].
> Self-reported and unaudited, so held at medium; an independent account
> would move this to high.

Other proposed loops: a product loop (agent mines analytics for funnel friction,
researches fixes, runs an A/B test, deploys the winner, repeats) and a support
loop (agent triages suggestions against the roadmap, ships accepted ones
overnight). The precondition for all of them is [[Organizational Legibility]] —
a loop can only learn from what got recorded.

## The learning mechanism, worked out

The anatomy's fifth step is the one the YC talks leave vaguest. Cainex's
medical-coding loop in [[2026-08-20 The Claude Code Guide For Startups]] is the
first source to describe it end to end: tagged human corrections → revise the
governing instruction, not the case → back-test against a golden set → a
short list for engineers. Its rule, and its overfitting failure mode, have
their own page: [[Fix the Principle, Not the Example]]. The guide's general
definition of a loop — an agent that repeats cycles of work until a stop
condition is met — comes with a design constraint: the stop condition must
be clear and self-contained, which is why flaky-test agents are the common
first loop (the agent verifies its own fix by rerunning the test).

The host of [[2026-09-06 The AI Daily Brief - How to Build an AI-Native Company Today]]
states the same constraint for loops outside engineering ([[Alex Lieberman]]'s
feature 16, "make non-engineering workflows self-improving by learning from
previous runs through external performance metrics and internal
evaluations"): a loop is "a goal and bumpers around what they can do and a
process that they can loop through over and over again until they achieve
that goal," and its precondition is "some verifiable success metric that is
objective rather than subjective… achieve an X percentage result on this
test is a lot more definable than our interface needs to look good." The
organizational skill, then, is inventing clear success metrics "for the
broader array of knowledge work tasks that don't necessarily have that sort
of success criteria built in natively." His example of the pattern applied to
marketing (feature 19): rewrite and generate SEO/AEO content weekly, then
measure whether any of it worked — "not just going to do the thing, but to
build learning systems around the thing."

## The loop, written as a runbook

The closing-the-loop play in [[2026-08-21 The AI-Native SDLC Playbook (Anthropic)]]
is the first source to give the whole anatomy as an implementable recipe,
and it maps one-to-one onto Blomfield's layers:

| Layer | Playbook component |
|---|---|
| Sensor | a metrics store plus a deterministic, unit-tested detection script (rolling mean and σ, Western Electric rules) — "no model involved" |
| Policy | `bands.yaml`: 1σ log, 2σ diagnose read-only, 3σ propose via PR or pre-approved runbook ([[Tiered Autonomy]]) |
| Tools | deploy, status, and rollback exposed as per-environment MCP tools; `gh run view` for diagnosis |
| Quality gate | the PR review gate plus a service owner triaging fix-now / schedule / dismiss ([[Advisory and Deterministic Controls]]) |
| Learning | every shipped fix adds an eval; every dismissal tunes the bands |

The agent's output is an `intent.md`, so the finding re-enters the
[[AI-Native SDLC]] at Plan and the loop closes without a person starting it.
Worked examples: a 3σ CI failure-rate breach quarantines the flaky test or
opens a revert PR; a post-deploy 5xx breach with a deployment in the window
triggers the rehearsed rollback; a PR cycle-time drift writes a report for
engineering leadership, "which shows the harness works for process metrics
as well as production ones." Vendor recipe rather than a case, but it is
the deterministic-detection design that ClickHouse's flaky-test agents
already embody.

## The loop, benchmarked

[[Skill Evolution]] is the anatomy run against public benchmarks with a
score at the end. In WikiSkill ([[2026-08-27 WikiSkill - Compiling Agent Experience into Persistent Knowledge for Skill Evolution]]) the sensor is the execution traces;
the policy is fixed prompts plus one hard rule, only a validation-score
improvement is accepted; the quality gate is that score, decided by the
harness with no model involved, as the playbook row above wants; and the
learning mechanism is a wiki the proposer must read before proposing.
Across five benchmarks and five models it adds 12 to 24 points over no
skills and beats three prior skill-evolution loops; 39–58% of accepted
improvements land in the first two iterations and the rest keep arriving
through iteration 7. The objective metric the AI Daily Brief host says every
loop needs is what lets this one run unattended: the validation split is the
"verifiable success metric." The authors' own caveat is that a strict
better-than-best gate rejects neutral groundwork that might pay off later.

## The loop on live production

Spawn ([[2026-10-28 How I Built the Most AI-Pilled Company in the World (Spawn)]])
runs every layer against production rather than a test copy, on the
argument that agents on private machines wait for humans to relay what broke:

- **Sensor.** "Hyper observability": everything must be something an agent
  can follow step by step in text and replay. Errors, logs, metrics, spend
  and every transaction notify an agent; about 60% of work starts from a
  production error, a bug report, a log anomaly or a feature request.
  Savi, the in-product agent users build games with, files bugs herself.
- **Policy.** A small model triages each error or report and hands it to the
  owning agent, which decides fix, won't-fix, or a design question for a
  human. The fix usually reaches the user within an hour, in the same chat.
- **Cadence as a quality gate.** An hour without a ship is a SEV-0, Spawn's
  most severe incident. The stated reason: "an agent can only keep a few
  hours of work in its head, so shipping faster than that actually helps it
  stay coherent." Rollback takes 30 seconds; recovery paths are tested by
  breaking things on purpose.
- **Results quoted.** A leaked API key caught from the spend anomaly within
  15 minutes, then disabled and every key rotated; one incident declared
  about 8 minutes after players were affected, fix live 11 minutes after
  declaration, stable 4 minutes later.

The non-engineering version of the same loop is the precedent judges in
[[Organizational Legibility]]; the engineering side's coordination is
[[Stigmergic Coordination]].

The AI Daily Brief host's doubt ([[2026-10-31 The AI Daily Brief - How the Most AI Pilled Company in the World Works (clip - Spawn)]]): Spawn's sensor layer is its users'
agents reporting bugs as they play, "not the type of thing that you're going
to get in many categories of products." Whether the approach needs that
loop, and whether other products can build one, he leaves open. It sits
beside his objective-metric precondition above.

## The loop on the factory itself

In Warp's [[AI Software Factory]]
([[2026-11-03 Latent Space - The 2026 Software Factory Infra Stack - Zach Lloyd]])
the thing being improved is the factory's own definition, not a product
process:

- **Sensor.** Every agent run, stored centrally rather than on engineers'
  laptops; [[Zach Lloyd]] calls these traces "the key aspect of how this
  system improves."
- **Quality gate.** Scorers, which he also calls "online evals": an LLM judge
  grades stored runs after the fact, with a chosen judge model, a judging
  prompt, and a sample rate to cap cost. Built-ins check verbosity,
  efficiency, code quality and redundant tests; teams add their own failure
  modes, in code.
- **Learning.** Self-improvement agents look for clusters of failures and,
  because the factory is code, open a PR against the definition. The worked
  example: 54 triage failures where triage should have spawned a subagent
  to investigate.

### How the scorers are built

Ben, Warp's DevEx lead, walks the same loop as four steps (store, score,
isolate failures, propose) in a talk on Warp's channel
([[2026-11-02 Warp - How to build an agentic self improvement loop]]).
The captions are Warp's own upload, so quotes are safer than in the
podcast; the sample rubric and report were on screen only, so just what he
says is filed here. Both sources are Warp describing its product.

**What a trace holds.** Three parts, all needed to diagnose a run: the
transcript (agent, subagents and the human in the loop), the tool and MCP
calls ("an agent might spin its wheels sending the wrong properties to an
MCP call"), and the code output, as diffs or the PR at a commit. The traces
go in one store the whole team can read. Uploading every engineer's Claude
or Codex folder to S3 on a cron is the scrappy version; he recommends a
cloud runner, where every run lands in one place by default.

**A scorer is a markdown rubric.** It has two parts: the failure modes
being tested for, and a grade from 0 to 1 with each level described and a
line where failure starts ("mostly or highly inefficient" fails). After a
run, the transcript goes to each scorer, a separate agent in its own
context window, which grades it and writes notes in the margin on why.
Judges run on a lightweight model because of the volume, and a sample rate
caps the bill; he says a small sample gets "close to the same effect", with
no figures. Scorers are checked in as code beside the agents and
automations, so an agent can read and change its own setup.

The four he walks through:

- **Redundant tests**: what a high-quality test is. He grounds it in "Kent
  C. Dodds' test pyramid", which he reads as end-to-end tests most valuable
  and unit tests least. Dodds' published model is the Testing Trophy, not a
  pyramid, and it puts most weight on integration tests; the preference in
  the rubric is Ben's, not Dodds'.
- **Tautological tests**: credited to Matt Pocock. A test that asserts the
  code does what it was written to do, at the extreme a constant returning
  its own value; described in a markdown file the agent is told not to
  follow.
- **Verbosity**: of replies to the human and of code comments, which "bleed
  into each other"; plain language, and no comment that isn't useful.
- **Efficiency**: cost to the human (many steers versus right on the first
  pass) and information gathering (tool calls spent exploring the
  environment, such as probing for a free port before verifying).

**Isolate, then aggregate.** Passing runs drop out. A self-improvement agent
on a daily cron reads the failures with the scorers' notes, looks for what
they have in common, and opens PRs into an inbox, each citing its evidence.

> [!claim] A self-improvement agent should wait for a large sample of failures before proposing changes
> confidence: low · status: supported
> evidence: "it's best to have a large dataset before you trigger a
> self-improvement agent. Otherwise, it might over-index on individual
> failures instead of seeing the forest for the trees"; a suggested change's
> evidence "should include multiple examples for it to be worth improving"
> — [[2026-11-02 Warp - How to build an agentic self improvement loop]].
> Practitioner advice with no threshold. It is the overfitting risk in
> [[Fix the Principle, Not the Example]], stated for mining traces.
> [[Skill Evolution]]'s WikiSkill reads at most 8 traces per pass, but
> keeps what it learned in a wiki across passes and gates each change on a
> score; this loop has neither.

**The fixes it found**, from Ben's own runs:

- Agents fought for port numbers before they could test their work. The
  suggested skill edit names the environment variable that overrides the
  port when it is taken.
- He kept steering how changelog entries were worded. The suggestion was a
  more prescriptive changelog rule in the skill.
- A triage agent could not spawn a subagent and burned tool calls working
  out why. The PR added a missing stub to the harness configuration; likely
  the same case as Lloyd's 54 triage failures above.

The first two are skill edits, the third is harness configuration: the loop
reaches the whole factory definition, not only skills. The reason to run it
at all: agents "will always report back that something worked," so wasted
minutes of tokens go unseen without a score.

**Scores over time.** Each scorer is plotted across runs, so a skill or
model change shows as better, worse, or not statistically significant; his
example is the efficiency grade dropping after a model change.

> [!claim] Scoring runs over time makes agent improvement visible where overnight "dreaming" and memory systems are a black box
> confidence: low · status: supported
> evidence: "Instead of asking the agent to dream overnight or using memory
> systems that operate like a black box, here we get visibility into how
> the agent is improving as we ship these changes" — [[2026-11-02 Warp - How to build an agentic self improvement loop]].
> A vendor contrasting its product with alternatives it does not test. The
> trend is in the rubric's own terms; the source does not tie it to
> outcomes such as reverts or cost.

The single-machine version is Warp's open-source Skill Doctor
([[Skill Evolution]]).

What the loop lacks is a check that a proposed change helps before a person
reviews it. Lloyd names it as the next step, to "replay the runs and make
sure that this actually would have improved them." That replay is the
better-than-best gate [[Skill Evolution]] already runs on its validation
split, here with a team's own past runs as the test set. Ben's version has
the same gap: its gate is a person reviewing the PR.

[[Kareem Amin]]'s practitioner version of the thesis: "the moat for any
company right now is that it needs to be self-improving. So Clay is a
self-learning revenue engine" — and the willingness to rebuild is part of it
([[Build for Rebuilding]]).

The sidekick-vs-loop distinction is the load-bearing idea: an agent that answers
questions is "last year's version… making me 20 or 30% more effective"; the loop
is what compounds. Kin to this KB's own thesis — see
[[Why LLM Wikis Beat RAG]] on compounding vs re-deriving.
