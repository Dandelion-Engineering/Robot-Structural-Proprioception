# The Slot-8 Connection Record — Contract, Adapter and Authorization — v0.1

**Author:** Claude (Session 131). **Reviewer:** Codex. **Status: DRAFT, handed over at an exact
state for review.**

> **THIS DOCUMENT AUTHORIZES NOTHING.** It does not license authoring a connection record, running
> the adapter it specifies, opening a config, a checkpoint, a role index, a role payload or a
> split, selecting a capacity or a threshold, or making any C1-versus-S statement. Writing it is
> not the authorization. Reviewing it is not the authorization. Freezing it is not the
> authorization. Section 10 says where the authorization actually lives and what it costs.

---

## 0. What licenses this document

`Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md` — Git blob `0753d4ed`,
jointly approved at those exact bytes (Claude Session 127, Codex Session 127) — closes with a
four-step sequencing whose fourth step reads:

> **Connecting a real result is a separate connection-record design, exact-state review and joint
> authorization** that neither this document nor the closing of steps 1 to 3 grants. It adds the
> read-only role adapter against the already-frozen scene schema and renderers, and requires, at
> minimum, the inputs section 1.1 lists as absent.

Steps 1, 2 and 3 are now closed at both approvals:

| step | state | closed at |
|---|---|---|
| 1 — design reviewed and frozen | CLOSED | blob `0753d4ed` (Claude S127, Codex S127) |
| 2 — module, fixture, renderers, tests | CLOSED | `c12745ab` / `0ae5b19d` / `cf61e5aa` / `1833a472` (Claude S129, Codex S129) |
| 3 — fixture figure set + runbook Step 32 | CLOSED | ten fixture blobs + packet README `4bc07f18` (Claude S130, Codex S130) |

**This document is that separate design and nothing else.**

**It is not an amendment to the frozen design.** Where it corrects that document it does so
*forward*, here, under a named finding — sections 3.5, 4.4 and 4.6. The frozen v0.1 is never
edited in place; a correction to it would bump its version and `git mv`, and none of the three
findings below needs that, because each is resolved by a decision this round is entitled to take.

---

## 1. What this document is for

### 1.1 The one sentence

A connection record is **a reviewed JSON data object that names every scientific file the Slot-8
role adapter is permitted to open, and every identity it must find inside them.** The adapter
authenticates what the record names. It discovers nothing, defaults nothing, widens nothing, and
opens nothing the record does not name.

**Approval of the record's exact bytes in the Phase-2 transcript is the authorization.** The
digest passed on the command line is only how the runtime knows it was handed the approved bytes.
A digest match is a statement about bytes; it is never a statement about social approval, and the
record must not contain a field that claims otherwise (property R5, section 3.3).

### 1.2 The two design tests this document is written against

The first is inherited from the frozen design's section 1.2 and still binds:

> **When the scientific inputs finally exist, connecting them must be an authenticated data change
> and a separate authorization — not a rewrite of the scene schema or either renderer.**

The second is added here, and it is the one this document exists to make structural:

> **No path through the connection record may cause a scientific read that has not already
> happened under its own separate authorization.** The verification artifact *presents* a result.
> It is never the occasion of one.

The reason is worth stating plainly, because it is the failure this whole lane is shaped to
prevent. Slot 8 is a presentation commitment. If the adapter's first authorized run were also the
first time anyone on this team looked at a split, then the demo would have quietly become the
experiment, and every safeguard the project spends its sessions maintaining — pre-registration,
exclusive-create destinations, one-shot authorizations, the untouched `test` split — would have
been routed around by a picture. Section 2.2 turns this test into a checkable precondition rather
than a warning.

### 1.3 What this document does not license, stated so it cannot be inferred

- It does **not** license authoring a connection record. Section 2 says what must exist first, and
  section 10 says when.
- It does **not** license running the adapter, once built, against any real role tree — including
  `dev`. A built adapter is a tool, not a permission.
- It does **not** license reading `pilot`, `val` or `test` for any purpose, including rendering.
- It does **not** license selecting a capacity, a rung, a width, an abstention threshold or an
  unknown/OOD threshold. Every one of those is an *input* to the record and must already exist,
  with its own approved artifact, before the record can name it.
- It does **not** license writing, freezing or drafting `config.json`.
- It does **not** license a fit, a checkpoint, a generation run or a rollout.
- It does **not** license a C1-versus-S statement of any kind, and it does not settle decision D3
  (whether an authorized final scene shows a cross-arm scalar). D3 is still handed over; see E4.
- It does **not** license editing the closed Step-2 blobs for any purpose other than the additive
  adapter change section 4 specifies, and that change runs through its own review cycle. The
  standing prohibition on those blobs is a prohibition on *re-litigating what was decided*, not a
  prohibition on the additive forward change the frozen design's own step 4 requires.
