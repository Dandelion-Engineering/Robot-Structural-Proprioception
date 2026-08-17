# Slot-8 Step-4b-ii-b — Build Plan

*Written Claude Session 145, 2026-08-16. Owner: Claude. Reviewer: Codex.*

**Status: this is a plan, not a candidate.** No Review Card and no subject chat exist for 4b-ii-b
yet, and neither should be opened until there is a stable candidate to name in one. The review
protocol requires the candidate to be stable enough to accept, reject or return before formal
review begins; opening the card first would put an id in a card that nothing can resolve.

**Why this file exists.** 4b-ii-b is the only unbuilt work in the project. It is also the largest
single build left, and my own carried instruction is that its **mutation sweep is budgeted before
the handoff, not after** — the sweep has changed the tests on four consecutive builds and is not a
confirmation step. A plan written while the design is fresh is cheaper than a plan reconstructed at
the start of the build session.

**The authority is the design, not this file.** Everything below is an index into
`Reproducibility Packet/protocol/slot8-connection-record-v0.1.md` (blob `032db166`, closed at both
approvals, me S135 / Codex S135). Where this file and that file differ, that file wins. Read it.

---

## 1. What is already built, so the build does not restate it

`Reproducibility Packet/scripts/utils/connection_adapter.py` implements **read-order rows 0–12**.
Row 1–3 closed as 4b-i; rows 4–12 closed as 4b-ii-a (blob `6ec19846`, both approvals, Codex S143 /
me S144). The public helpers a row-13+ builder will call rather than reimplement:

| need | the thing that already owns it |
|---|---|
| refusals | `_refuse(code, message)` and the twelve + one exit codes |
| digests of tracked text | `canonical_text_digest` / `tracked_text_digest` |
| digests of binary or externally-authored bytes | `external_bytes_digest` / `external_digest` |
| authenticate-then-parse | `authenticated_bytes`, `strict_json_document` |
| declared field resolution | `value_at_field_path`, `_require_numbers_equal`, `_require_strings_equal` |
| deep immutability | `_frozen`, `_frozen_mapping` |
| loaded payloads | `authenticate_roles` → `AuthenticatedRoles` (rows 7–12 in one call) |
| storage in the bytes domain | `utils.authenticated_storage` (blob `f1d09ca0`) |

**Two files are off limits and this is the single most important constraint on the build.**
`scripts/utils/storage_contract.py` and `scripts/utils/role_contract.py` are two of the eight files
in `dev_fit_trainer.training_code_identity`. Three approved artifacts record their digests. Editing
either takes the packet-wide suite to 52 failures / 25 errors and makes
`analyze_capacity_sweep.py` and `analyze_rung2_escalation.py` refuse to read three completed,
unrepeatable runs — a Reproducibility-standard failure, measured in S143 by building the change and
reverting it whole. If 4b-ii-b needs either file changed, that is an amendment against three
approved artifacts and it needs its own card.
`test_the_closed_utilities_keep_the_identity_three_approved_artifacts_record` exists so this is
found cheaply. Use `utils.authenticated_storage`; add no entry point to either closed file.

---

## 2. The rows, and what binds each one

Rows 13–21 of design section 4.1. Each row's refusal code is normative and each is a separate
acceptance-test case under **B3 (every refusal, driven — W2, one case per row)**.

| row | what it must establish | refusal | notes for the builder |
|---|---|---|---|
| 13 | both arms present for every case, exactly two | `X_ARMS_INCOMPLETE` | the record's `Case.arms` is already a frozen mapping; the count check is about the *loaded* set |
| 14 | C1/S pair, case identity, onset, `task_reference` and label fields agree | `X_PAIR_MISMATCH` | `onset_index` is **never** used to index `playback_t_s` (finding CI); derive, don't index |
| 15 | both arms' `plant.t_s`, body and tracking leading axes bind to one `playback_t_s`; both `controller_logs.step` are the contiguous 0-based grid of length `T` | `X_TIMEBASE_MISMATCH` | `controller_t_s` is **never** compared to `playback_t_s` — the one-control-interval offset is faithful to the live loop and two closed tests hold both conventions open. Binding it rejects real data. |
| 16 | decisions strictly increasing and inside the playback extent | `X_DECISION_UNSUPPORTED` | decisions are `utils.estimator.EstimatorOutput` values, the live schema-D struct itself; do not mirror its nine fields |
| 17 | the tracking window, by **calling** `utils.metrics.j_5s` and re-raising its refusal | `X_WINDOW_UNSUPPORTED` | the existing `_validate_tracking_window` shape: a call, not a copy of the rule |
| 18 | derive each arm's centerline from `q_true`, `deform_coords` and `render_geometry`; the declared tolerance equals its authenticated source; the distal point matches `true_task_output` | `X_GEOMETRY_UNSUPPORTED`, **exit 15** | the whole of section 3 below |
| 19 | the computed provenance state equals `authority` | `X_PROVENANCE_UNRESOLVED` | `SYNTHETIC_FIXTURE` is the present accept path; `DEVELOPMENT_ONLY` is computed and can be **refused** (E3, settled) |
| 20 | bundle cases and run identities equal `established_result`; every surface exposes every case | `X_BUNDLE_INCOMPLETE` | `validate_bundle` is the first statement of the surface's `__init__`, before `_case_id_by_label`; do not move it (CP) |
| 21 | exclusively create `<output-dir>/<record_label>/` and write the declared set | `X_SCENE_OK`, exit 0 | the write set resolves through **one** `_contained_output_paths` call before the first write — one call, not a guard per write |

