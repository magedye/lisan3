# LISAN3 — Batch 07 Semantic Campaign Report

> **Status: research output only.** This report is NOT independent semantic
> acceptance, NOT canonical publication, and NOT owner acceptance. Every result
> is a *research candidate* pending a fresh independent read-only review. Maximum
> implementation-thread state: `BATCH_07_READY_FOR_FRESH_INDEPENDENT_SEMANTIC_REVIEW`.

## 1. Campaign identity
- **Starting main SHA:** `fff83c57fa301febded7eb19c9b784719eb78c0a` (independently confirmed Batch 06, merged to `main`)
- **Branch:** `semantic-campaign-batch07`
- **Campaign ID:** `lisan-root-calibration`
- **Semantic runtime contract:** `LISAN3_SEMANTIC_RUNTIME_V3_2026_09_06` (`skills/lisan-semantic-extraction/SKILL.md`, sha256 `01784170cac4…`)
- **Source policy:** `QURAN_INTERNAL_ONLY` (no dictionaries, tafsir, translations, web, embeddings, or inherited lexical meanings used as semantic authority)
- **Checkpoints:**
  - Initialization / frozen population: `f92797a`
  - Wave 01: `e38e59b7adbaf397814527a1dca43a929b48234b`
  - Wave 02: `9e1435a9a292ddff30065ba3512930ffe1c7f2a2`
  - Wave 03: `ada0488c493d06eb3838dd0b984f3c2cc405edc8`
  - Wave 04: `b6c53e439963ca295f943b2c38fab3c35ba49d80`
  - Wave 05: `0fa54453a7a9457be28d387f4c8297fff2a0a2d6`
  - Wave 06: `01204fcf6eeddaaf76ff7dce5c36a166b440a5ba`

## 2. Population
- **120 previously-unresearched roots**, deterministically selected (`tools.campaign select --n 120`) over the live 1,642-root universe (128 already researched → 1,514 remaining), reproducible, zero overlap with prior batches or the 5 Batch 05 corrective roots.
- **Total occurrences researched: 8,168** (exact-set complete for all 120: 0 missing / 0 extra / 0 duplicate).
- Arabic identity is primary; Buckwalter is the technical corpus identifier; artifact filenames are storage identity.

## 3. Method
Per root: real corpus occurrence materialisation → deep MoA (2 independent analysts + 1 adversarial analyst → aggregator) over the actual Tanzil verse text + QAC morphology → single-writer canonical-contract serialisation → **independent adversarial overclaim sweep** → evidence-supported narrowing → V2 checkpoint → wave commit. One writer only; analysts read-only.

## 4. Outcome distribution (recomputed in V3 from the 120 artifacts)
| Result | Count |
|---|---|
| STRONG | 6 |
| MODERATE | 96 |
| WEAK | 0 |
| UNRESOLVED | 18 |

- **Claim scope:** UNIVERSAL 5 · REPRESENTATIVE 97 · LOCAL 18
- **Claim-scope kind:** ROOT_GENERALIZATION 5 · DERIVATIONAL_FAMILY 70 · LEXICALIZED_CLASS 27 · UNRESOLVED_CLASS_ONLY 18
- **Falsification:** PASSED 17 · NOT_RUN 85 · NOT_REQUIRED 18
- **Resistance:** 357 final resistant occurrences across 72 roots · 167 preliminary→final reconciliations · **0 failed reconciliations** · 0 incomplete lineages
- **Purity:** `NOT_EVALUATED` for all 120 (no authorized Purity evaluation occurred)

The distribution is deliberately conservative: **no root was optimised toward STRONG**, and where a coherent resistant sub-class or an undemonstrated bridge existed, the root was capped or returned UNRESOLVED. This mirrors the calibration the Batch 06 review demanded.

### STRONG roots (6)
ع ص و (ESw) · ص ي ح (SyH) · د ن و (dnw) · ف ل ح (flH) · ف و ه (fwh) · غ ل م (glm)

### UNRESOLVED roots (18)
ش م ل ($ml) · ذ ن ب (*nb) · ذ ر ر (*rr) · ا ل و (Alw) · ا ن ي (Any) · ع ذ ب (E*b) · ط و ع (TwE) · ب ح ر (bHr) · ه و ي (hwy) · ج ب ل (jbl) · ج ل د (jld) · ج و ر (jwr) · م ل ا (mlA) · ق ر ض (qrD) · ق ر ن (qrn) · س م و (smw) · س خ ر (sxr) · خ ل ل (xll)

## 5. Strongest evidence-supported nuclei
- **د ن و (dnw)** — the proximal/low pole of a salient scale relative to a reference point (spatial by default; adversarially SUPPORTED).
- **ف ل ح (flH)** — attaining/securing enduring well-being and success (Form-IV family; value-loaded, adversarially SUPPORTED).
- **ف و ه (fwh)** — the mouth as concrete oral organ / site of speech-emission.
- **ص ي ح (SyH)** — a single bounded audible sound-event (force-neutral).
- **غ ل م (glm)** / **ع ص و (ESw)** — coverage-universal single lexemes (youth; staff), graded STRONG for a lexicalised class (scope REPRESENTATIVE).

