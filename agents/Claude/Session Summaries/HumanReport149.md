# Human Report — Claude Session 149

**Current date and time:** 2026-08-17 12:25 PDT (measured with the shell immediately before writing this line)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session did two things. It **discharged both items Codex raised against my Session-148
build** in its own Session-148 cross-review — one of which was a genuine false claim I had
written — and it **built read-order row 18 of the connection adapter**, the geometry
derivation, which is the row the whole of sub-step 4b-ii-b was sequenced around.

The packet-wide test suite is at **2,901 passed, 0 failed** (from 2,889), and the arithmetic
closes exactly: 2,889 + 12 = 2,901.

**Nothing built this session is reviewed, and there is still no Review Card and no subject
chat for sub-step 4b-ii-b.** That remains deliberate: the review protocol requires a stable
candidate before a card can name one, and the candidate is not stable until rows 19 through
21, the audit-hook observer, the CLI wiring and the mutation sweep are done.

---

## What Codex found, and what I did about it

Codex's Session 148 was a general recent-work review of my Session-148 rows-13-17 build. It
edited no byte of mine — correctly, since I still own an unfinished build — and raised one
definite defect and one interpretation question.

### 1. The "largest closable window" claim was false. It is corrected forward.

My Session-148 test was named
`test_the_fixture_window_is_the_largest_this_grid_can_close`, and its docstring, a comment
beside the constant and my own human report all carried that claim. **It is not true.** The
contract fixture's grid runs 0.000 s to 0.062 s in 0.002 s samples; the live metric accepts a
0.040 s window *and* a 0.042 s window and refuses 0.044 s. The largest window this grid can
close is 0.042 s, not 0.040 s.

What makes this worth recording rather than just fixing: **my test had already driven 0.040
and 0.044 and I called that "the bound measured beside it."** Two values that bracket a
maximum do not locate it. The one call that would have settled the question — 0.042 — was the
one nobody made, and the superlative in the test's own name was a claim about the value I did
not try.

The repair keeps 0.040 s and states the convention that owns the choice, which is what Codex
offered as the alternative to changing the number: *the largest whole multiple of 0.01 s
inside the bound*. There is a real reason to prefer it over the maximum. A window at exactly
the grid's limit sits on a boundary, so any later change to the fixture's step count would
turn a passing fixture into a refusal for a reason that has nothing to do with the row under
test. The test is renamed to what it actually establishes and now drives all three values.

### 2. Row 16 bounds the time axis only, and that is now a written ruling rather than an inference.

Codex observed that row 16 requires a decision's `decision_time_s` to lie inside the playback
extent while accepting a decision whose `step` is at or past the playback grid's length, and
asked which reading of the design's "inside the playback extent" I meant. It explicitly did
not call this a defect, which was the right call.

The settled answer is **time only**, and the reflex answer — bound both axes, call it
fail-closed — is wrong here. The project has already paid for this lesson twice. Finding CI
forbids indexing the playback grid by the label's `onset_index`, and read-order row 15 forbids
comparing the controller's clock to the playback grid, in both cases because a faithful
producer offsets that axis by one control interval and binding it would reject real data. An
estimator that decides on its own cadence is the same class of faithful producer: the schema
calls `step` bookkeeping and ties it to no grid, and the one consumer of a decision — the
scene's causal call panel — selects by time and never uses `step` to reach into an array.
Declining the grid binding leaves `step` fully guarded in every other respect.

The argument is now in the function's docstring and pinned by a test named for the ruling, so
a later session that tightens it will read the reason instead of rediscovering it. If a later
artifact does make the estimator's step an index into the playback grid, that is an amendment
to the record design, not a quiet tightening in the adapter.

---

## What row 18 turned out to be

The plan gave row 18 three jobs. **One of them was already built.** Read-order row 5 —
approved and closed in sub-step 4b-ii-a — already compares the record's declared distal
tolerance against the named field of the authenticated geometry-validation artifact *and*
requires that artifact's recorded maximum deviation not to exceed it. So row 18's remaining
work is the derivation and the distal comparison, and both of those already existed as
functions after Session 147 built the shared forward map.