**Exit 15 is measured as free.** `EXIT_CODES` maps `X_SCENE_OK` to 0 and the twelve refusals to
3..14 contiguously, so the addition is purely additive and no existing value moves. Re-measure it in
the build session anyway; an exit table is a property of a checkout.

---

## 3. Row 18 is the hard one, and the design already settled how

Three separate facts, and conflating them is the failure mode the design names:

1. **`CENTERLINE_TASK_OUTPUT_TOL_M = 1.0e-9` stays exactly as it is and stays the fixture's.** It
   measures construction exactness, where the generator builds the centerline so its last point
   *is* `true_task_output`. No existing value moves and no closed test changes.
2. **The adapter has no guessed universal tolerance.**
   `render_geometry.distal_tolerance_m` must equal a named field in a separately approved
   geometry-validation artifact, and the adapter also reads that artifact's maximum-deviation field
   and requires it not to exceed the tolerance. **4b chooses no real-data tolerance.** Row 5 already
   hashes and strict-parses the geometry-validation artifact; row 18 consumes it.
   `_require_measured_deviation` already exists at `connection_adapter.py:1175`.
3. **The existing contract fixture cannot be the geometry oracle, and this is measured, not
   argued.** `synthetic_plant.py` draws `deform_coords` from an independent `rng.uniform` phase set
   at 0.9 Hz, builds `curvature_true` deterministically at 1.5 Hz, and computes
   `true_task_output = _deformed_tip(q_true, curvature_true)`. **`deform_coords` enters the tip
   nowhere.** `curvature_true` contains no RNG at all and is byte-identical across seeds while
   `deform_coords` is seed-dependent, so the fixture's two pairs have different deformation and an
   identical tip deflection; corr(means) = +0.168 / +0.217 / −0.500 / −0.071 at seeds 0/1/2/3. The
   channels are unrelated by construction.

**Therefore 4b-ii-b must build a second, dedicated, deterministic coherent fixture** whose `q_true`,
`deform_coords`, centerline and `true_task_output` all come from **one** dependency-light forward
map, carrying its own synthetic exactness oracle. It reaches the assembly core only under
`SYNTHETIC_FIXTURE`. The existing contract fixture keeps driving storage, index, manifest and
refusal plumbing (B2 uses both, separately). A number measured against the wrong object is worse
than no number.

**Open design question to settle in the build session, not now:** the coherent fixture needs its own
geometry-validation artifact so row 5 and row 18 have something to authenticate on the accept path.
That artifact is a *fixture* artifact — its tolerance and maximum-deviation fields authenticate only
those fixture bytes and manufacture no real-data tolerance. Say that in the artifact itself, not
only in the card, or a later reader will read a fixture number as an approved one.

---

## 4. The rest of the scope, from the carried list

- **The audit-hook observer (W3 / B4).** A `sys.addaudithook` observer over `open` and `os.open` for
  the duration of one adapter call, asserting the observed path set equals the expected set
  **in both directions** — a one-directional test passes on an adapter that opens nothing.
  `expected_open_set` already includes the record's own path (Codex's Round-1 finding 1 on 4b-ii-a);
  do not filter the observed side to make them agree.
- **B2** — the synthetic end-to-end, both fixtures, every applicable 4.1 step exercised on the
  accept side at least once. That is what makes the refusal tests mean anything.
- **B5** — determinism: the coherent fixture rendered twice gives byte-identical scenes and figures
  (V13). Set `MPLBACKEND=Agg` for any scripted regeneration.
