# Summary — Slot-8 Step-4a Connection-Record Design

**Participants:** Claude, Codex
**Date Range:** 2026-08-14
**Status:** Concluded — Approved in Round 2 under the superseding Review Card protocol.

## Outcome

Both agents explicitly approve the exact Step-4a design at
`Reproducibility Packet/protocol/slot8-connection-record-v0.1.md`, Git blob
`032db1666efbe00adec5696de70424d531ba33a2`, raw SHA-256
`f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc`, 83,181 bytes / 1,062 LF /
0 CR. Codex's Round-2 delta review passed its updated 72-check audit and the focused config-contract
suite passed 18/18.

Finding 1 is resolved: both development and final authority branches must cross the same internal
roles-mode entry point after record authentication. One explicit packet root governs every
packet-relative resolution needed to reach the deliberate Step-5 stop. Tests inject an isolated
temporary packet root; the public path positively proves that it binds the module-derived live
packet root and exposes no caller or environment override.

## What this closes and what follows

Step 4a is closed / both approved. It licenses only a new Step-4b adapter-and-test build under its
own Review Card and subject-scoped chat. That build must include B8's four authority/config drives,
keep every test write below the temporary root, prove the live packet never gains `config.json`,
and correct the tracked `build_role_bundle` docstring gloss as an additive follow-up.

No production connection record, real-role or scientific read, Step 4c–4f action, capacity or
threshold selection, final configuration, run, or C1-versus-S statement is authorized by this
closure.
