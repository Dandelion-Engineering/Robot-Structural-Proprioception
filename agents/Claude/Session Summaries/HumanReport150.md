# Human Report — Claude Session 150

**Current date and time:** 2026-08-17 14:22 PDT (measured with the shell immediately before closeout writing)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session did three things: it accepted and discharged both of the blocking forward
corrections Codex raised against my Session-149 work, and it built read-order **row 19**
of the Slot-8 connection adapter. Codex was right on both counts and I did not contest
either. Both were real, reachable defects that the whole green test suite — 2,901 passing
tests at the time — did not exercise, which is the useful part of the story rather than
an aside.

The plain-language version of what the adapter is for, restated so this report stands on
its own: the connection adapter is the piece of software that will eventually take a
sealed, signed description of one experiment — which data files, which configuration,
which model, which thresholds — and turn it into a picture a non-specialist can look at
and check. Its whole value is that it *refuses* anything it cannot verify. So the work of
building it is mostly the work of finding the things it currently accepts and should not.
Both of Codex's findings were exactly that, and so is row 19.

### What Codex found, and why each one mattered

**1 — The scene could claim to be a picture of a body the configuration never described.**
The design says the record's geometry block must "echo the config's `model_id`" — that
is, the record's claim about which robot model it is drawing has to match the
configuration that actually built it. The adapter hashed the *file* that generates the
model and stopped there. A file digest tells you which program built the model; it tells
you nothing about which model that program was asked to build. Codex proved the gap by
changing one field in a record to `not-the-config-model` and running the chain: it
accepted, returned a case, and printed the record's model name and the configuration's
model name side by side without noticing they disagreed.

Worse, and this is the part that says something about how defects survive: **the test
fixture had been declaring `"cable-two-link"` since it was written, and the project's
configuration has never carried that string.** Nothing noticed because nothing compared
them. The repair is a single equality check, and the fixture now declares the real value
as a literal with its own test pinning that literal against the configuration on disk.

**2 — The decision-timing rule was backwards on both axes.** In Session 149 I settled a
question Codex had asked in Session 148 about which of two bookkeeping numbers on each
estimator decision — a step counter and a timestamp — the adapter bounds. I ruled "the
timestamp only", wrote the argument down carefully, and pinned it with a test. The
argument was internally coherent and it was wrong, because I argued it from the schema's
wording instead of reading the code that produces the data.

Codex read the producer. The result is not ambiguous: the step counter *is* the control
loop's own index, running `0` to `T-1`; and the estimator makes its decision *before*
the simulator advances, while the simulator stamps its timestamp *after*. So on real
data every decision is one control interval earlier than the sample of the same index,
and the very first decision lands at time zero — strictly before the first recorded
sample. My Session-149 rule therefore **accepted a step number no producer can ever
emit, and refused the one decision every run necessarily emits.** Codex reproduced the
second half exactly against a live-shaped grid.

The repair binds the step counter to the control-step domain and bounds the timestamp
above only, leaving the lower end to a check the schema already performs totally. One
further decision is recorded rather than taken: now that the step counter is bound, it
becomes *possible* to pair each decision to the sample of its own index. I deliberately
did not, because that binds the estimator's clock to the simulator's grid sample by
sample, which is a class of over-binding the design already refuses twice for the same
reason — a faithful producer offsets the axis. A test named for that decision will fail
if a later session adds the pairing, so the reason is found rather than rediscovered.

### Row 19 — provenance, computed rather than accepted

Row 19's job is to compute what kind of data the record is really made of and require
that to equal what the record *claims* it is. The design is emphatic that a caller may
not supply this label, because a supplied label can lie.

Most of the computation was already spoken for by earlier rows: the split, the
configuration's lifecycle state, and the manifest's configuration identity are each
bound two to fifteen rows earlier. Following the rule the Session-148 build settled —
read who owns the fact before writing the guard — row 19 carries exactly one thing no
earlier row holds: **the dataset's own assignment identity.** Row 6 checks that the
record and both dataset audits *agree* about it and never checks what it *says*. So a
record claiming `FINAL`, naming a clean frozen configuration, a non-development split,
and a dataset whose audits both honestly report a development-lane assignment passes
every row before this one. Every digest agrees. Every echo agrees. And the resulting
picture would carry a "FINAL RESULT INPUTS" banner over data generated under a
development assignment. That is precisely the input set the design's invariant W6 asks
for, and row 19 is where it now refuses.

Row 19's tests are driven at the module's in-memory seam rather than end to end, and
that is forced rather than convenient: invariant W7 says a production `FINAL` state is
unreachable from every input this packet contains, and the project is *maintaining* that
unreachability on purpose. Building the offending input end to end would manufacture the
very reachability W7 exists to deny. The tests say so in their own text.

## Challenges, and how they were handled

**Being wrong in writing, twice, about work I had documented carefully.** The Session-149
row-16 ruling was not a slip — it was a four-point argument with a test named after it.
What made it wrong was the input to the argument: I reasoned from what the schema's
docstring said the field was *for* rather than from what the code that writes the field
actually does. The correction is recorded as a forward correction in the current build
plan and in the function's own docstring, with the superseded reading named, rather than
by editing Session 149's files. That is the project's append-never-overwrite discipline
applied to my own reasoning.

**A test that was passing because two copies of a wrong string agreed.** The fixture's
`"cable-two-link"` is the clearest example this project has produced of a defect that
survives because nothing joins two facts. The general repair is not "add a test" — it is
that the fixture's value is a literal pinned against the real source, so the fixture
cannot drift into private agreement with itself.

**One hygiene catch worth naming.** My first draft of the row-16 docstring contained a
Unicode ellipsis character. The file compiled, imported and passed all 2,913 tests. Only
the byte-level check found it. The check costs one command and it is the only instrument
that sees this class of change.

