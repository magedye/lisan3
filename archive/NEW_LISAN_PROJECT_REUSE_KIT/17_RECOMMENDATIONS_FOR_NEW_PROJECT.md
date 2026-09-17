# Recommendations for the New Project

This is decision support, not final architecture or accepted methodology.

## Recommended foundations

1. **Terminology charter first.** Approve analysis units and Arabic/English definitions before prompts, schemas and UI. [TR-123]
2. **Exact Quran source identity.** Preserve canonical bytes, immutable snapshot/hash and separate normalized search keys.
3. **Minimal structural layer.** Provide token/segment/root/lemma/form and only required syntax with exact source/alignment/ambiguity.
4. **Source/field roles.** Separate Quran text, Quran structure, internal observations, model priors, external sources and discovery candidates.
5. **Reviewable AI decision record.** AI may prefer a semantic conclusion, but the record must expose scope, reasons, alternatives, evidence, counterevidence, unresolved cases, rejection condition, completeness and verification.
6. **Persistent run and execution receipts.** Bind every result to protocol/model/tool/source revisions and actual calls.
7. **Layer attribution.** Root, lexical unit, form, construction, roles, discourse/context and local meaning remain separately assignable.
8. **Falsification and hard cases.** Freeze hypotheses, execute rejection searches and preserve failed predictions.
9. **Three independent measures.** Result strength, research completeness and independent verification must never collapse.
10. **Honest pretrained-risk label.** Control supplied sources but do not claim the model has no prior traditional knowledge.

These foundations are cheaper to build early than retrofit after semantic results accumulate. [TR-124]

## Recommended adaptations

- Adapt ResearchRun into a light research-case record without Lisan publication/governance states.
- Adapt Blind Lab into `INTERNAL_ANALYSIS` and `EXTERNAL_COMPARISON` source modes with an immutable internal snapshot.
- Adapt AIExecutionRecord into per-invocation receipts.
- Adapt Root Core into root-concept hypotheses over explicit lexical units/branches.
- Adapt Distinctive Residue into an evidence-backed multidimensional distinguishing feature set, with no-difference allowed.
- Adapt EvidenceResolver into identity/role resolution; semantic support remains an AI/human judgment.
- Adapt Pydantic/Pydantic AI only where Gem/Opal cannot enforce/export the same trust boundary.
- Adapt legacy freeze/influence-log and six-layer ideas into a short internal-snapshot → external-comparison → revised-decision lineage. [TR-125]

## Recommended experiments

1. **Terminology usability:** can two researchers classify the same examples consistently?
2. **Structural source qualification:** can exact occurrences/forms/constructions be reproduced with ambiguity preserved?
3. **AI decision quality:** can the model prefer a meaning and survive held-out hard cases without source fabrication?
4. **Layer-confound suite:** root/form/construction/context attribution under controlled counterexamples.
5. **No-invented-distinction suite:** different forms and near neighbors where no supported difference exists.
6. **Pretrained-prior sensitivity:** compare source-blind, source-exposed, different-model and human reviews.
7. **Completeness usability:** do multidimensional counts predict omitted decisive cases better than one score?
8. **Gem/Opal capability proof:** export, resume, branching, Tool receipts, source controls and immutable revisions.
9. **Retrieval baseline:** exact/manual candidates first; vector only if measured recall gap exists.
10. **Confidence calibration:** collect component predictions and later outcomes before assigning weights. [TR-126]

## Recommended deferrals

- final architecture;
- graph/vector databases and universal embeddings;
- external RAG framework;
- LangGraph or multiple orchestration layers;
- formal policy engines;
- DSPy/prompt optimization;
- four-axis lifecycle and publication system;
- Steward/role hierarchy;
- complete public cards/dictionary;
- numeric confidence weights;
- broad multi-root corpus production.

## Major risks

1. Calling model-mediated induction “purely internal” despite parametric priors.
2. Treating verified structure as semantic evidence beyond its allowed role.
3. Assuming a single root concept before lexical-unit analysis.
4. Inventing semantic differences because forms or neighbor labels differ.
5. Using complete occurrence counts to hide shallow analysis.
6. Turning retrieval similarity into confidence.
7. Letting external agreement retroactively support an internal conclusion.
8. Storing prose without proposition-level evidence relations.
9. Building governance/infrastructure before method capability.
10. Mistaking multiple same-model Agents for independent verification.
11. Treating schema validation as semantic validation.
12. Losing source/protocol/result identity during Gem/Opal export or retry. [TR-127]

## Suggested first prototype

Build the smallest experiment that tests the central hypothesis: **Can an AI produce a reviewable, evidence-grounded preferred Quranic root/local meaning while retaining freedom to infer and honestly preserving alternatives and uncertainty?** [TR-128]

Scope:

- one verified Quran snapshot;
- one qualified minimal morphology source or transparently provisional manual annotation set;
- one medium-size root with form/construction diversity;
- one close semantic neighbor;
- exact occurrence inventory;
- eight lightweight records: SourceIdentity, Occurrence, ResearchRun, Observation, Hypothesis, EvidenceRelation, SemanticDecision and ExecutionReceipt;
- Skills for analysis unit, collection, form/construction, hypotheses, neighbor comparison, falsification and synthesis;
- two reasoning roles: induction/decision and adversarial challenge;
- one held-out difficult-case set;
- internal result snapshot, then one controlled dictionary/tafsir comparison;
- human review of citations, layer assignments and preference explanation.

Success is not “a beautiful root definition.” Success is: no fabricated evidence/tool use; exact citations; visible layer attribution; genuine alternatives; executed falsification; separate strength/completeness/verification; and a decision that can narrow or remain unresolved. [TR-129]

Do not start by rebuilding Lisan3. Start by proving this research loop on one root, then let observed bottlenecks decide whether Gem, Opal or a lightweight engine owns each boundary. [TR-130]

## Exact recommended next owner decision

Approve or revise the **prototype decision envelope**—(a) candidate controlled terminology, (b) the eight-record minimum data boundary, (c) one-root/one-neighbor scope, (d) internal-snapshot then external-comparison rule, and (e) declared independence/pretrained-risk language—before choosing final Gem/Opal/engine architecture or authorizing implementation.
