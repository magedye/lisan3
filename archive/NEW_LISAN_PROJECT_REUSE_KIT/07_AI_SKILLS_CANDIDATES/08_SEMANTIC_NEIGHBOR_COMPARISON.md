# Candidate Skill: Semantic-Neighbor Comparison

**Classification:** `ADAPT`  
**Purpose:** Compare the target with essential neighbors in a shared domain without assuming synonymy or difference. Source: Semantic Skill Phases 5–6/§8; `EssentialNeighbor`. [TR-058]

**Inputs:** target hypothesis; candidate neighbors; occurrence/structure evidence.  
**Required context:** candidate-generation provenance and semantic-distance dimensions.  
**Allowed tools:** exact retrieval; vector/graph discovery as labeled candidate sources; evidence resolver.  
**Prohibited evidence:** similarity score as confidence; graph edge as truth; cherry-picked easy neighbors; non-occurrence as linguistic impossibility.

**Execution:** (1) state shared domain; (2) justify essentiality; (3) compare relevant dimensions; (4) run substitution/boundary/negative tests; (5) search convergence and divergence; (6) decide difference/no-difference/unresolved.  
**Required outputs:** comparison vector, matched examples, differences and overlaps, counterevidence, unresolved axes, implications for target hypothesis.  
**Failure/uncertainty:** allow `NO_DIFFERENCE_ESTABLISHED`; never invent a distinction because forms/labels differ.  
**Verification:** adversarial neighbor choice and false-positive retrieval cases.  
**Dependencies:** retrieval candidates, evidence resolver, occurrence and layer analyses.