`resolve_geometry` is therefore a call and not a copy: it derives each arm's centerline
through `utils.centerline_geometry` under the geometry the *record* declares, requires the
derived distal point to agree with the authenticated true tip to within the record's declared
tolerance, and carries the measured agreement forward rather than reducing it to a boolean. It
supplies no tolerance of its own — sub-step 4b chooses no real-data tolerance, and the fixture
generator's own construction constant is deliberately not reused.

**One design choice I made and want on the record.** The derivation module raises the row's
refusal itself, so I considered threading an "which arm is this" label through it so refusals
would name the arm. That would have moved 39 call sites. Before paying it I enumerated which
of the derivation's refusals are actually reachable through row 18: the rank, width,
grid-length and non-finite ones are all unreachable, because step 12 ran both arrays through
the schema's own role contract and step 15 bound every frame-bearing array's leading axis to
the one playback grid. What remains is either record-level — the same for every arm, so there
is no arm to name — or the distal comparison, which already takes the arm's name and prints
it. So the owner's refusal is passed through untouched, and the docstring says why.

## The accept path, and three things it had to be refused to learn

Row 18 cannot be accepted against the existing contract fixture, and that is measured rather
than assumed: its deformation and its tip come from two independent synthetic maps, so a
derivation walking its declared chain would miss its recorded tip for reasons that say nothing
about the derivation. Session 147 built the dedicated coherent fixture for exactly this.

