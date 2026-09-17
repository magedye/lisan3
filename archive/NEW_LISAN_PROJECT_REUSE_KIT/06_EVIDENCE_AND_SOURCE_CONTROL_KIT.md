# Evidence and Source Control Kit

## Governing distinction

Lisan3’s strongest reusable boundary is not “AI may never decide.” It is that source identity, source role, access stage, evidence type and execution reality must remain explicit. The new project can give AI greater semantic decision authority without letting it fabricate or relabel evidence. [TR-038]

## Candidate source/evidence taxonomy

| Source or artifact | Candidate type | Allowed internal-induction use | Allowed later use | Principal hazard |
|---|---|---|---|---|
| Verified Quran text | `QURAN_TEXT_PRIMARY` | Direct witness, exact citation, context | Always | Text/version/normalization drift |
| Verified structural annotation | `QURAN_STRUCTURE_AUXILIARY` | Root/lemma/form/POS/permitted syntax, with source identity and ambiguity | Always within fields | Gloss/ontology leakage; alignment error |
| Internal structural observation | `INTERNAL_OBSERVATION` | Directly, if derived from permitted sources and tool receipts | Always | Interpretation embedded in “observation” |
| Internal interpretation | `INTERNAL_INTERPRETATION` | Generates hypotheses, never primary evidence by itself | Review/explanation | Circular self-support |
| Internal hypothesis | `INTERNAL_HYPOTHESIS` | Research object to test | Revision/decision | Used as its own evidence |
| Previous AI result | `PRIOR_AI_RESULT` | Normally hidden or explicitly declared in cumulative mode | Comparison/challenge/reuse with dependency | Anchoring/circular confirmation |
| Model pretrained knowledge | `MODEL_PARAMETRIC_PRIOR` | Question/hypothesis generation only; never reported as executed lookup or Quran witness | Declared comparative reasoning | Unobservable source mixing and false purity claims |
| Dictionary | `EXTERNAL_DICTIONARY` | Not internal Quran evidence | Later comparison/hypothesis/challenge | Dictionary-first framing |
| Tafsir | `EXTERNAL_TAFSIR` | Not internal Quran evidence | Later interpretive comparison/challenge | Traditional conclusion retroactively supports internal result |
| Historical Arabic/poetry | `EXTERNAL_HISTORICAL_USAGE` | Not Quran-internal evidence | Diachronic/comparative evidence with its own scope | Chronology/register/source authenticity |
| External research | `EXTERNAL_RESEARCH` | Not internal evidence | Methods/linguistic challenge | Authority laundering through citation |
| Retrieval candidate | `DISCOVERY_CANDIDATE` | Candidate only until source-resolved | Research queue | Similarity/path treated as evidence |
| Tool output | `EXECUTION_OUTPUT` | Only within tool/source capability | Reproducibility | Tool configured vs executed; parser error |

## Lisan3 mechanisms worth reusing

### 1. Source identity before trust

Tanzil handling binds source ID, version, bytes/hash, format, verse identity index, counts, provenance and snapshot. Import validation and production activation are separate in Lisan3; the new project may simplify lifecycle names but should preserve immutable identity and exact readback. [TR-039]

### 2. Field-level source roles

QAC is a strong negative lesson: a corpus can contain useful morphology and prohibited gloss/ontology at once. Whole-source labels are insufficient; permit fields and transformations individually. [TR-040]

### 3. Source-resolved evidence

Hybrid Retrieval requires candidates to return through an EvidenceResolver to an exact source artifact. The resolver is canonical architecture but not implemented in current R3. Reuse the boundary, not the completion claim. [TR-041]

### 4. Access isolation across derived indexes

Blind Lab rules apply to APIs, AI context, graphs, vectors and cached embeddings. This closes an important bypass class: hiding a forbidden source API while exposing its embedding/index is not isolation. [TR-042]

### 5. Blocked versus disclosed access

A denied read is evidence that enforcement ran; it is not actual contamination. Lisan3 stores an isolation event and changes contamination only after actual exposure. [TR-043]

### 6. Immutable method/source revisions

`MethodologyRevision` binds source path/hash and prevents silent in-place provenance mutation. For the new project, bind each result to protocol/Skill revision and exact source profile even without Lisan governance machinery. [TR-044]

