# Human Report — Claude Session 147

**Current date and time:** 2026-08-16 22:22 PDT (measured with the shell during the session; the
closing measurement is recorded at the end of this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Outcome in one paragraph

This session started the build of **Slot-8 sub-step 4b-ii-b**, the only unbuilt connection-adapter
half, and completed the first item in my own build plan's sequencing: **the shared planar centerline
derivation and the dedicated coherent geometry fixture**. Both are new packet modules with a new
test file carrying **48 tests**; the design's fourteenth exit code, `X_GEOMETRY_UNSUPPORTED` at exit
status 15, was added to the exit table as the purely additive change design section 4.5 said it
would be. The packet-wide suite is **2,843 passed, 0 failed** in 163.24 s, up from 2,793 by exactly
the 50 tests this session added. **No Review Card and no subject chat were opened, and that remains
deliberate** — the review protocol requires a stable candidate before a card names one, and rows
13–21 are not built yet. **Zero scientific resource was spent.** The counters are unchanged at 278
rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads.

---

## Startup and state restoration

The automation turn gate named Claude and `.agent-session.lock` was absent. I created the lock,
re-read `.agent-turn`, confirmed it still named Claude, and then followed `AgentPrompt.md`.

I read `Project Details/Project Details.md` in full, my continuity file, every chat summary in the
folders I participate in, and the one active chat. The repository began clean at `66e9604`
(`Codex Session 146`).

**Chat review found nothing owed.** Codex's Session 146 completed the delta-only Round-3 review of
my public Live-Run README heartbeat repair and returned **Approved** at exactly the bytes I handed
over — blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`. Codex closed the Review Card, posted its
approval, concluded the subject chat and wrote its `Summary.md`. That review is closed at both
approvals and I am not reopening it. The one remaining active chat, Transcript Order Monitoring,
ends with my own Session-144 turn and Codex correctly added no clean-check noise to it, so no reply
was owed there either.

**Cross-review duty discharged.** I read Codex's `HumanReport146.md` in full. Its cross-review of my
Appendix A accepted the row-18 forward map, correctly characterised the sign as a declared fixture
convention rather than a measured MuJoCo fact, and repeated that no card should open until an
implementation exists. I found nothing to correct and had nothing to push back on. One thing in it
is worth carrying: Codex re-stated that the future build must complete its two-pass mutation sweep
before handoff. That is still budgeted, and this session is not the handoff.

---

## What I built

### 1. The fourteenth exit code (design 4.5)

`X_GEOMETRY_UNSUPPORTED` is now in `utils.verification_scene.EXIT_CODES` at exit status **15**.

I re-measured the table on this checkout by importing it rather than reading it off the design,
because an exit table is a property of a checkout: `X_SCENE_OK` held 0 and the twelve refusals held
3 through 14 contiguously, so 15 was free and **no existing value moved**. That confirms the
additivity claim design 4.5 made in advance.

The one thing additivity cannot protect is a *count*, and there was one:
`test_verification_scene.py` asserted `len(EXIT_CODES) == 13`. I moved it to 14 and, rather than
leave a bare count behind, added a test that pins **every code to its own value as a literal**. A
count assertion passes if a code is added and another is silently moved; the value map does not.

### 2. `scripts/utils/centerline_geometry.py` — the one forward map

Read-order row 18 requires the adapter to derive each arm's centerline from the authenticated
`q_true`, `deform_coords` and the record's `render_geometry`. Design 2.4 separately requires the
fixture's data to be generated from *one* dependency-light forward map. Those are the same map used
twice, so it is written once and imported by both. A second copy would agree with the first for
exactly as long as nobody edited either.

The module derives the centerline, measures the distal deviation, and refuses under
`X_GEOMETRY_UNSUPPORTED`. It imports no `mujoco` — invariant V18 — and a test asserts that in a
fresh interpreter, which matters because the producer this geometry describes,
`utils.cable_mechanics`, imports `mujoco` at module scope. That is the whole reason design 3.5 put
the chain in the record instead of reading it out of a live model.

### 3. `scripts/utils/coherent_geometry_fixture.py` — the fixture design 2.4 requires

It generates a schema-B `PrivilegedRecord` whose `q_true`, `deform_coords`, centerline and
`true_task_output` are one coherent geometric state, and it carries its own synthetic exactness
oracle: the generator re-derives the tip from the record it just built and refuses to return a
record that does not reproduce it. **Measured: the deviation is exactly 0.0 m.**

It also emits its own geometry-validation artifact, whose bytes say what it is not:

> "This artifact authenticates the bytes of a synthetic fixture and nothing else. Its tolerance is
> the fixture's construction-exactness constant, not a measured real-data agreement, and it
> manufactures no tolerance for any real role payload…"

That sentence is in the artifact rather than only in a review card on purpose. A fixture number
sitting in a file with no scope statement is exactly the thing a later reader mistakes for an
approved one.

### 4. `tests/test_centerline_geometry.py` — 48 tests

Written to invariant W2: build the input the derivation refuses and drive the refusal, rather than
assert a message exists.

---

## The chain, verified at source rather than carried

My Session-146 Appendix A recorded the row-18 forward map. **I re-derived every number from the
producer this session rather than trusting my own transcription**, and it holds:

| quantity | value | where I read it |
|---|---|---|
| `point_count_per_link` | 17 | `config/draft-config-v0.1.json`, `values.plant` |
| ordered bodies per link | 16 | `cable_body_names` returns `point_count - 1` names |
| internal bodies per link | 15 | `extract_deformation_coordinates` iterates `body_ids[1:]` |
| `n_def` | 90 | config, and 2 × 15 × 3 = 90 closes |
| segment length | 0.025 m | `link_length_m` 0.4 ÷ 16 bodies |
| centerline points | 33 | 16 + 16 + 1, pinned as a literal |
| base point | model (0, 0, 0.5) → scene (0.0, 0.5) | the `base_ref` site plus the declared projection |

An undeformed chain at zero joint angles lies straight from (0.0, 0.5) to (0.8, 0.5) with every
segment at exactly 0.025 m, which is the cheapest possible check that the arithmetic closes end to
end.

---

## Decisions I made, and why

**1. The derivation is its own module, not a section of the adapter.** The adapter is already 2,115
lines and rows 13–21 will add substantially to it, but that is not the reason. The reason is that
the fixture generator needs the same map, and if the map lived in the adapter the generator would
have to import the entire authentication chain to draw a line. One small module, two callers, and
the "one forward map" requirement is literal rather than aspirational.

**2. Each internal body's rotation applies *before* that body's own segment — and this corrects my
own plan.** Appendix A.4's sketch put the rotation update *after* the advance. I implemented it
before, because the ball joint that carries the triplet sits at the body's proximal end and orients
that body: the joint orients its own segment, not the next one. The sketch's ordering would have
shifted every triplet onto the following segment and left **the last internal body of each link
acting on nothing at all**.

This is worth naming plainly because of how invisible it is. Both versions produce a continuous,
smooth, finite, plausible centerline of the right shape. Nothing about the output reveals the
difference. So I wrote the test that does: it drives all thirty declared triplets one at a time and
requires each to move the distal point. Under the sketch's ordering the last one moves it by exactly
zero. **Measured: the smallest displacement of any of the thirty is 1.25 mm, and the last L2
internal body is one of the ones that moves.**

The design at blob `032db166` is the authority and it assigns "the exact `deform_coords` triplet to
each internal body" without pinning the order, so this is a choice the build had to make rather than
a departure from the contract. This paragraph is the forward correction to Appendix A.4; the plan
file is left standing as the recorded turn.

**3. The tangent sign is carried in the declared `projection` string, from a closed vocabulary.**
Appendix A.3 assigned the sign question to the future geometry-validation artifact, correctly. But
the *mechanism* by which a record declares a sign still had to be decided now, and I found that
`PlanarConvention` — parsed and closed at 4b-i — has **no sign field**. Adding one would reopen a
closed contract. So the sign rides in the `projection` string, and the module accepts exactly two
values, identical in their axis mapping and differing only in the sign clause. Anything else
refuses; neither is a default.

I want to be exact about what this proves and what it does not. The generator and the checker share
the declaration, so **the fixture would close under either sign**. It proves the derivation logic,
not the physics. A sign error against real data is caught by the geometry-validation artifact's
maximum-deviation field, because a flipped tangent misses by centimetres rather than nanometres —
and that artifact is not 4b's to build. The question is assigned, not open, and both module
docstrings say so.

`q_true_convention` got the same treatment with exactly one accepted value, because the alternative
reading — treating `q_true[1]` as absolute rather than relative to the distal L1 tangent — also
produces a plausible wrong answer. The separating test is a bent L1 with `q_true[1] = 0`: under the
declared convention the chain is one straight line, under the absolute reading it bends at the
elbow.

**4. The fixture's curvature is derived from its own deformation.** The contract fixture's defect is
that its strain lane and its geometry lane are unrelated by construction. I did not want to
reproduce a weaker version of that, so each gauge station's curvature is exactly one declared
`deform_coords` column divided by that body's segment length — and the test checks it as an
**identity**, not a correlation. It is still synthetic; it is a consistency property of the fixture,
not a claim about what a real gauge would read, and the docstring says that.

**5. I replaced an unreachable check of my own with a reachable one.** My first version of
`require_chain_arithmetic_closes` compared the total declared column count against 90. Writing the
test for it showed the branch could not be reached: once both links are known to carry fifteen
internal bodies, the total is always ninety. A test that cannot fail is worse than no test, so I
replaced the count with a **coverage** check — the declared columns, read in link order, must be
exactly `0 … 89` — which catches the case a count never could: fifteen triplets that all name the
same three columns. The test now builds precisely that geometry, confirms the body counts, segment
lengths and point count all still hold, and drives the refusal.

---

## The measurement that justifies this fixture existing

Design 2.4 says the existing contract fixture cannot be a geometry oracle. I re-measured it rather
than quote it, and the result is sharper than a threshold.

Comparing across the two fixtures' base points would have measured the half-metre offset between two
origins instead of the thing being asked, so I bound both chains to a common base first. With that
done, reconstructing the contract fixture's tip from its own `deform_coords` misses by **3.6 mm to
6.8 mm** across seeds 0–3 — millimetre-scale, consistent with the 2.81–6.20 mm design 2.4 recorded
under its own probe settings, and not the same measurement, so I am not claiming the numbers match.

The sharp part is what happens when the deformation is removed entirely. **The rigid
reconstruction misses by 4.513 mm at every seed** — identically, because `curvature_true` carries no
RNG — while the deformed reconstruction wanders between 3.6 and 6.8 mm around it. Adding the
fixture's deformation does not bring the reconstruction closer to the fixture's own recorded tip; it
adds seed-dependent noise around the same error. At some seeds the rigid reconstruction is the
*closer* of the two. If those two channels described one body, removing the deformation would have
to make things worse at every seed. That is the incoherence, stated as a property rather than as a
number, and it is now a test.

Against it, the coherent fixture closes at exactly **0.0 m**.

---

## Verification and evidence

| check | result |
|---|---|
| new focused file `test_centerline_geometry.py` | **48 passed**, 2.11 s |
| Slot-8 focused set (5 files) | **715 passed**, 32.47 s |
| packet-wide suite | **2,843 passed, 0 failed**, 163.24 s |
| the two changed/new scene files under `PYTHONOPTIMIZE=1` | **144 passed** |
| `py_compile` on all five files | clean |
| `git diff --check` | clean |
| `git status --porcelain` | only the five intended files |

The suite arithmetic closes exactly: 2,793 (the figure at the close of 4b-ii-a) + 48 new + 2 added
to `test_verification_scene.py` = **2,843**. I re-ran the packet-wide suite because an executable
file changed; that is the condition, and it was met this session.

All five files measure pure ASCII, LF only, zero CR, final newline — consistent with every other
Python file in the packet.

**No mutation sweep was run, and that is on plan rather than an omission.** My build plan sequences
the sweep at step 4, after rows 13–21, the observer and the CLI wiring exist, and immediately before
the handoff. Sweeping a third of a build would have to be redone against the finished one. The sweep
remains budgeted, with its staged-tree requirement (`scripts`, `tests`, `schema`, `config` **and**
`results`) and its mandatory two-pass shape carried forward.

---

## Resource boundary

**Zero scientific resource.** Counters unchanged: **278 rollouts, 67 fits, 67 checkpoints, zero
pilot/validation/test reads.**

I opened no production connection record, role index, role payload, checkpoint, estimator output,
controller log or production configuration, and no pilot, validation or test result. I **built no
MuJoCo model**, stepped no rollout, ran no fit and rendered no figure. The V18 test confirms in a
fresh interpreter that neither new module pulls `mujoco` or `torch` into the surface.

Disclosed reads, all tracked development text, none opening a payload behind it:
`config/draft-config-v0.1.json` (`values.plant`), `scripts/utils/cable_mechanics.py`,
`scripts/utils/synthetic_plant.py`, `scripts/utils/verification_scene.py`,
`scripts/utils/connection_record.py`, `scripts/utils/connection_adapter.py`,
`scripts/utils/schema_types.py`, `scripts/utils/dev_fit_trainer.py` (only its
`training_code_identity` list, to re-confirm which eight files are off limits),
`scripts/build_data_contract_fixture.py`, `tests/test_connection_adapter.py`, and design sections
2.4, 3.5, 4.1, 4.5 and 4.6.

**The two off-limits files were not touched.** `scripts/utils/storage_contract.py` and
`scripts/utils/role_contract.py` are two of the eight in `dev_fit_trainer.training_code_identity`,
and editing either breaks three completed, unrepeatable runs. Nothing this session needed them, and
neither new module adds an entry point to either.

---

## Live-run heartbeat check

Run, and the answer is **no new public entry**. This session finished no artifact, closed no phase
and produced no result: it built the first third of an unreviewed sub-step. A log entry announcing
that a build has started is exactly the session-journal texture the Live-Run README playbook
excludes. Root `README.md` is unchanged.

---

## Files created or updated

**Created:**
- `Reproducibility Packet/scripts/utils/centerline_geometry.py` — the one forward map, 18,251 B.
- `Reproducibility Packet/scripts/utils/coherent_geometry_fixture.py` — the coherent fixture and its
  own geometry-validation artifact, 26,695 B.
- `Reproducibility Packet/tests/test_centerline_geometry.py` — 48 tests, 36,619 B.
- `agents/Claude/Session Summaries/HumanReport147.md` — this report.

**Updated:**
- `Reproducibility Packet/scripts/utils/verification_scene.py` — `X_GEOMETRY_UNSUPPORTED` at exit 15,
  plus the comment block recording the additivity measurement (`+9 / −2`).
- `Reproducibility Packet/tests/test_verification_scene.py` — the count assertion moved 13 → 14, and
  two tests added: the full value map, and the new code raising as a refusal (`+42 / −4`).
- `agents/Claude/README.md` — current state.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 148.

---

## Next steps

1. **Rows 13–17** — the consistency checks over already-authenticated payloads. Row 5 already does
   the tolerance-equality and maximum-deviation work, so row 18's remaining job is only the
   derivation and the distal comparison, both of which now exist.
2. **Rows 19–21**, then the audit-hook observer (W3/B4), then the `roles` CLI wiring and the
   additive `build_role_bundle` edit.
3. **The two-pass mutation sweep**, on the finished pair, before any handoff.
4. **Then** the Review Card and the subject chat, naming the candidate three ways and resolving
   every blob id with `git cat-file -t` before the card governs. The carried 4b-ii-a follow-up — the
   adapter's raw-domain schema comparison silently depending on the `schema/schema.json text eol=lf`
   pin — goes into that card as documentation; "add a test" is not available, because the test that
   would catch the pin's removal cannot exist while the pin holds.
5. Steps 4c–4f and every scientific gate behind them remain blocked. **A closed review loop
   authorizes the next step only, and never a run.**
6. My next regular progress report is **Session 152**.

**Report written and committed 2026-08-16 22:38 PDT.**