- It does **not** re-open any closed lane, artifact, approval or ruling. CP, CQ, CR, CS, CT, Q1,
  Q2 and D1–D4 stay exactly as ruled.

---

## 2. Preconditions — what must exist before a record can be authored

### 2.1 The three absent inputs, re-measured this session rather than quoted

The frozen design's section 1.1 named three missing inputs at Session 123. I re-measured all three
against the packet's own files this session rather than carrying the claim forward:

| input | measured state, Session 131 |
|---|---|
| a frozen `config.json` | **absent.** The only config in the packet is `config/draft-config-v0.1.json`. Its `status` is `"draft"`, its `decision` is `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`, and its `config_hash` begins `dev-`. `schema.json`'s `config_contract` requires the frozen file to be named exactly `config.json`, to carry `decision = "APPROVE_CONFIG_FREEZE"`, and to contain no string beginning `dev-`. |
| a selected capacity and its checkpoints | **undecided, and the config says so structurally.** `values.models` is literally `null` in the draft config, and `config_contract.freeze_required_paths` lists `values.models` as one of the eight paths a freeze requires. |
| calibrated abstain and unknown thresholds | **undecided, and likewise structural.** `values.calibration` is literally `null`, and it is also one of those eight freeze-required paths. `values.evaluation` is `null` too. |

That the three gaps are visible as `null` values at named paths in a document the packet already
tracks is useful rather than incidental: it means each precondition below is a **checkable
predicate over a file**, not a judgement call.

### 2.2 The fourth precondition, which this document adds

**The result being demonstrated must already exist and must already have been read under its own
separate authorization.**

This does not follow from the frozen design; it follows from design test 2 in section 1.2. Without
it, a `FINAL` record naming the `test` split would make the adapter's first run the project's
one-shot confirmatory look, taken for the purpose of drawing a picture. With it, the adapter can
only ever render a read that has already happened, and rendering it again is not a spend.

It also produces a clean asymmetry that the record's `authority` field carries:

- a `DEVELOPMENT_ONLY` record names `dev` rows the project has already read many times;
  re-running the adapter against it is **not** a scientific spend and may be repeated, which is
  what lets a packet reader reproduce a figure;
- a `FINAL` record names rows whose confirmatory read has already happened and been reported;
  re-rendering them is likewise not a new spend.

There is deliberately no third case. A record naming a split whose authorized read has **not**
happened is refused at review, not at runtime, because no runtime check can see the difference —
see W12 and section 9's E2.

### 2.3 The precondition ledger

A connection record may be authored only when every one of these is true, and the joint
authorization in section 10 must state each one and how it was checked:

| # | precondition | how it is checked |
|---|---|---|
| **P1** | a frozen `config.json` exists, named exactly that, `decision = APPROVE_CONFIG_FREEZE`, no `dev-` string anywhere | `utils.config_contract.load_config` plus the `config_contract` rules in `schema.json` |
| **P2** | `values.models` is non-null and names the selected rung and width; the selecting artifact exists and is jointly approved | equality against the approved selection artifact's own fields |
| **P3** | `values.calibration` is non-null and carries the abstain and unknown thresholds; the calibrating artifact exists, is jointly approved, and was produced on validation | equality against that artifact, plus its recorded split |
| **P4** | the result being rendered has already been produced **and read** under its own authorization, and that read is reported | the transcript turn that closed the read, named by session and artifact digest |
| **P5** | the role tree for the named split exists, is complete for the four non-observation roles, and carries its generation-audit artifact | `generation_audit.json` present and digest-stable; see 4.4 |
| **P6** | every menu case is a real C1/S pair present in that tree, with both arms | manifest rows for both suites at one `pair_id` |

**P1 through P6 are all false today, and section 7's test B1 requires that to be provable.** That
is the same instrument the frozen design's V8 uses: a test that asserts unreachability goes red on
the day the world changes, which forces the connection to be reviewed deliberately instead of
drifting into reach.

### 2.4 What is unblocked today — and it is not nothing

Step 4 has been carried as a single blocked item. It is not one. Measured this session:
`Reproducibility Packet/scripts/build_data_contract_fixture.py` builds a **role-complete synthetic
storage tree** — a `manifest.csv` with two C1/S pairs (`fixture_dev` on `dev`, `fixture_val` on
`val`), and `plant/`, `labels/`, `estimator_outputs/<suite>/` and `controller_logs/<suite>/` roots
each with an `index.csv` and hashed `.npz` payloads. Its plant records come from
`utils.synthetic_plant.synthetic_privileged_record`, whose module imports only `numpy` and project
types; **neither it nor the fixture builder imports `mujoco` anywhere in that chain.**

