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

---

## Appendix E — sequencing step 3 continued, and a measured stop (Claude Session 151)

*Appended 2026-08-17, Session 151. Codex's Session-150 cross-review finding is
discharged, read-order row 20 is built, and the boundary that stops its accept path
is measured rather than guessed. Rows 21 and the rest of section 4 remain. The design
at blob `032db166` is still the authority.*

### E.1 Codex was right a third time, and the finding was in the evidence, not the code

Codex's Session-150 review found no defect in `resolve_provenance`. It found that the
**test seam feeding it built a state the read order refuses two rows earlier**, while
the tests' own comments asserted the opposite. That distinction is the whole finding
and it is worth keeping in those terms: the row-19 verdicts were right, and the
evidence for invariant W6 was not evidence.

**Driven at source before it was accepted, and it came out wider than reported.** A
probe built the harness in a scratch tree, authenticated it, applied the exact
Session-150 `_reprovenanced` helper and re-checked the joins rows 4 through 6
establish. Against the unedited authenticated connection **all eleven hold**; after
the helper **three hold and eight are broken**. Codex reported eight equalities with
one surviving; the same fault, partitioned slightly differently — I split the
established-result comparison in two and added the record-versus-audit `config_hash`
join on each audit, both of which happen to survive because neither side of them
moved.

| join | before | after the S150 helper |
|---|---|---|
| record `config.config_hash` == the validated config | holds | **broken** |
| `established_result` split == the record's split | holds | **broken** |
| `established_result` config_hash == the record's echo | holds | holds |
| every manifest row `config_hash` == the validated config | holds | **broken** |
| every named run's split == the record's split | holds | **broken** |
| record `<audit>.assignment_hash` == `<audit>.json` (x2) | holds | **broken** |
| record `<audit>.config_hash` == `<audit>.json` (x2) | holds | holds |
| `<audit>.json` config_hash == the validated config (x2) | holds | **broken** |

**The repair, and its shape is the part to carry.** `_reprovenanced` now moves every
copy the earlier rows bind — the record's own config echo, both audit `config_hash`
echoes, the established result's split and config identity at their *declared field
paths*, both audit documents, and every manifest row's `config_hash` and split — and
then requires the result to satisfy `_provenance_joins` before returning it. The join
set is written **once**, so the helper's post-condition and the tests that assert it
cannot drift apart.

*** THE POST-CONDITION RAISES RATHER THAN ASSERTS, AND THAT IS DELIBERATE. *** This
file's suite is re-run under `PYTHONOPTIMIZE=1` on purpose, and `assert` disappears
there. A post-condition that vanishes under optimisation is absent exactly when
nobody is watching.

*** AND IT HAS A NEGATIVE CONTROL, WHICH IS THE OTHER HALF OF THE REPAIR. *** The
Session-150 partial edit is reconstructed as an input and required to be caught,
naming all eight broken joins. Without it the new post-condition would be a guard no
input can make decisive — lesson 242, on the seam that carries invariant W6's only
evidence, which is the last place it should be allowed to happen twice.

Four tests: the join set measured against a real post-row-12 state (so a join written
down wrongly fails loudly instead of weakening the seam), the seam preserving all
eleven, the negative control, and the field-path setter refusing a path it cannot
write.

### E.2 Row 20 is built, and its accept path is measured as unreachable today

`resolve_bundle(connection, cases, geometry, provenance) -> VerificationBundle`, plus
`_scene_for` and `_arm_identity`. It does four things:

1. requires the record's menu, `resolve_cases`' output and `resolve_geometry`'s
   output to be **one sequence, in one order** — decidable because those are three
   separately produced values and a caller can pair the geometry of one connection
   with the series of another, the same seam rows 13 and 19 sit on;
2. requires the assembled menu to equal the **established result's** declared case
   list, ordered. Row 6 compared that list against the *record's menu*; this compares
   it against the *assembly*, which is a different object;
3. calls `validate_bundle`, the gate both surfaces run as the first statement of
   their own entry points, and re-raises nothing — the surface gate's code is the
   right code and this row invents no second one;
4. requires each scene's arm `run_id` and `pair_id` to be the record's own.

*** ONE CHECK IS DELIBERATELY ABSENT AND THE REASON IS IN THE MODULE. *** The
interactive surface exposes cases through a `display label -> case_id` map, and
requiring that map to be a bijection looks like row 20's business. It always is one:
`validate_bundle` already refuses duplicate labels, and a duplicate label is the only
way `dict(zip(...))` loses a case. Lesson 242 again — the exposure property is held
where it is decidable and not restated where it is not.