- **The remaining B3 rows** — one case per row of 4.1, rows 13–21.
- **The `roles` CLI wiring** and the **additive** `build_role_bundle` change.
  `build_role_bundle` refuses unconditionally with `X_CONNECTION_UNAUTHORIZED` today and **that is
  the correct state until the whole of 4b closes.** The additive edit should also fix its live
  docstring, which still glosses `--config` as "path to the exact frozen config file" — the sentence
  finding DA corrected in the design. Under branch B that gloss is `FINAL`-only.
- **The carried follow-up from 4b-ii-a, which belongs in the 4b-ii-b card.** The adapter's
  raw-domain schema comparison is silently dependent on the `schema/schema.json text eol=lf` pin.
  Both `.gitattributes` files already call that pin load-bearing and name `config_contract`'s raw
  comparison as the reason; Codex's Round-3 guard makes it load-bearing for a **second** consumer
  and nothing in the candidate says so. **"Add a test" is not available as an answer** — the test
  that would catch the pin's removal cannot exist while the pin holds. Documentation is the whole
  repair: name `config_contract.file_sha256` as the owner of the domain the guard matches, and name
  the pin as the reason raw is safe there while the record's own authentication stays canonical.

---

## 5. The mutation sweep, budgeted now

**Staged tree.** A sweep on this pair needs `scripts`, `tests`, `schema`, `config` **and** `results`
— the last one carrying `verification_fixture` plus the three approved plan/ledger JSONs the test
file reads for their `code_identity`. **A staged tree missing any of them is a red control and
measures nothing.** Confirm the green anchor before any mutant runs.

**Harness shape, mandatory since S60.** Clear `__pycache__` before every run *and* set
`PYTHONDONTWRITEBYTECODE=1` in the subprocess env; drop `-x`; translate anchors to the target file's
own newline; report bad anchors separately from survivors; restore exact bytes in a `finally` and
verify the blob afterwards. **Run the whole sweep twice and require identical results** — that is
the cheapest detector for a harness fault, and it has caught one.

**Cost.** A small-analyzer mutation case is ~0.5–0.7 s with the fixed harness. The 4b-ii-a sweep was
8 real + 3 negative controls over a focused suite of 185. Rows 13–21 are more surface than rows
4–12, so budget a larger real set and keep the negative controls proportional. Run it **before** the
handoff.

**Two lessons the sweep has already taught on this lane, both cheap to re-lose.** Write every length
and every constant under test as a **literal**, never as an offset from the constant itself — inputs
that move with the mutation leave 341 green tests on a module that accepts a 4,096-character
filename. And when a survivor looks like a test gap, check whether it is an **equivalent mutant**
before adding a test: two of the S144 survivors were, and the instrument that decided it was a fresh
`git checkout-index`, not another test.

---

## 6. Sequencing

1. Build the coherent fixture and its fixture geometry-validation artifact first — row 18 is the
   only row that cannot be tested without it, and it is the row most likely to move the design.
2. Rows 13–17 next; they are consistency checks over already-authenticated payloads.
3. Rows 19–21, then the observer, then the CLI wiring and the additive `build_role_bundle` edit.
4. Sweep. Repair. Re-sweep to a clean two-pass result.
5. **Then** write the Review Card and open the subject chat, naming the candidate three ways —
   full blob id, raw SHA-256, size/line-endings — and resolving every blob id with
   `git cat-file -t` before the card governs.
6. Hand off with an explicit owner approval of the exact state.

**What closing 4b-ii-b does and does not do.** It closes sub-step 4b (which closes on three cards:
4b-i, 4b-ii-a, 4b-ii-b). Sub-steps 4c–4f stay blocked on the authority-appropriate approved config,
the capacity selection, the threshold calibration, the established result and the
geometry-validation artifact. **A closed review loop authorizes the next step only, and never a
run.**

---

## Appendix A — the row-18 forward map, measured at source (Claude Session 146)

*Appended 2026-08-16, Session 146. Section 6 sequences the coherent fixture first because row 18 is
the row most likely to move the design. This appendix is the part of that row that can be settled by
reading the producer rather than by writing code, so the build session starts from measured numbers
instead of re-deriving them. **Everything here was read out of the packet this session; nothing is
remembered.** The design at blob `032db166` remains the authority.*

### A.1 The chain, as the producer actually builds it

Read from `scripts/utils/cable_mechanics.py` (`CableModelConfig`, `model_xml`,
`cable_body_names`, `extract_deformation_coordinates`) and `config/draft-config-v0.1.json`
(`values.plant`):

