# Summary — Slot-8 Step-4b-i Connection-Record Contract

**Participants:** Claude, Codex
**Date Range:** 2026-08-14
**Status:** Concluded — Approved in Round 3 under the Review Card protocol.

## Outcome

Both agents explicitly approve the exact Step-4b-i candidate:

- `Reproducibility Packet/scripts/utils/connection_record.py`, Git blob
  `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`;
- `Reproducibility Packet/tests/test_connection_record.py`, Git blob
  `f854b894a76eb972f9b2e65903233909f05ef287`; and
- `Reproducibility Packet/scripts/render_verification_scene.py`, Git blob
  `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`.

The connection-record contract now authenticates and strict-parses read-order rows 1–3,
deep-freezes the authenticated state, binds every declared domain to one injected packet root,
derives the expected open set, and refuses non-portable or ambiguous output namespaces. The
renderer independently checks the complete write set for containment, component length and
case-insensitive uniqueness before writing. The 251-character, fixed-manifest-name and
case-fold-collision probes all refuse without partial output; the valid seed-7 bundle remains ten
byte-identical files whose reported digest hashes the manifest it names.

Final reviewer evidence passed 341 focused tests, 341 under optimized Python, 2,608 packet-wide
tests, a separate 19-check boundary audit, `py_compile`, `git diff --check`, and exact regeneration
of the ten tracked Step-3 fixture files at bundle digest
`3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

One review-record-only correction was made at closure: Git's actual Round-3 numstats are module
`+128/−10`, renderer `+51/−3`, and tests `+421/−0`. The changed-region boundary remained correct,
and no candidate code byte changed.

## Boundary and next step

This closes only Step 4b-i. Full Step 4b remains open. Claude may begin one new Step-4b-ii build
under a new Review Card and subject chat. No production connection record, real-role or scientific
read, Step 4c–4f work, capacity or threshold selection, final configuration, adapter invocation, or
C1-versus-S claim is authorized by this closure.
