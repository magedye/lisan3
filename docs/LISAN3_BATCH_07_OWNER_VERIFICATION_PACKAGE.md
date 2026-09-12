# Batch 07 — Owner / Human Canonical-Acceptance Verification Package

Status: **HUMAN_VERIFICATION_REQUIRED_FOR_CANONICAL_ACCEPTANCE**

Published main SHA: `999da692ca9006a2f6a055a8eabb0175658ce8ea` · Reviewed research checkpoint: `0c21d82f12439f7fd57bc4cdcae0eab31befeaaa`

> The AI implementation agent produced this package. It has **not** filled any human decision field and has **not** created any VerificationRecord. Independent AI review is recorded as *supporting evidence only*.

## Why human action is required

- Canonical transition: `backend/domain/services/canonicalization.py :: CanonicalizationPolicy.canonicalize(actor="TRUSTED_LOCAL_OWNER")`
- Verification endpoint: `POST /judgments/{claim_id}/verification (backend/main.py record_independent_verification); server stamps verifier_identity=TRUSTED_LOCAL_INDEPENDENT_VERIFIER; a VERIFIED decision requires verification_type=INDEPENDENT`
- Canonicalize endpoint: `POST /judgments/{claim_id}/canonicalize`
- Required verifier identity: TRUSTED_LOCAL_INDEPENDENT_VERIFIER (independent-human / trusted-local-owner authority), distinct from the AI research/producer endpoint which has no ACCEPTED transition and must not self-grant.
- **Blocking structural fact:** Zero SemanticClaim rows and zero VerificationRecords exist in either database (data/campaign/runtime.db, lisanapp.db). The Batch 07 campaign is file-based (JSON artifacts + ledger + CampaignState) and never materialized SemanticClaim rows, so there is no claim_id to verify or canonicalize, no integer revision_id, and no VerificationRecord.claim_id target.
- Required VerificationRecord fields: id, claim_id (FK to an existing SemanticClaim), verifier_identity (NOT NULL), verification_type=INDEPENDENT, decision=VERIFIED, evaluated_claim_revision == claim.revision_id, rationale, evidence_refs, created_at

---

## ع ص و (`ESw`)