Rather than build a second harness with a second role tree — manifest, audits, indexes,
checkpoints, observations, labels, estimator outputs, controller logs, none of which row 18 is
about — the accept path **installs the coherent fixture over the existing harness**. A context
manager rewrites the three things the row is about (both arms' plant payloads, the
geometry-validation artifact, and the record's whole geometry block) and regenerates every
identity the rewrite moves from the files themselves, so the chain still authenticates end to
end and a refusal comes from row 18 rather than from an earlier digest check.

Three things the build learned by being refused first:

1. **Both arms must carry the same plant record.** Row 14 requires the two arms to agree about
   the commanded trajectory, so two independently generated ones are refused a row before the
   one under test.
2. **The coherent record's grid must be the contract fixture's grid** — 32 steps at 500 Hz —
   or row 15 refuses the rewrite before row 18 is reached. The control rate is a literal in the
   test file, pinned by equality against the config the harness actually loads.
3. **Displacing the tip to drive the tolerance refusal must carry the tracking error with
   it.** The role contract requires the tracking error to equal the commanded trajectory minus
   the true tip, so moving the tip alone is refused at step 12 as an inconsistent payload and
   never reaches row 18. Carried consistently, the payload is internally impeccable and still
   describes a body the declared chain does not produce — which is exactly the fault row 18
   exists to see, and exactly the one no single-payload check can.

The coherent fixture's agreement is **exactly 0.0 m**, because its generator sets the recorded
tip to the derived distal point itself. A non-zero value there would mean the generator's copy
of the map and the adapter's copy had diverged — which is the failure the shared module exists
to make impossible.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — `+214/-7`. Row 18's wiring
  (`ArmGeometry`, `CaseGeometry`, `AuthenticatedGeometry`, `resolve_geometry`), the row-16
  interpretation ruling in `resolve_decisions`' docstring, and the module docstring moved from
  rows 4-17 to rows 4-18. Blob `88ea30e753d24e295c18e0175983224cb0c8f88c`, raw SHA-256
  `d1ac714b7511804253590824b20745f409ab7d5e7d8203239289383816b1b035`, 136,290 B / 2,922 LF /
  0 CR / pure ASCII / no BOM / final newline.
- `Reproducibility Packet/tests/test_connection_adapter.py` — `+448/-23`. Twelve new tests
  (eleven for row 18, one for the row-16 ruling), the renamed and corrected window test, and
  the coherent-fixture installer. Blob `7fde611f7ef1c65be72861122496623ec90b3fae`, raw SHA-256
  `d0f42d5b9b7d55ce6203d1f96a3b592e153d0f00a339d80b148aa53926130b17`, 171,732 B / 4,180 LF /
  0 CR / pure ASCII / no BOM / final newline.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — `+91/-0`, Appendix C: what row 18 turned
  out to own, how the accept path is driven, both of Codex's items, and what is left in order.
- `agents/Claude/Permanent Instruments.md` — lessons 263 through 266.
- `agents/Claude/Session Summaries/HumanReport149.md` — this file.
- `agents/Claude/README.md` — Session 149.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 150.

**No Review Card, chat transcript, root README, protocol document, schema, configuration or
scientific result was changed.**

## Verification

All figures measured this session with the project interpreter from the repository root.

- focused adapter / authenticated-storage pair: **243 passed** (was 231);
- the same pair under `PYTHONOPTIMIZE=1`: **243 passed**;
- packet-wide suite: **2,901 passed, 0 failed, 156.24 s** (was 2,889). **2,889 + 12 = 2,901
  exactly**;
- `py_compile` clean on both edited files; `git diff --check` clean; `git status --porcelain`
  shows exactly the three files listed above.

**No mutation sweep ran, and that is on plan rather than an omission.** The build plan
sequences the two-pass sweep on the *finished* pair, immediately before the handoff. Sweeping
a partial build would have to be redone against the whole. Its staged-tree set (`scripts`,
`tests`, `schema`, `config` and `results`) and its two-pass shape are still budgeted.

## Scientific and authorization boundary

**This session spent zero scientific resource.** Counters unchanged: **278 rollouts, 67 fits,
67 checkpoints, zero pilot/validation/test reads.** It opened no role index, role payload,
checkpoint, estimator output, controller log, production configuration or pilot/validation/test
result; **built no MuJoCo model**, stepped no rollout, ran no fit and rendered no figure. It
built the synthetic contract fixture and the synthetic coherent fixture into temporary trees,
which is what the test suite does on every run. The two off-limits code-identity files —
`storage_contract.py` and `role_contract.py` — were **read at source and not edited**.

Disclosed reads, all tracked development text, none opening a payload: `role_contract.py`
(read for its tracking-error rule), `estimator.py` (read for the schema-D struct's own
statement about `step`), `build_data_contract_fixture.py`, `verification_scene.py`,
`centerline_geometry.py`, `coherent_geometry_fixture.py`, and the approved Step-4a design's
read-order table.

Slot-8 Steps 1, 2 and 3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed at both approvals
at their recorded exact bytes. **Step 4b-ii-b remains in progress and wholly unapproved.** The
public `roles` subcommand still refuses unconditionally, which is the correct state until the
whole of sub-step 4b closes. Steps 4c through 4f and every later scientific gate remain shut.

## Live-Run README heartbeat

**The check ran and answered no.** No artifact finished, no phase closed and no result was
produced. Three quarters of an internal build, one forward correction and one recorded
interpretation are not a public milestone, and an entry announcing progress inside an
unreviewed build is the session-journal texture the playbook forbids. The root README is
unchanged at the jointly approved blob `7342bc8c`.

## Next steps

1. **Rows 19, 20 and 21** — the computed provenance state, the bundle assembly and the
   exclusive-create write. Row 19's accept path is `SYNTHETIC_FIXTURE`; `DEVELOPMENT_ONLY` is
   computed and can be refused.
2. Then the audit-hook observer of invariant W3, acceptance tests B2 and B5, the remaining B3
   rows, the `roles` CLI wiring and the additive `build_role_bundle` edit.
3. **Then** the two-pass mutation sweep on the finished pair, before the handoff and not after.
4. **Then** the Review Card and the subject chat, naming the candidate three ways and resolving
   every blob id before the card governs. Seven files will be named in it, including the four
   previously closed ones that this build has authorised movement of.
