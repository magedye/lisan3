# Stitch Gap-Closure Prompt — Lisanapp Governed UX v4.0

## Goal

Continue the **existing Lisanapp Stitch project** and complete the missing UX/UI required by **Lisanapp Governed UX Constitution & Implementation Reference v4.0**.

Do **not** redesign the application from scratch.

Treat the current 18 high-fidelity screens as the baseline. First inspect and reuse them, then perform a focused **UX Gap Closure Pass** that:

1. fixes any constitutional modeling violations,
2. adds only missing screens, states, inspectors, drawers, and flows,
3. connects the complete governed research lifecycle interactively,
4. preserves the current Arabic RTL visual language and design system.

The goal is to make the Stitch prototype a trustworthy **UX implementation reference**, not merely a collection of attractive screens.

---

## Source of truth

The authoritative product model is:

**Research Workspace + Evidence System + Epistemic State + Governed Runtime + Human Review + Knowledge Memory + Governance Control Plane + Purity Assurance.**

The conversation interface is only an entry point above these layers.

The application is **not**:
- a conventional chatbot,
- a generic analytics dashboard,
- a direct knowledge editor,
- or a confidence-scoring system.

Every claim shown to the user must make it possible to answer:

- What is its status?
- Why does it have this status?
- What evidence supports it?
- What counterevidence challenges it?
- Is it methodologically pure?
- Who reviewed it?
- What does it depend on?
- What could invalidate it?
- Which Research Run, Corpus Snapshot, methodology revision, and provenance chain produced it?

---

# Phase A — Audit the current 18 screens before adding anything

Create a concise **UX Coverage / Gap Map** inside the Stitch canvas.

For every existing screen, identify:

- screen name,
- functional purpose,
- related v4.0 capability,
- whether it is complete, partial, duplicated as a state variant, or missing required behavior,
- the screen or flow that must be added or amended.

Do not count two state variants of the same screen as two distinct product capabilities.

Preserve all useful existing work.

Do not generate duplicate versions of screens that already satisfy the requirement.

---

# Phase B — Correct the epistemic state model first

The application MUST NOT represent knowledge as one linear maturity pipeline.

Use four independent state axes everywhere:

### 1. Epistemic Status
Examples:
- OBSERVATION
- HYPOTHESIS
- TESTED
- SUPPORTED
- LOCK_BLOCKED
- LOCK_INTERNAL_RESULT
- REJECTED
- UNRESOLVED

### 2. Review Status
Examples:
- NOT_REVIEWED
- REVIEW_REQUIRED
- IN_REVIEW
- APPROVED
- REJECTED
- OWNER_DECISION_REQUIRED

### 3. Freshness Status
Examples:
- CURRENT
- STALE
- INVALIDATED
- REVALIDATION_REQUIRED

### 4. Publication Status
Examples:
- PRIVATE_WORKING
- REVIEWABLE
- PUBLISHABLE
- PUBLISHED
- WITHDRAWN

Example valid combined state:

`LOCK_INTERNAL_RESULT + REVIEW_REQUIRED + CURRENT + PRIVATE_WORKING`

Do not visually imply that:

`LOCK_INTERNAL_RESULT = approved = published`

They are independent dimensions.

Each axis must have:
- Arabic text,
- machine-readable code,
- icon,
- color,
- short explanation.

Never rely on color alone.

Never display a single numeric semantic confidence such as `87%`.

---

# Phase C — Fix Lock Gate presentation

Lock Gates must be shown as dynamic contract-driven items, not hard-coded frontend rules.

Design the UI as if the gates are returned by a `GateReport`.

Each Gate card must support:

- Arabic name,
- `gate_code`,
- PASS / FAIL / NOT_APPLICABLE,
- supporting evidence,
- failure reason,
- evaluated revision,
- required next action.

A summary may say:

`8 passed | 2 failed | 1 not applicable`

but explicitly indicate:

**This is a gate summary, not a confidence score.**

Do not hard-code a fixed gate count.

---

# Phase D — Complete these missing P0 experiences

## 1. Global Contextual Inspector

Create one reusable contextual inspector available from all major entities:

- Claim
- Evidence
- Counterevidence
- Hypothesis
- Root
- Word
- Verse
- Concept
- Gate
- Rule
- Resource
- Research Run
- Dependency

Use a right/left side drawer appropriate for RTL.

Include:

- ID
- entity type
- current four-axis status where applicable
- source
- corpus
- methodology
- revision
- provenance hash
- evidence
- counterevidence
- dependencies
- dependents / used by
- reason for current status
- history
- raw technical details / JSON in Technical mode

