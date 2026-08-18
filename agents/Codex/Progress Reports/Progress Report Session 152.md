# Progress Report — Codex, Session 152

**Written:** 2026-08-17 19:13 PDT
**Covers:** my Sessions 145–152 (previous regular report: Session 144)
**Phase:** 2 — Execution, with limited Phase-3 verification-packet assembly
**Written for:** Randy

---

## The short version

The project has spent this eight-session stretch finishing and stress-testing the second half of
the bridge that will eventually connect an already-established result to the director's visual
verification screen. The production code is now built through read-order row 20: it can
authenticate paired cases, bind their time and decisions, reconstruct their body geometry,
resolve whether the source is development or final, and assemble a complete three-case bundle.
It still cannot write that bundle or expose it through the real command-line path.

The work is moving, but it is not ready for formal review. Claude has deliberately kept the build
owner-held until row 21, the observed file-open boundary, the remaining acceptance tests, command
wiring and mutation sweep are complete. That is the correct sequencing.

My cross-reviews found and Claude repaired five concrete defects in the partial build: a false
maximum-window claim, an impossible decision step, an unbound geometry model identity, an
incoherent provenance test seam and a provenance banner that a caller could forge. This session
found two remaining evidence problems: the seam still calls an invalid draft document “frozen,”
and the new three-case test context leaves its rewritten connection record behind after exit.

All 2,935 packet tests pass. That means the current code is internally regression-free against
the suite. It does not mean the two missing properties are proved; both gaps are in what the tests
claim to witness.

## What this bridge is doing

The verification screen must be a display of a result established elsewhere, not a place where
the project quietly takes a new look at scientific data. The connection record is the manifest
that names exactly which configuration, result, cases, indexes, payloads and checkpoints are being
displayed. The adapter's job is to authenticate those named bytes, refuse anything else, assemble
the display object, and write only the declared output files.

That is why this infrastructure is being reviewed so aggressively before a real record exists.
A display can look polished while being connected to the wrong file, the wrong model, a changed
payload or a caller-supplied label. The safest time to discover those paths is in synthetic tests,
before any later-role read is authorized.

## What happened in Sessions 145–152

### 1. The public Step-4b-ii-a heartbeat closed without rewriting history

Session 145 confirmed that Claude's prose repair fixed two accuracy errors in the public running
log, but it also found that the repair rewrote an already-published line in place. Session 146
approved the final form only after the original published line was restored byte for byte and a
dated correction was appended beneath it. The resulting README is jointly approved and the review
chat is concluded.

This matters beyond one sentence. The public running log is the record of what the project said at
the time. A later correction should make the truth clearer without making the earlier state
disappear.

### 2. Rows 13–20 were built incrementally instead of being handed over half-finished

Sessions 147–152 reviewed Claude's partial owner work as it grew. No Review Card was opened because
there was no stable candidate yet. That kept ordinary cross-review separate from formal approval
and let corrections propagate forward without pretending an unfinished file was settled.

The build now covers:

- both C1 and S arms for each case;
- pair identity, onset, task reference and label agreement;
- playback and controller time grids;
- valid decision ordering and the declared tracking window;
- centerlines reconstructed from authenticated joint/deformation data;
- development-versus-final provenance; and
- assembly of a complete structure/actuator/sensor bundle.

### 3. Five forward defects were found and repaired

Across Sessions 148–152, the general reviews found:

1. a `0.040 s` fixture window described as the largest supported one even though `0.042 s` also
   passed;
2. decision step `T` accepted even though the live producer's valid step domain is `0..T-1`, while
   its real initial step-0/time-0 decision was rejected;
3. the geometry producer's `model_id` was not joined to the authenticated configuration;
4. the row-19 provenance seam changed a few identity copies while leaving census, manifest,
   role-index and config-document copies inconsistent; and
5. row 20 accepted a separately constructed `FINAL` or `SYNTHETIC_FIXTURE` banner over a
   development connection.

Claude accepted and repaired each one. The production provenance guard added in Session 152 is
especially important: it runs before any scene is built, so a forged banner never becomes an
otherwise-valid visual object.

### 4. Two test-evidence defects remain

The row-19 seam now checks eighteen identity joins plus the row-3 and row-4 authority policies.
But its “frozen” test document still lives at the draft filename and retains the draft decision,
false confirmatory flag, open gates and unresolved model/calibration/evaluation fields. The real
configuration validator rejects it immediately. The test therefore still does not represent a
state that rows 3–12 could have produced, despite its new name.

The three-case menu context has a separate cleanup problem. It restores the files named by its
temporary connection record but not the record itself. After the context exits, the remaining
record points at digests that no longer exist. A later automatic fixture repair hides that from
subsequent tests; the context manager's own restoration promise is nevertheless false.

Neither is a scientific defect, and neither proves the production adapter wrong. Both matter
because the acceptance evidence must say exactly what it actually tested.

## What is working

- Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a are closed at explicit same-state approval.
- The current partial adapter code passes 277 focused tests normally and under optimized Python.
- All 2,935 packet tests pass.
- Rows 13–20 now have a complete synthetic accept route, including a three-source menu.
- The production row-20 provenance binding is correct and refuses forged public/private states.
- Claude has preserved ownership and has not opened a Review Card prematurely.
- The real-result entry remains shut and no later-role scientific input has been opened.

## What is not working or remains open

- The row-19 “post-row-12” witness is still not accepted by the production config validator.
- The three-case context manager does not restore its own rewritten connection record on exit.
- Row 21 output writing is unbuilt.
- The audit-hook proof that the adapter opens exactly the declared file set is unbuilt.
- Remaining B2/B3/B5 acceptance rows, roles command wiring, the additive real-entry edit and the
  mutation sweep are unbuilt.
- No stable Step-4b-ii-b candidate, Review Card, subject chat or approval exists.
- No production connection record, selected capacity, selected checkpoint set, probability or
  abstention threshold, or frozen final configuration exists.
- The Claim Sheet director review remains open and non-blocking in `director_requests.md`.

All eight Codex sessions covered here spent **zero scientific resource**. Counters remain 278
rollouts, 67 fits and 67 checkpoints, with zero pilot/validation/test reads.

## Verification artifact

The visible synthetic verification screen has not changed and no new public heartbeat was earned.
The work underneath it has advanced: the future real-result bridge can now assemble a complete
three-case bundle through row 20, but it cannot write or expose that bundle yet.

That distinction is the honest state. The screen still demonstrates interface behavior with
fabricated data. It does not show a project result and cannot say whether structural sensing helps.

## What happens next

1. Claude repairs the row-19 witness so it is either genuinely accepted by the production config
   validator or explicitly narrowed so it no longer claims full post-row-12 equivalence.
2. Claude makes the three-case context restore the connection record itself and strengthens the
   restoration test so no manual cleanup hides the property being tested.
3. Claude completes row 21, the observed open-set proof, the remaining acceptance rows, command
   wiring and the two-pass mutation sweep.
4. Claude then creates the first Step-4b-ii-b Review Card and narrow subject chat and hands off one
   stable exact candidate.
5. Codex performs the one complete Round-1 review. Production records, scientific reads and every
   later gate remain separate authorizations after that.

The important state is simple: most of the bridge is built, the production provenance repair is
sound, and the suite is green. Two of the suite's strongest claims are still wider than what their
own fixtures prove, so formal review should wait.

— Codex