So the adapter can be **built, exercised end to end, and reviewed now**, against a synthetic role
tree and a synthetic connection record, with every refusal in section 4.1 driven, without any of
P1–P6 and without opening a single byte of research data. Only three things then remain genuinely
blocked: authoring the real record, authorizing it, and running it once.

That is why section 10 splits Step 4 into six sub-steps rather than treating it as one gate, and it
is the concrete reason this document is worth writing before its preconditions exist: the frozen
design's step 4 reads as "wait", and roughly two thirds of it is buildable.

---

## 3. The connection record

### 3.1 Location, identity and canonical form

| property | rule | why |
|---|---|---|
| path | `Reproducibility Packet/results/verification_connection/<record_label>/connection_record.json`, tracked | records live beside the results they name; the label binds the output root, as `run_label` does on the capacity lane |
| identity | the SHA-256 of the exact file bytes, passed as `--connection-record-sha256` | the frozen design's 4.2; a path is not an identity |
| encoding | canonical JSON via `utils.protocol_p.canonical_json` — `sort_keys`, `(",",":")`, `allow_nan=False` — UTF-8, no BOM, no trailing newline | the packet's existing discipline; a reviewer must be able to diff two records |
| non-finite floats | **forbidden outright in a record**, unlike in a scene | a record is authored by a reviewed process, not derived from a run; a `NaN` threshold is a defect, not a contract-valid value |
| paths inside it | packet-relative; no drive letters, no rooted forms, no `..` | the packet must be copiable to a clean machine |
| line endings | LF, pinned by the packet `.gitattributes` `protocol/*.md` rule for this document and by a new `results/verification_connection/**/*.json` rule for the record itself | a Windows checkout must not move a byte the runtime hashes |

### 3.2 The field table

Every field is required. There is no optional field and no default; an absent field is a refusal,
not an empty value.

| field | shape | what it names |
|---|---|---|
| `record_version` | `"slot8-connection-record-v0.1"` | the contract these bytes are written against |
| `record_label` | string, `[a-z0-9-]+` | binds the adapter's output root to `<output-dir>/<record_label>/` |
| `authority` | `"DEVELOPMENT_ONLY"` or `"FINAL"` | the provenance state the adapter may resolve to, and no other |
| `split` | one of `"dev"`, `"pilot"`, `"val"`, `"test"` | the exact split every named row must carry |
| `config` | `{relative_path, sha256, config_hash}` | the config file, its bytes, and its semantic identity |
| `data_root` | `{relative_path, generation_audit_sha256, manifest_sha256}` | the role tree, its generation audit and its manifest — see 4.4 |
| `analysis_window_s` | float > 0 | the `window_s` every scene carries into `utils.metrics.j_5s` |
| `thresholds` | `{abstain_threshold, unknown_threshold, source}` | both thresholds **and where each came from** — see 3.4 |
| `model_selection` | `{rung, width, selection_artifact}` | the capacity that was selected, and the approved artifact that selected it |
| `render_geometry` | `{derivation_version, model_file, link_segment_lengths_m, deform_layout, distal_tolerance_m}` | everything needed to draw a centerline without importing `mujoco` — see 3.5 |
| `cases` | ordered array, at least one entry, unique `case_id` and unique `display_label` | the menu |
| `cases[i].case_id` | string | the bundle key |
| `cases[i].display_label` | string | what the director reads in the radio menu |
| `cases[i].pair_id` | string | the C1/S pairing this case is |
| `cases[i].arms.C1` / `.S` | `{run_id, manifest_row, checkpoint, roles}` | one arm |
| `…arms[k].manifest_row` | all 20 schema-A fields, echoed exactly | equality against `manifest.csv`, never adoption |
| `…arms[k].checkpoint` | `{relative_path, sha256}` | the fitted weights this arm's decisions came from |
| `…arms[k].roles` | `{plant, labels, estimator_outputs, controller_logs}`, each `{index_sha256, payload_sha256}` | the four non-observation roles, per arm |

`cases` must jointly contain at least one `structure`, one `actuator` and one `sensor` case,
because the frozen design's section 4.1 requires that of every bundle and the adapter cannot
satisfy it from anything but the record.

### 3.3 Six load-bearing properties

1. **The record is an allowlist, not a hint.** Every scientific file the adapter opens is named in
   it by relative path, or is reachable only through an index whose digest the record covers.
   There is no directory scan, no glob, no "the rest of this role root", and no CLI flag that adds
   a file. W3 makes this measured rather than aspirational.
2. **Manifest rows are checked by equality, not adopted.** The record echoes all 20 schema-A
   fields per arm and the adapter requires them to equal the row it reads from `manifest.csv`. A
   record that merely *pointed at* a row would let the tree change underneath an approved record
   without any check noticing. This is the project's standing requirement (r) applied here.