**THE BOUNDARY, AND IT IS MEASURED.** `validate_bundle` requires a menu carrying at
least one `structure`, one `actuator` and one `sensor` case. The contract fixture
writes **two** C1/S pairs: `fixture_dev`, whose labels are `healthy`, and
`fixture_val`, whose labels are `structure` — and row 6 refuses a run whose split is
not the record's, so the `val` pair cannot enter a `dev` record's menu at all. **No
menu this packet can currently build passes the surface gate.** Driven end to end on
the coherent fixture:

```text
validate_scene:  ACCEPTED
validate_bundle: REFUSED X_BUNDLE_INCOMPLETE -- a bundle must contain at least one
                 structure/actuator/sensor case; missing ['structure', 'actuator',
                 'sensor']
```

So row 20 ships with its three ordering refusals driven, the surface gate's refusal
driven end to end, and **the per-case assembly driven on its own** — `_scene_for` is
reachable because `validate_scene` is a different gate from the menu-completeness
rule, and a test drives the whole field-by-field mapping through it. What has **no
test yet** is the accept path and the two identity refusals, which sit behind a gate
no input available today can pass. That is written into the test file beside the
tests rather than left to be rediscovered, in the same form lesson 261 gave row 13.

*** THIS IS NOT AN ARGUMENT FOR RELAXING THE SURFACE GATE. *** A menu that cannot
show a reader a structure, an actuator and a sensor change side by side is a menu
that cannot support the comparison the whole artifact exists to let a reader make.
The repair is a fixture, not a rule change.

*** AND IT IS NOT A REASON TO EXTEND `build_data_contract_fixture.py`. *** That file
writes the tree whose census — two pairs, four runs — closed tests pin. The three-case
harness belongs in the test file, built the way `_coherent_geometry` already builds
its installation: write the extra `dev` pairs' payloads and indexes over the harness
tree, rewrite `manifest.csv` and both audits from the recomputed census, declare the
three cases in the record, and restore every byte on exit.

### E.3 One additive change to a closed-half surface, and the card must name it

`AuthenticatedConnection` gained **`record_sha256`**, set from the digest
`load_connection_record` checked. Row 20 puts it on every scene's provenance block,
and a provenance identity supplied by the caller at assembly time is an identity that
can lie (V7); a digest re-taken at assembly time is a statement about the file as it
is *then*, not about the bytes rows 1 and 2 authenticated. **This is the second
closed-half signature change 4b-ii-b carries**, beside `authenticate_sources`' third
parameter, and the card must name both.

### E.4 Numbers

`test_connection_adapter.py` **245** (was 235), the focused pair **265** (was 255) and
**265 again under `PYTHONOPTIMIZE=1`**; packet-wide **2,923 passed / 0 failed /
152.03 s**. The arithmetic closes: 2,913 + 10 = 2,923, and the ten are four seam tests
and six on row 20. `git diff --numstat` reads `217 0` on the module and `464 9` on the
test file. `py_compile` and `git diff --check` clean; both files pure ASCII, LF, 0 CR,
no BOM, final newline — the byte check run on the final bytes, per lesson 269.

### E.5 What is left, in order

The three-case coherent harness and row 20's accept path; then row 21; then the
audit-hook observer (W3/B4); then B2, B5 and the remaining B3 rows; then the `roles`
CLI wiring and the additive `build_role_bundle` change; **then** the two-pass mutation
sweep on the finished pair, whose staged-tree set (`scripts`, `tests`, `schema`,
`config` **and** `results`) is unchanged; **then** the Review Card and the subject
chat; then the handoff. Still no card and no chat for 4b-ii-b, and that is still
deliberate — seven consecutive sessions have held that line.

*** THE CARD NOW CARRIES THREE DISCLOSURES: the `schema.json` EOL-pin dependency, the
`authenticate_sources` third parameter, and the `AuthenticatedConnection.record_sha256`
field. All three move bytes that were part of the closed 4b-ii-a approval. ***

---

## Appendix F — Codex's two Session-151 findings discharged, and row 20's accept path opened (Claude Session 152)

*Appended 2026-08-17, Session 152. Both of Codex's Session-151 cross-review findings
are discharged, neither contested, both re-driven at source first and one of them
found wider than reported. The three-case coherent menu exists, so row 20's accept
path and its two identity refusals are reachable and driven. Row 21 and the rest of
section 4 remain. The design at blob `032db166` is still the authority.*

### F.1 Codex was right a fourth time, and its second finding is the same shape as its first

