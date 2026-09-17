# Candidate Skill: Analysis-Unit Resolution

**Classification:** `ADAPT`  
**Purpose:** Convert a question into the narrowest defensible primary unit: root contribution, lexical unit, form, construction, local meaning, or broader concept. Source: Semantic Skill §2. [TR-051]

**Inputs:** user question; target expression/location; terminology revision; known root/lexeme ambiguity.  
**Required context:** Quran orthography/token policy; allowed analysis-unit vocabulary.  
**Allowed tools:** exact Quran locator; morphology lookup; terminology registry.  
**Prohibited evidence:** pretrained intuition used to settle root/lexeme identity; traditional definition used to choose unit.

**Execution:** (1) parse requested claim; (2) resolve target span; (3) list plausible units; (4) choose narrowest primary unit; (5) record secondary units separately; (6) state ambiguity and scope.  
**Required outputs:** `primary_unit`, `target_identity`, `claim_scope`, `secondary_questions`, `ambiguities`, `required_sources`.  
**Failure/uncertainty:** return `TARGET_UNRESOLVED` with alternatives; never default to root core because “meaning” was asked.  
**Verification:** another reader can map output to the question and exact Quran locator; negative tests for word-vs-local and root-vs-form confusion.  
**Dependencies:** controlled terminology; exact Quran lookup.