## 6. Multi-class / unresolved (no forced unification)
The 18 UNRESOLVED roots each carry two or more internally-coherent classes with **no demonstrated Quran-internal bridge**, e.g.: `smw` sky-expanse vs verbal-designation (with "elevation" etymon internally disconfirmed at 87:1); `E*b` torment vs "sweet water" (*opposite* valence); `qrn` generation vs coupling vs the Dhū-l-Qarnayn name; `jld` skin vs flogging vs endurance; `Alw` fall-short vs oath vs the "except" particle. Each is persisted as a LOCAL / UNRESOLVED_CLASS_ONLY partition with root-specific reopen triggers.

## 7. Semantic boundaries (major "does-not-entail" findings)
Representative negative results persisted per root, e.g.: `Eml` does not entail moral goodness (valence is contextual) nor achieved efficacy; `Ayy` (Batch-06-adjacent pattern) — a sign does not entail the referent itself; `nEm` well-being does not extend to the livestock (anʿām) lexeme; `nSr` backing does not entail success; `n*r` warning does not entail efficacy; `bED` excludes the "gnat" homonym.

## 8. Rejected interpretations
Traditional single-nucleus etymologies rejected as Quran-internally undemonstrated or disconfirmed, e.g.: `smw` "elevation" unifier (highness delegated to ʿlw at 87:1); `E*b`/`kll` "withhold/encompass" etymologies (barred lexicon priors); `Ayy` "sign vs technical-verse" two-lexeme split (refuted — bridged); the moral-deed reading as the *lexical* core of `Eml` (refuted by God-as-agent 36:71).

## 9. Lexicalized / opaque seams (made explicit)
27 roots carry a LEXICALIZED_CLASS scope; recurrent resistant lexicalized seams include: `nEm` anʿām (livestock), `rHm` arḥām (wombs/kinship), `$hd` al-shahādah (manifest realm), `Sdq` ṣadaqah/ṣadīq, `dwn` the bleached *min dūni-llāh* idiom, `nbA` the nabiyy (prophet) branch, `bED` the "gnat" homonym.

## 10. Cross-root candidates (NOT promoted)
Cross-root relations surface only as candidates in per-root artifacts where evidenced; none has been made canonical. Example candidate contrast families for the independent reviewer: dnw↔fwq (proximity/upper-side, cross-batch), Eml↔faʿl/ṣanaʿ/kasaba (agency, distinctiveness not established), nEm↔Darr (well-being vs harm poles). These require separate establishment.

## 11. False-synonym / differentiation candidates
Recorded where a shared gloss masks a differentiating axis, e.g.: `Eml` vs `ṣnE`/`ksb` (answerability axis — *not* lexically established from this packet, flagged CONSISTENT-only); `nZr` vs `bSr` (attention-direction vs achieved apprehension); `n*r` vs `bashīr` (warning vs glad-tiding pole). All remain candidates.

## 12. Opposition / contrast candidates
Lexical/contextual poles recorded per root, e.g. `nEm`↔harm (naʿmāʾ baʿda ḍarrāʾ), `mwt`↔ḥ-y-y (lifeless vs living), `Esr`↔ease, `kbr` big↔`Sgr`(Batch06) small. Distinguished from mere thematic pairing; not promoted.

## 13. Purity limitation
`purity_status = NOT_EVALUATED` for all 120 roots (8 diagnostics each `NOT_EVALUATED`). No cleanliness was inferred.

## 14. Verification (V3, recomputed from durable artifacts)
- Population: **120/120** artifacts, all in ledger; occurrences **8,168** reproduced (manifest match).
- Exact-set: **0 missing / 0 extra / 0 duplicate** across all 120.
- Canonical contract: **0 errors / 120**; no legacy aliases.
- Controls: **120/120 distinct rejection conditions**, **120/120 distinct reopen sets**, **0 positional hard cases**, **0 unsupported PASSED falsifications**, **0 unresolved-with-universal**.
- Overclaim sweeps: Wave 01 flagged & corrected **7**; Waves 02–06 flagged **0** (all 100 later roots confirmed honest on first pass).
- Collisions: **0** (roots dir 248 casefold-unique; universe 1642/1642).
- Ledger/manifest/status: agree (processed **248/1642**; canonicalisation PENDING for all).
- Prior batches: **0** prior root files modified; Batch 05's 5 corrective roots byte-identical; Batch 02–06 intact.
- Tests: **48 focused** (`test_campaign_coverage` 42 + `test_qac_morphology` 6) pass at each wave and at V3; Ruff clean; `py_compile` OK. (Green tests are not treated as semantic truth.)

## 15. Boundaries
No merge · no push · no canonicalisation · no adoption · no Batch 08. The `VERIFIED` component of the adoption threshold can only be produced by a fresh independent review, which the implementation thread must not self-grant.