Opening the Inspector must never lose the current workspace context.

---

## 2. Steward — Global Governed Command Drawer

Implement Steward now as a **global drawer**, not a standalone optional feature.

Create the complete interaction:

`User intent → Governed Command → Preview → Authorization → Validation → Impact Preview → Execute → Result → Audit Record`

Example commands:

- re-evaluate a rejection condition,
- request revalidation,
- propose a rule change,
- add a research note,
- submit a review request.

Show:

- parsed user intent,
- generated command,
- affected entities,
- required authority,
- validation result,
- expected epistemic impact,
- confirmation before execution.

Include blocked states:

- Unauthorized
- Validation failed
- Owner decision required
- Command cannot change canonical knowledge directly

Steward must never imply it can directly establish a Root Core from free-form user text.

---

## 3. Hypothesis Lab

Create a dedicated comparison workspace for:

`H1 | H2 | C0`

Show candidates side-by-side.

Comparison dimensions:

- proposed definition,
- rejection condition,
- supporting evidence,
- counterevidence,
- hardest verse/location,
- strongest competitor,
- corpus coverage,
- abstraction problems,
- neighbor separation,
- failed gates,
- unresolved questions.

Allow selecting evidence to open the Contextual Inspector.

Do not declare a winner automatically when evidence is insufficient.

---

## 4. Semantic Differentiation Lab

Create a specialized workspace for:

`Current root ↔ Semantic neighbor`

Show:

- shared semantic area,
- Distinctive Residue of each root,
- substitution test,
- strongest lexical competitor,
- decisive verses,
- supporting evidence,
- counterevidence,
- unresolved distinction,
- related gate result.

Support:

`DISTINCT / NOT_DISTINCT / UNRESOLVED`

Also create a **Split Comparison View** for two roots side-by-side.

---

## 5. Evidence / Counterevidence Workspace

Create a balanced dual-view interface.

Do not visually subordinate counterevidence.

For each item show:

- source verse/artifact,
- structural observation,
- relation to hypothesis,
- provenance,
- status,
- affected claim,
- inspector action.

Support filters:

- supporting,
- opposing,
- unresolved,
- decisive,
- methodology revision,
- corpus snapshot.

---

## 6. Investigation Coverage

Add an investigation coverage component inside research workspaces.

Example:

- analyzed occurrences: `12 / 12`
- examined forms: `4 / 5`
- critical neighbors examined: `3 / 4`
- falsification tests completed: `5 / 7`

Always show this warning:

**Completion of examination does not mean correctness of the hypothesis.**

Never convert Investigation Coverage into semantic confidence.

---

## 7. Quality Profile

Do not represent quality as a single score.

Create a multidimensional table/profile covering at least:

- corpus coverage,
- evidence coverage,
- counterevidence search completeness,
- root/form/context separation,
- semantic neighbor differentiation,
- internal consistency,
- cross-root / cross-verse consistency,
- dependency completeness,
- provenance completeness,
- citation completeness,
- methodology compliance,
- falsifiability clarity,
- unresolved conflict burden,
- reproducibility,
- stability across repeated analyses,
- human-review status,
- explanatory adequacy.

Each dimension needs:

- status,
- evidence,
- deficiency,
- required action.

Keep **Methodological Purity** separate from general Quality.

---

# Phase E — Complete the Research Runtime

The current Run Builder is only the creation step.

Add:

## Research Runs List

Show:
- run ID,
- research question,
- target entity,
- methodology,
- corpus,
- current stage,
- status,
- last activity,
- checkpoint,
- owner/researcher.

## Research Run Detail

Tabs or sections:

- Overview
- Inputs
- Stages
- Artifacts
- Evidence
- Tests
- Gates
- Agent/Tool Trace
- Dependencies
- History
- Reproduce

Show the full research progression.

## Smart Resume

Support suspended or interrupted runs.

Display:

- last durable checkpoint,
- completed stages,
- current stage,
- artifacts already produced,
- assumptions that must be revalidated,
- `Resume from checkpoint` action.

A Research Run must not depend on chat memory alone.

---

# Phase F — Complete the Blind Lab experience

Preserve the existing Blind Lab, but verify that the complete interaction exists:

`Corpus`
→ `Observations`
→ `Structure`
→ `Hypotheses`
→ `Negative Boundary`
→ `Falsification`
→ `Lexical Differentiation`
→ `Counterevidence`
→ `Gates`
→ `Internal Lock`