- Artifact: `artifacts/semantic-campaign/roots/E_53_w.json`
- Result strength: **STRONG** · Claim scope: **REPRESENTATIVE / LEXICALIZED_CLASS** · contract_type: ROOT_CONCEPT
- Revision binding: methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`, batch `batch07-wave1`, snapshot `snap_tanzil_1_1_ac0724796cbb`
  - _File-based campaign: no DB SemanticClaim / integer revision_id exists yet. A materialized SemanticClaim would start at revision_id=1. The human decision must bind to THIS persisted revision identity._

**Proposed canonical semantic claim (verbatim — do not rewrite):**

> A single lexicalized concrete count-noun: a rigid, elongated, hand-held rod/staff. The root ESw surfaces in the Quran only as this object-denoting noun (singular عَصَا / broken plural عِصِيّ), inflected for number, case, and possessor. It is function-neutral (support, herding, striking, casting are contributed by the surrounding verbs, not by the noun), carries no verbal, abstract, figurative, sacral, or authority content, and is distinct from the disobedience root ع ص ي.

_Plain explanation (verbatim):_ Every one of the 12 tokens denotes the same physical object — a wooden staff held by a person. 20:18:3:1 supplies the Quran's own ostensive definition (Moses leans on it, beats foliage for his sheep with it, and has 'other uses'), fixing the referent as an ordinary multi-purpose stick before any miracle. The remaining 11 tokens are the identical object under three action-frames — cast down (becomes a serpent / swallows the illusions), struck against rock or sea (springs / parting), and the magicians' plural staffs cast in sorcery. The variety lives entirely in the verbs (ألقى، اضرب، أتوكّأ، أهشّ), never in the noun. Because the root is realized solely as this one lexicalized concrete noun within a single narrative domain (the Moses cycle), the claim is a lexicalized-class account, not a generalizable root-wide abstract nucleus.

**Coverage:** researched 12 / expected 12 · exact-set match: **True** (missing [], unexpected [], duplicate [])

**Supporting evidence refs (6):** 20:18:3:1, 26:32:2:1, 2:60:7:2, 26:63:6:2, 20:66:6:2, 26:44:3:2

**Counterevidence refs (0):** —

**Hard cases:**
- `20:66:6:2` [ADVERSARIAL_BOUNDARY] — Magicians' (non-prophetic) plural staffs in sorcery, coordinated with حِبَال (ropes); tests and defeats both the sacral/sign-instrument reading and the 'sorcery-props generally' broadening, since the noun is precisely the rigid-rod member contrasted with flexible cordage.
- `26:44:3:2` [ADVERSARIAL_BOUNDARY] — Second attestation of the magicians' plural staffs cast (أَلْقَوْا) alongside حِبَالَهُمْ; confirms the same concrete rod-class in a non-prophetic, non-miraculous-per-word setting.
- `20:18:3:1` [ADVERSARIAL_BOUNDARY] — The only token outside a miracle frame and the only one enumerating multiple heterogeneous uses — the natural place to fracture a single account; instead it anchors a mundane, function-neutral object and defeats the miracle-instrument reading.

**Falsification:** status **PASSED** · verdict SUPPORTED · falsifiable True · distinctiveness_ok True · failing_occurrences []
  - Rationale: Four independent refutation wedges were run: (1) miracle/sign-instrument nucleus — refuted by mundane 20:18:3:1 and non-prophetic 20:66:6:2/26:44:3:2; (2) plural-broadening to 'sorcery-props generally' — refuted by the حِبَال contrast that isolates عِصِيّ as the rigid-rod member; (3) transformation wedge ('word means serpent') — refuted because عَصَا is the pre-transformation subject (فَأَلْقَىٰ ع

**Independent AI semantic review:** `VERIFIED_AT_SCOPE` — SUPPORTING REVIEW EVIDENCE ONLY — NOT the required independent-human VerificationRecord. Does not satisfy CanonicalizationPolicy condition 6.

**Human decision (to be completed by the independent human / TRUSTED_LOCAL_OWNER):**

- [ ] VERIFY_AT_SCOPE  [ ] REJECT  [ ] RETURN_FOR_CORRECTION
- Reviewer identity: __________   Timestamp: __________
- Exact claim revision affirmed: __________
- Rationale: ______________________________________________
- Confirms: (1) claim matches evidence (2) scope not broader than evidence (3) supporting refs genuinely support (4) hard cases/counterevidence honest (5) falsification material (6) no unresolved seam defeats the claim

---

## د ن و (`dnw`)

- Artifact: `artifacts/semantic-campaign/roots/dnw.json`
- Result strength: **STRONG** · Claim scope: **UNIVERSAL / ROOT_GENERALIZATION** · contract_type: ROOT_CONCEPT
- Revision binding: methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`, batch `batch07-wave1`, snapshot `snap_tanzil_1_1_ac0724796cbb`
  - _File-based campaign: no DB SemanticClaim / integer revision_id exists yet. A materialized SemanticClaim would start at revision_id=1. The human decision must bind to THIS persisted revision identity._

**Proposed canonical semantic claim (verbatim — do not rewrite):**

> د-ن-و marks occupying or moving toward the PROXIMAL/LOW pole of a salient scale relative to a reference point. The default axis is spatial (near, close, within reach, low / hanging-low), and the single relational primitive extends productively along whatever axis context supplies: temporal immediacy (al-dunyā = the near/present life vs the latter al-ākhira), lesser quantity (adnā vs akthar), lesser magnitude (al-ʿadhāb al-adnā vs al-akbar), inferior rank/value (adnā vs khayr), and proximity-to-an-outcome (adnā an … = 'more conducive'). The root supplies only the near/low RELATION; the 'world / life / fruit / sky' content and any moral negativity come from the modified head noun and the ākhira contrast, never from the root itself.

_Plain explanation (verbatim):_ Every form of this root places something at the 'near' or 'low' end of some scale, measured from a reference point. Concretely it is physical nearness: a person who 'drew near' (danā, 53:8), garments 'drawn down/close' (yudnīna, 33:59), fruit and shade 'within reach / low-hanging' (dāniyah). The comparative adnā is 'nearer / lower / lesser' on whatever scale is in view — distance, amount, size, worth, or nearness-to-a-result. The dominant word al-dunyā is just the feminine of that comparative, 'the nearer/lower one', frozen for 'this present life' set against al-ākhira 'the latter life' — and the corpus keeps the literal sense visible by using al-dunyā for 'the nearest heaven' (67:5). So this is one relational idea ('near/low on a scale'), not several unrelated meanings.

**Coverage:** researched 133 / expected 133 · exact-set match: **True** (missing [], unexpected [], duplicate [])