### 7. Tool reality

The Semantic Skill forbids reporting a simulated validator as passed. Current `ToolDispatcher` only invokes registered tools, but should be extended because failures are not logged and a dummy corpus search is registered. Reuse the principle, adapt the implementation. [TR-045]

## Candidate source identity record

```yaml
source_id: "stable identifier"
source_class: "QURAN_TEXT_PRIMARY | QURAN_STRUCTURE_AUXILIARY | EXTERNAL_..."
title: "..."
version_or_revision: "..."
artifact_ref: "immutable/local controlled reference"
sha256: "..."
license_and_use_status: "verified | pending | restricted"
field_roles:
  - field: "root"
    allowed_use: ["INTERNAL_STRUCTURE"]
  - field: "gloss"
    allowed_use: ["POST_INTERNAL_COMPARISON"]
    prohibited_use: ["INTERNAL_EVIDENCE"]
normalization_policy: "..."
alignment_policy: "..."
known_gaps: ["..."]
```

Agent recommendation; derived from Tanzil/QAC lessons rather than copied wholesale. [TR-046]

## Minimum evidence structure for an AI-issued conclusion

At minimum, a reviewable semantic decision needs: [TR-047]

1. result ID, revision and target/analysis unit;
2. exact Quran/corpus snapshot and source-role profile;
3. conclusion type, statement and scope;
4. AI decision status: preferred / competing / unresolved;
5. primary witness locators and resolved observations;
6. explicit layer-attribution map;
7. supporting evidence relations stating what each item supports;
8. strongest counterevidence and unresolved cases;
9. serious alternatives and why they were not preferred;
10. rejection/narrowing/reopen condition plus whether it was executed;
11. completeness vector with denominators/exclusions;
12. result-strength components, never raw model self-confidence alone;
13. independent-verification state and independence class;
14. model/provider/prompt/Skill/context/tool execution receipts;
15. external-influence record, including pretrained-exposure risk classification;
16. concise decision reasons and change history.

## Contamination detection candidates

### Deterministic detection

- access-control allowlist/denylist by source/field/stage;
- complete server-side source/tool access log;
- content hashes and dependency links for every read;
- output phrase/reference matching against actually opened external sources;
- support-graph checks for external dependencies before internal snapshot;
- separate indexes/namespaces and query APIs;
- frozen internal hypothesis/result revision before external comparison.

### Probabilistic/adversarial detection

- compare outputs from source-blind and source-exposed runs;
- seed external definitions as canaries in a controlled eval and detect leakage;
- ask for source attribution and penalize unverifiable attribution;
- use a model with declared training provenance where possible;
- compare model families or a human verifier for sensitivity;
- challenge the result with deliberately conflicting traditional definitions.

These can detect evidence of contamination; none proves a pretrained model contains no relevant prior. [TR-048]

## Post-analysis external comparison

Recommended flow: [TR-049]

```text
verified Quran + permitted structure
→ internal observations
→ internal hypotheses and preferred result snapshot
→ freeze snapshot/hash
→ open declared external sources
→ comparison/challenge record
→ revised or retained preferred conclusion
→ separate internal-support and external-support lists
```

AI may change its judgment after comparison. The system must show exactly what changed and must not relabel external agreement as Quran-internal evidence.

## What not to copy

- Do not copy exact Lisan3 QAC/Tanzil status names as new-project authority.
- Do not require owner/release/publication approval fields for every research artifact.
- Do not treat current QAC adapter or alignment service as production-ready; the canonical documents explicitly describe the real importer/persistence gap.
- Do not claim complete Purity from the current evaluator; seven dimensions are hard-coded `NOT_EVALUATED`.
- Do not use a model-manifest declaration as proof of no pretrained exposure.

## Adoption tests

1. A structural source containing a gloss must expose structure but never the gloss in internal mode.
2. A vector candidate must not become evidence without exact source resolution.
3. A forbidden read that is blocked must create a denied receipt but not contamination.
4. An actually disclosed forbidden source must mark the affected result lineage and force review/revision.
5. A model statement claiming a tool ran must fail unless a server-owned receipt exists.
6. An unknown source/field role must fail closed for internal evidence but may remain a labeled research candidate.
7. External comparison must never mutate the frozen internal snapshot; it creates a descendant revision.