Before Internal Lock, hide:

- previous semantic results,
- Semantic Definition Registry,
- priors,
- owner answers,
- dictionaries,
- tafsir,
- glossary information not admitted by policy,
- post-lock comparison.

Design explicit isolation states:

### Isolation Safe
**العزل سليم**

### Prior Contamination
**تم اكتشاف تلوث بالمعرفة السابقة — لا يمكن القفل**

Code:

`PRIOR_CONTAMINATED`

Prior contamination must visibly block Internal Lock.

After Internal Lock, enable a separate:

**Post-Lock Comparison**

Do not merge this comparison into the pre-lock workspace.

---

# Phase G — Add the remaining subject workspaces

Preserve the current Root Workspace and derive consistent variants for:

## Word Workspace

Focus:
- lexical form,
- morphology,
- occurrences,
- root relation,
- constructions,
- local meanings.

## Verse Workspace

Focus:
- verse identity,
- corpus source,
- relevant words,
- layer separation,
- arguments,
- contexts,
- claims,
- evidence,
- unresolved interpretations.

## Concept Workspace

Focus:
- concept hypothesis,
- participating roots,
- related verses,
- boundaries,
- competing conceptual models,
- evidence,
- dependencies.

All four workspaces:

`Root / Word / Verse / Concept`

must share the same governed shell and contextual inspector.

---

# Phase H — Complete Operations & Audit

Create a dedicated area:

## 1. Audit Log

Show:

- actor,
- action,
- timestamp,
- reason,
- affected entity,
- before / after state,
- epistemic impact.

## 2. Agent / Tool Trace

Create a chronological research execution trace.

Example:

`Corpus loaded`
→ `Observation artifact created`
→ `Structure analyzer executed`
→ `H1 created`
→ `Falsification F-17 executed`
→ `Gate G-X failed`

Each trace event can open its artifact or technical details.

## 3. Provenance View

Create a drill-down relationship such as:

`Claim`
→ `Evidence`
→ `Artifact`
→ `Research Run`
→ `Corpus Snapshot`
→ `Methodology Revision`
→ `Tool / Agent revision`

## 4. Reproducibility Workspace

Provide:

**إعادة إنتاج النتيجة**

Show required reproducibility inputs:

- result revision,
- research run,
- corpus snapshot,
- methodology revision,
- rule versions,
- relevant tool versions,
- artifact hashes.

This is a prototype UI only; do not claim a real backend reproduction occurred unless connected to an actual implementation.

---

# Phase I — Complete Governance

Extend the existing Governance Center with the following if they are not already implemented.

## Registry Explorer

Explore governed registries and their revisions.

## Change Proposals

Use the governed flow:

`Proposed change`
→ `Impact Analysis`
→ `Review`
→ `Authority / Owner Decision`
→ `Apply new revision`
→ `Invalidate affected knowledge`
→ `Audit`

Do not allow direct canonical rule editing to bypass this flow.

## Conflict Management

Create UI for:

`OPEN_AUTHORITY_QUESTION`

Show:
- conflict,
- affected claims,
- competing rules/decisions,
- responsible authority,
- history,
- resolution action.

## Decision History

Show human and owner decisions with provenance and consequences.

## Skills & Tools Management

Show:

- installed skill/tool,
- version,
- hash,
- role,
- permitted scope,
- status.

## Validation / Test Dashboard

Show:

- test suite,
- revision,
- passed,
- failed,
- skipped,
- failure reason,
- affected contract.

Do not imply tests establish semantic truth.

## Owner Decision UI

Create explicit experiences for:

- OWNER_DECISION_REQUIRED
- approve
- reject
- defer
- request more evidence.

Authority must be visibly separated from developer permission.

---

# Phase J — History and change impact

Create:

## History Timeline

Show changes over time across:

- epistemic status,
- review status,
- freshness,
- publication,
- methodology revision,
- corpus,
- rules,
- dependencies.

## Methodology Comparison Mode

Compare two methodology revisions side-by-side:

- changed rules,
- changed gates,
- changed evidence requirements,
- resulting status differences,
- affected roots,
- affected runs,
- newly stale results.

## Transitive Invalidation View

Visualize:

`Rule change`
→ `Affected artifact`
→ `Dependent root`
→ `Dependent claim`
→ `STALE / REVALIDATION_REQUIRED`

Make transitive impact understandable without requiring the graph alone.

Always provide a textual/table alternative.

