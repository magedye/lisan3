# Candidate Skill: Construction Analysis

**Classification:** `ADAPT`  
**Purpose:** Identify semantic effects attributable to valency, prepositions, complements, syntax or recurring constructions. Source: Semantic Skill §§2, 7, 11. [TR-057]

**Inputs:** token/segment parse; occurrence inventory; lexical-unit and form assignments.  
**Required context:** parser/source provenance and known ambiguities.  
**Allowed tools:** deterministic syntax/morphology adapter; concordance and contrast queries.  
**Prohibited evidence:** parser label as semantic proof; unverified syntactic guess; context outcome promoted to construction meaning.

**Execution:** (1) normalize construction signatures; (2) group occurrences; (3) compare same lexeme across constructions; (4) compare neighbors in matched constructions; (5) test participant/context confounds; (6) decide candidate effect.  
**Required outputs:** construction signature, observations, effect hypothesis, controlled contrasts, counterexamples, ambiguity and scope.  
**Failure/uncertainty:** retain multiple parses/effects; return no established effect when evidence is weak.  
**Verification:** parser/source locator resolution and negative cases for mismatched/ambiguous segments.  
**Dependencies:** structural corpus; occurrence collection.
