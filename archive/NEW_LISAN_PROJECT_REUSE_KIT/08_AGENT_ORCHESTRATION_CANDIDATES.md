# Agent Orchestration Candidates

## Governing recommendation

Use Skills for stable method, deterministic Tools for factual/reproducible operations, and Agents only for roles whose independent context, objective, or adversarial posture materially changes the work. Do not create one Agent per document section. [TR-064]

Multiple Agents using the same underlying model, prompt family, retrieval context and evidence are **not automatically independent evidence**. At best they provide repeated reasoning samples. Independence must name what differs: hidden evidence, model family, prompt, seed, source access, human reviewer, data split, or organizational authority. Lisan3’s fresh read-only review boundary is a governance example, not proof of semantic independence. [TR-065]

## Candidate roles

| Role | Classification | Genuine value | Main risk | Recommendation |
|---|---|---|---|---|
| Research orchestrator | `ADAPT` | Selects Skills, checks dependencies, resumes runs, decides next informative test | Becomes a second methodology or state system | One thin orchestrator; state transitions are explicit and tool-read, not caller-asserted. |
| Induction agent | `ADAPT` | Builds internal hypotheses from Quran/structure-only context | Pretrained priors remain latent despite source isolation | Use a strict internal source profile and disclose parametric-prior risk; do not call it cognitively pure. |
| Hypothesis agent | `REFERENCE_ONLY` | Divergent alternatives can reduce premature convergence | Produces ceremonial paraphrases and cost | Usually a Skill within the induction Agent; separate only for difficult/high-stakes roots. |
| Adversarial/falsification agent | `REUSE_AS_IS` | Opposed objective and withheld preferred rationale can expose counterexamples | Same-model correlated blind spots | Separate context/objective; give hypothesis statement and evidence space, not persuasive synthesis prose. |
| Semantic-difference agent | `ADAPT` | Focused comparison across dimensions, matched cases and no-difference outcome | Invents distinctions to justify its role | Use only for essential neighbors; explicit `NO_DIFFERENCE_ESTABLISHED`. |
| Source-contamination reviewer | `ADAPT` | Reviews access/dependency logs and external influence separately from semantic appeal | Cannot prove absence of pretrained knowledge | Combine deterministic log checks with risk assessment; separate from synthesis. |
| Independent blind verifier | `OPEN_QUESTION` | Held-out context/model/human can test reproducibility and anchoring | False independence when same model/context is reused | Define independence classes first; strongest early option is a human or different model family on held-out evidence. |
| Synthesis/decision agent | `ADAPT` | New project explicitly permits AI to prefer semantic conclusions | Overweights polished narratives or majority votes | One accountable decision record; consumes evidence, alternatives and falsification, and explains disagreement. |

## Recommended minimum orchestration

```text
Research Orchestrator
    ├── deterministic preflight / occurrence / structure Tools
    ├── Induction Agent using fixed analysis Skills
    ├── Adversarial Agent using falsification Skill and restricted context
    ├── deterministic evidence / coverage / provenance Tools
    └── Synthesis Agent issuing the bounded decision

Optional after decision:
    ├── External Comparison Agent
    └── Independent Verifier with declared independence class
```

This keeps three genuinely different reasoning objectives without reproducing Lisan3’s whole governance organization. [TR-066]

## What should be a Skill

- analysis-unit resolution;
- occurrence-collection protocol;
- derivational/form/construction analysis;
- local-meaning and root-concept method;
- neighbor comparison and difference dimensions;
- hypothesis generation;
- falsification/counterevidence;
- contamination review;
- result synthesis.

Skills define procedures and outputs. They do not determine that a source exists, that a query ran, or that a conclusion is accepted.

## What should be an Agent

- orchestration when a run branches or needs next-test selection;
- internal induction for nontrivial research;
- adversarial challenge with a deliberately opposed objective/context;
- synthesis/decision because the project explicitly grants AI semantic preference;
- optional external comparison and independent verification when their contexts are genuinely isolated.

## What should remain deterministic Tools

- corpus snapshot verification and exact text lookup;
- token/root/lemma/form occurrence retrieval;
- structural-source parsing/alignment and ambiguity preservation;
- source/field role enforcement;
- access logging and content delivery;
- coverage calculation;
- evidence/reference resolution;
- hash/manifest creation;
- schema validation;
- dependency and cycle detection;
- execution receipt generation;
- evaluation dataset scoring.

## Agent state and authority

The orchestrator must read persisted state and invoke server-owned transitions; it must not accept caller-supplied “completed,” “verified,” or source-authority flags. Lisan3’s computed gates and run-admission policy demonstrate the general rule that valid state is derived from persisted evidence rather than trusted request values. The new project can use a simpler state model while retaining this trust boundary. [TR-067]

## Gem and Opal placement

Repository evidence establishes no Gem/Opal capabilities. Candidate placement is therefore conditional:

- Gem: conversation, exploration, explanation, user choices, and display of evidence/provenance if it can preserve stable run/result identities.
- Opal: Skill/workflow orchestration if it can persist branches, retries, artifacts and tool receipts without opaque state.
- Lightweight engine: required only for capabilities Gem/Opal cannot reliably enforce—source identity/roles, exact corpus/structure retrieval, immutable receipts, schemas, coverage, and durable result lineage.

Before selection, run a capability proof with export/readback, failure recovery, tool authorization, artifact hashing and branch resume. [TR-068]

## Independence labels

| Label | Meaning |
|---|---|
| `REPEAT_SAME_CONFIGURATION` | Same model/context/protocol; reproducibility sample only. |
| `CONTEXT_BLIND_REVIEW` | Preferred rationale/result hidden; evidence may be shared. |
| `HELD_OUT_EVIDENCE_REVIEW` | Reviewer receives a challenge/holdout set not used in synthesis. |
| `MODEL_FAMILY_INDEPENDENT` | Different model family/provider; training overlap may remain. |
| `HUMAN_INDEPENDENT` | Named human reviews without being the original analyst. |
| `SOURCE_INDEPENDENT` | Uses independently acquired/verified source artifact. |

Do not compress these into a Boolean `independent=true`. [TR-069]