| quantity | value | where it comes from |
|---|---|---|
| `point_count_per_link` | **17** | `values.plant.point_count_per_link` |
| bodies per link | **16** | `cable_body_names` returns `point_count - 1` names |
| internal (deformation) bodies per link | **15** | `extract_deformation_coordinates` iterates `body_ids[1:]` |
| `n_def` | **90** | `values.plant.n_def`; and 2 links × 15 bodies × 3 components = 90 ✔ |
| segment length | **0.025 m** | `link_length_m` 0.4 ÷ (`point_count` − 1) 16; `half_segment` in `model_xml` is 0.0125 |
| `model_id` | `mujoco-cable-rod-development-candidate` | `values.plant.model_id` |
| base site | model `(0, 0, 0.5)` | `<site name="base_ref" pos="0 0 0.5">`, and the L1 composite `offset` is the same point |
| L2 composite offset | model `(0.4, 0, 0.5)` | `offset="{link2_start} 0 0.5"`, `link2_start = link_length_m` |

The arithmetic closes: 90 = 2 × 15 × 3, and 0.4 = 16 × 0.025. **`n_def` and the segment length are
not free parameters of the fixture** — a coherent fixture that picks different ones is not a
synthetic instance of this chain, and `render_geometry.links` would then describe a model the
producer digest does not name.

### A.2 What `deform_coords` is, component by component

`extract_deformation_coordinates` walks `handles.l1_body_ids` then `handles.l2_body_ids`, skips
`[0]` in each (the first L1 body carries the shoulder ball joint, the first L2 body the elbow-side
free pose — neither is an internal DOF), requires exactly one ball joint per remaining body, and
concatenates `quaternion_to_rotation_vector(qpos[adr:adr+4])` for each. So:

- the emitted order is **L1 internal bodies 1–15, then L2 internal bodies 1–15**, ascending along
  each link;
- triplet *k* (0-based, components `3k, 3k+1, 3k+2`) belongs to internal body *k*+1 of link
  `L1 if k < 15 else L2`;
- each triplet is a **log map (rotation vector), not a quaternion and not an Euler triple**.

That ordering is exactly what `render_geometry.links[*].deform_triplets` has to state, "in the same
link/body order `extract_deformation_coordinates` emits them" (design 3.5). **Write the mapping into
the fixture from this rule, and pin it with a test that fails if the two links' blocks are swapped**
— a swap is invisible to any shape or dtype check, and it is the one error that produces a
plausible-looking centerline.

### A.3 Which component advances the planar tangent, and the sign question 4b cannot settle

Both actuators are `<motor … gear="0 0 0 0 1 0">`, i.e. torque about the **model y axis**, so the
motion the plant is driven through is planar in the model **x–z** plane. The rotation-vector
component that advances a planar tangent is therefore the **y component — index 1 of each triplet**,
and the projection design 3.5 names is model `x → scene x`, model `z → scene y`.

**The sign is a convention, and it is the one thing here I am deliberately not asserting.** A
positive rotation about `+y` carries `+x` toward `−z`, so the scene-frame tangent angle advances by
`−θ_y` under the obvious reading of that projection. I have not measured that against a MuJoCo
rollout and **must not**, because V18 forbids the adapter importing `mujoco` and this session opened
no model. The honest structure is:

1. `render_geometry.planar_convention.rotation_vector_component` and `.projection` **declare** the
   component and the sign; the adapter applies what is declared and invents nothing.
2. The coherent fixture generates its `q_true`, `deform_coords`, centerline and `true_task_output`
   under **one** declared convention, which is what proves the *derivation logic* — the fixture
   cannot and does not prove the convention matches MuJoCo.
3. **A sign error against real data is precisely the class the geometry-validation artifact's
   maximum-deviation field catches**, because a flipped tangent puts the derived distal point
   centimetres away, not nanometres. That artifact does not exist and 4b does not build it, so this
   question is not open inside 4b — it is *assigned*, and to the right place.

Say that in the fixture's own geometry-validation artifact as well: a fixture tolerance
authenticates fixture bytes and manufactures no real-data number.

### A.4 The forward map the fixture and row 18 must share

One map, used by the generator to build the data and by the adapter to check it — the same shape
`_forward_kinematics` already has in `verification_scene.py`, but over the real chain:

```
angle ← q_true[0]                       # first L1 body's absolute tangent, scene frame
point ← base_xy_m                       # (0.0, 0.5) for this producer
for link in (L1, L2):
    if link is L2:
        angle ← distal L1 tangent + q_true[1]      # q_true[1] is relative (design 3.5)
    for body b in 0..15:
        emit point
        point ← point + segment_lengths_m[b] * (cos angle, sin angle)
        if b is an internal body:
            angle ← angle + s * deform_triplet(link, b)[1]     # s is the declared sign
emit point                              # the distal point compared to true_task_output
```

Three properties the build must hold, and each is a test:

1. **`emit` count.** The centerline is `[T, N, 2]` and `N` is fixed by the chain, not chosen — one
   point per body plus the distal point. A fixture that emits a different `N` will still satisfy
   `verification_scene`'s `[T,N,2]` shape gate, which only requires `N ≥ 2`. **Pin `N` as a
   literal**, per lesson 229: a test written as `len(links) * 16 + 1` moves with the mutation.
2. **`q_true[1]` is relative.** Applying it as an absolute orientation produces a centerline that is
   continuous, plausible and wrong. The separating fixture case is a non-zero L1 deflection with
   `q_true[1] = 0`: under the relative convention L2 continues straight on from L1's distal tangent,
   under the absolute one it snaps back to the base frame.
3. **The distal point is `true_task_output` by construction** in the fixture, to
   `CENTERLINE_TASK_OUTPUT_TOL_M = 1.0e-9` — that constant stays the fixture's and does not move
   (design 4.6). The adapter's own tolerance still comes only from the authenticated
   `distal_tolerance_m`.

### A.5 Exit 15, re-measured this session

`utils.verification_scene.EXIT_CODES` drives `X_SCENE_OK → 0` and the twelve refusals to **3 … 14
contiguously**; **15 is free** and no existing value moves. Measured by importing the live table on
this checkout, not read off the design. Adding `X_GEOMETRY_UNSUPPORTED: 15` is purely additive.

### A.6 One correction carried forward from Codex's Session-145 cross-review

The plan's "Why this file exists" block calls 4b-ii-b "the only unbuilt work in the project." Codex flagged
that as a non-blocking wording error and it is right: 4b-ii-b is the only unbuilt **connection-adapter
half**. Steps 4c-4f are also unbuilt — they are blocked rather than startable, which is a different
thing from built. The plan's own final section already says so. The sentence is left standing and
this is its forward correction, in the same instrument this session had to learn to use on the
public log.

---

## Appendix B — sequencing step 2 executed (Claude Session 148)

*Appended 2026-08-17, Session 148. Rows 13-17 are built. This appendix records what the
build session settled that the plan could not, so the next session starts from decisions
rather than from re-derivation. The design at blob `032db166` remains the authority.*

### B.1 The rule the build settled, and it narrowed the rows

`utils.role_contract._semantic_role_checks` — which read-order step 12 already runs every
payload through — was read at source before a line was written. It already establishes,
**within one payload**: a `labels` struct's known source class, non-empty subtype and
finite non-negative onset; an `estimator_outputs` payload's minimum of one decision, every
row's conformance to `utils.estimator.EstimatorOutput.validate`, and both decision axes
strictly increasing; and a `controller_logs` payload's `step` being a non-empty contiguous
0-based grid whose `t_s` is strictly increasing and finite.

**So rows 13-17 carry exactly the facts a single payload cannot carry, because each is a
relation *between* payloads.** Restating any of the above would have produced guards no
input could reach. The one deliberate exception is row 16's per-decision `validate()`,
which is applied to the `EstimatorOutput` values *the adapter constructs* and therefore
holds this module's transcription rather than the payload — a defect no earlier row sees.

**Rows 18-21 must be written to the same rule.** Read the owner before writing the guard.

### B.2 Three measurements the next session should not re-take

1. **The harness window is `ANALYSIS_WINDOW_S = 0.04`, not 5.0.** The contract fixture runs
   32 steps at 500 Hz: grid 0.000-0.062 s, onset 0.020 s, so a window must close on a
   sample at or before 0.062 s, bounding it at 0.042 s. 0.040 closes exactly on the sample
   at 0.060 s. The 5 s value is now the row-17 refusal case. It is a **fixture** number and
   the constant's comment says so; `analysis_window_s` is shape-gated and this lane selects
   no analysis window.
2. **Row 13 is a post-condition across a module boundary and cannot fail in production.**
   `connection_record` parses `cases[*].arms` as a mapping keyed exactly by `SUITE_KEYS`
   and `roles` exactly by `ROLE_NAMES`, so step 12 can only load the complete set. The row
   exists so the dependency is a named refusal rather than a silent inheritance; its tests
   drive the function directly, and one further test drives a one-armed record end to end
   and records that the step-2 refusal is real today. **Do not "fix" this by deleting the
   row, and do not fake reachability for it.**
3. **Row 16's lower bound is unreachable on the contract fixture's grid.** That grid starts
   at 0.000 s, so any time below the first sample is negative and the schema-D contract
   refuses it one branch earlier. A live plant grid starts at one control interval
   (`cable_plant` stamps `t_s` after advancing), so the test shifts the grid to the live
   shape. **A boundary that looks covered because a fixture cannot reach it is the same
   defect shape as an unreachable guard.**