---

# Phase K — Three display levels

Implement a persistent view-level control:

**مبسط | بحثي | تقني**

Do not navigate to a different page when changing level.

Do not lose context.

### Simplified
Show:
- result,
- status,
- direct reason,
- limitations,
- next step,
- essential sources.

### Research
Add:
- evidence,
- counterevidence,
- hypotheses,
- gates,
- layer separation,
- semantic neighbors,
- quality,
- purity.

### Technical
Add:
- IDs,
- schema fields,
- revisions,
- hashes,
- dependencies,
- raw JSON,
- agent/tool traces,
- audit records.

---

# Phase L — Role-aware UX

Create and verify UI states for:

- Researcher
- Specialist Researcher
- Human Reviewer
- Steward
- Developer / Auditor
- Owner / Decision Authority

Do not simply hide navigation.

Design:

- disabled actions,
- read-only states,
- permission explanations,
- approval requirements,
- unauthorized-transition states.

Critical rule:

**Developer permission does not grant epistemic authority.**

---

# Phase M — Ask Lisan: insufficient evidence flow

Verify that Ask Lisan supports a valid governed non-answer:

**الأدلة الحالية غير كافية لإصدار جواب محكوم.**

Code/state:

`INSUFFICIENT_EVIDENCE`

Primary action:

**إنشاء بحث لهذه المسألة**

Connect it directly to the Research Run Builder with the question and available context pre-filled.

Never invent a definitive answer merely to satisfy the conversational interface.

---

# Phase N — UI Contract Gap Register

Create a Developer / Operations screen called:

**فجوات عقود الواجهة — UI Contract Gap Register**

Use a table such as:

| UI Capability | Required Contract | Backend Status | Blocker | Mock/Fixture |
|---|---|---|---|---|

Examples:

- Root Workspace DTO
- Research Run
- GateReport
- PurityReport
- Reproduce Run
- Steward Command
- Impact Analysis
- Review Decision

Statuses:

- AVAILABLE
- PARTIAL
- MISSING
- MOCK_ONLY

This screen is critical.

Do not invent backend contracts merely because a UI exists.

Clearly distinguish prototype fixtures from implemented backend capability.

---

# Phase O — Onboarding Launchpad

Add or verify an onboarding experience on the home Attention Center.

Use `{ن ش ز}` only as a UI example of a non-established / blocked result.

Do not present a canonical semantic definition for it.

Guide a new user through:

1. question,
2. evidence,
3. hypotheses,
4. counterevidence,
5. gates,
6. why `LOCK_BLOCKED`,
7. next research action.

---

# Phase P — Interaction journeys that must work in the prototype

Connect and test these prototype journeys.

## Journey 1 — Governed research

`Ask Lisan`
→ `INSUFFICIENT_EVIDENCE`
→ `Create Research`
→ `Run Builder`
→ `Blind Lab`
→ `Hypothesis Lab`
→ `Falsification`
→ `Semantic Differentiation`
→ `Counterevidence`
→ `Gate Report`
→ `LOCK_INTERNAL_RESULT`
→ `Human Review`
→ `Publication decision`

Remember that epistemic, review, freshness, and publication statuses remain independent.

---

## Journey 2 — Rule change

`Rule`
→ `Change Proposal`
→ `Impact Preview`
→ `Review`
→ `Authorized Decision`
→ `New Revision`
→ `Transitive Invalidation`
→ `STALE`
→ `Revalidation`

---

## Journey 3 — Claim traceability

`Claim`
→ `Contextual Inspector`
→ `Evidence`
→ `Research Artifact`
→ `Research Run`
→ `Corpus`
→ `Methodology`
→ `Trace`
→ `Reproduce`

---

## Journey 4 — Steward

`Free-form user intent`
→ `Steward command draft`
→ `Preview`
→ `Authorization`
→ `Validation`
→ `Impact`
→ `Confirmation`
→ `Execution result`
→ `Audit`

---

## Journey 5 — Prior contamination

`Blind Lab`
→ `Prior contamination detected`
→ `PRIOR_CONTAMINATED`
→ `Internal Lock blocked`
→ `Isolation explanation`
→ `Restart / remediation`

---

# Design constraints

Preserve the current Lisan visual identity.

Requirements:

