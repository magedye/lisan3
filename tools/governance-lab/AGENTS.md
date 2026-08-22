# Governance & Methodology Lab Policy

This directory contains evaluation and verification tooling.

Nothing under this directory becomes canonical Lisan authority merely because
it is executable or produces a passing result.

## Purpose

Use lab tooling to challenge and evaluate:
- domain invariants;
- methodology behavior;
- AI behavior;
- API contracts;
- test strength;
- policy consistency.

## Authority Boundary

Canonical requirements define what must hold.

Lab tools test those requirements.

Do not rewrite canonical requirements to satisfy a lab tool.

## Evidence Discipline

Record separately:

- CONFIGURED
- EXECUTED
- PASSED
- FAILED
- BLOCKED
- DEFERRED

Never treat configuration as execution evidence.

## Approved Tooling

Follow:
`docs/canonical/LISAN_TOOLING_ADOPTION_REFERENCE.md`

Do not introduce additional policy/formal/eval tools without satisfying
the documented adoption trigger.

## Experimental Results

Experimental OPA/CUE/Z3/DSPy/etc. results remain evaluation evidence only
until an explicit canonical decision adopts their output.

Store reports under the lab reports area, not canonical directories.