### B.3 What rows 18-21 begin from

`resolve_cases(connection) -> AuthenticatedCases`, a tuple of `CaseSeries`, each carrying
`playback_t_s`, the agreed `truth` (`utils.verification_scene.LabelFields`), the declared
`window_s`, and two `ArmSeries` holding `q_true`, `deform_coords`, `task_reference`,
`true_task_output`, the decisions and the three controller axes. Every array is a reference
to the read-only array step 12 built over an immutable buffer; nothing is copied and the
value carries **no cross-arm scalar** (invariant W13).

Row 18 then needs, and none of it is built: the adapter wiring that calls
`utils.centerline_geometry.derive_centerline` and `require_distal_point_within_tolerance`
per arm; a harness record whose `render_geometry` is
`coherent_geometry_fixture.coherent_render_geometry`; a role tree built from
`coherent_privileged_record`; and the fixture geometry-validation artifact that
`coherent_geometry_fixture.geometry_validation_document` already generates, written so it
says in the artifact itself that a fixture tolerance authenticates fixture bytes and
manufactures no real-data number.

---

## Appendix C — sequencing step 3, first half (Claude Session 149)

*Appended 2026-08-17, Session 149. Row 18's adapter wiring is built and Codex's two
Session-148 cross-review items are discharged. Rows 19-21, the observer, the CLI wiring
and the additive `build_role_bundle` edit remain. The design at blob `032db166` is still
the authority.*

### C.1 Row 18 turned out to own exactly two facts, and the rest were already owned

Section 2's row table gives row 18 three jobs: derive the centerline, require the
declared tolerance to equal its authenticated source, and require the distal point to
match `true_task_output`. **The middle one is row 5's and was already built** —
`authenticate_sources` compares `distal_tolerance_m` against the artifact's named field
*and* requires the artifact's maximum-deviation field not to exceed it
(`_require_measured_deviation`). So `resolve_geometry` is a call to
`utils.centerline_geometry` and a call to `require_distal_point_within_tolerance`, and
nothing else. That is B.1's rule reaching row 18: **read the owner of the fact at source
before writing the guard.**

**The refusals are passed through untouched rather than prefixed with the arm.** The
geometry module raises `X_GEOMETRY_UNSUPPORTED` itself, so there is nothing to
translate. Prefixing was considered and rejected on a measurement rather than a
preference: of the refusals `derive_centerline` can raise, the rank, width, grid-length
and non-finite ones are **unreachable through `resolve_geometry`** — step 12 ran both
arrays through the role contract and step 15 bound every frame-bearing plant array's
leading axis to the playback grid — so the reachable ones are record-level (no arm to
name) plus the distal comparison, which already takes `where` and names the arm itself.
Threading a `where` through `derive_centerline` would have moved 39 call sites to add a
prefix to messages no input reaches.

### C.2 The accept path: the coherent fixture installed *over* the contract harness

`_coherent_geometry` in the test file rewrites both arms' `plant` payloads, the
geometry-validation artifact and the record's whole `render_geometry` block, then
regenerates every identity the rewrite moves from the files themselves. **No second
harness and no second role tree were built**, and that is worth keeping: the contract
harness already owns the manifest, audits, indexes, checkpoints, observations, labels,
estimator outputs and controller logs, none of which row 18 is about.

Three things the build had to find out, all cheap to re-lose:

1. **Both arms must carry the same plant record.** Row 14 requires the arms to agree
   about `task_reference`, so two independently generated trajectories are refused a row
   before the one under test. The contract fixture already writes one record per pair.
2. **The coherent record's grid must be the contract fixture's grid**, or step 15
   refuses the rewrite. `n_steps = 32` at `f_ctrl = 500.0` reproduces `0.000 … 0.062 s`
   exactly. The control rate is a literal in the test file pinned by equality against the
   config the harness loads.
3. **Displacing the tip to drive the tolerance refusal must carry `tracking_error` and
   its norm.** `utils.role_contract` requires `tracking_error == task_reference -
   true_task_output`, so moving the tip alone is refused at step 12 as an inconsistent
   payload and never reaches row 18. Carried consistently, the payload is internally
   impeccable and still describes a body the declared chain does not produce — which is
   the fault row 18 exists to see and the one no single-payload check can.

The geometry is built twice: once with a placeholder tolerance digest so the generator
can run, then `dataclasses.replace` of exactly that one field once the validation
artifact exists. The agreement the fixture achieves is **exactly 0.0 m**, because the
generator sets `true_task_output` to the derived distal point itself.

### C.3 Codex's two Session-148 items, both discharged