- Arabic-first.
- Native RTL layout.
- IBM Plex Sans Arabic or the existing approved Arabic type system.
- Quranic text receives a dedicated readable Quranic treatment.
- Use CSS/logical RTL concepts visually.
- Preserve current epistemic color language where valid.
- Every state needs text + icon + color.
- No color-only communication.
- No semantic confidence percentage.
- No gold color implying superior epistemic truth.
- Charts must have table/text alternatives.
- Use progressive disclosure.
- Dense technical information must remain understandable.
- Do not turn research workspaces into generic admin dashboards.
- Do not turn Ask Lisan into a conventional chat UI.
- Do not make the Knowledge Graph the only way to understand dependencies.

---

# Prototype integrity constraint

Stitch is designing the **UX prototype**, not proving backend behavior.

Therefore:

- simulated transitions must be visibly prototype states,
- do not claim authorization has been cryptographically enforced,
- do not claim real provenance hashes were verified,
- do not claim real transitive invalidation ran,
- do not claim real reproduction succeeded,
- do not claim the Purity algorithm detected contamination unless using an explicitly labeled fixture,
- do not invent API contracts.

Use realistic fixtures only to demonstrate states and journeys.

---

# Preserve

Preserve and refine the current implemented screens:

- Home / Attention Center
- Ask Lisan
- Research Run Builder
- Root Workspace
- Blind Lab
- Lock flow
- STALE state
- Governance Rules Repository
- Impact Preview
- Quality / Purity
- Resource Admission
- Human Review Queue
- Knowledge Explorer
- Mass Revalidation
- Analytics / Oversight

Do not recreate these as unrelated parallel versions.

Extend them into one coherent system.

---

# Verification

Before declaring the prototype complete, build a **UX Constitution Traceability Matrix**.

Map every v4.0 acceptance criterion to:

- screen,
- component,
- state,
- interactive journey,
- implemented / partial / missing.

At minimum verify:

1. Every claim can reach its evidence and Research Run.
2. UNKNOWN / UNRESOLVED states are visible.
3. Counterevidence is first-class.
4. Four status axes remain independent.
5. No semantic confidence score exists.
6. Lock Gates are dynamic.
7. Blind Lab hides priors before lock.
8. Derived views do not increase authority.
9. Unauthorized transitions are blocked in UX.
10. Steward always previews governed commands.
11. Governing changes use Change Proposals.
12. Unadmitted corpora are visibly blocked.
13. STALE results are never presented as current truth.
14. Invalidation is traceable.
15. Reproduction is tied to revision, methodology, and corpus.
16. Graphs have textual/table alternatives.
17. Core screens are native RTL.
18. Resume does not rely on chat memory.
19. Onboarding exists.
20. Dependency impact is understandable.
21. Purity Gate blocks contaminated-result publication.
22. Purity report exposes its dimensions, reasons, and recommendations.
23. Three display levels preserve context.
24. Core components are designed for accessibility.
25. Performance-sensitive screens avoid unnecessary visual overload.
26. A Research Run can visually resume from checkpoints.
27. Governing changes are traceable to Audit Log.

Do not mark a criterion complete unless the prototype visibly demonstrates it.

---

# Success criteria

The final Stitch project should no longer be described merely as:

“18 completed screens.”

It should be demonstrably organized as one connected governed research product with:

- Global Shell
- four subject workspaces
- Blind Lab
- Hypothesis Lab
- Semantic Differentiation Lab
- Evidence / Counterevidence
- Quality Profile
- Purity Assurance
- Research Runtime
- Human Review
- Steward
- Knowledge Explorer
- Governance Control Plane
- Operations / Audit
- Provenance
- Reproducibility
- Role-aware UX
- three display levels
- History / Methodology comparison
- UI Contract Gap Register

---

# Stop condition

Stop adding new product concepts once:

1. the current 18 screens have been audited,
2. all required v4.0 UX gaps have been closed or explicitly marked `BACKEND_CONTRACT_MISSING`,
3. all required journeys are connected,
4. the Traceability Matrix has no unexplained UX gaps,
5. duplicate screens have been consolidated,
6. the existing design system remains coherent.

Do not add unrelated features.

Do not redesign completed screens merely for novelty.

---

# Return only

At the end, provide a concise completion report containing:

1. Existing screens preserved.
2. Existing screens corrected.
3. New screens/components added.
4. New interactive journeys added.
5. Constitutional issues corrected.
6. Remaining gaps caused specifically by missing backend contracts.
7. UX Constitution Traceability Matrix status.
8. Exact recommendation: `READY_FOR_USER_TESTING`, `PARTIAL`, or `GAPS_REMAIN`.

Do not call the prototype “complete” unless the traceability evidence supports that claim.