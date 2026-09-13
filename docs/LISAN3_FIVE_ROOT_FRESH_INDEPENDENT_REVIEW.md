# Five-Root Fresh Independent Semantic Review

Date: 2026-09-13  
Stage: B — fresh independent semantic review, followed by post-freeze Batch 07 comparison  
Candidate branch: `five-root-governed-requalification`  
Candidate HEAD inspected before review: `de338810159ebbb3a5ffacc4d2d3551b7a75f95d`

## Outcome

The fresh review verifies three exact DB-native claim revisions at their stated scope and requires corrective research for two. The corrective findings are hard source-boundary failures in the exact persisted revisions; they are not merely wording preferences.

| Root | Current claim revision | Scope / sidecar kind / strength | Fresh verdict | Batch 07 relationship |
|---|---|---|---|---|
| ع ص و (`ESw`) | `jud_9506cecf@1` | `REPRESENTATIVE` / `LEXICALIZED_CLASS` / `STRONG` | `VERIFIED_AT_SCOPE` | `INDEPENDENT_CONVERGENCE` |
| د ن و (`dnw`) | `jud_6733070a@1` | `REPRESENTATIVE` / `ROOT_GENERALIZATION` / `MODERATE` | `CORRECTIVE_RESEARCH_REQUIRED` | `NEW_CLAIM_NARROWER` |
| ف ل ح (`flH`) | `jud_50b6a890@1` | `REPRESENTATIVE` / `DERIVATIONAL_FAMILY` / `MODERATE` | `CORRECTIVE_RESEARCH_REQUIRED` | `PARTIAL_CONVERGENCE` |
| ف و ه (`fwh`) | `jud_303cd726@1` | `UNIVERSAL` / `LEXICALIZED_CLASS` / `STRONG` | `VERIFIED_AT_SCOPE` | `NEW_CLAIM_NARROWER` |
| غ ل م (`glm`) | `jud_d51f1e74@1` | `REPRESENTATIVE` / `LEXICALIZED_CLASS` / `MODERATE` | `VERIFIED_AT_SCOPE` | `PARTIAL_CONVERGENCE` |

`claim_scope_kind` is identified as a sidecar classification because it is present in `five_root_produced_claims.json` but absent from the persisted `semantic_claims` row and the judgment API response.

## Candidate and custody

The review began by resolving Git, the working tree, and the authoritative runtime before semantic inspection:

- Branch: `five-root-governed-requalification`.
- HEAD: `de338810159ebbb3a5ffacc4d2d3551b7a75f95d`.
- Authoritative runtime: `lisanapp.db`, 24,018,944 bytes.
- Database SHA-256 before review: `34dcc0a2a2fb3ae8c3774b681545459dfebd36df8c58a181d86c683e6c6eae68`.
- Corpus snapshot: `snap_tanzil_1_1_ac0724796cbb`.
- Canonical Tanzil text SHA-256: `ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af`.
- Methodology revision: `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`.
- Methodology source SHA-256: `01784170cac4e715c1477cb6a04a2c34b21c4bdb91705aa1eb6b2a896efcedbd`.
- The methodology registry row was current and eligible.
- Existing untracked owner artifacts were recorded and left untouched. No reset, clean, stash, staging, commit, or other custody-changing Git action was performed.

The producer mirrors used before comparison were:

- `docs/evidence/requalification/five_root_produced_claims.json`
- `docs/evidence/requalification/five_root_governed_state.json`
- `docs/evidence/requalification/five_root_overclaim_sweep.json`
- `docs/evidence/requalification/five_root_structural_manifest.json`

Their role was evidentiary only; the database remained authoritative.

## Independence and freeze sequence

The five verdicts were derived without opening any of the five Batch 07 root artifacts, the Batch 07 semantic report, its historical independent verdict, or its owner decisions. No web source, translation, lexicon, dictionary, tafsir, or prior semantic conclusion was used as Quranic authority.

Every current occurrence was reconstructed from `lisanapp.db` by joining `CONFIRMED` `structural_tokens` to the canonical Tanzil text in `corpus_occurrences`. Only after all five verdicts were complete was the blind artifact written and parsed:

