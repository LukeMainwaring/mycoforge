---
type: decision
status: proposed
created: 2026-07-23
updated: 2026-07-23
related:
  - "[[Subtractive Onboarding]]"
  - "[[Company Brain]]"
  - "[[AI-Native Company]]"
  - "[[Just-in-Time Planning]]"
  - "[[AI-Native Role Archetypes]]"
  - "[[ADR-002 Fractal Federation for Nested KBs]]"
tags: [adr, onboarding, positioning]
---

# ADR-005 Onboarding Archetypes as Presets

## Context

Two recurring instance shapes have emerged: the **personal second-brain** (an
individual's compounding research/reading KB) and the **AI-native company
playbook** (a venture's durable context layer). The ingested AI-native cluster
supplies the evidence that the second shape is real and valuable:

- [[Company Brain]]'s context-as-moat claim — "a proprietary knowledge
  substrate that no generalist AI can match" — is the playbook's pitch, and
  that page already observes a MycoForge instance is a candidate company-brain
  implementation.
- [[Just-in-Time Planning]]'s reconciliation: feature design docs die, but
  durable context documents become *more* necessary. The playbook holds the
  frame (architecture, scope, decisions), not feature plans.
- [[AI-Native Role Archetypes]] notes an archetype scheme needs three role
  axes; [[Self-Improving AI Loop]]'s five-part anatomy and
  [[AI-Native Startup Lifecycle]]'s stage/exit-criteria table give playbook
  pages their shapes.

The `product` feature (embedded prompts, ADRs, MCP seam) already covers much of
the playbook path. The question is whether archetypes need new machinery — new
page types, a second template — or are a curation of what exists.

## Decision

**Archetypes are interview presets in `/onboard`, not new machinery.** A new
first question in the Phase 1 interview offers `personal second-brain | company
playbook | custom`; a preset pre-fills three existing interview answers, all
overridable (`custom` = today's flow unchanged):

- **Feature keep-set** — personal: `media-capture + insight` (cut `product`,
  `orchestrator`; `mcp-server` optional). Playbook: `product + mcp-server +
  insight` (`orchestrator` optional — multi-venture federation per
  [[ADR-002 Fractal Federation for Nested KBs]]).
- **Taxonomy** — personal: `concepts/people/syntheses` (today's default).
  Playbook: `concepts/decisions/playbooks/roles`, via the existing per-instance
  taxonomy mechanism. **No template-level page types are added.**
- **Seed pages** — playbook gets moderately opinionated scaffolding: a
  lifecycle-stage frame with exit criteria, a loop-anatomy playbook template,
  role scaffolds on the three axes. Validated by dogfooding on Luke's own
  venture(s) before being treated as stable for template users generally.

Preset keep-set data lives in `.template/features.toml` (new `[archetypes]`
block; `verify_matrix.sh` gains the two preset combos); taxonomy and seed prose
live in the `/onboard` skill. `onboard.py` prune logic is unchanged.

**Positioning: the substrate framing leads.** The README stays "a template for
compounding LLM wikis"; the two archetypes appear as a short entry-paths
section, not a new identity.

## Consequences

- Zero new instance machinery: presets are template-time and deleted with
  `.template/`, leaving no residue in onboarded KBs.
- Onboarding judgment load drops — evidence-backed defaults replace five raw
  feature questions for the common cases.
- The playbook preset's quality is gated on dogfooding; findings fold back into
  the preset before generalizing.
- Implementation (`/onboard` question, `[archetypes]` block, seed pages, README
  section, matrix combos) is deferred to a follow-up session tracked on
  `roadmap.md` — this ADR is its spec.

## Alternatives

- **A second template (or fork) per archetype** — rejected: same reasoning as
  [[ADR-002 Fractal Federation for Nested KBs]]; archetypes are presets over
  one template, not different species.
- **New first-class page types (playbook/role/eval) in the template** —
  rejected: the per-instance taxonomy mechanism already supports them where
  wanted; template-level types would burden every instance and the linter.
- **Playbook-leads repositioning** — rejected: strongest single pitch
  ([[Company Brain]] moat) but dilutes the substrate identity the template is
  built on; revisit if dogfooding proves the playbook is the dominant use.
- **No presets (status quo)** — rejected: wastes the ingested evidence; every
  onboarder re-derives the same defaults interactively.