Codex's two findings are, at the level that matters, **one finding at two sites**: a
value that reaches a checked object from beside it rather than from inside it.

  * **Finding 1** — the row-19 test seam's post-condition named eleven joins and said
    in its message that it recognised every state a post-row-12 connection can be in.
  * **Finding 2** — `resolve_bundle` took `provenance` as a separately constructible
    argument and put its `state` on every scene without ever comparing it to the
    authenticated record.

Both were driven at source in a scratch probe before either was accepted, against the
exact Session-151 bytes.

**Finding 2, measured.** On the coherent fixture, whose authenticated authority is
`DEVELOPMENT_ONLY` and whose `resolve_provenance` returns `DEVELOPMENT_ONLY`:

```text
forged FINAL              -> validate_scene ACCEPTED
forged SYNTHETIC_FIXTURE  -> validate_scene ACCEPTED
```

`validate_scene` accepting the forged scene is the part that makes the finding
blocking rather than cosmetic: **nothing downstream of the assembly can see the
disagreement, because by then the label is the only statement of the fact.** The
one-case harness then stopped both at `validate_bundle`'s incomplete-menu rule, an
unrelated refusal that would have disappeared the moment the three-case menu landed.

**Finding 1, measured, and wider than reported.** Applying the Session-151
`_reprovenanced` to an authenticated connection and then measuring the relations the
earlier rows establish:

| relation | owner | before | after the S151 seam |
|---|---|---|---|
| the eleven declared joins | rows 4-6 | hold | hold |
| recomputed census == carried census | row 6 | holds | **broken** (`{'val': 4}` vs `{'dev': 2, 'val': 2}`) |
| each audit `manifest_audit` == recomputed census | row 6 | holds | **broken** (x2) |
| record 20-field `manifest_row` echoes | row 10 | 2/2 | **0/2** |
| role-index `config_hash` == validated config | row 12 | 8/8 | **0/8** |
| validated `config_hash` == its document's canonical digest | row 4 | holds | **broken** |
| row 4's authority/config **policy** | row 4 | accepts | **refuses** — a FINAL record names a 'draft' configuration |

The last row is mine rather than Codex's, and it is the one that shows the seam was
not only missing identity copies but had produced a state a *policy* refuses outright.

### F.2 The repair, and the line it draws

`_provenance_joins` now states **eighteen** joins rather than eleven — the seven new
ones are the rows above — and the post-condition is renamed
`_require_post_row12_state`, because it now checks three separable things and the old
name described only the first:

  1. every identity join;
  2. row 4's authority/config **policy**, by *calling* `require_authority_config_policy`;
  3. row 3's authority/split **policy**, by *calling*
     `connection_record._require_authority_split_policy` — the function that owns the
     rule, imported deliberately rather than restated.

**`_reprovenanced` has no `config_hash` parameter any more, and that is the structural
half of the repair.** It takes `config_status`, edits the config *document*'s `status`,
and re-derives the identity with `expected_config_hash`. An identity a caller hands in
is an identity no document produced — which is finding 2's defect, in the test seam.

*** ONE STATE ROW 3 FORBIDS IS STILL NEEDED, AND THE EXCEPTION IS CHECKED RATHER THAN
GRANTED. *** One row-19 test needs `FINAL` over the `dev` split, because that is the
only way to reach the split input of row 19's computation. It passes
`split_policy_violated=True`, and the post-condition **inverts** the check rather than
skipping it: a caller that declares the violation on a state row 3 would accept fails
there. A declared exception nothing verifies is a bypass.

*** AND THE POST-CONDITION NAMES WHAT IT DOES NOT CLAIM. *** It does not require the
config document to be one `validate_config_document` would accept under the frozen
lifecycle. That document is a complete frozen `config.json` with every freeze-required
path resolved, and invariant W7's whole content is that this packet does not contain
one and is not to manufacture one. The seam moves `status` and re-derives the digest —
so row 4's *identity* and row 4's *policy* both hold — and stops there, saying so.

**Two negative controls now, not one.** The Session-150 partial edit is the first and
breaks **11 of 18**; the Session-151 partial edit is the second, added this session,
and breaks **7 of 18**. Both are additionally required to fail row 4's policy. A new
post-condition whose only witness is the *previous* generation's defect has never been
shown to see the current one — that is lesson 272.

**Row 20's repair is three lines and one paragraph.** `resolve_bundle` requires
`provenance.state == connection.record.authority` **before the first scene is built**,
with `X_PROVENANCE_UNRESOLVED`. It is not a second copy of row 19's rule: row 19
requires *its own computed result* to equal the authority, this row requires *the value
it was handed* to be that authority, and the two separate exactly when a caller
substitutes. `SYNTHETIC_FIXTURE` is refused as a consequence rather than as a special
case — `utils.connection_record` admits only the two public authorities, so no
authenticated record can make the equality hold (V7).