1. **The "largest closable window" claim was false and is corrected forward.** The bound
   is `0.042 s`; `0.040 s` is kept, and the convention that owns the choice is now
   written beside the constant — *the largest whole multiple of 0.01 s inside the bound*,
   chosen so the fixture window does not sit on a boundary where a later `FIXTURE_N_STEPS`
   change would turn a passing fixture into a refusal for a reason unrelated to the row
   under test. The test is renamed and now **measures** the bound (0.040 and 0.042 close,
   0.044 does not) instead of asserting maximality.
2. **Row 16 bounds `decision_time_s` only, and that is now stated rather than inferred.**
   The argument is in `resolve_decisions`' docstring and pinned by
   `test_row16_bounds_the_time_axis_only_and_that_is_the_settled_reading`: schema section
   D calls `step` bookkeeping and ties it to no grid; the design already refuses two
   bindings of exactly this shape (finding CI's `onset_index`, step 15's `controller_t_s`)
   because a faithful producer offsets the axis; nothing downstream uses `step` as an
   index — the causal call panel selects by time; and step 12 plus row 16's own checks
   still hold everything about `step` except the grid binding. A later artifact that makes
   the estimator's step an index into the playback grid is an amendment, not a quiet
   tightening.

### C.4 What is left, in order

Rows 19, 20 and 21; then the audit-hook observer (W3/B4); then B2, B5 and the remaining
B3 rows; then the `roles` CLI wiring and the additive `build_role_bundle` edit; **then**
the two-pass mutation sweep on the finished pair, whose staged-tree set (`scripts`,
`tests`, `schema`, `config` **and** `results`) is unchanged; **then** the Review Card and
the subject chat; then the handoff. Still no card and no chat for 4b-ii-b, and that is
still deliberate.

---

## Appendix D — sequencing step 3, second half begun (Claude Session 150)

*Appended 2026-08-17, Session 150. Codex's two Session-149 cross-review findings are
discharged and read-order row 19 is built. Rows 20 and 21, the observer, the CLI wiring
and the additive `build_role_bundle` edit remain. The design at blob `032db166` is still
the authority.*

### D.1 Codex was right twice, and neither finding was contested

Both were driven at source before they were accepted, and both were reachable states
that the green aggregate suites did not exercise. Neither is a Review Card round: there
is still no card and no subject chat for 4b-ii-b, and the corrections propagate forward
into the build the way the constitution's cross-review rule says they should.

**1 — `render_geometry.source.model_id` was never joined to the config.** Design 3.5
says the geometry source "names and hashes the actual producer ... and echoes the
config's `model_id`". Step 5 hashed the producer and stopped there. The producer digest
fixes *which file built the model* and says nothing about *which model the run was
configured to build*, so a record could name any model at all and rows 1 through 18
accepted it. **The repair is one comparison at step 5**, `X_IDENTITY_MISMATCH`, run
through `value_at_field_path` so an absent config field is a named refusal rather than a
`None` that compares unequal for the wrong reason. `authenticate_sources` now takes the
`AuthenticatedConfig` step 4 produced — the config the record must agree with is the one
step 4 digested and validated, not whatever the path names on a second read.

*** THE HARNESS RECORD HAD DECLARED `"cable-two-link"` SINCE THE FIXTURE WAS WRITTEN,
AND THE CONFIGURATION HAS NEVER CARRIED THAT STRING. *** Nothing noticed because nothing
compared them. The fixture now echoes `PLANT_MODEL_ID`, written as a **literal** and
pinned by equality against the loaded config in its own test — never read out of the
config at build time, because a fixture whose input is a function of the value under test
keeps agreeing however the value moves.

**2 — the Session-149 row-16 ruling was backwards on both axes.** That session settled
row 16 as bounding `decision_time_s` only and pinned `step == T` as *accepted*. Codex
read the live producer instead, and the chronology is not ambiguous:

| fact | source, read again this session |
|---|---|
| `step` is the loop variable | `run_online_rollout` iterates `step_index in range(n_steps)`; `EstimatorCommandPolicy` persists that exact integer in every `EstimatorOutput` |
| `step`'s declared unit | `schema/schema.json` gives it `control_step_index` |
| the decision precedes the advance | `run_online_rollout` reads `plant.data.time`, calls the policy, **then** calls `plant.advance` |
| the sample follows the advance | `CablePlant.advance` stamps `PlantStepState.t_s` from the clock after the integration loop |

So a faithful trace of `T` control steps carries `0 <= step <= T-1`, and its first
decision is stamped `0.0 s` while `playback_t_s[0]` is one control interval later. The
Session-149 row **accepted a step no producer can emit and refused the step-0 decision
every producer does emit.** Codex's probe reproduced the second half exactly:
`X_DECISION_UNSUPPORTED ... decision 0 at t=0.0 s lies outside the playback extent
[0.002, 0.064] s`.

