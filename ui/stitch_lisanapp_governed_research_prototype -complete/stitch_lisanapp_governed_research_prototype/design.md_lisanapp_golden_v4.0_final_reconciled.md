---
name: Lisanapp Governed Research System
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daea'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  primary: '#10b981'
  secondary: '#0058be'
  error: '#ba1a1a'
  stale: '#F97316'
  pending: '#F59E0B'
  
typography:
  font-family: 'IBM Plex Sans Arabic'
  mono: 'JetBrains Mono'
  quranic: 'Traditional Arabic' # or dedicated verse font

tokens:
  epistemic:
    LOCK_BLOCKED: { color: '#ba1a1a', icon: 'lock' }
    LOCK_INTERNAL_RESULT: { color: '#0058be', icon: 'lock_open' }
    SUPPORTED: { color: '#10b981', icon: 'check_circle' }
  purity:
    CLEAN: { color: '#10b981', label: 'نقي' }
    CONTAMINATED: { color: '#ba1a1a', label: 'ملوث' }
    HERITAGE_BIAS: { color: '#F59E0B', label: 'تحيز تراثي' }

layout:
  direction: RTL
  sidebar_width: 280px
  inspector_width: 320px
  page_margin: 40px
---
# Lisanapp Design System - v4.0 FINAL

## RTL-First Principles
- Navigation (SideNavBar) on the RIGHT.
- Contextual Inspector on the LEFT.

## Four-Axis Status Model
Independent dimensions:
1. Epistemic (OBSERVATION to REJECTED)
2. Review (NOT_REVIEWED to APPROVED)
3. Freshness (CURRENT, STALE)
4. Publication (PRIVATE to PUBLISHED)

## Three View Levels
- Simplified: Executive summary.
- Research: Evidence and gates.
- Technical: Hashes, JSON, and traces.
