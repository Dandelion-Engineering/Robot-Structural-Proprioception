# Human Report - Codex Session 147

**Current date and time:** 2026-08-16 23:07 PDT (measured with the shell immediately
before writing this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

## Outcome

I completed the required general recent-work review of Claude Session 147's first,
deliberately partial Step-4b-ii-b build. Claude has implemented the shared planar
centerline derivation, the dedicated coherent geometry fixture, the new
`X_GEOMETRY_UNSUPPORTED` exit and their focused tests, but has not yet built read-order
rows 13-21, the full-call observer, bundle/output/CLI wiring or the planned two-pass
mutation sweep.

This is therefore **not a formal artifact review and not an approval**. There is no stable
candidate, Review Card, subject chat or handoff. I inspected the actual new modules, the
complete new test file, the two changed exit-code regions, the governing design sections
and the tracked producer functions. I found no forward defect worth flagging before the
build is complete. The focused surface independently passes **144 tests**.

No project file owned by the partial build was edited. No chat response was owed. No
technical or scientific gate moved, and no public README entry was warranted.

## Startup and state restoration

The automation turn gate named Codex and `.agent-session.lock` was absent. I created the
lock atomically, re-read `.agent-turn`, confirmed it still named Codex and then followed
`AgentPrompt.md`.

I read `Project Details/Project Details.md`, Codex continuity, all eleven summaries in
Codex-participant chat folders and the complete 900-line active Transcript Order
Monitoring chat. That active chat ends with Claude's independent confirmation of the
Session-143 append repair; it requests no response, and the standing rule says a clean
check is not a reason to append.

The repository began clean at `a2e3ea9` (`Claude Session 147`), with
`HEAD == origin/main`. I read Claude's complete `HumanReport147.md`, the packet playbook,
the Live-Run README playbook, and the relevant closed design sections 2.4, 3.5, 4.1,
4.5 and 4.6 before evaluating the new code.

## General cross-review scope

The inspected Claude-authored state is:

| artifact | Git blob | role |
|---|---|---|
| `scripts/utils/centerline_geometry.py` | `385eb59c...` | one dependency-light planar forward map |
| `scripts/utils/coherent_geometry_fixture.py` | `5753c6a7...` | synthetic fixture generated and checked by that map |
| `scripts/utils/verification_scene.py` | `d186a9b1...` | additive exit-code registration |
| `tests/test_centerline_geometry.py` | `c6f3a781...` | 48 new geometry/fixture tests |
| `tests/test_verification_scene.py` | `60caeb21...` | complete exit-value map and new refusal test |

These bytes remain an unfinished owner build. The identities above are useful for
continuity only; they are not jointly approved candidate identities.

### Producer-to-map check

I re-read the producer rather than accepting the report's arithmetic by transcription.
The mapping is consistent with the tracked source and closed Step-4a design:

- `point_count_per_link = 17` produces 16 ordered bodies per link.
- `extract_deformation_coordinates` iterates `body_ids[1:]`, producing 15 internal
  ball-joint log maps per link and 90 scalar columns in L1-then-L2 order.
- `extract_state` defines `q_true[0]` as the first L1 tangent and `q_true[1]` as the first
  L2 tangent relative to the distal L1 tangent.
- The producer's link length is 0.4 m, so the 16 body segments are 0.025 m and the joined
  chain has 33 centerline points.
- The planar component is the model-y rotation-vector component; model x/z projects to
  scene x/y.

Claude's correction to the older planning sketch is coherent with this representation:
an internal body's ball joint is at that body's proximal end, so its declared rotation
acts before traversing its own segment. The test that drives all 30 triplets separately
would fail if the last L2 joint were shifted onto a nonexistent following segment.

### Boundary and refusal check

The new code keeps the important separations intact:

- The fixture and checker share one map, but their agreement is stated only as synthetic
  construction consistency. It is not presented as a MuJoCo or real-role measurement.
- The unresolved tangent sign is a closed record vocabulary with two explicit choices;
  neither choice is treated as a measured MuJoCo fact. The later approved
  geometry-validation artifact still owns the real-data deviation check.
- The 1 nm `CENTERLINE_TASK_OUTPUT_TOL_M` remains the fixture's construction tolerance.
  The production adapter takes a tolerance argument with no default and does not invent a
  real-data tolerance.
- `X_GEOMETRY_UNSUPPORTED` is additive at exit 15. The prior success/refusal values remain
  pinned individually rather than protected only by a count.
- Fresh-interpreter tests keep both `mujoco` and `torch` out of the new import surface.

The test file also distinguishes the plausible wrong maps that shape-only checks would
miss: relative-versus-absolute `q_true[1]`, swapped L1/L2 triplet blocks, after-versus-before
joint application, unrecognised conventions, non-finite payloads, grid mismatches and a
fixture whose strain and geometry lanes are generated independently.

## Verification

Using only the project virtual environment, I ran:

```text
.\venv\Scripts\python.exe -m pytest Reproducibility Packet\tests\test_centerline_geometry.py Reproducibility Packet\tests\test_verification_scene.py -q
```

Result: **144 passed in 3.86 s**.

I did not rerun the 2,843-test packet-wide suite. Claude already ran it against these exact
committed executable bytes, and Codex changed no executable file this session. The focused
reproduction is proportionate to a general review of a partial, non-handed-off build.

## Decision and communication

No formal review cycle was opened. The governing continuity explicitly says not to create
the Step-4b-ii-b card or subject chat before a stable candidate exists, and Claude's report
says the same. A formal approval now would incorrectly transfer authority from one-third of
the build to rows and write boundaries that do not exist yet.

I also posted no informal chat message. The general recent-work review found no correction
that Claude needs to integrate, and the review method does not require an approval ritual
when no artifact has been flagged.

## Live-run heartbeat check

Run against `Playbooks/live-run-readme.md`, and the answer is **no new public entry**.
Session 147 started an unfinished internal sub-step; it finished no artifact, closed no
phase and produced no scientific result. Root `README.md` remains unchanged at jointly
approved blob `7342bc8c...`.

## Verification and scientific-resource boundary

I opened no production connection record, role index, role payload, checkpoint, estimator
output, controller log, production config or pilot/validation/test result. I built no
MuJoCo model, stepped no rollout, ran no fit and rendered no figure. Counters remain
**278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.

Full Step 4b, production records, adapter execution, real-role reads, configuration freeze,
capacity or threshold choice, final configuration, Steps 4c-4f and every C1-versus-S claim
remain separately blocked.

## Files created or updated

- `agents/Codex/Session Summaries/HumanReport147.md` — this report.
- `agents/Codex/README.md` — navigation and current-state entry for Session 147.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten continuity
  for Session 148.

No packet code, test, Review Card, chat transcript or root `README.md` byte was changed by
Codex.

## Next steps

1. Claude owns completion of rows 13-21, the bidirectional full-call open observer,
   output/CLI wiring and the two-pass mutation sweep.
2. Open the Step-4b-ii-b Review Card and narrow subject chat only after Claude produces and
   explicitly hands off one stable candidate.
3. At that handoff, run the full Round-1 review against the complete card boundary; this
   session's clean general review is context, not inherited approval.
4. Carry the `schema/schema.json text eol=lf` dependency into that future card's
   documentation as the closed Step-4b-ii-a follow-up.
5. Preserve every production, scientific, configuration and downstream gate.
6. The next regular Codex progress report is Session 152.
