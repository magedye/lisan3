---
name: Lisanapp Governed Research System
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daea'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eefe'
  surface-container-high: '#e2e8f8'
  surface-container-highest: '#dce2f3'
  on-surface: '#151c27'
  on-surface-variant: '#3c4a42'
  inverse-surface: '#2a313d'
  inverse-on-surface: '#ebf1ff'
  outline: '#6c7a71'
  outline-variant: '#bbcabf'
  surface-tint: '#006c49'
  primary: '#006c49'
  on-primary: '#ffffff'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#4edea3'
  secondary: '#0058be'
  on-secondary: '#ffffff'
  secondary-container: '#2170e4'
  on-secondary-container: '#fefcff'
  tertiary: '#a43a3a'
  on-tertiary: '#ffffff'
  tertiary-container: '#fc7c78'
  on-tertiary-container: '#711419'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3af'
  on-tertiary-fixed: '#410005'
  on-tertiary-fixed-variant: '#842225'
  background: '#f9f9ff'
  on-background: '#151c27'
  surface-variant: '#dce2f3'
  status-supported: '#10B981'
  status-hypothesis: '#3B82F6'
  status-blocked: '#F59E0B'
  status-rejected: '#EF4444'
  status-stale: '#F97316'
  status-owner: '#8B5CF6'
  surface-background: '#F9FAFB'
  surface-card: '#FFFFFF'
  border-subtle: '#E5E7EB'
typography:
  quran-verse-display:
    fontFamily: Traditional Quranic Font
    fontSize: 32px
    fontWeight: '400'
    lineHeight: 56px
  headline-lg:
    fontFamily: IBM Plex Sans Arabic
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: IBM Plex Sans Arabic
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: IBM Plex Sans Arabic
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: IBM Plex Sans Arabic
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: IBM Plex Sans Arabic
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  mono-technical:
    fontFamily: jetbrainsMono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  gutter: 24px
  margin-page: 40px
  panel-width-inspector: 400px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is anchored in **Academic Rigor and Epistemic Transparency**. It is built for a governed environment where Quranic research is treated with the precision of a scientific laboratory or a legal framework. The visual language prioritizes clarity, auditability, and the "traceability of truth."

The chosen style is **Corporate / Modern with a focus on Information Density**. It avoids decorative flourishes in favor of structured data visualization and clear hierarchy. The interface follows a "Governance-First" philosophy, where the UI serves as a governed runtime for methodology.

- **Primary Axis:** Native RTL (Right-to-Left) layout.
- **Visual Tone:** Professional, authoritative, and structured.
- **Key Principles:** Progressive disclosure of complexity, multi-axis status visibility, and generous whitespace to maintain focus during intensive research.

## Colors

The color palette is strictly semantic and status-driven. Color is never the sole carrier of meaning; it must always be accompanied by icons and text labels to ensure accessibility and methodological clarity.

- **Primary (Green - #10B981):** Represents `SUPPORTED`, `APPROVED`, and Methodological Purity.
- **Secondary (Blue - #3B82F6):** Represents `HYPOTHESIS`, `IN_REVIEW`, and Work-in-Progress research.
- **Amber (#F59E0B):** Indicates `LOCK_BLOCKED` or `REVIEW_REQUIRED`.
- **Red (#EF4444):** Denotes `REJECTED` findings or `HERITAGE_BIAS` (Methodological Pollution).
- **Orange (#F97316):** Used for `STALE` data requiring revalidation.
- **Special Purple (#8B5CF6):** Reserved for actions requiring `OWNER_DECISION`.
- **Neutral Gray (#6B7280):** Represents `UNKNOWN` or unresolved states.

Avoid "Gold" or metallic gradients to prevent traditionalist aesthetic tropes that conflict with the platform's scientific mandate.

## Typography

Typography is divided into three functional roles:
1. **UI & Navigation:** IBM Plex Sans Arabic is used for its clarity and modern technical feel.
2. **Sacred Text:** A traditional, high-legibility Quranic font is used exclusively for verses to distinguish primary source material from commentary or research.
3. **Technical Data:** JetBrains Mono is used for IDs, JSON schemas, hashes, and audit traces in the Expert view.

Headlines should be bold and authoritative. Body text requires generous line heights (1.5x minimum) to accommodate Arabic diacritics and ensure readability during long-form research.

## Layout & Spacing

This design system utilizes a **Fluid Grid** with fixed-width side panels for contextual inspection. 

- **Layout Hierarchy:** 
  - **Global Shell:** A right-hand primary navigation sidebar (RTL).
  - **Main Workspace:** Central area for data grids and research matrices.
  - **Contextual Inspector:** A left-hand slide-over panel for metadata and evidence inspection.
- **Spacing Philosophy:** Use generous whitespace to separate distinct epistemic layers. Research cards and data rows should not feel crowded; clarity is prioritized over density.
- **Breakpoints:** 
  - **Desktop (1280px+):** Full 12-column visibility with persistent side panels.
  - **Tablet (768px-1279px):** Inspector panels become overlays; navigation collapses to icons.
  - **Mobile (Below 768px):** Single column stack; focused Quranic text view with modal-based governance gates.

## Elevation & Depth

Hierarchy is conveyed through **Tonal Layering** and **Structural Containment** rather than deep shadows.

- **Surface Tiers:** The main background uses a subtle off-white (`#F9FAFB`), while active work surfaces and cards use pure white (`#FFFFFF`) with 1px borders.
- **Borders:** Low-contrast outlines (`#E5E7EB`) are used for standard containers. Semantic colors are applied to borders to indicate the status of the data within (e.g., a blue border for a hypothesis card).
- **Epistemic Layering:** The "Steward" command interface and "Blind Lab" isolation banners use high-z-index overlays with backdrop blurs to signal a change in the user's operational state.
- **Shadows:** Only used for floating elements like the Contextual Inspector or dropdown menus, using a soft, diffused neutral shadow (0px 4px 20px rgba(0,0,0,0.05)).

## Shapes

The shape language is **Soft (0.25rem / 4px)**. This subtle rounding maintains the academic and precise feel of the platform without appearing overly clinical or sharp.

- **Standard Elements:** Buttons, inputs, and small badges use `rounded` (4px).
- **Cards & Panels:** Large containers like the Research Matrix or Layered Cards use `rounded-lg` (8px).
- **Interactive States:** Governance Steppers use circular (pill) shapes for indicators to distinguish them from data objects.

## Components

- **Epistemic Status Badges:** Compact labels with an icon + text + semantic background. They must appear in clusters of four (Epistemic, Review, Freshness, Publication) to provide a complete purity report.
- **Layered Cards:** Used for the "Layer Separation Matrix." These cards should be visually stacked or indented to represent the equation: `ROOT + FORM + CONSTRUCTION + ARGUMENT + CONTEXT`.
- **Governance Steppers:** Vertical or horizontal indicators showing the progress of a research run through methodological gates (e.g., Purity Gate).
- **Contextual Inspector:** A side panel containing metadata, audit logs, and evidence links. It should use a distinct background shade to separate it from the primary workspace.
- **Data Grids:** High-density tables with monospace fonts for technical IDs and crisp borders for clarity.
- **Isolation Banner:** A high-contrast, top-fixed banner that appears during "Blind Lab" mode to alert the user that heritage dictionaries are hidden to prevent bias.