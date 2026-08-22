# Lisanapp Design System - v4.0 UX Golden Prototype

## RTL-First Principles
- Primary navigation (SideNavBar) is docked to the **RIGHT**.
- Contextual Inspector (Entity Details) is docked to the **LEFT**.
- Page margins: `px-margin-page` (40px).
- Text alignment: Right-aligned for Arabic, left-aligned for technical/mono codes.

## Typography
- **Primary:** IBM Plex Sans Arabic.
- **Technical/Mono:** JetBrains Mono.
- **Quranic Verse:** Dedicated Quranic Font with increased line height (`56px`).
- **Headlines:** `headline-lg` (24px/Bold), `headline-md` (20px/SemiBold).

## Four-Axis Status Model
Every entity must display four independent status axes:
1. **Epistemic:** OBSERVATION, HYPOTHESIS, TESTED, SUPPORTED, LOCK_BLOCKED, LOCK_INTERNAL_RESULT, REJECTED, UNRESOLVED.
2. **Review:** NOT_REVIEWED, REVIEW_REQUIRED, IN_REVIEW, APPROVED, REJECTED, OWNER_DECISION_REQUIRED.
3. **Freshness:** CURRENT, STALE, INVALIDATED, REVALIDATION_REQUIRED.
4. **Publication:** PRIVATE_WORKING, REVIEWABLE, PUBLISHABLE, PUBLISHED, WITHDRAWN.

## Semantic Color Palette
- **Primary:** #10b981 (Research Success/Positive).
- **Secondary:** #0058be (Governed Actions).
- **Blocked/Error:** #ba1a1a (Lock Blocked / Fail).
- **Stale:** #F97316 (Invalidated / Old).
- **In-Review:** #F59E0B (Pending Human Decision).

## Shared Components
- **Global Shell:** SideNavBar (Right) + TopAppBar (Sticky).
- **Contextual Inspector:** Global side drawer (Left) with identity, status axes, hash, and dependencies.
- **Steward Drawer:** Global command interface for governed intent.
- **Lock Gate Cards:** Dynamic items showing PASS/FAIL/N-A with evidence link.

## Interaction Conventions
- **Progressive Disclosure:** Simplified view by default; Research/Technical levels for deeper data.
- **Audit Trace:** Every claim links back to a Research Run and Corpus Snapshot.
- **No Confidence Scores:** Never display numeric percentages for truth.