**The repair, and the shape of it matters.** `step` is bound to the control-step domain
(`step < T`; the lower side is already total in schema-D and is re-driven over this
module's own transcription by the `validate()` call). The time axis is bounded **above
only** — after the last playback sample there is no frame to draw against — and its lower
side is left to schema-D's non-negativity, because a second comparison there is a branch
no input can reach. *** THE PAIRING `decision_time_s <= playback_t_s[step]` BECAME
WRITABLE ONCE `step` WAS BOUND, AND IT IS DELIBERATELY NOT WRITTEN. *** It would bind the
estimator's clock to the plant's grid sample by sample, which is the class of binding
finding CI forbids for `onset_index` and step 15 forbids for `controller_t_s`, both
because a faithful producer offsets the axis. A test named for that decision fails if a
later session adds it.

### D.2 Row 19 owns exactly one fact, and B.1's rule is why

Rows 3 and 4 already hold three of the four provenance inputs:
`_require_authority_split_policy` refuses a `DEVELOPMENT_ONLY` record whose split is not
`dev` and a `FINAL` record whose split is `dev`; `require_authority_config_policy`
refuses every wrong authority/lifecycle cell and a `FINAL` `config_hash` carrying a
`dev-` trace; row 6 binds every manifest row's `config_hash` to the authenticated
config's, so a development trace in the manifest is caught two rows earlier.

**What no earlier row holds is the dataset's `assignment_hash`.** Row 6 checks it for
*agreement* — record against both audits, and the two audits against each other — and
never for what it says. A record claiming `FINAL`, naming a frozen clean config, a
non-`dev` split and a dataset whose audits both honestly echo a `dev-` assignment passes
rows 1 through 18 today: every digest agrees, every echo agrees, and the scene carries a
`FINAL RESULT INPUTS` banner over data generated under a development assignment. That is
the exact input set invariant W6 asks for, and `resolve_provenance` is where it refuses.

*** ROW 19 IS DRIVEN AT THE IN-MEMORY SEAM AND THAT IS FORCED, NOT CHOSEN. *** W7 says
production `FINAL` is unreachable from every input this packet contains, and that
unreachability is a property the project is maintaining rather than a gap to be filled.
Building W6's input set end to end would manufacture the very reachability W7 exists to
deny. The seam is the only instrument that reaches it — the same position row 13 is in,
and it is written into the tests rather than left to be rediscovered.

`SYNTHETIC_FIXTURE` is never computed by this row. It is the private assembly seam's
state, supplied by a construction path that opens no connection record at all; a public
invocation able to resolve to it would be a public path able to disclaim its own inputs.

### D.3 Numbers

Focused pair **255** (was 243) and **255 again under `PYTHONOPTIMIZE=1`**; packet-wide
**2,913 passed / 0 failed / 152.25 s**. The arithmetic closes: 2,901 + 12 = 2,913, and
the twelve are three model-identity tests, a net three on row 16 (two removed, five
added) and six on row 19. `py_compile`, `git diff --check` and `git status --porcelain`
all clean; both edited files pure ASCII, LF, 0 CR, no BOM, final newline.

*** ONE HYGIENE CATCH WORTH KEEPING: THE FIRST WRITE OF THE ROW-16 DOCSTRING CARRIED A
U+2026 ELLIPSIS AND THE FILE STOPPED BEING PURE ASCII. *** It compiled, it passed every
test, and only the byte check found it. The check is cheap and it is the only instrument
that sees this class.

### D.4 What is left, in order

Rows 20 and 21; then the audit-hook observer (W3/B4); then B2, B5 and the remaining B3
rows; then the `roles` CLI wiring and the additive `build_role_bundle` edit; **then** the
two-pass mutation sweep on the finished pair, whose staged-tree set (`scripts`, `tests`,
`schema`, `config` **and** `results`) is unchanged; **then** the Review Card and the
subject chat; then the handoff. Still no card and no chat for 4b-ii-b, and that is still
deliberate.

*** THE CARD MUST NAME THE STEP-5 SIGNATURE CHANGE. *** `authenticate_sources` gained a
third parameter and its behaviour gained a comparison, and that function's bytes were
part of the closed 4b-ii-a candidate. This is authorized — 4b-ii-a and 4b-ii-b are a
split of one build's review and rows 13-21 necessarily move the same file — but a
reviewer must be told which closed-half function moved and why, beside the `schema.json`
EOL-pin follow-up already carried.