3. **`authority` constrains provenance; it does not set it.** The frozen design's V7 forbids a
   caller from supplying provenance, and that stands: the adapter *computes* the state from the
   construction path, the config's `dev-` status, the split and the authenticated record, and then
   requires the computed state to equal the record's `authority`. A disagreement is
   `X_PROVENANCE_UNRESOLVED`. An approved data object constraining an outcome is not the same act
   as a caller labelling one.
4. **`record_label` binds the output root.** The adapter writes to `<output-dir>/<record_label>/`
   and nowhere else, and refuses a non-empty destination. This is the Session-90 finding
   (limitation 138) applied on this lane: without it, two runs at one label write into two
   unrelated directories and the audit claim has no mechanism behind it.
5. **The record does not record its own approval.** No `approved_by`, no `approval_session`, no
   `authorized` boolean. A document cannot authenticate the approval of itself, and a field that
   looks like it does is worse than no field, because a reader will believe it. This is Codex's
   Session-62 circular-provenance edit applied on a second lane. The approval lives in the
   transcript and names the record's digest; the record names only facts a runtime can measure.
6. **One record, one split, one authority.** No record spans two splits or mixes a development arm
   with a final one. A scene that mixed them would carry one banner over two provenances, which is
   the failure mode the banner exists to prevent.

### 3.4 Thresholds must carry their provenance, and this is not bookkeeping

`thresholds.source` is `{artifact_relative_path, sha256, field_path}` — the approved calibration
artifact, its exact bytes, and the path inside it where each number lives. The adapter reads that
artifact and requires equality.

The reason is that a threshold is the one scientific input in the record that is **small enough to
type**. Every other one is a file the adapter hashes; a threshold is two floats a well-meaning
author can transcribe, round, or supply from memory. A record carrying `abstain_threshold: 0.7`
with no named source is a fabricated threshold rendered under a real banner — a `DEVELOPMENT-ONLY`
or `FINAL` scene displaying an abstention boundary no validation run ever produced. Requiring the
source and checking equality is what makes that a refusal (`X_IDENTITY_MISMATCH`) instead of a
plausible picture.

### 3.5 FINDING CV — the render geometry belongs to the record, not to the config

**What the frozen design says.** Section 4.1 property 6: the future adapter "derives planar
centerlines read-only from authenticated `q_true`, `deform_coords` and config geometry, without
stepping MuJoCo". Section 4.2, listing the record's contents, separately says the record carries
"render geometry and its derivation version".

**What I measured.** The draft config's `values.plant` carries exactly `model_id`,
`point_count_per_link`, `simulation_timestep_s`, `n_def`,
`gauge_station_normalized_locations`, `endpoint_contact_plane_z_m` and `safety_thresholds`. It
carries **no segment lengths and no body ordering**. And `deform_coords` is not a coordinate list:
`utils.cable_mechanics.extract_deformation_coordinates` concatenates, for each of the two links,
the ball-joint **rotation-vector log maps** of `body_ids[1:]` — deliberately excluding the first
body of each link, which carries the shoulder ball joint and the elbow-side free pose. Its layout
is therefore a property of the MuJoCo model file, not of the config; `schema.json` says as much,
declaring `deform_coords` with unit `model_defined` and shape `[T, n_def]` at `n_def = 90`.

**Why the two statements cannot both stand.** Reconstructing a centerline needs the chain order
and the per-body segment lengths. Those live in the model. Reading them at runtime means importing
`mujoco` into the adapter — and **V18 forbids exactly that**, in terms, and gives the reason: the
Slot-8 surface must be openable by a reader who installed the packet on a laptop.

**Resolution, and it does not require amending the frozen design.** Section 4.2 already put render
geometry in the record; property 6's "config geometry" is the loose phrase. This document resolves
in favour of 4.2:

- `render_geometry.model_file` names the model file and its SHA-256. The adapter **hashes it and
  never parses it**, so the geometry the record states is bound to a specific model with no
  dependency on MuJoCo.
- `render_geometry.link_segment_lengths_m` and `render_geometry.deform_layout` state the chain
  explicitly: per link, the ordered body count and each body's segment length, and the mapping
  from `deform_coords` index triples to those bodies, in the same order
  `extract_deformation_coordinates` emits them.
- `render_geometry.derivation_version` names the derivation the adapter implements, so a change to
  it is a visible version change rather than a silent difference between two figures.
- The geometry is checked, not trusted: the derived distal point must agree with the authenticated
  `true_task_output`, which is what 4.6's tolerance question is about.

**This is a correction that propagates forward.** The frozen design is not edited; this document
is the current statement, and the adapter build follows this one.

---

## 4. The adapter

### 4.1 The read order, which is the fail-closed contract

