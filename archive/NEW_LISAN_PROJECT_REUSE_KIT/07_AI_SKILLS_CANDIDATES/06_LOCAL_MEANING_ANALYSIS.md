# Candidate Skill: Local-Meaning Analysis

**Classification:** `ADAPT`  
**Purpose:** Decide the meaning of a target expression at an exact Quran location from lexical/root, form, construction, roles and context. Source: Semantic Skill §§2–3, 11, 23. [TR-056]

**Inputs:** exact target occurrence; structural analysis; lexical/root hypotheses; context window.  
**Required context:** claim scope and source roles.  
**Allowed tools:** exact Quran/context lookup; morphology/syntax tools; evidence resolver.  
**Prohibited evidence:** whole-verse interpretation silently assigned to the word; root concept treated as sufficient; tafsir/dictionary used as internal evidence.

**Execution:** (1) resolve target span; (2) record structure; (3) assign candidate layer contributions; (4) compare plausible readings; (5) test contextual constraints; (6) prefer or retain alternatives.  
**Required outputs:** local meaning, contribution map, alternative readings, reasons, evidence/counterevidence, unresolved assignments, scope.  
**Failure/uncertainty:** return alternatives or insufficient structure; do not generalize to all occurrences.  
**Verification:** same lexeme in different contexts and neighbor substitution probes; exact citation readback.  
**Dependencies:** analysis-unit, occurrence, form and construction Skills.