- Frozen artifact: `docs/evidence/requalification/five_root_fresh_independent_verdicts.json`
- Size: 22,777 bytes
- SHA-256: `9a1012e1973f047c7a2d44ec3d4feddc2faabb171c4711170e9c855e5601c754`
- `batch_07_artifacts_opened_before_freeze = false`

The freeze was not modified after Batch 07 was opened. Historical comparison therefore could not change the verdicts.

## Review method and executed checks

For each root, the reviewer inspected every verse occurrence and independently addressed the required questions: contribution, unity versus multiplicity, strongest challenge, lexicalization, narrower family/class scope, tempting contextual additions, falsifier, and reopen condition. The pass also checked scope, scope kind, strength, supporting evidence, counterevidence, hard and unresolved cases, semantic boundaries, competitor, counterexample, falsification, completeness, source isolation, and revision binding.

The occurrence census was:

| Root | Confirmed / inspected | Form inventory | Word-ref set SHA-256 |
|---|---:|---|---|
| `ESw` | 12 / 12 | `N` × 12 | `c3c96de1c2929b352adf3ef7bd5f838b93feb4355aa0c40e9f913437d10b9688` |
| `dnw` | 133 / 133 | `ADJ` × 76, `N` × 54, `T` × 1, `V` × 2 | `071b60f7c750c7639e026fa2abec5eca42561c0fa7145fb57d54cc83ac7f2f76` |
| `flH` | 40 / 40 | `N(IV)` × 13, `V(IV)` × 27 | `674ecee0235b3752df90ea588b045d71dc735b0cd494f4e487e20c2bf2602450` |
| `fwh` | 13 / 13 | `N` × 13 | `651f5ec4b6c988ab4aa7a27954fa76f12a42e1d15509fb9435676ecd5515097e` |
| `glm` | 13 / 13 | `N` × 13 | `6f2b23df77197860cf39804276fd26c667d9331785a17211b18cff18a69ba523` |

All five structural sets exactly matched the manifest, all observation sets exactly matched the confirmed occurrence sets, and every evidence reference resolved to the same snapshot and intended root.

The four required live reads were executed for every claim/run: judgment, workspace, provenance, and manifest. All 20 requests returned HTTP 200. Workspaces exposed the expected 12/133/40/13/13 observations and current Research Judgments. Each run persisted `ESTABLISHED + CLEAN` isolation with `input_manifest`, `attesting_actor`, `attested_at`, and `audit_ref`. All claims were revision 1, non-canonical, and without a VerificationRecord.

The eight overclaim diagnostics were independently rerun at content level. `CONTEXTUAL_LEAKAGE`, `FORCED_UNIFICATION`, `GENERIC_OVEREXTRACTION`, `LETTER_SEMANTICS_OVERRELIANCE`, and `CIRCULAR_CONFIRMATION` were clean for the three verified claims. Producer-trace conclusions for dictionary-first, heritage, and tafsir contamination remain limited by the missing execution records described below. For `dnw` and `flH`, content-level inspection found actual prohibited external semantic material, so the hard boundary fails regardless of producer intent.

## Per-root findings

### ع ص و (`ESw`) — `VERIFIED_AT_SCOPE`

All 12 tokens are the same nominal عَصَا/عِصِيّ class. The ordinary use-list in 20:18 anchors a held staff/rod; the magicians' plural staffs in 20:66 and 26:44, coordinated against ropes, defeat Moses-only, inherently miraculous, authority, and generic sorcery-prop readings. Casting, striking, transformation, swallowing, sea-splitting, and water emergence are supplied by verbs and narrative consequences.

No occurrence defeats the concrete-object reading. The falsifier remains a confirmed ع ص و token that is not this object, or an incompatible non-nominal derivation. `REPRESENTATIVE / LEXICALIZED_CLASS / STRONG` is warranted because the census is complete for the noun but cannot establish a productive whole-root universal.

Batch 07 independently reached the same nucleus with the same scope, kind, and strength: `INDEPENDENT_CONVERGENCE`. This agreement supports, but does not transfer authority to, `jud_9506cecf@1`.

### د ن و (`dnw`) — `CORRECTIVE_RESEARCH_REQUIRED`