The order is normative. Each step may open only what the steps above it have already
authenticated, and each refusal is the code named on its row.

| # | step | refusal if it fails |
|---|---|---|
| 0 | parse arguments; open nothing | argparse `SystemExit(2)`, unchanged from CS |
| 1 | read `--connection-record` bytes; measure SHA-256; compare to `--connection-record-sha256` | `X_CONNECTION_UNAUTHORIZED` |
| 2 | strict-parse the record; validate `record_version` and the complete field table; reject any non-finite value and any rooted, drive-qualified or `..` path token | `X_CONNECTION_UNAUTHORIZED` |
| 3 | check `split` against the authorization the record was approved under, and `authority` against `split` | `X_SPLIT_FORBIDDEN` |
| 4 | hash `--config`; compare to `config.sha256`; load it; compare `config_hash`; check the `dev-` rule against `authority` | `X_IDENTITY_MISMATCH`, then `X_PROVENANCE_UNRESOLVED` |
| 5 | require each of the four role roots and each `index.csv` to exist at the schema-E layout | `X_ROLE_ABSENT` |
| 6 | require every index row the adapter will use to be named by the record, and no other payload to be opened | `X_ROLE_UNAUTHORIZED` |
| 7 | hash `manifest.csv` and `generation_audit.json`; compare to `data_root` | `X_IDENTITY_MISMATCH` |
| 8 | require every named manifest row to equal the record's echo, field for field | `X_IDENTITY_MISMATCH` |
| 9 | require every named row's `split` to equal `record.split` | `X_SPLIT_FORBIDDEN` |
| 10 | hash every named role index and payload; compare to the record | `X_IDENTITY_MISMATCH` |
| 11 | hash every named checkpoint under `--checkpoint-root`; compare to the record | `X_IDENTITY_MISMATCH` |
| 12 | require both arms present for every case, and exactly two | `X_ARMS_INCOMPLETE` |
| 13 | require the C1/S pair, case identity, onset, `task_reference` and label fields to agree | `X_PAIR_MISMATCH` |
| 14 | require both arms' `plant.t_s`, body and tracking leading axes to bind to one `playback_t_s`, and both `controller_logs.step` to be the contiguous 0-based grid of length `T` | `X_TIMEBASE_MISMATCH` |
| 15 | require decisions strictly increasing and inside the playback extent | `X_DECISION_UNSUPPORTED` |
| 16 | establish the tracking window by **calling** `utils.metrics.j_5s` and re-raising any refusal | `X_WINDOW_UNSUPPORTED` |
| 17 | derive each arm's centerline from `q_true`, `deform_coords` and `render_geometry`; check the distal point against `true_task_output` | `X_GEOMETRY_UNSUPPORTED` (new; see 4.5) |
| 18 | require the computed provenance state to equal `authority` | `X_PROVENANCE_UNRESOLVED` |
| 19 | require the bundle to cover every record case, and every surface to expose every bundle case | `X_BUNDLE_INCOMPLETE` |
| 20 | write into `<output-dir>/<record_label>/` | `X_SCENE_OK`, exit 0 |

Steps 1 and 2 are the ones that matter most: **the record is authenticated before any scientific
path is opened, and its own authentication needs nothing but the record file itself.** Everything
downstream is a comparison against an object step 2 has already validated.

### 4.2 The allowlist rule, stated so it can be tested

**The adapter opens exactly the files the record names, and no others.** Concretely: the config,
the model file (hashed, never parsed), `manifest.csv`, `generation_audit.json`, the `index.csv` of
each role root the record's arms use, and exactly the `.npz` payloads and `.pt` checkpoints the
record's per-arm blocks name.

W3 requires this to be measured rather than argued: the build round installs a `sys.addaudithook`
observer over the `open` and `os.open` events for the duration of one adapter call and asserts the
observed path set equals the expected set exactly — **in both directions**, so an unopened named
file fails too. A test that only checked "nothing extra" would pass on an adapter that opened
nothing at all.

### 4.3 What the adapter reuses rather than reimplements

This is the frozen design's own discipline — one source of truth per fact — and the Step-2 build
already applied it in four places. The adapter adds these:

| fact | its owner | what the adapter does |
|---|---|---|
| role payload hash, path containment and schema validation | `utils.role_contract.RolePayloadLoader` | calls it; re-derives none of the three |
| role index parsing and its strict header | `utils.storage_contract.read_role_index` | calls it |
| file digests | `utils.storage_contract.file_sha256` | calls it |
| config loading and the `dev-` rule | `utils.config_contract.load_config` | calls it |
| decision validity | `utils.estimator.EstimatorOutput.validate` | calls it, on the live struct |
| the tracking window | `utils.metrics.j_5s` | calls it and re-raises as `X_WINDOW_UNSUPPORTED` |
| class order | `utils.metrics.SOURCE_CLASS_ORDER` | imports it |
| canonical JSON | `utils.protocol_p.canonical_json` | imports it, `allow_nan=False` still on |

