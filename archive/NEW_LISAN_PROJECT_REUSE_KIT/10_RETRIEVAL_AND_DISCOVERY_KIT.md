# Retrieval and Discovery Kit

## Reusable hierarchy

```text
Exact source lookup
    → resolved Quran/structure artifact

Vector / graph / AI discovery
    → candidate
    → source resolution
    → evidence candidate
    → semantic evaluation by AI
    → preferred / competing / unresolved conclusion
```

Lisan3’s formula “retrieval discovers candidates; evidence resolves them” remains valuable even when AI has more decision authority. The change is that AI may issue the final bounded semantic preference after resolution and challenge; retrieval still does not manufacture source evidence. [TR-073]

## Exact retrieval

Use exact retrieval for Quran text/verse identity, target occurrences, root/lemma/form where verified, structural annotations, and known evidence references. It should return source identity, exact locator, revision/hash, query rules, ambiguity and exclusions. [TR-074]

Important Arabic concerns for the new project:

- preserve canonical text bytes separately from normalized search keys;
- declare diacritic, hamza, alif/ya, ta marbuta and orthographic matching policies;
- never overwrite source text with normalized text;
- distinguish surface match, lemma match and root match;
- preserve token/segment ambiguity and multi-segment words.

## Candidate versus evidence

| Item | Can generate a research candidate? | Can establish source fact? | Can directly support semantic conclusion? |
|---|---:|---:|---:|
| Exact Quran record | Yes | Yes, within source role | Yes, through an explicit evidence relation |
| Verified structural annotation | Yes | Yes, structurally | Yes for structural premises, not semantic gloss |
| Vector result | Yes | No | No until source-resolved and semantically evaluated |
| Graph path | Yes | Only if it projects authoritative dependencies | Not by connectivity alone |
| AI suggestion | Yes | No | Only as reasoning attached to source evidence, not as evidence itself |
| External retrieved passage | Yes | Yes about that external source | Only in declared external-comparison scope |

## Vector discovery

Potential uses: semantic-neighbor candidates, contextual outliers, counterevidence candidates and research-artifact retrieval. Preserve embedding space, model/revision, preprocessing/config hash, source revision/hash, index revision, distance/similarity and reason. [TR-075]

Do not use:

- nearest K as the methodological neighbor set;
- aggregate metric to excuse a failing task/space;
- similarity as semantic confidence;
- one embedding space for incomparable entity types without evidence;
- external-source vectors inside an internal Quran index;
- stale vectors after source/model/config changes.

Lisan3’s R2 benchmark is an observed warning: the aggregate leader still failed `CLAIM`, `STRUCTURAL_PROFILE` and a `ROOT_CANDIDATE` false-positive trap. No evaluated model was adopted. [TR-076]

## Graph discovery

Potential uses: evidence/dependency paths, circular-support detection, downstream invalidation, provenance browsing and candidate relation exploration. Every edge needs type, origin, status and provenance. A rebuildable projection is safer than a second hand-edited truth store. [TR-077]

For the first prototype, direct dependency records and ordinary traversal are enough. Add a graph only when repeated multi-hop queries or three or more consumers justify it.

## EvidenceResolver candidate contract

Input:

```yaml
candidate_id: "..."
source_layer: "EXACT | VECTOR | GRAPH | EXTERNAL | AI"
entity_ref: "..."
candidate_provenance: {...}
```

Output:

```yaml
resolution_status: "RESOLVED | REJECTED | AMBIGUOUS | SOURCE_UNAVAILABLE"
source_identity: "..."
exact_locator: "..."
artifact_hash: "..."
allowed_uses: ["..."]
resolved_content_ref: "..."
ambiguities: ["..."]
resolution_receipt: "..."
```

Resolution proves identity/role, not that content supports a semantic hypothesis. That support relation is a separate AI/human judgment. [TR-078]

## Change under higher AI authority

Keep unchanged:

- source/candidate labels;
- exact resolution;
- provenance;
- separate scores and confidence;
- index/source isolation;
- stale/rebuild behavior.

Change:

- after resolution, AI may decide that a candidate is supporting evidence, counterevidence, irrelevant, or ambiguous;
- AI may select semantic neighbors and prefer a conclusion;
- the decision record must cite resolved inputs and explain why retrieval rank did or did not matter;
- an unresolved resolver output cannot be silently upgraded by AI.

## Minimal retrieval experiment

Start with exact retrieval and a manually curated candidate-neighbor pool. Measure missed candidates and analyst effort. Add vector discovery only if there is a demonstrated recall problem, then evaluate with hard negatives and per-task metrics. Add graph projection later for provenance/circularity, not semantic discovery theater. [TR-079]

## Adversarial tests

1. Highest-similarity item is a semantic false positive.
2. A vector index contains a forbidden external definition; internal query cannot expose it.
3. Graph visual proximity is not an edge or semantic relation.
4. A candidate resolves to the wrong corpus revision and must fail.
5. Same entity appears in two embedding spaces; cross-space comparison fails.
6. Source/model config changes; stale index is excluded.
7. Candidate is resolved correctly but judged irrelevant; resolver does not force support.
8. Exact source conflicts with a retrieval suggestion; source record governs the factual premise.
