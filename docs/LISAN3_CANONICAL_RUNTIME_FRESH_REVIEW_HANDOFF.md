# Fresh Independent Runtime Review — Handoff Prompt

Paste the block below to a NEW read-only reviewer (Sol xhigh), with no access to
the implementation chat. The reviewer must independently challenge the Canonical
Runtime Qualification infrastructure and return exactly one verdict.

---

```
You are an independent, READ-ONLY reviewer. Do NOT modify code, data, or DB state.
Work on d:\APP\tafseer\lisanapp3, branch `canonical-runtime-qualification`
(base main = 6dea680052cf3ccf00ccb89396503763c0dc1839).

Context: an implementation agent ran a Canonical Runtime Qualification Track whose
goal was to make the DB-native governed research path genuinely usable WITHOUT
fabricating provenance — NOT canonicalization and NOT semantic requalification of
the five roots (ESw, dnw, flH, fwh, glm). It claims status
CANONICAL_RUNTIME_READY_FOR_FRESH_INDEPENDENT_REVIEW.

Authority order: owner instruction > AGENTS.md > AUTHORITY_MAP.md >
SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md > docs/canonical/* > services/
models > tests > DB state. Repository authority beats historical chat assumptions.

Independently CHALLENGE each of the following. For each, try to DISPROVE the claim;
default to skeptical. Report CONFIRMED / REFUTED / UNCERTAIN with exact file:line
or query evidence.

1. DB authority choice. Is lisanapp.db genuinely the authoritative governed store
   (default path + only Alembic-stamped + schema CURRENT), and was the unstamped
   data/campaign/runtime.db correctly NOT promoted? Check backend/infrastructure/
   database.py, alembic.ini, and that no new "third truth store" was created.

2. Data migration/admission. Confirm the corpus entered lisanapp.db ONLY via the
   repository-native import/activation services (tools/converge_runtime.py), never
   a raw SQLite row copy and never a hand-edited status. Re-run convergence read-path
   and confirm idempotency. Verify the three artifacts' SHA-256/bytes match authority
   (Tanzil ac0724…/1,334,737; index 0d0a22…; QAC a1d129…/6,309,503).

3. Tanzil production activation. Independently reproduce that snapshot
   snap_tanzil_1_1_ac0724796cbb is is_production_validated==True with
   production_validation_failures==[], 6,236 verses, fixture_only=False, and an
   OWNER_AUTHORITY activation audit row. Confirm activation was NOT achieved by
   directly setting VALIDATED/PRODUCTION_ACTIVE in SQL. Attempt to break it.

4. Methodology source binding. Confirm @01784170cac4 is CURRENT, run-eligible,
   QURAN_INTERNAL_CUMULATIVE_RUN, and its persisted source_sha256 equals the LIVE
   sha256 of skills/lisan-semantic-extraction/SKILL.md. methodology_authority_failures==[].

5. Occurrence identity/materialization. Scrutinize the decision to adopt
   StructuralToken (word-level, from admitted QAC) as the governed root-occurrence
   authority instead of overloading the verse-level CorpusOccurrence. Is this
   faithful to Track D and AUTHORITY_MAP? Confirm 49,968 tokens / 1,642 roots are
   deterministically derived from QAC, not from Batch 07 judgments. Verify the five
   roots' confirmed counts (12/133/40/13/13) reproduce from QAC independently and
   that the Batch 07 comparison is post-hoc only (no tuning).

6. Isolation semantics (MOST IMPORTANT). Verify CLEAN now fails closed: a fresh/bare
   IsolationState is NOT_ESTABLISHED and cannot be canonicalized; only
   establish_semantic_isolation (production-valid snapshot + current methodology +
   allowed-source boundary + manifest + immutable audit) yields ESTABLISHED/CLEAN.
   Try to reach ACCEPTED with an un-established or contaminated isolation. Confirm
   the change is coherent across models/migration/service/API/tests and that no
   Batch-07-only special case exists. Confirm honest representation of enforcement
   limits (no over-claimed technical guarantee).

7. Evidence resolution. Try to smuggle external evidence through the token: bridge;
   reference a wrong-snapshot / wrong-root / non-CONFIRMED / verse-level ref; confirm
   each is rejected with a precise reason and that a campaign artifact path can never
   be an evidence ID. Confirm duplicates cannot substitute for missing coverage.

8. Completeness derivation. Confirm ROOT_CONCEPT completeness is host-derived from
   confirmed word_refs and that NO path imports the campaign "COMPLETE" string or
   artifact occurrence counts into a SemanticClaim. A UNIVERSAL claim must require
   every confirmed occurrence.

9. Governance fail-closed behavior. Independently verify CanonicalizationPolicy
   still rejects: non-production snapshot, missing methodology, absent/unestablished/
   contaminated isolation, missing/non-INDEPENDENT/stale verification, ambiguous
   corpus dependency, fixture, root-unity counterexample, unresolved evidence, and
   unauthorized actor. Confirm NO existing control was weakened (diff the policy).

10. Retroactive fabrication audit. Confirm there is NO ResearchRun, IsolationState,
    ObservationArtifact, SemanticClaim, or VerificationRecord asserting that Batch 07
    already ran through the DB-native runtime; zero SemanticClaims/VerificationRecords/
    ACCEPTED for the five roots; and the five Batch 07 JSONs are byte-identical
    (E_53_w f19863…, dnw 3de4b1…, fl_48_ 93824e…, fwh 4aaa42…, glm 4018df…).

Also check: (a) the stale backend/alembic chain (head 5542b3a62e23) was left in place
and flagged, not silently migrated; (b) docs/canonical/ADMISSION_TANZIL.md historical
provenance text was not rewritten.

Run the non-e2e suite read-only (./.venv/Scripts/python -m pytest tests --ignore=tests/e2e -q)
and confirm green (expect 251 passed). Do NOT run semantic analysis for the five roots.
Do NOT canonicalize anything.

Return exactly one:
  CANONICAL_RUNTIME_INDEPENDENTLY_CONFIRMED
or:
  CANONICAL_RUNTIME_REVIEW_BLOCKED  — with the exact defects.

Only a CONFIRMED verdict authorizes the separately-scoped five-root semantic
requalification; this review does NOT itself begin it.
```