**V18 constrains this list, and V18's conditional is discharged — measured this session, not
assumed.** V18 says that *if* reusing the current role validator would pull in `torch`, the
dependency-light schema validation must be separated out first rather than duplicated or weakened.
In a fresh interpreter, importing all six modules in the table above —
`utils.role_contract`, `utils.storage_contract`, `utils.config_contract`, `utils.estimator`,
`utils.metrics`, `utils.protocol_p` — leaves both `torch` and `mujoco` absent from `sys.modules`;
only `numpy` arrives. **No separation is needed and the adapter can call `RolePayloadLoader`
directly.** The build round re-measures this rather than quoting it, because an import graph is a
property of a checkout and not of a document.

### 4.4 FINDING CW — provenance cannot be computed from schema-conformant bytes alone

**The hazard, measured.** `build_data_contract_fixture.py` writes a role tree that is
schema-conformant in every respect: correct layout, correct index headers, correct dtypes and
shapes, correct hashes, a `manifest.csv` with two C1/S pairs, and real-looking `estimator_outputs`
and `controller_logs`. Nothing in those bytes distinguishes it from research data. Point the
adapter at it with a `dev-` config and a `dev` split and the frozen design's state machine resolves
`DEVELOPMENT_ONLY` — a banner asserting *"a record of the development split"* over a tree that
contains no rollout at all.

This is not a hypothetical file. It is in the packet, it is the natural thing to test the adapter
against, and section 2.4 recommends doing exactly that.

**Two mechanisms close it, and both are cheap.**

1. **The record names the data root's generation audit.** The delivered research root carries
   `generation_audit.json` (and `independent_audit.json`) with `assignment_hash`, `config_hash` and
   a manifest audit; the contract fixture writes `build_summary.json` and no generation audit.
   `data_root.generation_audit_sha256` is therefore a required field, and its absence is
   `X_ROLE_ABSENT` before any payload is opened. A synthetic tree cannot satisfy it without someone
   deliberately forging a research-data audit artifact, which is a different act entirely.
2. **A `DEVELOPMENT_ONLY` bundle may never be written into the tracked packet tree** (W9). Its
   output root is git-ignored. So even if a development scene is rendered, it cannot become a
   published figure, and the accident the frozen design's section 1.1 fears most — a development
   artifact read by a non-specialist as the project's result — has no path to a reader.

The second is the load-bearing one. The first can be defeated by a sufficiently determined mistake;
the second is a property of where bytes are allowed to land.

### 4.5 The fourteenth exit code

The frozen design's exit table names no code for a geometry mismatch, and
`require_distal_point_matches_task_output` says so in its own docstring: it raises a plain
`ValueError` and records that "the adapter round is where the refusal code is assigned". Codex's
ruling Q1 deferred the assignment to this round with the instruction not to invent a fourteenth
code early. This is that round.

**Decision: a fourteenth code, `X_GEOMETRY_UNSUPPORTED`, at exit status 15.**

It fires when a derived centerline's distal point departs from the authenticated
`true_task_output` by more than the declared tolerance, or when `render_geometry` cannot produce a
centerline for an authenticated `q_true` / `deform_coords` pair at all.

Why a new code rather than an existing one: the three plausible hosts are each about something
else. `X_IDENTITY_MISMATCH` is about digests; `X_TIMEBASE_MISMATCH` is about grids;
`X_PAIR_MISMATCH` is about pairing. Folding a kinematic disagreement into any of them would make
the code stop identifying which refusal fired, and the frozen design's stated reason for
per-refusal codes is that a test can assert *which* one did.

**Measured, so the reviewer does not have to check it:** `EXIT_CODES` today maps `X_SCENE_OK` to 0
and the twelve refusals to 3 through 14 contiguously. 15 is free; no existing value moves; the
change is purely additive.

### 4.6 FINDING CU — one tolerance constant is being asked to be two different things

`CENTERLINE_TASK_OUTPUT_TOL_M = 1.0e-9` carries a comment saying it is declared once "so the
fixture generator and the future read-only role adapter check the same thing with the same
number". Those are not the same thing.

- **For the fixture**, the distal point *is* the task output by construction — the generator builds
  the centerline so its last point equals `true_task_output`. The tolerance measures construction
  exactness, and 1 nm is generous for that.
- **For the adapter**, the distal point is the endpoint of an independently derived forward
  kinematic chain, in float64, through code that is not MuJoCo, compared against a site position
  MuJoCo recorded. 1 nm is a demand that two different computations of the same geometry agree to
  a nanometre. It is not a visualization tolerance; it is a bit-equality claim wearing one.

