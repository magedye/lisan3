# Candidate Skill: Source-Contamination Review

**Classification:** `ADAPT`  
**Purpose:** Determine whether prohibited external/prior content influenced an internal result and distinguish detected, suspected, unknown and blocked access. Sources: Purity contract; Blind Lab implementation/tests. [TR-062]

**Inputs:** source-role profile; complete access/tool/context logs; internal snapshot; external comparison revision; model exposure declaration.  
**Required context:** phase-specific permissions and log completeness.  
**Allowed tools:** access-log query, dependency graph, content-match/canary checks.  
**Prohibited evidence:** model assertion “I did not use prior knowledge”; absence from an incomplete log; blocked read labeled contamination.

**Execution:** (1) verify log coverage; (2) classify each source/read; (3) trace dependencies; (4) detect pre-boundary external influence; (5) assess pretrained-exposure risk separately; (6) report impact and remediation.  
**Required outputs:** contamination status by class, disclosed/blocked/unknown reads, affected artifact revisions, confidence limits, required rerun/relabel.  
**Failure/uncertainty:** incomplete logs yield `NOT_EVALUATED`; pretrained exposure generally remains risk/unknown, not “clean.”  
**Verification:** direct, paraphrased, cached-index, blocked-access and incomplete-log fixtures.  
**Dependencies:** authoritative tool gateway; source identity/role registry; snapshots.
