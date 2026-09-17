# Candidate Skill: Distinctive-Feature Discovery

**Classification:** `ADAPT`  
**Purpose:** Find the smallest positive, layer-neutral, neighbor-discriminating and falsifiable feature set. Source: Semantic Skill P5/§9. [TR-059]

**Inputs:** target and neighbor comparison results; layer attribution; predictions/counterexamples.  
**Required context:** declared target scope.  
**Allowed tools:** contrast matrix, evidence resolver, prediction checker.  
**Prohibited evidence:** negative-only definition; generic label; context/form feature; rhetorically elegant wording as proof.

**Execution:** (1) enumerate candidate features; (2) remove unsupported/generic features; (3) test alternate layer explanations; (4) test essential neighbors; (5) minimize feature set; (6) write rejection condition.  
**Required outputs:** feature set or none established; positive definition; supporting/negative cases; layer controls; falsification.  
**Failure/uncertainty:** return unresolved/none established when residue disappears.  
**Verification:** genericity, layer-swap and withheld-neighbor tests.  
**Dependencies:** semantic-neighbor and falsification Skills.
