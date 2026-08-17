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