**Supporting evidence refs (15):** 53:8:2:1, 33:59:8:1, 55:54:9:1, 69:23:2:1, 6:99:24:1, 76:14:1:2, 30:3:2:1, 53:9:5:1, 58:7:26:1, 73:20:6:1, 32:21:4:2, 67:5:4:2, 7:169:10:2, 13:26:9:2, 22:11:20:2

**Counterevidence refs (6):** 2:61:27:1, 2:282:93:2, 4:3:26:1, 5:108:2:1, 33:51:17:1, 33:59:13:1

**Hard cases:**
- `2:61:27:1` [ADVERSARIAL_BOUNDARY] — The only token where no physical/temporal/quantitative proximity is available; survives solely on the low->inferior extension.
- `2:282:93:2` [ADVERSARIAL_BOUNDARY] — «أَدْنَىٰٓ أَلَّا تَرْتَابُوٓا۟» projects proximity onto an abstract epistemic outcome; extension is inferred, not surface-derived.
- `4:3:26:1` [ADVERSARIAL_BOUNDARY] — «أَدْنَىٰٓ أَلَّا تَعُولُوا۟»: proximity-to-outcome reading; metaphor not glossed by the corpus.
- `5:108:2:1` [ADVERSARIAL_BOUNDARY] — «أَدْنَىٰٓ أَن يَأْتُوا۟ بِٱلشَّهَٰدَةِ»: 'more conducive' reading; proximity onto abstract outcome, inferred.
- `33:51:17:1` [ADVERSARIAL_BOUNDARY] — «أَدْنَىٰٓ أَن تَقَرَّ أَعْيُنُهُنَّ»: purely modal 'more apt'; no overt scale on the surface.
- `33:59:13:1` [ADVERSARIAL_BOUNDARY] — «أَدْنَىٰٓ أَن يُعْرَفْنَ»: proximity-to-outcome; but shares its verse with the concrete yudnīna, evidence the tradition felt concrete and abstract as one root.

**Falsification:** status **PASSED** · verdict SUPPORTED · falsifiable True · distinctiveness_ok True · failing_occurrences []
  - Rationale: A genuine refutation was run: the strongest competitor — a two-nucleus split of neutral spatial PROXIMITY (verbs, participles, adnā-of-distance, al-samāʾ al-dunyā) versus evaluative LOWNESS / a frozen al-dunyā = 'world' — was tested against the corpus and returned SUPPORTED for unity, i.e. the split failed. It is dissolved by single-word/single-verse counter-evidence: 67:5 uses al-dunyā spatially 

**Independent AI semantic review:** `VERIFIED_AT_SCOPE` — SUPPORTING REVIEW EVIDENCE ONLY — NOT the required independent-human VerificationRecord. Does not satisfy CanonicalizationPolicy condition 6.

**Human decision (to be completed by the independent human / TRUSTED_LOCAL_OWNER):**

- [ ] VERIFY_AT_SCOPE  [ ] REJECT  [ ] RETURN_FOR_CORRECTION
- Reviewer identity: __________   Timestamp: __________
- Exact claim revision affirmed: __________
- Rationale: ______________________________________________
- Confirms: (1) claim matches evidence (2) scope not broader than evidence (3) supporting refs genuinely support (4) hard cases/counterevidence honest (5) falsification material (6) no unresolved seam defeats the claim

---

## ف ل ح (`flH`)

