# Candidate Skill: Competing-Hypothesis Generation

**Classification:** `ADAPT`  
**Purpose:** Generate serious, testably distinct explanations plus a no-qualified-invariant option when warranted. Source: Semantic Skill Phase 4 and §12. [TR-060]

**Inputs:** observations, clusters, unresolved cases, prior hypothesis revisions.  
**Required context:** internal/external source phase and target scope.  
**Allowed tools:** observation retrieval, branch/coverage summaries.  
**Prohibited evidence:** prior external definition in internal phase; alternatives differing only in wording; discarded counterexamples.

**Execution:** (1) derive candidates from observations; (2) state predictions/layer assumptions; (3) merge paraphrases; (4) retain materially distinct alternatives; (5) add no-establishment option when real; (6) snapshot before challenge.  
**Required outputs:** hypothesis set, distinction matrix, predictions, source/influence refs, snapshot hash.  
**Failure/uncertainty:** one serious hypothesis is allowed; no ceremonial H2.  
**Verification:** each pair has an observable discriminator; snapshot cannot be silently mutated.  
**Dependencies:** observation and cluster artifacts; source policy.