### F.3 The three-case coherent menu, and why it is a fixture

`_three_case_menu` installs three additional `dev` pairs over the harness tree:
`menu-structure`, `menu-actuator` and `menu-sensor`, each carrying the **same coherent
plant record** row 18 needs, its own `labels` payload naming one required source class,
and an `estimator_outputs` payload whose `p_class` names that same class. It rewrites
`manifest.csv`, recomputes the census, rewrites both audits, appends to six role
indexes, rewrites the established-result artifact, declares the three cases in the
record — and restores every byte on exit.

*** THREE THINGS ABOUT IT A LATER SESSION SHOULD NOT REDISCOVER. ***

  1. **`observations` is not written at all.** `ROLE_NAMES` is `controller_logs`,
     `estimator_outputs`, `labels`, `plant` — no connection record names an
     observation payload, so none is opened and none had to be synthesised. That fact
     removed most of the expected work; read the owner of the fact first.
  2. **`controller_logs` is copied byte for byte** from the pair the contract fixture
     already wrote. Nothing in it is per-case, and rows 15 to 17 already accept it —
     the same reason `_coherent_geometry` leaves it alone while replacing the plant.
  3. **The restoration is a tested property, not a promise.** The installer touches
     twenty-odd files in a *session-scoped* tree, and a leak would not fail anywhere —
     it would quietly change what every later test in the file measures. So both trees
     are digested path by path before and after and required to be equal, with the
     connection record excluded and its own restoration asserted separately, because
     that one file is the autouse fixture's job.

**It is a fixture, never a rule change.** A menu that cannot show a reader a structure,
an actuator and a sensor change side by side cannot support the comparison the artifact
exists to let a reader make.

### F.4 What row 20 now has that it did not

  * the **accept path**: one scene per declared case, filed under the record's own case
    ids, in the record's order, every scene carrying the row-19 state and the record
    digest rows 1 and 2 authenticated, and the whole bundle passing `validate_bundle`;
  * the **run-id and pair-id identity refusals**, driven by patching `_arm_identity` —
    the guard is a post-condition over this row's own construction, so breaking the
    construction is how it is tested;
  * the **ordered** established-result comparison, which one case could not separate
    from an unordered one and three cases can;
  * both **forged-provenance refusals**, driven end to end, plus an observer test
    proving **no scene is built at all** on the forged path.

### F.5 Numbers

`test_connection_adapter.py` **257** (was 245), the focused pair **277** (was 265) and
**277 again under `PYTHONOPTIMIZE=1`**; packet-wide **2,935 passed / 0 failed /
178.15 s**. The arithmetic closes: 2,923 + 12 = 2,935. `git diff --numstat` reads
`49 13` on the module and `1066 92` on the test file. `py_compile` and
`git diff --check` clean; both files pure ASCII, LF, 0 CR, no BOM, final newline,
checked on the final bytes.

### F.6 What is left, in order

**Row 21**, which is now unblocked for the first time — its accept path needs a bundle
the surface gate accepts, and there is one. Then the audit-hook observer (W3/B4); then
B2, B5 and the remaining B3 rows; then the `roles` CLI wiring and the additive
`build_role_bundle` change; **then** the two-pass mutation sweep on the finished pair,
whose staged-tree set (`scripts`, `tests`, `schema`, `config` **and** `results`) is
unchanged; **then** the Review Card and the subject chat; then the handoff. Still no
card and no chat for 4b-ii-b, and that is still deliberate — eight consecutive sessions
have held that line.

*** THE CARD STILL CARRIES THREE DISCLOSURES: the `schema.json` EOL-pin dependency, the
`authenticate_sources` third parameter, and the `AuthenticatedConnection.record_sha256`
field. Session 152 added no fourth — `resolve_bundle` is 4b-ii-b's own code and its new
guard moves no byte that was part of the closed 4b-ii-a approval. ***

---

## Appendix G — Codex's two Session-152 findings discharged, and row 21 built (Claude Session 153)

*Appended 2026-08-17, Session 153. Both of Codex's Session-152 cross-review findings
are discharged, neither contested, both re-driven at source first and both found to
have a sharper form than reported. **Read-order row 21 is built, so all twenty-one
rows now exist.** What remains of section 4 is the audit-hook observer, B2/B5, the
remaining B3 rows, the `roles` CLI wiring, the additive `build_role_bundle` change,
the two-pass mutation sweep, and only then the Review Card and the chat. The design at
blob `032db166` is still the authority.*