- Artifact: `artifacts/semantic-campaign/roots/fl_48_.json`
- Result strength: **STRONG** · Claim scope: **REPRESENTATIVE / DERIVATIONAL_FAMILY** · contract_type: ROOT_CONCEPT
- Revision binding: methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`, batch `batch07-wave4`, snapshot `snap_tanzil_1_1_ac0724796cbb`
  - _File-based campaign: no DB SemanticClaim / integer revision_id exists yet. A materialized SemanticClaim would start at revision_id=1. The human decision must bind to THIS persisted revision identity._

**Proposed canonical semantic claim (verbatim — do not rewrite):**

> flH is attested Quran-internally ONLY as the Form IV af'ala family (the finite verb aflaHa/yufliHu/tufliHu and its agent-noun al-mufliHun/al-mufliHin), and in this family it denotes, for a person(-class) subject and always intransitively, ATTAINING/COMING OUT WELL — settling into the aimed-at favorable end-state, coming out ahead. It names an outcome/achievement (the result the imperatives aim at), not an action, effort, or feeling; it is evaluative-total (the subject's whole standing) and binary/class-defining (one is of al-mufliHun or is denied it), never gradable, never transitive/causative, never concrete/agrarian. The moral, eschatological, or salvific value everywhere attached to it is supplied by the subject and context, NOT entailed by the lexeme.

_Plain explanation (verbatim):_ Every one of the 40 occurrences is Form IV, in two shapes: 27 verbs and 13 active participles (al-mufliHun / al-mufliHin). Across all four grammatical deployments the meaning holds steady: perfect qad aflaHa = the good subject HAS come out well (believers 23:1, the self-purifier 87:14/91:9); negated lA yufliHu = the wrongdoer-class (mujrimun, Zalimun, kafirun, sAHir, liars-against-God) will NOT come out well; laAAallakum tufliHun = so that you MAY come out well (held out as the hoped-for result of taqwA, jihAd, dhikr, patience, shunning khamr/ribA); and al-mufliHun = the standing designation of those who have attained it. What varies is grammar and rhetorical polarity, not sense. The one sharp test, 20:64 (Pharaoh's sorcerers: 'and whoever gains the upper hand TODAY has aflaHa'), is worldly, time-bounded, and spoken by the condemned party, and the text rebuts it five verses later (20:69, 'the sorcerer does not yufliHu wherever he comes'). That token shows the bare word means only 'attain the aimed-at good outcome' — the salvation-coloring elsewhere is contextual, not lexical. Because the root never appears outside Form IV, this is honestly a claim about the Form-IV family, not about a deeper triangulated root sense.

**Coverage:** researched 40 / expected 40 · exact-set match: **True** (missing [], unexpected [], duplicate [])

**Supporting evidence refs (15):** 23:1:2:1, 87:14:2:1, 91:9:2:1, 20:64:7:1, 10:17:13:1, 12:23:22:1, 23:117:17:1, 20:69:13:1, 7:8:9:2, 23:102:6:2, 58:22:51:2, 5:90:15:1, 2:189:27:1, 2:5:8:2, 28:67:11:2

**Counterevidence refs (2):** 20:64:7:1, 20:69:13:1

**Hard cases:**
- `20:64:7:1` [ADVERSARIAL_BOUNDARY] — The single strongest counterexample: a worldly, time-bounded (al-yawma), opponent-voiced (Pharaoh's sorcerers) affirmative use of aflaHa about sheer domination (istaAAlA), rebutted in-narrative at 20:69. It bounds the gloss by refuting any salvific/eschatological lexicalization while confirming the 
- `28:67:11:2` [STRUCTURAL_ATYPICALITY] — Atypical participle framing: AAasA an yakuna mina l-mufliHin makes membership among al-mufliHun merely POSSIBLE even for one who repented, believed, and did good, showing al-mufliHun is a contingent attainment rather than a fixed conferred title.

**Falsification:** status **PASSED** · verdict SUPPORTED · falsifiable True · distinctiveness_ok True · failing_occurrences []
  - Rationale: The strongest available refutation — 20:64 (worldly, opponent-voiced, time-bounded) plus its in-narrative rebuttal 20:69 — was run against the thin nucleus and did not break it: the token is absorbed as a worldly instantiation and, decisively, refutes the competing thick salvific gloss instead. distinctiveness_ok is asserted on the strength of four Quran-internally demonstrable negative boundaries

**Independent AI semantic review:** `VERIFIED_AT_SCOPE` — SUPPORTING REVIEW EVIDENCE ONLY — NOT the required independent-human VerificationRecord. Does not satisfy CanonicalizationPolicy condition 6.

**Human decision (to be completed by the independent human / TRUSTED_LOCAL_OWNER):**

- [ ] VERIFY_AT_SCOPE  [ ] REJECT  [ ] RETURN_FOR_CORRECTION
- Reviewer identity: __________   Timestamp: __________
- Exact claim revision affirmed: __________
- Rationale: ______________________________________________
- Confirms: (1) claim matches evidence (2) scope not broader than evidence (3) supporting refs genuinely support (4) hard cases/counterevidence honest (5) falsification material (6) no unresolved seam defeats the claim

---

## ف و ه (`fwh`)

- Artifact: `artifacts/semantic-campaign/roots/fwh.json`
- Result strength: **STRONG** · Claim scope: **UNIVERSAL / ROOT_GENERALIZATION** · contract_type: ROOT_CONCEPT
- Revision binding: methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`, batch `batch07-wave5`, snapshot `snap_tanzil_1_1_ac0724796cbb`
  - _File-based campaign: no DB SemanticClaim / integer revision_id exists yet. A materialized SemanticClaim would start at revision_id=1. The human decision must bind to THIS persisted revision identity._

