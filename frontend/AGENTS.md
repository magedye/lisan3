# Lisanapp Frontend Policy

This file supplements the root `AGENTS.md` for work under `frontend/`.

## Source of Truth

Use the canonical UX Constitution for product behavior.

Use the Stitch Golden Prototype as a visual/interaction reference only.

Do not treat Stitch HTML, fixtures, or prototype state transitions
as semantic/domain authority.

For Knowledge Explorer, Semantic Differentiation candidate discovery, graph
visualization, or retrieval-provenance UI changes, read and follow
`docs/canonical/LISAN_HYBRID_KNOWLEDGE_RETRIEVAL_ARCHITECTURE.md`.

## Stack

Preserve the approved frontend baseline:
- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- Radix UI
- CSS Logical Properties
- generated OpenAPI TypeScript contracts

Do not hand-edit generated API contract files.

## RTL

Arabic is the native design direction.

Prefer logical properties and direction-neutral components.

Do not implement RTL as a translated LTR afterthought.

## Domain State

The UI must display but must not invent authoritative state.

Preserve independent display of:
- Epistemic
- Review
- Freshness
- Publication

Do not infer semantic confidence from percentages, colors, progress bars,
or visual maturity.

Color alone must never communicate state.

## Canonical Writes

The frontend never writes canonical semantic knowledge directly.

All governed changes go through backend commands/contracts.

Do not reproduce prototype-only shortcuts that bypass backend policy.

## Evidence UX

Counterevidence is first-class.

Preserve traceability from claims to evidence, run, Corpus, methodology,
provenance, and applicable audit information.

## Verification

Distinguish:
- static build;
- component tests;
- backend integration;
- browser E2E.

`npm run build` does not prove E2E behavior.

Use Playwright for canonical browser journeys when required by the current gate.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