### G.1 Codex was right a fifth time, and both findings were about a claim, not a value

Session 152's two findings were one fault at two sites — a value reaching a checked
object from beside it. Session 153's two are also one fault at two sites, and it is a
different one: **a helper whose name and docstring claimed more than the code checked,
where the missing check was cheap and available all along.**

**Finding 1, measured against my own Session-152 bytes.** `_require_post_row12_state`
ran row 4's *policy* and never row 4's *validator*. Applying the Session-152
`_reprovenanced` with `authority=FINAL`, `config_status='frozen'` and then handing the
result to `validate_config_document(..., require_frozen=True)`:

```text
row-4 validator REFUSES: the frozen configuration must be named exactly config.json
```

That is the first clause only. Driving the rest against the same document:

| frozen clause | required | the Session-152 seam produced |
|---|---|---|
| source path name | `config.json` | `config/draft-config-v0.1.json` |
| `decision` | `APPROVE_CONFIG_FREEZE` | `BLOCK_CONFIG_FREEZE_PENDING_…` |
| `confirmatory_payloads_allowed` | `True` | `False` |
| `open_gates` | `[]` | five gates |
| freeze-required paths resolved | 8 of 8 | **0 of 8** |

So the state was not a near-miss on one clause; it failed every clause the frozen
lifecycle names.

**Finding 2, measured, and it is worse than stale.** `_three_case_menu` rewrote the
connection record and restored every file that record *names*, so the record left
behind declared the temporary established result against the restored artifact:

```text
before context: 25c94f41…daacc27c
during context: 56a6d1b1…f233d36d64b4
after  context: 56a6d1b1…f233d36d64b4      restored: False
post-exit authenticate_connection -> X_IDENTITY_MISMATCH on established_result.sha256
```

Codex's two digests and mine agree exactly. **The record is not merely stale on exit —
it is refused**, and the same hole was in this file's other two installers,
`_coherent_geometry` and `_rewritten_payload`.

### G.2 The repairs, and the non-claim that turned out not to be one

**Finding 1.** `_require_post_row12_state` now checks four things rather than three:
every identity join, **row 4's own `validate_config_document` at the
authority-appropriate `require_frozen`**, row 4's authority/config policy, and row 3's
authority/split policy. `_reprovenanced` builds the frozen lifecycle out of
`_synthetic_frozen_document` — the complete validator-accepted fixture this file has
carried since acceptance test B8 — under a `config.json` source path, and moves
`record.config.relative_path` with it. `_provenance_joins` gains a nineteenth join
binding the validated config's `source_path` to that relative path.

*** THE PART TO CARRY IS WHY THE SESSION-152 NON-CLAIM WAS WRONG. *** Session 152 wrote
down, deliberately, that the post-condition does not require the config document to be
one the validator would accept, on the ground that invariant W7 forbids this packet
manufacturing a frozen `config.json`. Measured this session: **`validate_config_document`
reads `source_path` only for its name and never opens it**, so a validator-accepted
frozen state needs no file at all — the probe confirms neither the live packet nor the
harness's temporary packet gains a `config.json`. W7 is a rule about what the packet
*contains*; it was never a reason to skip a check that opens nothing. A stated
non-claim is a load-bearing claim, and it has to be re-derived at source like any other.

**What is still not claimed is now exactly one echo**, and it is named: the seam does
not move `record.config.sha256`, because that is a digest of file *bytes*, the seam
writes no file, and computing a byte rendering here would put an identity into the
state that no read produced — which is precisely the Session-152 defect shape. A test
pins that the field is unmoved, so a later session cannot "complete" the seam by
deriving it.

**Finding 2.** All three installers now save and restore the connection record in
their own `finally`. The restoration test compares the whole tree **with no exclusion
and no manual repair**, and a new test drives the property over all three installers by
re-authenticating after each context exits.

### G.3 The third negative control, built so only the new check can fire

Lesson 272 said a widened post-condition must be shown to see the *current*
generation's defect. Applying that to the widening itself, the two existing controls
are not enough: both break joins *and* fail row 4's policy, so the old post-condition
would have caught them too. Measured:

| control | broken joins | row 4 policy | row 4 validator |
|---|---|---|---|
| Session-150 partial | 11 of 19 | refuses | refuses |
| Session-151 partial | 7 of 19 | refuses | refuses |
| **Session-152 document** | **0 of 19** | **accepts** | **refuses** |

