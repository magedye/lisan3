# Candidate Skill: Quran Occurrence Collection

**Classification:** `REUSE_AS_IS`  
**Purpose:** Produce a complete, reproducible inventory of target occurrences under declared matching rules. Source: Semantic Skill Phase 1/§6; Tanzil identity contract. [TR-052]

**Inputs:** target identity; corpus snapshot; token/root/lemma matching policy.  
**Required context:** exact text source, structural-source roles, normalization and alignment rules.  
**Allowed tools:** deterministic corpus query, token/segment index, hash verifier.  
**Prohibited evidence:** memory-derived occurrence lists; orthographic guessing presented as verified; unadmitted gloss/ontology.

**Execution:** (1) verify snapshot; (2) execute exact query; (3) preserve locators/text; (4) retain ambiguous candidates; (5) compute denominators by form/lemma/construction where available; (6) record exclusions and tool receipt.  
**Required outputs:** ordered occurrences, ambiguous matches, excluded items/reasons, source hashes, query/config hash, coverage counts, execution receipt.  
**Failure/uncertainty:** distinguish no occurrences from unavailable structure; return incomplete coverage with the missing capability.  
**Verification:** rerun returns identical ordered IDs; every item resolves to the snapshot; mutation of source/config changes the manifest.  
**Dependencies:** verified Quran snapshot; structural adapter when root/lemma matching is requested.
