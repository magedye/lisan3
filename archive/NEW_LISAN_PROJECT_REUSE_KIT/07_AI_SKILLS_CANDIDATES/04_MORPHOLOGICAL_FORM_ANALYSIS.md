# Candidate Skill: Morphological-Form Analysis

**Classification:** `ADAPT`  
**Purpose:** Distinguish observed form from a hypothesized semantic contribution. Source: Semantic Skill §§11, 13.1; Purity structural boundary. [TR-054]

**Inputs:** form-tagged occurrences; lexical-unit assignment; comparable constructions.  
**Required context:** structural-source provenance and uncertainty.  
**Allowed tools:** morphology parser/lookup, exact grouping, contrast tables.  
**Prohibited evidence:** form label treated as semantic proof; provisional operator projected into root core; dictionary gloss as internal evidence.

**Execution:** (1) verify form tags; (2) find controlled contrasts; (3) list candidate effects; (4) test construction/participant/context confounds; (5) search counterexamples; (6) decide supported/unsupported/unresolved effect.  
**Required outputs:** structural observations, contrast set, effect hypotheses, confounds, counterevidence, decision scope.  
**Failure/uncertainty:** return `FORM_EFFECT_NOT_ESTABLISHED`; different forms do not require a semantic distinction.  
**Verification:** held-out and same-construction contrasts; negative test where forms differ but evidence does not.  
**Dependencies:** occurrence collection; construction analysis.