The third control is the only one the new call is *forced* to catch, and building it
that way is the point. It reaches the seam through a `config_document` hook that exists
for the controls and nothing else: it substitutes the document while every dependent
copy still moves coherently, so the control isolates the document rather than
reproducing an older generation's broken joins. A second, one-field control puts the
genuinely frozen document under the draft filename, which separates *what the document
says* from *what its file is named*.

### G.4 Row 21, and the seam it deliberately creates

`write_bundle` is the last row of the read order. It refuses a bound output root not
named for `record_label`, creates `<output-dir>/<record_label>/` with
`mkdir(parents=True, exist_ok=False)`, and then publishes the declared set.

*** THE SCRIPTED WRITER IS A PARAMETER, AND THAT IS FORCED RATHER THAN PREFERRED. ***
`scripts/render_verification_scene.py` is the entry point that calls *into* this
module, so importing it here closes a cycle; it is also the only module on this surface
that imports matplotlib, and the adapter opens nothing and draws nothing. Injection
keeps both properties — and an injected collaborator is exactly the seam this review has
now found twice, so **nothing the writer reports is adopted**:

  * the file set is derived from the bundle's own case ids and compared to the tree by
    set equality **in both directions**, with no directory permitted below the root;
  * the bundle document must be byte-identical to `canonical_bundle_text(bundle)` and
    must reproduce itself through `bundle_from_json`; its digest is **re-measured here**;
  * `verification_bundle.sha256` must hold that re-measured digest, because that file is
    the one instruction a reader is given;
  * every scene document must be `canonical_scene_text` of the scene this chain built;
  * **every figure's own `pHYs` chunk must state the resolution the report claims**, and
    that resolution must be 300 DPI. A report of a DPI is not a DPI. Measured against the
    tracked Step-3 figure set, matplotlib writes `pHYs 11811 11811 1`, and
    `round(300 / 0.0254) = 11811`, so the check is derived rather than pinned to a magic
    number.

**The exclusive create runs before anything is written and nothing is cleaned up after a
refusal.** A second run at the same label refuses without touching the first publication
(W10, driven with a counting writer that is never called), and a post-condition that
fires after the writer has run leaves the partial tree standing as evidence — the
discipline finding AU left behind.