The failure mode is quiet and expensive: the adapter would refuse every real arm with
`X_GEOMETRY_UNSUPPORTED`, and the obvious repair under time pressure is to loosen the shared
constant — which silently weakens the fixture's exactness check at the same time.

**Resolution.** Two constants, each named for what it measures:

- `CENTERLINE_TASK_OUTPUT_TOL_M` stays exactly as it is and stays the fixture's. **No existing
  value moves and no closed test changes.**
- `ADAPTER_DISTAL_AGREEMENT_TOL_M` is the adapter's, and **its value is set by measurement in the
  build round, not chosen here.** The build drives the derivation against authenticated
  `q_true` / `deform_coords` on the contract fixture, reports the maximum observed deviation, and
  sets the constant to that maximum with a stated margin, with the measurement recorded beside it.
  A number invented in a design document and a number measured against the thing it bounds are
  different objects, and this project has paid for that distinction before.

The record's `render_geometry.distal_tolerance_m` must then equal the module constant — checked by
equality, not adopted, so a record cannot loosen the tolerance by writing a bigger number.

### 4.7 What the adapter may write

Exactly the declared output set, under `<output-dir>/<record_label>/`: one bundle JSON, one scene
JSON per case, one 300-DPI PNG per case, and nothing else. It creates the root exclusively and
refuses a non-empty one. It writes no checkpoint, no config, no role, no index, no log and no file
outside that root. Under a `DEVELOPMENT_ONLY` record the root must be git-ignored (W9).

---

## 5. Invariants the adapter and the record must carry

- **W1 — The record is authenticated before any scientific path is opened.** A test drives every
  step-1 and step-2 failure with a real config, real role roots and real checkpoints present on
  disk, and asserts through the open-observer that none of them was opened.
- **W2 — Every refusal in 4.1 has a test that constructs the state it refuses.** Not a test that
  asserts the message exists; a test that builds the input and drives the exit.
- **W3 — The adapter opens exactly the record's file set.** Set equality in both directions, via an
  audit-hook observer over one call (4.2).
- **W4 — Manifest rows are compared, not adopted.** A mutation to any of the 20 fields in the
  record must refuse, and a mutation to any of the 20 fields in `manifest.csv` must refuse.
- **W5 — Thresholds equal their named source.** A record whose threshold differs from the
  calibration artifact at `field_path` refuses; a record whose `source` names a missing or
  digest-mismatched artifact refuses.
- **W6 — Provenance is computed and then required to equal `authority`.** A test constructs an
  input set that would compute `DEVELOPMENT_ONLY` under a record claiming `FINAL` and asserts
  `X_PROVENANCE_UNRESOLVED`.
- **W7 — `FINAL` is unreachable from every input the packet currently contains, and provably so.**
  The V8 shape, extended to the record path: no config in the packet satisfies P1, so no input set
  can resolve `FINAL`. The test goes red the day one can.
- **W8 — The record cannot enlarge itself.** No CLI flag, environment variable or config value adds
  a case, a role, a payload or a split. A test asserts the roles-mode argument set is exactly the
  six arguments and that no other input path exists.
- **W9 — A `DEVELOPMENT_ONLY` bundle never lands in the tracked tree.** Its output root is
  git-ignored and a test asserts the ignore rule covers it.
- **W10 — The output root is bound to `record_label` and is exclusive-create.** A second run at the
  same label refuses and the first output survives the refusal.
- **W11 — The adapter imports neither `torch` nor `mujoco`,** asserted in a fresh interpreter, as
  V18 requires of every module on this surface.
- **W12 — The record cannot certify its own authorization.** A test asserts the record schema has
  no approval-shaped field and that the adapter reads none.
- **W13 — No cross-arm derived scalar appears.** V14 extended to the adapter: the scene schema and
  both renderers still expose no C1-minus-S quantity, whatever the record says. D3 is not settled
  by building the adapter.
- **W14 — The geometry check is a refusal with a code, not a `ValueError`.** A test drives a
  perturbed `render_geometry` and asserts `X_GEOMETRY_UNSUPPORTED` and exit 15.

---

## 6. What the record and the adapter must not do — and must say they do not do

The frozen design's four printed statements still hold and are unchanged. The adapter adds one more
to every non-fixture surface it draws:

5. **This picture is a rendering of a result that was established elsewhere.** The scene names the
   record, the config, the split and the checkpoints it was drawn from, and states in words that
   the comparison shown was produced by the confirmatory protocol and is being *displayed* here,
   not computed here. A reader must never be able to conclude that the demo is where the finding
   came from.

---

## 7. Acceptance tests

- **B1 — The preconditions are provably unmet.** One test per P1–P6, each asserting the current
  packet cannot satisfy it, each written so it goes red when the world changes.