**Proposed canonical semantic claim (verbatim — do not rewrite):**

> The root ف و ه denotes the mouth — the concrete external oral aperture of the face, the boundary-organ between interior (heart/belly) and exterior through which intake passes in (water: 13:14), emission of speech/breath/manifested states passes out (18:5, 3:118, 61:8/9:32), and which can be physically sealed (36:65). It is a neutral, purely nominal body-part noun; it carries no lexical charge of speech-content, truth, falsity, insincerity, or externality-as-such.

_Plain explanation (verbatim):_ Every occurrence of fwh means the physical mouth. Sometimes it is a plain body part (water reaching the mouth in 13:14; hands to mouths in 14:9; mouths sealed in 36:65), and very often it is the aperture from or with which speech issues (words come 'out of' mouths in 18:5; people say things 'with their mouths' in 3:167, 5:41, 9:8, 24:15, 33:4, 9:30; they try to blow out God's light 'with their mouths' in 61:8, 9:32). The frequent hypocrisy/insincerity flavor is not in the word fwh itself: it is built every time by an explicit contrast term — heart (qalb), breast (sadr), knowledge (ilm), or God's truth (haqq). Strip that contrast and the mouth reverts to a neutral organ, as the drinking and gesture verses prove.

**Coverage:** researched 13 / expected 13 · exact-set match: **True** (missing [], unexpected [], duplicate [])

**Supporting evidence refs (13):** 13:14:18:1, 14:9:24:1, 18:5:12:1, 24:15:5:2, 33:4:22:2, 36:65:4:1, 3:118:19:1, 3:167:25:2, 5:41:13:2, 61:8:5:2, 9:30:13:2, 9:32:6:2, 9:8:12:2

**Counterevidence refs (0):** —

**Hard cases:**
- `61:8:5:2` [ADVERSARIAL_BOUNDARY] — Metonymic use: 'mouths' stands for feeble breath/propaganda aimed at extinguishing divine light, bordering on 'by their speech.' Tests whether the root shades from organ to utterance.
- `9:32:6:2` [ADVERSARIAL_BOUNDARY] — Parallel to 61:8: the same 'extinguish God's light with their mouths' metonymy, the strongest pull toward an 'utterance/breath' reading.
- `14:9:24:1` [STRUCTURAL_ATYPICALITY] — The hand-to-mouth gesture is pragmatically underdetermined by the co-text, making this the least semantically informative token, though the referent 'mouths' is unambiguous.

**Falsification:** status **PASSED** · verdict SUPPORTED · falsifiable True · distinctiveness_ok True · failing_occurrences []
  - Rationale: The enriched 'insincere-speech nucleus' competitor was actively tested and refuted by 13:14, 14:9, and 36:65 (pure physical uses with no verbal/inner content), while the concrete 'mouth' claim survives every occurrence. Distinctiveness is affirmed by explicit same-verse contrasts against lisān (24:15), jawf (33:4), and qalb/sadr, ruling out nearest neighbours. No occurrence fails; the claim is gen

**Independent AI semantic review:** `VERIFIED_AT_SCOPE` — SUPPORTING REVIEW EVIDENCE ONLY — NOT the required independent-human VerificationRecord. Does not satisfy CanonicalizationPolicy condition 6.

**Human decision (to be completed by the independent human / TRUSTED_LOCAL_OWNER):**

- [ ] VERIFY_AT_SCOPE  [ ] REJECT  [ ] RETURN_FOR_CORRECTION
- Reviewer identity: __________   Timestamp: __________
- Exact claim revision affirmed: __________
- Rationale: ______________________________________________
- Confirms: (1) claim matches evidence (2) scope not broader than evidence (3) supporting refs genuinely support (4) hard cases/counterevidence honest (5) falsification material (6) no unresolved seam defeats the claim

---

## غ ل م (`glm`)

- Artifact: `artifacts/semantic-campaign/roots/glm.json`
- Result strength: **STRONG** · Claim scope: **REPRESENTATIVE / LEXICALIZED_CLASS** · contract_type: ROOT_CONCEPT
- Revision binding: methodology `LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4`, batch `batch07-wave1`, snapshot `snap_tanzil_1_1_ac0724796cbb`
  - _File-based campaign: no DB SemanticClaim / integer revision_id exists yet. A materialized SemanticClaim would start at revision_id=1. The human decision must bind to THIS persisted revision identity._

**Proposed canonical semantic claim (verbatim — do not rewrite):**

> glm surfaces in the Quran exclusively as one nominal lexeme (sg غُلَام, dual غُلَٰمَيْن, broken pl غِلْمَان) denoting a HUMAN MALE in the young / pre-full-maturity life-stage (a 'boy / youth'). Two features are lexically entailed across all 13 tokens: (1) male sex, and (2) youth bounded above by أَشُدّ (maturity). All richer readings — son/offspring, servant, ward/orphan, merchandise, eschatological servitor, and every moral quality — are supplied by the syntactic frame or context, NOT by the root itself.

_Plain explanation (verbatim):_ Every one of the 13 occurrences names a young male person. When the word means 'son' (the 8 annunciation tokens to Abraham, Zechariah, Mary), the sonship is carried entirely by the surrounding frame — نُبَشِّرُكَ بِ (announce to you), أَهَبَ لَكِ (grant to you), يَكُونُ لِى (be mine) — and the reproductive objections (barren wife 19:8, virgin 19:20, old age 3:40) presuppose a male child produced by generation. Strip the frame and only 'young male' remains: unrelated finders simply say هَٰذَا غُلَٰمٌ of Joseph (12:19); Khidr kills an unrelated boy (18:74); the two غلامان are orphans not yet reached أَشُدّ (18:82); the غِلْمَان serve Paradise's dwellers 'belonging to them' (52:24). The single positive age-anchor is 18:82 (يَبْلُغَآ أَشُدَّهُمَا = they had not yet reached maturity), which fixes غلام as the stage BEFORE maturity. That the same noun takes different external adjectives — عَلِيم, حَلِيم, زَكِيّ, plus the name يَحْيَى — proves those qualities are predicated onto a neutral base noun, not part of it.

**Coverage:** researched 13 / expected 13 · exact-set match: **True** (missing [], unexpected [], duplicate [])

**Supporting evidence refs (5):** 18:82:4:2, 19:20:5:1, 12:19:10:1, 18:74:5:1, 52:24:3:1

**Counterevidence refs (0):** —

**Hard cases:**
- `52:24:3:1` [ADVERSARIAL_BOUNDARY] — Sole plural and sole eschatological-servitor use; it kills the strongest rival account ('glm = son/offspring') because these young males belong to and serve the dwellers without being their sons.
- `15:53:6:2` [ADVERSARIAL_BOUNDARY] — Unborn referent with a mature epithet is the point of maximum pressure on the age-stage feature, showing the youth component is proleptic in the annunciation cluster.
- `18:80:2:2` [ADVERSARIAL_BOUNDARY] — Moral-religious agency (طُغْيَان, كُفْر) ascribed to a غلام tests the upper boundary of 'youth'; the one genuinely under-determined variable is the precise ceiling.

**Falsification:** status **PASSED** · verdict SUPPORTED · falsifiable True · distinctiveness_ok True · failing_occurrences []
  - Rationale: An adversarial pass attacked the nucleus 'young human male, pre-maturity' across all three clusters. Maleness held 13/13 (masculine agreement, son-presupposing objections, no female token). The youth feature is directly anchored by 18:82 (أَشُدّ) and contradicted by no occurrence; the two rival enrichments cancel (52:24 defeats 'son', the unborn-plus-mature-epithet tokens defeat age-criteriality),

**Independent AI semantic review:** `VERIFIED_AT_SCOPE` — SUPPORTING REVIEW EVIDENCE ONLY — NOT the required independent-human VerificationRecord. Does not satisfy CanonicalizationPolicy condition 6.

**Human decision (to be completed by the independent human / TRUSTED_LOCAL_OWNER):**

- [ ] VERIFY_AT_SCOPE  [ ] REJECT  [ ] RETURN_FOR_CORRECTION
- Reviewer identity: __________   Timestamp: __________
- Exact claim revision affirmed: __________
- Rationale: ______________________________________________
- Confirms: (1) claim matches evidence (2) scope not broader than evidence (3) supporting refs genuinely support (4) hard cases/counterevidence honest (5) falsification material (6) no unresolved seam defeats the claim

---

## Next action after decisions

For each root marked VERIFY_AT_SCOPE by a genuine independent human: materialize the SemanticClaim if required, POST /judgments/{claim_id}/verification (decision=VERIFIED, verification_type=INDEPENDENT, evaluated_claim_revision==claim.revision_id), then POST /judgments/{claim_id}/canonicalize. The AI must not perform the human verification step.