## Decisions I made

1. **Accept both of Codex's findings without contest**, after driving each at source
   myself rather than taking the report at face value. Both reproduced.
2. **Put the model-identity join at row 5**, not row 18. It is an identity claim between
   the record and an authenticated artifact, which is what row 5 is for, and its refusal
   code is the identity one. Row 18 is about deriving geometry, not about who the record
   says it belongs to.
3. **Change `authenticate_sources`' signature** to take the authenticated configuration.
   That function's bytes were part of the closed Session-144 approval, so this is
   recorded in the build plan as something the eventual Review Card must name explicitly.
   It is authorized — the two review halves are a split of one build and rows 13–21
   necessarily move the same file — but a reviewer must be told, not left to find it.
4. **Bound the estimator step but not the per-decision time pairing.** Recorded above and
   pinned by a test.
5. **Did not open a Review Card or a subject chat.** Still deliberate: a card names a
   candidate, and the candidate is not stable. This is the sixth consecutive session that
   has held that line.
6. **Did not write a progress report.** Session 150 is not a multiple of eight for me, no
   phase closed, and no amendment was approved. My next regular one is Session 152.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — the model-identity join
  at step 5, the row-16 correction, and read-order row 19 (`resolve_provenance`,
  `ResolvedProvenance`, `DEVELOPMENT_TRACE_PREFIX`). `+223 / -51` against Session 149.
  Blob `88fb94fb8208e71c7ec5be9e78c27643da1e706d`, raw SHA-256
  `a6f528c4afb3a9eec998c8b6c2a13a5cc73749c048edc2c2c25c36536aa725c5`,
  145,409 B / 3,094 LF / 0 CR / ASCII / no BOM / final newline.
- `Reproducibility Packet/tests/test_connection_adapter.py` — twelve net new tests.
  `+396 / -36` against Session 149. Blob `678c1485ab21c6f030203c0ffcdc2316afa57a52`, raw
  SHA-256 `6cec67985a460695b0b9ebfe3f72c54ce782c0e8b9d9e4e7b3ec9d9ffb9de932`,
  186,977 B / 4,540 LF / 0 CR / ASCII / no BOM / final newline.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — Appendix D, appended.
- `agents/Claude/Session Summaries/HumanReport150.md` — this report.
- `agents/Claude/README.md` — Session 150 entry.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.

Nothing else was touched. No Review Card, no chat transcript, no schema, no protocol
document, no configuration, no result artifact and no root README.

## Verification

Every command used `./venv/Scripts/python.exe`, as the project requires.

- focused pair (`test_connection_adapter.py` + `test_authenticated_storage.py`):
  **255 passed in 7.00 s** (was 243);
- the same pair under `PYTHONOPTIMIZE=1`: **255 passed**, with the expected optimized-
  assertion warning;
- packet-wide: **2,913 passed / 0 failed / 152.25 s**, re-run on the final bytes after
  the ASCII fix. The arithmetic closes exactly: 2,901 + 12 = 2,913;
- `py_compile` clean on both files; `git diff --check` clean; `git status --porcelain`
  shows exactly the two packet files plus this session's own documents.

**No mutation sweep ran, and that is on plan rather than an omission.** The build plan
sequences it at step 4, on the finished pair, immediately before the handoff. Its
staged-tree set (`scripts`, `tests`, `schema`, `config` **and** `results`) and its
two-pass shape are still budgeted.

## Scientific and authorization boundary

**This session spent zero scientific resource.** Counters unchanged: **278 rollouts, 67
fits, 67 checkpoints, zero pilot/validation/test reads.** It opened no role index, role
payload, checkpoint, estimator output, controller log, production configuration or
pilot/validation/test result. It built no MuJoCo model, stepped no rollout, ran no fit
and rendered no figure. Every tree its tests bind is under `tmp_path`. The two off-limits
files in the training-code identity set — `storage_contract.py` and `role_contract.py` —
were not edited.

Disclosed reads, all tracked development text, none opening a payload:
`utils/online_loop.py`, `utils/estimator.py`, `utils/cable_plant.py`,
`utils/config_contract.py`, `utils/verification_scene.py`, `utils/connection_record.py`,
`utils/coherent_geometry_fixture.py`, `config/draft-config-v0.1.json` (its
`values.plant.model_id`), `schema/schema.json` (searched for `model_id`), and design
sections 2.4, 3.3, 3.5, 4.1, 4.4, 4.7, 4.8, 5 and 9.1–9.4.

Slot-8 Steps 1–3, 4a, 4b-i and 4b-ii-a remain closed at both approvals. Step 4b-ii-b is
mine, incomplete and unapproved. Steps 4c–4f and every later scientific gate remain
blocked.

**Live-Run README heartbeat: checked, answered no.** No artifact finished, no phase
closed, nothing publishable was produced. An unfinished internal build is the
session-journal texture the playbook forbids. The root README stands at the jointly
approved `7342bc8c`.

## Next steps

1. **Rows 20 and 21** — the bundle-completeness join against the established result, and
   the exclusive-create write of the declared output set.
2. Then the audit-hook observer (W3/B4), acceptance tests B2 and B5, the remaining B3
   refusal rows, the `roles` CLI wiring and the additive `build_role_bundle` edit.
3. Then the **two-pass mutation sweep** on the finished pair, before the handoff.
4. Then the Step-4b-ii-b **Review Card** and subject chat, naming every moved file three
   ways, and carrying two disclosures: the `schema/schema.json` end-of-line pin the
   adapter's raw-domain schema comparison silently depends on, and the step-5 signature
   change this session made to a function whose bytes were part of the closed 4b-ii-a
   approval.
5. Only then the handoff to Codex for the Round-1 review.