**Codes.** The read-order table names only `X_SCENE_OK` for row 21, so the refusals reuse
the codes the rows above already use: `X_PROVENANCE_UNRESOLVED` for the destination (row
3's own code for output-dir violations) and `X_BUNDLE_INCOMPLETE` for the published set,
with `X_IDENTITY_MISMATCH` where a *reported* identity disagrees with an authenticated
one. No fifteenth exit code was added; design section 4.5's table is not reopened.

**The stub writer is bound to the real one.** Thirteen refusal cases run against a stub
so they stay fast and precise, and one test drives the real
`render_verification_scene.render_bundle` and the stub over the same bundle and requires
them to agree on the file set, the report's identity fields, the published bundle and
scene bytes and each figure's declared resolution. A refusal test whose writer differs
from the shipped one in some *other* way measures nothing about the shipped path.

### G.5 Numbers

`test_connection_adapter.py` **279** (was 257), the focused pair **299** (was 277) and
**299 again under `python -O`**; packet-wide **2,957 passed / 0 failed / 190.80 s**. The
arithmetic closes: 2,935 + 22 = 2,957, and the 22 are 4 on the seam and the installers
plus 18 on row 21. `git diff --numstat` reads `343 1` on the module and `842 37` on the
test file. `py_compile` and `git diff --check` clean; both files pure ASCII, LF, 0 CR, no
BOM, final newline, checked on the final bytes.

*** ONE OPERATIONAL FAULT OF MY OWN, CAUGHT BY THAT LAST CHECK AND WORTH KEEPING. ***
Scripted edits made with `Path.write_text` converted **both** candidate files to CRLF —
`write_text` translates `\n` to `os.linesep` on Windows. `git diff --numstat` showed
nothing, because `core.autocrlf` normalises on read, so **the diff is blind to exactly
this**. The instrument that saw it is a byte count of the working tree, which is why
lesson 269 says to check the final bytes rather than the diff. Both files were converted
back to LF and the suites re-run.

### G.6 What is left, in order

The audit-hook observer (W3/B4); then B2, B5 and the remaining B3 rows; then the `roles`
CLI wiring and the additive `build_role_bundle` change; **then** the two-pass mutation
sweep on the finished pair, whose staged-tree set (`scripts`, `tests`, `schema`, `config`
**and** `results`) is unchanged; **then** the Review Card and the subject chat; then the
handoff. Still no card and no chat for 4b-ii-b, and that is still deliberate — nine
consecutive sessions have held that line.

*** THE CARD STILL CARRIES THREE DISCLOSURES: the `schema.json` EOL-pin dependency, the
`authenticate_sources` third parameter, and the `AuthenticatedConnection.record_sha256`
field. Session 153 added no fourth — `write_bundle` is 4b-ii-b's own new code and moves no
byte that was part of the closed 4b-ii-a approval. ***

---

## Appendix H — Codex's two Session-153 findings discharged, and the audit-hook observer built (Claude Session 154)

*Appended 2026-08-17, Session 154. Both of Codex's Session-153 cross-review findings
are discharged, neither contested, both re-driven at source by me before a line was
changed, and both of my measurements reproduce Codex's published digests exactly. The
**audit-hook observer (W3 / B4)** is built, which is the first item of section 4's
remaining scope. What is left is B2, B5, the remaining B3 rows, the `roles` CLI wiring,
the additive `build_role_bundle` change, the two-pass mutation sweep, and only then the
Review Card and the chat. The design at blob `032db166` is still the authority and this
plan loses to it wherever they differ.*

### H.1 Codex was right a sixth time, and both findings are the same fault as each other

Session 152's pair was one fault at two sites — a value reaching a checked object from
beside it. Session 153's pair was a different one — a helper claiming more than it
checked. **Session 154's pair is the first one, returned at two new sites, and it has a
sharper statement: a row that takes an *already assembled* value and the thing that
value is supposed to have been assembled from must bind the two to each other, because
nothing in a signature makes two parameters come from one chain.**

`write_bundle(connection, bundle, render=...)` takes three. Session 153 checked the
third one exhaustively — the writer is a seam and its report is compared field by field
against the bytes it leaves behind — and did not notice that the *second* one is the
same kind of seam.

**Finding 1, driven at source before repair, and it reproduces to the digit.** Two
genuinely authenticated connections over one fresh harness, same `DEVELOPMENT_ONLY`
authority and same three-case menu, differing only in record label and therefore in
record digest:

```text
connection A label   adapter-fixture
connection A sha256  56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
connection B label   adapter-fixture-b
connection B sha256  af93cceab0196ec4d8cf6d7a2fa0a10660ffa83dd6af46451c878ea00d645647
```

Rows 13–20 resolved under A; row 21 handed the resulting bundle together with
connection B. **It published.** The tree was named for B and every scene inside it —
including the copy of the bundle document a reader is told to check the digest of —
identified A. Both of my numbers are Codex's numbers.

**And the destination half, which is the same finding one layer down.** The docstring
said row 21 refuses a root that is not the named child of the authority's parent; the
code compared `output_root.name` against `record_label` and nothing else. Substituting
`<harness-root>/wrong-parent/adapter-fixture` — *correct basename, wrong place* — was
accepted and populated. The existing refusal test moves the basename, so it could not
see this direction at all. That is Session 153's own lesson 279 landing on Session
153's own code.

**Finding 2, also driven at source.** `_png_pixels_per_metre` walked the chunk sequence
but bounded nothing and verified nothing:

```text
corrupted pHYs CRC        accepted, returned (11811, 11811) pixels per metre
pHYs header of 9 over a
one-byte body             IndexError("index out of range"), no refusal code
```

**Those two outcomes look opposite and are one defect**: a parser that indexes into
bytes it has not proved are present, and believes a chunk it has not proved is intact.
Which of the two a given malformed file produces is an accident of where the missing
bound happened to bite.

### H.2 The repairs

**One owner for the provenance block.** `_provenance_for(connection, case, state)` is
new, and `_scene_for` now calls it instead of building a `Provenance` inline. Row 21
builds its comparand with **the same function row 20 assembles with**, and compares by
walking `dataclasses.fields(Provenance)` rather than a hand-listed field set. *A field
added to that dataclass is therefore bound at row 21 without anyone remembering to bind
it* — which is the property a hand-listed set cannot have, and the reason the extraction
was worth doing rather than restating nine comparisons.

Before anything is created, row 21 now requires: the bundle's menu to be the record's
menu in the record's order; the bundle's declared version to be this module's; the
bundle's own `provenance_state` to be the authenticated authority; and every field of
every scene's provenance block to equal `_provenance_for`'s. Codes: `X_IDENTITY_MISMATCH`
for a presented identity that disagrees with an authenticated one (Session 153's own
rule), `X_PROVENANCE_UNRESOLVED` for the state, `X_BUNDLE_INCOMPLETE` for the menu and
the version. **No fifteenth exit code; design 4.5's table is still not reopened.**

**One derivation for the destination.** `_authority_output_root(connection)` re-derives
`<packet-root>/<authority output parent>/<record_label>/` from the authenticated
authority, the authenticated record label and the one packet root W8 names, and requires
the *bound* value to equal it, after proving the derived path resolves inside the packet
root — the same junction/symlink argument row 3 makes about `--output-dir`.

*** THE BASENAME CHECK WAS REPLACED, NOT KEPT BESIDE THE NEW ONE. *** A guard whose
refusal is reachable but whose deletion changes no outcome is a branch nothing can
distinguish from its absence, which is finding 5's shape and lesson 242's rule. The
equality catches both directions; the two tests that drive it — a moved basename and a
moved parent — are what make each direction visible.

**A total PNG walk.** Every chunk is now bounded before it is read (the header must fit,
then the declared body must fit) and checked before it is believed
(`zlib.crc32(kind + body)` against the chunk's own CRC field). The sequence must end at
an `IEND` chunk with nothing after it, and exactly one `pHYs` chunk is permitted — two of
them disagreeing would make the declared DPI a function of which one a reader's decoder
kept, and returning the first would be this row making that choice for the reader.

*** A THIRD HOLE THE FINDING EXPOSED, AND IT IS THE SAME SHAPE. *** The scene loop
indexes `bundle.scenes[case_id]` with case ids taken from the *record*. A bundle whose
menu is not the record's therefore produced a raw `KeyError` rather than a named
refusal. The menu check above closes it, and a test drives it with a case dropped.

### H.3 The audit-hook observer (W3 / B4)

`sys.addaudithook` sees the interpreter's own `open` event, so an open through `numpy`,
through `csv`, through a closed utility or through a bare builtin arrives identically.
That is what the Step-4b-ii-a review's `_open_counts` instrument — which patches
`Path.read_bytes` — structurally cannot do.

**Measured, and the equality closes with nothing filtered on either side:**

```text
one authenticate_connection call over the three-case menu
  48 raw `open` events over 47 distinct paths
  observed - expected  = {}      expected - observed = {}
  the one path opened twice is `schema/schema.json`, and the count is 2
```

The pinned second read is therefore now pinned *at the interpreter* rather than at one
door: a future second read of any file taken through any other route fails the
multiplicity test instead of joining an allowance.

*** THE OBSERVER OWES ITS OWN ANCHOR AND IT IS WRITTEN FIRST. *** A hook that recorded
nothing would satisfy set equality against an empty expected set and would satisfy
containment in either direction. So
`test_the_open_observer_records_an_open_the_allowlist_does_not_name` drives a builtin
`open` **and** an `os.open` on a file no allowlist names and requires both to be
recorded, and requires an inactive recorder to stay empty.

**The hook is process-wide and cannot be removed**, so it is written to cost nothing
when inert: one truth test on a list, and a return. Measured cost on the packet-wide
suite: **180.46 s without it and 185.03 s with it**, against 190.80 s in Session 153 —
inside run-to-run variation, and stated as a measurement rather than as an absence.

A fourth test uses the same instrument on row 21: during `write_bundle`, every path the
row **or its injected writer** opens is a child of the root row 3 bound, and the set of
their names is exactly the published file set.

### H.4 Numbers

`test_connection_adapter.py` **309** (was 279), the focused pair **329** (was 299) and
**329 again under `python -O`**; packet-wide **2,987 passed / 0 failed / 185.03 s**. The
arithmetic closes: 2,957 + 30 = 2,987, and the 30 are 26 on the two findings and 4 on
the observer. `git diff --numstat` reads `239 42` on the module and `561 1` on the test
file. `py_compile`, `git diff --check` and `git status --porcelain` all clean; both files
pure ASCII, LF, 0 CR, no BOM, final newline, **checked on the final bytes** — lesson 282's
instrument, run again because this session also edited by script.

### H.5 What is left, in order

B2 and B5; the remaining B3 rows; the `roles` CLI wiring and the additive
`build_role_bundle` change; **then** the two-pass mutation sweep on the finished pair,
whose staged-tree set (`scripts`, `tests`, `schema`, `config` **and** `results`) is
unchanged; **then** the Review Card and the subject chat; then the handoff. Still no card
and no chat for 4b-ii-b, and that is still deliberate — ten consecutive sessions have held
that line.

*** THE CARD STILL CARRIES THREE DISCLOSURES: the `schema.json` EOL-pin dependency, the
`authenticate_sources` third parameter, and the `AuthenticatedConnection.record_sha256`
field. Session 154 added no fourth — `_provenance_for` is an extraction inside 4b-ii-b's
own half, `_authority_output_root` and the strict PNG walk are new code in it, and no
public surface of the closed 4b-ii-a approval moved. ***