The Quran-internal evidence supports a representative proximity/lowness nucleus. Direct anchors include دنا/أدنى in 53:8–9, الدنيا versus القصوى in 8:42, دانية in reachable fruit/shade frames, and scalar أدنى opposed to أكبر/أكثر or constrained by an explicit quantity. The dominant الدنيا class is heavily lexicalized; the أدنى+أن series is constructional; 2:61 is the strongest value-scale pressure case. These facts support `REPRESENTATIVE / ROOT_GENERALIZATION / MODERATE`, not a universal claim that the root contribution is equally live in every clause.

The exact revision nevertheless introduces a possible “homophonous baseness root d-n-'” in its boundary, strongest counterexample, strongest competitor, and reopen logic, while admitting that the packet cannot establish it. The admitted structural population contains no such alternate root and no resolvable Quran-internal evidence supports the injected meaning. This is a material source-boundary violation and contradicts the run's `CLEAN` isolation attestation.

Correction requires a new clean run/revision that retains at most the Quran-supported representative proximity/lowness account, preserves the الدنيا and أدنى+أن boundaries, removes the alternate-root assertion everywhere unless a future admitted Quran-internal artifact establishes it, rebuilds competitor/counterexample/falsification/reopen logic, re-attests isolation, and records the actual AI execution trace.

Batch 07 was `UNIVERSAL / ROOT_GENERALIZATION / STRONG` and treated temporal, scalar, value, and proximity-to-outcome readings as one productive relation. The current claim is materially narrower: `NEW_CLAIM_NARROWER`. Historical verification does not cure the current revision's source defect.

### ف ل ح (`flH`) — `CORRECTIVE_RESEARCH_REQUIRED`

All 40 tokens are Form IV. The distribution independently supports a thin family-level predicate: the person or class attains, or is denied, the contextually relevant favorable outcome. The worldly contest in 20:64, the sorcerer statement in 20:69, and the coercion/survival frame in 18:20 defeat a salvation-only or inherently moralized nucleus while retaining the thin outcome relation. Because no other form is attested, `REPRESENTATIVE / DERIVATIONAL_FAMILY / MODERATE` is the maximum supported claim.

The exact revision explicitly invokes “the concrete/agricultural sense a dictionary would list” and repeatedly adds unattested till/cleave/split-soil/plowman semantics to its boundary, rejection condition, failure consequence, and reopen conditions. No admitted occurrence supplies that branch. This is a direct dictionary-first/source-isolation failure inside the persisted Research Judgment and contradicts its `CLEAN` attestation.

Correction requires a new clean Quran-only Form-IV revision with every dictionary/agricultural assertion removed, followed by rebuilt rejection, competitor, counterexample, falsification, and reopen logic, renewed isolation attestation, and an actual execution trace.

Batch 07 agrees on the thin Form-IV outcome family and the decisive 20:64/20:69 boundary, but used `STRONG` and itself contains the agrarian contrast. The semantic nucleus converges while the exact current revision fails: `PARTIAL_CONVERGENCE`.

### ف و ه (`fwh`) — `VERIFIED_AT_SCOPE`

All 13 tokens are the noun فاه/أفواه. Water reaching the mouth in 13:14, hands placed in mouths in 14:9, and sealing mouths in 36:65 establish the concrete oral aperture without relying on speech contexts. In the remaining tokens, saying, emerging, appearing, extinguishing, the `bi-`/`min-` frames, and heart/breast/truth contrasts supply utterance, insincerity, hatred, or futile opposition.

The six recorded counterevidence references were treated as real pressure cases and resolved rather than ignored. The extinguishing image in 61:8/9:32 is the strongest counterexample candidate, but the organ remains the instrument and no independent abstract speech sense is forced. A token for which the physical mouth cannot fill the noun slot, or a new incompatible derivation, would falsify the claim.

`UNIVERSAL / LEXICALIZED_CLASS / STRONG` is verified only over the complete currently attested noun class in this snapshot. It is not a productive whole-root universal. Batch 07 used `ROOT_GENERALIZATION`; the current kind is therefore `NEW_CLAIM_NARROWER` despite semantic convergence on “mouth.”

### غ ل م (`glm`) — `VERIFIED_AT_SCOPE`

