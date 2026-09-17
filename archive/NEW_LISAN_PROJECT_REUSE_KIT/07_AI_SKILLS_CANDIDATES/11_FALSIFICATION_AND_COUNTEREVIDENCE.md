# Candidate Skill: Falsification and Counterevidence

**Classification:** `REUSE_AS_IS`  
**Purpose:** Actively search the declared evidence space for findings that reject, narrow, split or reopen a semantic hypothesis. Source: Semantic Skill §§8–10; Purity Generic/Forced/Circular contracts. [TR-061]

**Inputs:** frozen hypothesis; rejection condition; complete occurrence index; layer confounds; neighbor set.  
**Required context:** canonical source profile and exact search space.  
**Allowed tools:** exact search, structural filters, evidence resolver, dependency/cycle checker.  
**Prohibited evidence:** absence as proof without search completeness; circular labels; reinterpretation of every failure to save the hypothesis.

**Execution:** (1) validate condition operationality; (2) search hardest/outlier/negative cases; (3) test predictions; (4) control form/construction/context confounds; (5) attach counterevidence; (6) apply predeclared decision effect.  
**Required outputs:** executed search receipt, cases inspected, counterevidence, failed predictions, confounds, verdict and required revision.  
**Failure/uncertainty:** incomplete search lowers completeness; ambiguous case stays unresolved.  
**Verification:** injected counterexample must be found; direct/transitive circular support must fail.  
**Dependencies:** occurrence collection; evidence resolver; hypothesis snapshot.