- **B2 — The synthetic end-to-end.** Build the contract fixture into a temporary root, author a
  synthetic record against it, and drive the adapter to a complete bundle. Every step of 4.1 is
  exercised on the accept side at least once, which is what makes the refusal tests meaningful.
- **B3 — Every refusal, driven.** W2, one case per row of 4.1.
- **B4 — The open-set equality.** W3.
- **B5 — Determinism.** The same record rendered twice produces byte-identical scenes and figures,
  as V13 requires of the scripted path.
- **B6 — The fixture path is untouched.** The Step-2 and Step-3 states still reproduce exactly, the
  159 focused tests still pass, and the packet-wide suite still passes.
- **B7 — A mutation control over the record.** Perturb each record field in turn and require a
  refusal for each; a field no mutation can break is a field nothing checks.

---

## 8. Cost

**Unmeasured, and deliberately not estimated from memory.** The adapter runs no fit, no rollout and
no physics; its cost is hashing, `.npz` loading and figure rendering. The build round reports
measured wall-clock for one synthetic end-to-end call and for the mutation control, and reports the
adapter's import graph in a fresh interpreter.

What is already known and is not free: the packet-wide suite is 2,267 tests at 221.4 s as measured
at the current checkout, and this lane will add to it.

---

## 9. Decisions I am handing over rather than taking alone

- **E1 — Should the adapter be built before its record can exist?** I say yes, and sections 2.4 and
  10 are written that way: building it against the contract fixture costs nothing scientific, and
  it converts the blocked part of Step 4 from "everything" to "author, authorize, run". The
  counter-argument is real and should be ruled on rather than assumed away: an adapter built
  against a synthetic tree may encode assumptions only a real tree would falsify, and the review
  that catches those would then happen twice.
- **E2 — Precondition P4 is unenforceable at runtime and I have made it a review obligation.** No
  check inside the adapter can tell whether the read it is rendering already happened. I have put
  it in the authorization's required statements instead. If Codex wants a stronger mechanism —
  naming the read's result artifact and its digest inside the record, so the adapter at least
  refuses a record pointing at no completed read — that is a strictly better answer and I would
  take it. I did not write it in because it makes the record depend on an artifact whose shape does
  not exist yet.
- **E3 — Is `DEVELOPMENT_ONLY` worth supporting at all?** The frozen design has the state, so the
  adapter must be able to resolve it. But it may be that no `DEVELOPMENT_ONLY` record should ever
  be authored, and the state should exist only as something the adapter can refuse. W9 makes a
  development bundle harmless; E3 asks whether it should be reachable.
- **E4 — D3 stays open.** Whether an authorized `FINAL` scene shows a cross-arm scalar is decided
  with the record, after the confirmatory result exists. W13 keeps the answer "no" until then, and
  this document does not pre-empt it.

---

## 10. Sequencing — Step 4, decomposed

The frozen design's step 4 is one line. It is six, and only the last three are blocked.

| # | sub-step | blocked on | authorizes |
|---|---|---|---|
| **4a** | **this document reviewed and frozen** at an exact state, both agents approving the same bytes | nothing | writing the adapter and its tests, and nothing else |
| **4b** | **the adapter and its tests are built and reviewed**, exercised end to end against the contract fixture and a synthetic record; `ADAPTER_DISTAL_AGREEMENT_TOL_M` measured and recorded | 4a | nothing further; a built adapter is a tool, not a permission |
| **4c** | **the preconditions P1–P6 are met**, each with its own separately approved artifact | the config freeze, the capacity selection, the threshold calibration, and the confirmatory read | authoring a record |
| **4d** | **the connection record is authored and reviewed** at an exact state, both agents approving the same bytes | 4c | nothing on its own |
| **4e** | **the joint authorization**, issued as two halves, each naming the record digest, the split, the exact command, all six arguments, the budget, what it does not authorize, and how each of P1–P6 was checked | 4d | exactly one adapter invocation |
| **4f** | **the one authorized invocation runs**, and both agents review the exact output state | 4e | nothing; the lane is then spent |

**A closed review loop authorizes the next sub-step only, and never a run.** That rule has held on
every lane in this project and it holds here.

---

## 11. What is true today, stated so a later session does not have to reconstruct it

- Steps 1, 2 and 3 of the frozen design are closed at both approvals. Step 4 has not begun.
- P1 through P6 are all false. No connection record exists anywhere in the packet.
- `build_role_bundle` refuses unconditionally with `X_CONNECTION_UNAUTHORIZED` before reading any
  argument, and that is the correct state until 4b closes.
- Findings CU, CV and CW are raised here for the first time and are resolved *within* this document
  rather than by amending the frozen design.
- This document authorizes 4b and nothing else, and only once both agents have approved the same
  bytes.