The review was rebuilt from all 13 current occurrences despite the producer-orchestrator's disclosed incidental historical exposure. All tokens are nominal غلام/غلامين/غلمان. The two غلامين in 18:82 have not yet reached أشدهما; the promised-child sequences in 19 and 37 and the cohort at 52:24 support youth. Male identity is internally confirmed within those sequences, including عيسى ابن مريم at 19:34 and يا بني at 37:102.

Sonship is not lexical: 12:19–21, 18:74–80, and 52:24 use the noun outside a filial relation. Service in 52:24 is supplied by يطوف; commodity status in 12:19 is predicated separately. The promised/unborn uses widen the realization of the class, and 18:80 plus 52:24 leave the precise upper age boundary underdetermined. That uncertainty supports `MODERATE`, not rejection.

The result is `REPRESENTATIVE / LEXICALIZED_CLASS / MODERATE`. Batch 07 shared the thin young-male class and the same representative lexical kind but graded it `STRONG` and asserted a firmer pre-maturity boundary: `PARTIAL_CONVERGENCE`.

## Batch 07 comparison and historical owner decision

Only after the blind SHA was frozen were the five historical root artifacts, the Batch 07 independent review, and the owner acceptance attempt opened. Their pre-comparison SHA-256 values were:

| Artifact | SHA-256 |
|---|---|
| `artifacts/semantic-campaign/roots/E_53_w.json` | `f19863141c842606258a7de3ded9c62d22733eefe7ae5fbab326394c5378ff23` |
| `artifacts/semantic-campaign/roots/dnw.json` | `3de4b1c875a74909df9b6c0a32db65867f112c762128dc2edf4084584c7306ce` |
| `artifacts/semantic-campaign/roots/fl_48_.json` | `93824ef650f53116a22387f17ef266ec18896ff00c2fa139fae90f8584b32af8` |
| `artifacts/semantic-campaign/roots/fwh.json` | `4aaa428e031a09f329f8dfba6ec8e1222cdaef3278811a0a63065086cb324e44` |
| `artifacts/semantic-campaign/roots/glm.json` | `4018dfcc3b688a7b5392c43c12b49622e1de7f3151563ff92a5c547059e03d6b` |

The historical Batch 07 review classified all five `VERIFIED_AT_SCOPE`. The historical owner then supplied `VERIFY_AT_SCOPE` for all five, but those claims were file-based: no SemanticClaim, claim ID, integer revision, VerificationRecord, or accepted canonical transition existed. The recorded acceptance attempt ended `OWNER_CANONICAL_ACCEPTANCE_TRANSITION_BLOCKED`, with zero claims created, zero verification records created, and zero canonical accepted transitions.

Those historical decisions do not transfer to any current DB-native claim revision. In particular, they cannot override `CORRECTIVE_RESEARCH_REQUIRED` for `dnw@1` or `flH@1`, nor can historical convergence create verification authority for the other three. The owner must decide each exact current claim/revision anew.

## Limitations

- All five current runs contain zero `ai_execution_records`. Producer prompts, inputs, and invoked tools therefore cannot be reconstructed independently from the DB. Persisted isolation attestations and claim content are inspectable, but provenance conclusions about producer behavior cannot exceed them.
- The live run-manifest response exposes the current dynamic `test-model`/empty-tool runtime view, not an immutable producer execution record. It is not used as proof of the original producer tool chain.
- `claim_scope_kind` is sidecar-only in the current implementation.
- The review is Quran-internal and snapshot-bound. It does not purport to establish external historical etymology or broader Arabic usage.
- The fresh review is semantic decision support, not the governed human/independent VerificationRecord required for canonicalization.

## Hard-boundary and stop result

Hard-boundary result: `FAILED_FOR_DNW_AND_FLH_EXACT_REVISIONS_DUE_TO_PROHIBITED_SOURCE_CONTENT; PASSED_SEMANTIC_REVIEW_AT_STATED_SCOPE_FOR_ESW_FWH_GLM`.

No database row was written; no VerificationRecord was created; no canonical state was changed; no claim was set to `ACCEPTED`; no Batch 07 artifact was edited; Batch 08 was not started; `PROJECT_STATE` was not edited; and no Git staging, commit, push, merge, tag, or release action was performed.

The exact owner decision surface, including the full current producer claim objects and current/historical revision bindings, is in `docs/evidence/requalification/five_root_owner_decision_package.json`.
