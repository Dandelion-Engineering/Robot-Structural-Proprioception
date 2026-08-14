# The Slot-8 Connection Record — Contract, Adapter and Authorization — v0.1

**Author:** Claude (Session 131). **Reviewer:** Codex. **Status: REVIEWER-REPAIRED AFTER SECOND OWNER
RE-REVIEW AND CODEX APPROVED. Claude's approval names the preceding bytes; owner re-review of these
exact bytes is required. Finding CZ and the branch-B ruling on CY stand, finding CX stays accepted,
and findings DA and DB are accepted in substance. Finding DC (section 9.4) repairs the one remaining
test-contract gap created by DA without changing any of those rulings.**

> **THIS DOCUMENT AUTHORIZES NO SCIENTIFIC READ OR RUN.** Once both agents approve the same exact
> bytes, section 10.4a licenses only the synthetic adapter-and-test build in 4b. It does not license
> authoring a production connection record, running the adapter against real roles, opening a
> real-data config, checkpoint, role index, role payload or split, selecting a capacity or threshold, or
> making any C1-versus-S statement. Writing it is not authorization. Section 10 says where each
> later authorization lives and what it costs.

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
*forward*, here, under a named finding — sections 3.5, 4.4, 4.6 and 9.3. The frozen v0.1 is never
edited in place; a correction to it would bump its version and `git mv`, and none of those four
forward corrections needs that, because each is resolved by a decision this round is entitled to
take. The fourth did not exist before this round: the finding-CY ruling makes a disagreement
*internal* to the frozen design operative, and section 9.3 records which of its two statements
governs.

---

## 1. What this document is for

### 1.1 The one sentence

A connection record is **a reviewed JSON data object that names every scientific file the Slot-8
role adapter is permitted to open, and every identity it must find inside them.** The adapter
authenticates what the record names. It discovers nothing, defaults nothing, widens nothing, and
opens nothing the record does not name.

**Approval of the record's exact bytes establishes the record state eligible for a later
authorization; it is not itself executable authorization.** The two separately recorded halves in
section 10.4e authorize one exact invocation. The digest passed on the command line is only how the
runtime knows which reviewed bytes it was handed. A digest match is a statement about bytes; it is
never a statement about social approval, and the record must not contain a field that claims
otherwise (property R5, section 3.3).

### 1.2 The two design tests this document is written against

The first is inherited from the frozen design's section 1.2 and still binds:

> **When the scientific inputs finally exist, connecting them must be an authenticated data change
> and a separate authorization — not a rewrite of the scene schema or either renderer.**

The second is added here, and it is the one this document exists to make structural:

> **No path through the connection record may discover a scientific result or open scientific
> role bytes without a separate authorization for that exact read.** The result must already have
> been established under its own authorization, and the later rendering read must receive the
> distinct two-half authorization in section 10.4e. The verification artifact *presents* a result.
> It is never the occasion of one.

The reason is worth stating plainly, because it is the failure this whole lane is shaped to
prevent. Slot 8 is a presentation commitment. If the adapter's first authorized run were also the
first time anyone on this team looked at a split, then the demo would have quietly become the
experiment, and every safeguard the project spends its sessions maintaining — pre-registration,
exclusive-create destinations, one-shot authorizations, the untouched `test` split — would have
been routed around by a picture. A later adapter invocation still opens scientific bytes and is
not made free merely because an earlier read occurred. Section 2.2 binds it to the
already-established result, and section 10.4e separately authorizes that exact rendering read.

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
one-shot confirmatory look, taken for the purpose of drawing a picture.

The record therefore names the exact already-established result artifact and the field paths that
bind its split, config, cases and run identities. The adapter hashes and strict-parses that artifact
before opening a role payload, and requires the record's facts to equal it. That mechanism proves
that the rendering is attached to an existing result rather than to a future hope; it cannot prove
that the social read was authorized or closed. The two section-10.4e halves must still name the
transcript turn that closed the earlier result read and must separately authorize the adapter's own
role re-open. A previous read does not make a later file access cease to be a read.

There is deliberately no third authority case. `DEVELOPMENT_ONLY` names `dev`; `FINAL` names the
approved final split. A record naming a result whose read has not closed is refused in review, and
a record pointing at no digest-stable result artifact refuses at runtime. See W12 and E2.

### 2.3 The precondition ledger

A connection record may be authored only when every one of these is true, and the joint
authorization in section 10 must state each one and how it was checked:

| # | precondition | how it is checked |
|---|---|---|
| **P1** | the exact authority-appropriate config bytes exist and are approved: `DEVELOPMENT_ONLY` requires a versioned draft file not named `config.json`, `status = draft`, `confirmatory_payloads_allowed = false` and a `dev-` `config_hash`; `FINAL` requires frozen `config.json`, `decision = APPROVE_CONFIG_FREEZE` and no `dev-` string anywhere | `utils.config_contract.load_config(require_frozen=False)` plus the explicit draft branch for development; `load_config(require_frozen=True)` for final; record equality binds the path, bytes and `config_hash`, while exact-state social approval remains a 4c/4d/4e review obligation |
| **P2** | `values.models` is non-null and names the selected rung and width; the selecting artifact exists and is jointly approved | equality against the approved selection artifact's own fields |
| **P3** | `values.calibration` is non-null and carries the abstain and unknown thresholds; the calibrating artifact exists, is jointly approved, and was produced on validation | equality against that artifact, plus its recorded split |
| **P4** | the result being rendered has already been produced **and read** under its own authorization, that read is reported, and the result artifact exists | transcript closure named by session and digest in 4e; runtime hash and field equality against `established_result` |
| **P5** | the role tree for the named split exists, carries the generation and independent audits, and contains every named non-observation role index and payload | strict semantic audit checks plus the per-arm index/payload checks in 4.1 |
| **P6** | the established-result artifact enumerates every menu case as a real C1/S pair and the record echoes those exact case/run identities | equality against `established_result`, then both manifest rows and all four per-arm roles |

**Final P1 and P2 through P5 are false today; no complete `DEVELOPMENT_ONLY` precondition set exists
either.** The current draft can be machine-validated as a draft, but `values.models` and
`values.calibration` are null, no approved established result selects this surface's cases, and
the downstream roles do not exist. This document neither claims nor grants exact-state approval of
that draft for a connection record. P6 is not an independent absent-world fact: the delivered base
manifest already contains 472 complete C1/S pairs (152 `dev`, 152 `pilot`, 168 `val`), so a test
claiming that no pair exists would be false. What is absent is the approved result artifact that
selects menu cases and the downstream role completion that makes those pairs renderable. Section
7's B1 proves the current connection path unreachable from those actual missing predicates, while
the future record review checks P6 against its concrete proposed cases.

**P1 is authority-scoped by finding CY in section 9.2.** That decision is made here, before 4b,
because the adapter's config-validation branch and its accept/refusal tests must implement one
answer. B8 makes the positive side of both authority branches measurable rather than relying on
refusal coverage alone.

### 2.4 What is unblocked today — and it is not nothing

Step 4 has been carried as a single blocked item. It is not one. The existing
`build_data_contract_fixture.py` can drive storage, manifest, index and refusal plumbing without a
research read. It cannot serve as the geometry oracle Claude's first draft assigned to it:
`synthetic_privileged_record` generates `deform_coords` independently of the `curvature_true` used
to generate `true_task_output`. A direct reconstruction probe at the delivered fixture settings
misses that output by 2.81–6.20 mm, not by floating-point noise. Treating that maximum as a real
adapter tolerance would make the distal check meaningless.

Sub-step 4b may therefore build the adapter now, but it must add a **dedicated deterministic
adapter fixture** whose `q_true`, `deform_coords`, centerline and `true_task_output` are generated
from one dependency-light forward map. That fixture reaches the assembly core only under
`SYNTHETIC_FIXTURE`; the public `roles` CLI continues to accept only reviewed
`DEVELOPMENT_ONLY`/`FINAL` records. The existing contract fixture still drives the storage and
refusal seams. No real tolerance is chosen in 4b: its value and source are later bound by the
approved geometry-validation artifact named in the record. Thus the implementation and its
synthetic accept path are buildable now, while real record authoring, real-data tolerance binding,
authorization and invocation remain blocked.

That is why section 10 splits Step 4 into six sub-steps rather than treating it as one gate, and it
is the concrete reason this document is worth writing before its preconditions exist: the frozen
design's step 4 reads as "wait". Sub-steps 4a and 4b are buildable; 4c through 4f are blocked.

---

## 3. The connection record

### 3.1 Location, identity and canonical form

| property | rule | why |
|---|---|---|
| path | `Reproducibility Packet/results/verification_connection/records/<record_label>/connection_record.json`, tracked | records live *beside* the bundles they name — two sibling subtrees of one parent, never nested; the label binds both, as `run_label` does on the capacity lane. **The nesting is what section 4.8 refuses; do not collapse the two trees back together.** |
| identity | the SHA-256 of the exact file bytes, passed as `--connection-record-sha256` | the frozen design's 4.2; a path is not an identity |
| encoding | canonical JSON via `utils.protocol_p.canonical_json` — `sort_keys`, `(",",":")`, `allow_nan=False` — UTF-8, no BOM, no trailing newline | the packet's existing discipline; a reviewer must be able to diff two records |
| non-finite floats | **forbidden outright in a record**, unlike in a scene | a record is authored by a reviewed process, not derived from a run; a `NaN` threshold is a defect, not a contract-valid value |
| paths inside it | each path declares its root domain; no drive letters, rooted forms or `..` | packet artifacts are packet-relative; payload paths are `--role-root`-relative; checkpoints are `--checkpoint-root`-relative |
| line endings | LF, pinned by the packet `.gitattributes` `protocol/*.md` rule for this document and by a new `results/verification_connection/**/*.json` rule for the record itself | a Windows checkout must not move a byte the runtime hashes |

The root domains are not interchangeable. The delivered data lives at the machine-selected
`--role-root`, outside a copied packet; therefore `data_root.relative_path` from the owner draft is
removed rather than forcing a real data path to pretend it is packet-relative. The six closed CLI
arguments remain unchanged. `--config` must resolve to the packet-relative `config.relative_path`
and names the **authority-appropriate** config file rather than a necessarily frozen one — the
frozen design's 4.2 gloss "the exact frozen config file" describes the `FINAL` case only, per
section 9.3. Each role payload must resolve under `--role-root`; each checkpoint must resolve
under `--checkpoint-root`; every source/result artifact resolves inside the packet; and
`--output-dir` is constrained by authority as section 4.7 specifies.

### 3.2 The field table

Every field is required. There is no optional field and no default; an absent field is a refusal,
not an empty value.

| field | shape | what it names |
|---|---|---|
| `record_version` | `"slot8-connection-record-v0.1"` | the contract these bytes are written against |
| `record_label` | string, `[a-z0-9-]+` | binds the adapter's output root to `<output-dir>/<record_label>/` |
| `authority` | `"DEVELOPMENT_ONLY"` or `"FINAL"` | the provenance state the adapter may resolve to, and no other |
| `split` | one of `"dev"`, `"pilot"`, `"val"`, `"test"` | the exact split every named row must carry |
| `schema` | `{relative_path, sha256}` | the fixed packet schema used to validate the config and role contracts |
| `config` | `{relative_path, sha256, config_hash}` | the config file, its bytes, and its semantic identity |
| `data_root` | `{dataset_label, manifest_sha256, generation_audit, independent_audit}`; each audit is `{sha256,status,assignment_hash,config_hash}` | stable identity for the external `--role-root`; both audits are strict-parsed and their echoed fields checked — see 4.4 |
| `established_result` | `{artifact_relative_path,sha256,split_field_path,config_hash_field_path,cases_field_path}` | the already-produced and already-read result whose cases this surface presents |
| `analysis_window_s` | float > 0 | the `window_s` every scene carries into `utils.metrics.j_5s` |
| `thresholds` | `{abstain_threshold,unknown_threshold,sources}`; each source is `{artifact_relative_path,sha256,field_path}` | each threshold and its own approved validation source — see 3.4 |
| `model_selection` | `{rung,width,source}` where source is `{artifact_relative_path,sha256,rung_field_path,width_field_path}` | the capacity and the approved artifact that selected it |
| `render_geometry` | `{derivation_version,source,planar_convention,links,distal_tolerance_m,tolerance_source}` | the explicit dependency-light chain plus the approved geometry-validation source — see 3.5 and 4.6 |
| `render_geometry.source` | `{producer_relative_path,producer_sha256,model_id}` | the generated-model producer (`scripts/utils/cable_mechanics.py`), not a nonexistent static model file |
| `render_geometry.planar_convention` | `{base_xy_m,q_true_convention,rotation_vector_component,projection}` | origin, absolute/relative joint convention, log-map component and x/z projection |
| `render_geometry.links` | ordered `L1`,`L2` entries, each `{segment_lengths_m,deform_triplets}` | one segment length per body and the exact `deform_coords` triples in emitted order |
| `render_geometry.tolerance_source` | `{artifact_relative_path,sha256,maximum_deviation_field_path,tolerance_field_path}` | where the real-data agreement and allowed tolerance were established |
| `cases` | ordered array, at least one entry, unique `case_id` and unique `display_label` | the menu |
| `cases[i].case_id` | string | the bundle key |
| `cases[i].display_label` | string | what the director reads in the radio menu |
| `cases[i].pair_id` | string | the C1/S pairing this case is |
| `cases[i].arms.C1` / `.S` | `{run_id, manifest_row, checkpoint, roles}` | one arm |
| `…arms[k].manifest_row` | all 20 schema-A fields, echoed exactly | equality against `manifest.csv`, never adoption |
| `…arms[k].checkpoint` | `{relative_path, sha256}` | the fitted weights this arm's decisions came from |
| `…arms[k].roles` | `{plant, labels, estimator_outputs, controller_logs}`, each `{index_sha256,payload_relative_path,payload_sha256}` | the four non-observation roles, per arm; the path is role-root-relative and must equal the authenticated index row |

`cases` must jointly contain at least one `structure`, one `actuator` and one `sensor` case,
because the frozen design's section 4.1 requires that of every bundle and the adapter cannot
satisfy it from anything but the record.

### 3.3 Six load-bearing properties

1. **The record is an allowlist, not a hint.** Every scientific file the adapter opens is named in
   it by path and digest, including the packet schema, established result, capacity-selection
   source, two threshold sources, geometry source and geometry-validation source. Role indexes and
   payloads additionally name their root-relative paths. There is no directory scan, no glob, no
   "the rest of this role root", and no CLI flag that adds a file. W3 makes this measured rather
   than aspirational.
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
4. **`record_label` and `authority` bind the output root.** The adapter writes to
   `<output-dir>/<record_label>/` and nowhere else, refuses a non-empty destination, and requires
   the authority-specific parent from section 4.7. This is the Session-90 finding
   (limitation 138) applied on this lane: without it, two runs at one label write into two
   unrelated directories and the audit claim has no mechanism behind it.
5. **The record does not record its own approval.** No `approved_by`, no `approval_session`, no
   `authorized` boolean. A document cannot authenticate the approval of itself, and a field that
   looks like it does is worse than no field, because a reader will believe it. This is Codex's
   Session-62 circular-provenance edit applied on a second lane. Review approval and the later
   executable authorization live in the transcript and name the record's digest; the record names
   only facts a runtime can measure.
6. **One record, one split, one authority.** No record spans two splits or mixes a development arm
   with a final one. A scene that mixed them would carry one banner over two provenances, which is
   the failure mode the banner exists to prevent.

### 3.4 Thresholds must carry their provenance, and this is not bookkeeping

`thresholds.sources` has separate `abstain_threshold` and `unknown_threshold` entries, each
`{artifact_relative_path, sha256, field_path}`. They may name the same artifact, but they cannot
share one ambiguous field path. The adapter hashes and strict-parses every distinct artifact and
requires each number to equal its named field.

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
is therefore a property of the generated MuJoCo model, not of the config; `schema.json` says as much,
declaring `deform_coords` with unit `model_defined` and shape `[T, n_def]` at `n_def = 90`.

There is **no static model file** in this packet. `cable_mechanics.model_xml` constructs the MJCF
string in memory. The owner draft's proposed `render_geometry.model_file` would therefore require a
record to name an object that does not exist.

**Why the two statements cannot both stand.** Reconstructing a centerline needs the chain order
and the per-body segment lengths. Those live in the model. Reading them at runtime means importing
`mujoco` into the adapter — and **V18 forbids exactly that**, in terms, and gives the reason: the
Slot-8 surface must be openable by a reader who installed the packet on a laptop.

**Resolution, and it does not require amending the frozen design.** Section 4.2 already put render
geometry in the record; property 6's "config geometry" is the loose phrase. This document resolves
in favour of 4.2:

- `render_geometry.source` names and hashes the actual producer,
  `scripts/utils/cable_mechanics.py`, and echoes the config's `model_id`. The adapter hashes that
  source and never imports it, preserving V18 without inventing a static MJCF artifact.
- `planar_convention` states the base point, that `q_true[0]` is the first L1 body's absolute
  tangent orientation and `q_true[1]` is the first L2 body's orientation relative to the distal L1
  tangent, which rotation-vector component advances the planar tangent, and how model x/z becomes
  scene x/y.
- `links` states the chain explicitly: one segment length per ordered body and the exact
  `deform_coords` triplet assigned to each internal body, in the same link/body order
  `extract_deformation_coordinates` emits them.
- `render_geometry.derivation_version` names the derivation the adapter implements, so a change to
  it is a visible version change rather than a silent difference between two figures.
- The geometry is checked, not trusted: the derived distal point must agree with the authenticated
  `true_task_output`. The allowed tolerance is not invented in the record or measured on the
  incoherent contract fixture; it equals the named, approved geometry-validation artifact under
  section 4.6.

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
| 3 | validate root domains without opening them: bind `schema`, `--config` and every source/result artifact to their packet-relative paths; bind every checkpoint/payload path under its CLI root; require `--role-root` basename = `dataset_label`; enforce the authority-specific output parent; check the fixed authority/split policy | `X_IDENTITY_MISMATCH`, `X_SPLIT_FORBIDDEN`, or `X_PROVENANCE_UNRESOLVED` |
| 4 | hash `schema` and `--config` before parsing either; compare both digests; load the config through the authenticated schema; compare `config_hash`; check the `dev-`/frozen rule against `authority` | `X_IDENTITY_MISMATCH`, then `X_PROVENANCE_UNRESOLVED` |
| 5 | hash and strict-parse `established_result`, the model-selection artifact, both threshold-source artifacts, the geometry producer and the geometry-validation artifact; resolve every declared field path and require equality | `X_IDENTITY_MISMATCH` |
| 6 | hash and strict-parse `manifest.csv`, `generation_audit.json` and `independent_audit.json`; compare all digests; require both audit status/config/assignment echoes, their manifest census, and `established_result`'s split/config/case/run identities to agree | `X_IDENTITY_MISMATCH` or `X_SPLIT_FORBIDDEN` |
| 7 | require each named role root and `index.csv` to exist at the schema-E layout | `X_ROLE_ABSENT` |
| 8 | hash **every named role index before parsing any of them** and compare to the record | `X_IDENTITY_MISMATCH` |
| 9 | parse the now-authenticated indexes; require every named run and exact `payload_relative_path` to be present, and plan no other payload open | `X_ROLE_UNAUTHORIZED` or `X_IDENTITY_MISMATCH` |
| 10 | require every named manifest row to equal the record's 20-field echo and `record.split` | `X_IDENTITY_MISMATCH` or `X_SPLIT_FORBIDDEN` |
| 11 | hash every named payload and checkpoint before loading any payload; compare to the record and to the authenticated index row | `X_IDENTITY_MISMATCH` |
| 12 | load exactly the authenticated payload set through `RolePayloadLoader`; require its schema and semantic checks to pass | `X_IDENTITY_MISMATCH` |
| 13 | require both arms present for every case, and exactly two | `X_ARMS_INCOMPLETE` |
| 14 | require the C1/S pair, case identity, onset, `task_reference` and label fields to agree | `X_PAIR_MISMATCH` |
| 15 | require both arms' `plant.t_s`, body and tracking leading axes to bind to one `playback_t_s`, and both `controller_logs.step` to be the contiguous 0-based grid of length `T` | `X_TIMEBASE_MISMATCH` |
| 16 | require decisions strictly increasing and inside the playback extent | `X_DECISION_UNSUPPORTED` |
| 17 | establish the tracking window by **calling** `utils.metrics.j_5s` and re-raising any refusal | `X_WINDOW_UNSUPPORTED` |
| 18 | derive each arm's centerline from `q_true`, `deform_coords` and `render_geometry`; require the declared tolerance to equal its authenticated source; check the distal point against `true_task_output` | `X_GEOMETRY_UNSUPPORTED` (new; see 4.5) |
| 19 | require the computed provenance state to equal `authority` | `X_PROVENANCE_UNRESOLVED` |
| 20 | require the bundle cases and run identities to equal `established_result`, and every surface to expose every case | `X_BUNDLE_INCOMPLETE` |
| 21 | exclusively create `<output-dir>/<record_label>/` and write the declared set | `X_SCENE_OK`, exit 0 |

Steps 1 and 2 are the first boundary: **the record is authenticated before any scientific path is
opened, and its own authentication needs nothing but the record file itself.** Steps 4, 5, 6, 8
and 11 are the second: a schema, artifact, audit, index or payload is hashed before it is parsed or
loaded.
The owner draft parsed role indexes at step 6 and authenticated them only at step 10; that order
would have opened scientific index bytes before their identity was established. This table is the
corrected normative order.

### 4.2 The allowlist rule, stated so it can be tested

**The adapter opens exactly the declared set and no others.** Concretely: the record; the fixed
packet schema bound by the config; the config; established-result, model-selection, threshold,
geometry-producer and geometry-validation artifacts; `manifest.csv`; both dataset audits; every
named role `index.csv`; and exactly the `.npz` payloads and `.pt` checkpoints the per-arm blocks
name. The expected set is derived from the record only after step 2 validates every path domain.

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

This is not a hypothetical producer. It is in the packet and is the natural storage fixture for
the adapter build. It must not be allowed to acquire research provenance merely by having a
reviewer-computed digest added beside it.

**Four mechanisms close it, each covering a different boundary.**

1. **The record names both dataset audits and their semantic fields.** The delivered research root
   carries `generation_audit.json` and `independent_audit.json`; the contract fixture carries only
   `build_summary.json`. The adapter hashes and strict-parses both audits. It requires each echoed
   `status` to equal the record, both `assignment_hash` and `config_hash` values to equal the record
   and each other, and both manifest/split censuses to equal a census recomputed from the manifest.
   A digest alone proves only that one nominated file was stable; it does not prove that the file
   says research data were generated.
2. **The record names the already-established result.** Its menu case and run identities must
   equal the exact result artifact that was read and closed before rendering. A schema-valid tree
   with invented estimator rows has no such artifact.
3. **The synthetic accept path remains synthetic.** The dedicated adapter fixture from 2.4 enters
   the assembly core as `SYNTHETIC_FIXTURE`; it does not create a production connection record and
   the public `roles` CLI does not accept a synthetic authority.
4. **A development output has one mechanically fixed scratch parent.** Under
   `DEVELOPMENT_ONLY`, `--output-dir` must equal
   `results/verification_connection_development`, and that exact tree is added to the packet
   `.gitignore`; any other destination refuses. This prevents accidental tracking. It is not
   described as making deliberate publication impossible — Git ignore rules are not an access
   control system.

The audit/result binding establishes provenance; the output rule limits accidental publication.
Neither substitutes for the other or for the transcript authorization.

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

**Resolution.** Separate the fixture check from the later measured real-geometry check:

- `CENTERLINE_TASK_OUTPUT_TOL_M` stays exactly as it is and stays the fixture's. **No existing
  value moves and no closed test changes.**
- The production adapter has no guessed universal tolerance. The existing contract fixture cannot
  set it because its `deform_coords` and `true_task_output` come from independent synthetic maps.
  A separately approved geometry-validation artifact later records the maximum real agreement
  deviation, the declared margin rule and the resulting tolerance without changing a role payload.
- `render_geometry.distal_tolerance_m` must equal that artifact's named tolerance field, and the
  adapter also reads the artifact's maximum-deviation field and requires it not to exceed the
  tolerance. The exact record review can reject an unjustified margin; the runtime prevents a
  different number from travelling under those approved bytes.

The dedicated coherent adapter fixture in 2.4 carries its own synthetic exactness oracle and proves
the derivation logic now. It does not manufacture the future real-data tolerance.

### 4.7 What the adapter may write

Exactly the declared output set, under `<output-dir>/<record_label>/`: one bundle JSON, one scene
JSON per case, one 300-DPI PNG per case, and nothing else. It creates the root exclusively and
refuses a non-empty one. It writes no checkpoint, no config, no role, no index, no log and no file
outside that root. For `DEVELOPMENT_ONLY`, `--output-dir` must be exactly
`results/verification_connection_development`, a tree added to the packet `.gitignore` in 4b. For
`FINAL`, it must be exactly `results/verification_connection/bundles`, the tracked publication
root. The record label remains the exclusive-created child in both cases (W9, W10).

### 4.8 FINDING CX — the record may not live inside the tree the adapter exclusively creates

**The state this repairs.** The reviewer-repaired 4.7 pinned the `FINAL` output parent to
`results/verification_connection`, while 3.1 puts the record at
`results/verification_connection/<record_label>/connection_record.json`. Step 21 then exclusively
creates `<output-dir>/<record_label>/` and 4.7 refuses a non-empty root. Those are the same
directory, and it is non-empty before the adapter starts, because the record has to exist and be
reviewed at 4d before the authorization at 4e can name its digest. **Under those rules a `FINAL`
invocation could never have reached exit 0.**

Two properties make this worse than an ordinary typo, and they are why it is written up rather than
quietly fixed:

- **It is `FINAL`-only.** `DEVELOPMENT_ONLY` writes to a different parent and does not collide, and
  the 4b accept path is `SYNTHETIC_FIXTURE` and writes to a temporary root. So the whole of 4b, and
  a development rehearsal too, would pass while the one authority that publishes was unreachable.
- **It would surface at 4f.** That is after the two authorization halves are spent on a one-shot
  invocation, which is the most expensive place in the lane to discover it.

This is the shape findings AU and AV had — an executable that could not have completed the thing it
exists to do, discovered only by asking what the accept path actually reaches. That it appeared
twice before is the reason this document asks the question of its own accept path.

**Resolution.** The record tree and the bundle tree become siblings under one parent:
`results/verification_connection/records/<record_label>/connection_record.json` for the record and
`results/verification_connection/bundles/<record_label>/` for the bundle. The exclusive create is
untouched, the label still binds both, the `.gitattributes` rule in 3.1 (`**/*.json` under the
parent) still covers the record, and the `FINAL` parent stays a single mechanically fixed
destination, which is the property the reviewer's edit was for.

---

## 5. Invariants the adapter and the record must carry

- **W1 — Authentication precedes interpretation at every layer.** The record is hashed before it
  is parsed; each schema/source/result/audit/index/payload/checkpoint is hashed before it is parsed
  or loaded. Tests drive the ordering failures with later files present and assert the open
  sequence, not merely the final refusal.
- **W2 — Every refusal in 4.1 has a test that constructs the state it refuses.** Not a test that
  asserts the message exists; a test that builds the input and drives the exit.
- **W3 — The adapter opens exactly the declared file set.** Set equality in both directions,
  including the packet schema and every source/result/audit file, via an audit-hook observer over
  one call (4.2).
- **W4 — Manifest rows are compared, not adopted.** A mutation to any of the 20 fields in the
  record must refuse, and a mutation to any of the 20 fields in `manifest.csv` must refuse.
- **W5 — Every typed scientific choice equals its named source.** Both thresholds, rung, width,
  result cases/run identities and geometry tolerance are checked at their declared field paths. A
  missing source, digest mismatch, absent field or unequal value refuses.
- **W6 — Provenance is computed and then required to equal `authority`.** It includes strict
  semantic agreement among both dataset audits, the manifest, config and established result. A
  test constructs an input set that would compute `DEVELOPMENT_ONLY` under a record claiming
  `FINAL` and asserts `X_PROVENANCE_UNRESOLVED`.
- **W7 — Production `DEVELOPMENT_ONLY` and `FINAL` are unreachable from every input the packet
  currently contains.** No reviewed production record exists; no frozen config satisfies final
  P1; the current draft has null model and calibration fields and therefore cannot complete P2 or
  P3; and the downstream roles and established-result selection are absent. The dedicated 4b
  accept fixture reaches only the private synthetic assembly seam, never the public roles CLI.
  The test goes red when a production connection becomes reachable.
- **W8 — The record cannot enlarge itself.** No CLI flag, environment variable or config value adds
  a case, a role, a payload or a split. A test asserts the roles-mode argument set is exactly the
  six arguments and that no other input path exists.
- **W9 — A `DEVELOPMENT_ONLY` bundle cannot accidentally target the tracked publication tree.**
  The CLI requires its exact scratch parent, the packet ignore rule covers that parent, and a test
  drives every other project-relative destination to refusal.
- **W10 — The output root is bound to `record_label` and is exclusive-create.** A second run at the
  same label refuses and the first output survives the refusal. **A test asserts the record's own
  tree is not inside the output parent under either authority** — that is finding CX, and the
  exclusive create is what makes the nesting fatal rather than untidy.
- **W11 — The adapter imports neither `torch` nor `mujoco`,** asserted in a fresh interpreter, as
  V18 requires of every module on this surface.
- **W12 — The record cannot certify its own authorization.** A test asserts the record schema has
  no approval-shaped field and that the adapter reads none. Separate tests pin that record review
  closes 4d without authorizing a run and that the two transcript halves in 4e are required by the
  exact command protocol.
- **W13 — No cross-arm derived scalar appears.** V14 extended to the adapter: the scene schema and
  both renderers still expose no C1-minus-S quantity, whatever the record says. D3 is not settled
  by building the adapter.
- **W14 — Geometry is coherent, sourced and fail-closed.** The dedicated synthetic adapter fixture
  derives its centerline and tip from one map; the production tolerance equals its authenticated
  validation artifact; a perturbed chain, source or tolerance refuses with
  `X_GEOMETRY_UNSUPPORTED` and exit 15 rather than a `ValueError`.

---

## 6. What the record and the adapter must not do — and must say they do not do

The frozen design's four printed statements still hold and are unchanged. The adapter adds one more
to every non-fixture surface it draws:

5. **This picture is a rendering of a result that was established elsewhere.** The scene names the
   established-result artifact and digest, the record, the config, the split and the checkpoints
   it was drawn from. It states whether the named prior read was development or final and says in
   words that the comparison was established by that named prior read and is being *displayed*
   here, not computed here. A reader must never be able to conclude that the demo is where the
   finding came from or that a development result was confirmatory.

---

## 7. Acceptance tests

- **B1 — The preconditions are provably unmet.** Drive the final P1 failure; drive the current
  draft through the development config validator and then prove that the current bytes cannot
  complete P2–P5; and test the absence of an established-result selection satisfying P6. Each test
  goes red when the world changes. The test must not claim that the packet lacks complete C1/S
  pairs: the delivered base manifest already contains 472 of them. **FINDING DB — P5 is proved the
  same way P6 is: from the packet's own bytes, never from the delivered tree.** No connection record
  exists, so no split, role root or payload identity is named and P5 has no referent to satisfy.
  The role root is a machine-selected external path, git-ignored and absent from a fresh checkout,
  and no test in the current suite depends on it existing — measured this session: the only
  occurrences of its name under `tests/` are string literals in `test_dev_fit_contract.py` used for
  name validation, not filesystem access. A test that proved P5 unmet by looking at that tree would
  be green on this machine, red on a fresh one, and would put the packet's own fresh-environment
  standard behind a 3.86 GB download.
- **B2 — The synthetic end-to-end.** Build the existing contract fixture into a temporary root to
  exercise storage, index, authentication and refusal plumbing. Separately build the dedicated
  coherent adapter fixture from 2.4 and drive the private `SYNTHETIC_FIXTURE` assembly seam to a
  complete bundle. No production connection record is authored, and only the coherent fixture is
  used as the geometry accept oracle. Every applicable step of 4.1 is exercised on the accept side
  at least once, which is what makes the refusal tests meaningful.
- **B3 — Every refusal, driven.** W2, one case per row of 4.1.
- **B4 — The open-set equality.** W3.
- **B5 — Determinism.** The same coherent synthetic fixture rendered twice produces byte-identical
  scenes and figures, as V13 requires of the scripted path. The production path reuses that same
  assembly and rendering code; 4b does not claim a second, unauthorized real-data render.
- **B6 — The fixture path is untouched.** The Step-2 and Step-3 states still reproduce exactly, the
  159 focused tests still pass, and the packet-wide suite still passes.
- **B7 — Mutation controls at the layers 4b can actually reach.** Perturb every generic record and
  authenticated-source field in the complete synthetic validation harness and require its owning
  validator to refuse. Drive every production-only provenance/result/tolerance field to its named
  refusal with a baseline that has passed all earlier validators. At 4d, repeat the control against
  the exact proposed production record; 4b does not claim that an unavailable production path has
  already accepted end to end. A field no mutation can break is a field nothing checks.
- **B8 — Both authority-scoped P1 branches cross their own step-4 gate.** In the temporary complete
  synthetic validation harness, an authenticated `DEVELOPMENT_ONLY` record plus versioned draft
  config must pass step 4 and then refuse only on a deliberately corrupted step-5 source; the same
  draft config under `FINAL` must refuse at step 4. A separately generated complete synthetic
  frozen config plus `FINAL` record must pass step 4 and reach the same later refusal; that frozen
  config under `DEVELOPMENT_ONLY` must refuse at step 4. These are validator-path tests over
  temporary synthetic documents, not a public production accept path or an authored production
  record. They make an unconditional `require_frozen=True` implementation impossible to pass.

---

## 8. Cost

**Unmeasured, and deliberately not estimated from memory.** The adapter runs no fit, no rollout and
no physics; its cost is hashing, `.npz` loading and figure rendering. The build round reports
measured wall-clock for one synthetic end-to-end call and for the mutation control, and reports the
adapter's import graph in a fresh interpreter.

What is already known and is not free: the packet-wide suite is **2,267 tests**, measured twice at
this checkout at **221.4 s** (Session 130) and **204.35 s** (Session 131), and this lane will add to
it. The count is the load-bearing figure; the two wall-clocks are the same suite on the same
machine and neither is *the* number. *(The first draft of this section quoted only 221.4 s in a
session that had itself measured 204.35 s — corrected here rather than left standing.)*

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

### 9.1 Codex reviewer rulings

- **E1 — Yes, with the split fixture boundary in 2.4.** Build the adapter now against the existing
  contract fixture for authenticated storage/refusal plumbing and the dedicated coherent fixture
  for geometry. Neither fixture may enter the public production authority path.
- **E2 — Use the stronger mechanism.** The record names the exact established-result artifact,
  digest and field paths; the adapter hashes, strict-parses and equality-checks them. That proves
  the rendered identities were established elsewhere. It does not prove the social read gate
  closed and does not authorize reopening the bytes; the two transcript halves in 4e do both.
- **E3 — Retain `DEVELOPMENT_ONLY` as a future authorable production state under the
  authority-scoped P1 in finding CY.** It requires an exact approved versioned draft config, a
  separately reviewed connection record and the later two-half authorization. The present accept
  path is `SYNTHETIC_FIXTURE`, not development, and this ruling authorizes no record or read.
- **E4 — D3 remains open and the adapter carries no cross-arm scalar.** A later exact-state record
  decision may add one only through a separately reviewed design change; this design does not.

### 9.2 FINDING CY — P1 and the `DEVELOPMENT_ONLY` entry condition cannot both stand as written

**Measured against the frozen design, which is the authority here.** Its section 4.3 provenance
table gives `DEVELOPMENT_ONLY` this entry condition, in terms:

> an exact approved development connection record authenticates the roles, **and the config is
> `dev-` and split is `dev`**

P1 in section 2.3 requires, of every record, a frozen `config.json` carrying
`decision = APPROVE_CONFIG_FREEZE` **and no `dev-` string anywhere**; section 10's 4c makes P1–P6
the precondition for authoring *any* record. A record satisfying P1 therefore cannot satisfy the
`DEVELOPMENT_ONLY` entry condition, and a record satisfying that condition cannot satisfy P1. The
reviewer's first E3 wording — "reachable only through an explicitly reviewed development record
after P1–P6 are satisfied" — names a path that P1 forecloses. One of the two has to move.

**Why it must be settled before 4b rather than bound to 4c.** The two branches produce different
executables. A refusal-only `DEVELOPMENT_ONLY` state requires the public roles path to reject an
otherwise authentic development record unconditionally; an authorable state requires that path to
accept the same record after the draft-config, provenance and record checks pass. The runtime
cannot infer the social rule "no development record should be authored" from a digest — and the
record deliberately contains no approval-shaped field. Therefore the claim that nothing in 4b
depends on the choice is false. Freezing the choice as open would license two incompatible config
branches and two incompatible acceptance suites.

**The two coherent branches, stated so the round that settles it does not re-derive them.**

**Resolution: branch B, authority-scoped P1.** For `DEVELOPMENT_ONLY`, the record names the exact
approved versioned draft config; `load_config(require_frozen=False)` must validate `status = draft`,
the filename must not be `config.json`, `confirmatory_payloads_allowed` must be false, and
`config_hash` must begin `dev-`. The record, `--config` path, file digest and semantic hash must all
agree, and the split must be `dev`. For `FINAL`, `load_config(require_frozen=True)` enforces frozen
`config.json`, `decision = APPROVE_CONFIG_FREEZE`, complete freeze-required paths and no `dev-`
string. In both branches, runtime authentication proves only the bytes and their semantics;
exact-state approval of the config, the record review and the two authorization halves remain
separate social gates in 4c–4e.

Branch A is rejected. It would leave the only real-data exercise until the one-shot final
invocation, make section 4.4's development destination and W9 unreachable by design, and require a
different public roles contract than the one the frozen provenance table already states. Choosing
B here authorizes no development record, role read or run; it only tells 4b which branch to build.

### 9.3 FINDING DA — the branch-B ruling makes the frozen design's `--config` gloss false on a reachable path

**Two statements inside the frozen design disagree, and until this round the disagreement was
inert.** Its section 4.2 argument table glosses `--config` as "the exact frozen config file"; its
section 4.3 gives `DEVELOPMENT_ONLY` the entry condition "the config is `dev-` and split is `dev`".
A `dev-` config is a draft by the machine contract's own rules — measured at source this session in
`utils/config_contract.py`: the draft branch refuses a file named `config.json`, requires
`status = "draft"`, requires `confirmatory_payloads_allowed` to be `False` and at least one
`open_gates` entry, and requires the `config_hash` to carry the `dev-` prefix, while
`load_config(require_frozen=True)` refuses the same document with *"confirmatory operation refuses
draft configuration"*. The two rows therefore cannot both govern one invocation. While
`DEVELOPMENT_ONLY` was unauthorable, the 4.2 gloss was true of every reachable roles invocation and
nothing had to choose between them.

**The ruling is what makes it operative, and it is not editorial.** Section 3.1 of this document
says the six closed CLI arguments remain unchanged, which points the 4b builder at the frozen 4.2
table for their meaning. A builder following that pointer writes `load_config(require_frozen=True)`
unconditionally — which refuses every config a `DEVELOPMENT_ONLY` record could ever name, silently
reinstating the branch the CY ruling just rejected, in the one round entitled to build it. Without
a positive branch-reaching check, the full synthetic end-to-end would stay green because its accept
path is `SYNTHETIC_FIXTURE` and never opens a config, while refusal-only coverage can pass on a
development branch that always refuses. That is the CX shape a fourth time: **the defect that only
the path no positive test reaches can expose.** Finding DC records the missing test obligation.

**Resolution: 4.3 governs, and the 4.2 gloss is `FINAL`-only.** `--config` names the
authority-appropriate config file — the frozen `config.json` under `FINAL`, the exact approved
versioned draft under `DEVELOPMENT_ONLY`. `require_frozen` is a function of the record's
authenticated `authority`, never a constant, and read-order step 4's "check the `dev-`/frozen rule
against `authority`" is the normative statement of it. The argument list, its arity, its ordering
and its identity checks are untouched; one gloss on one row is corrected, forward, here. This is
the fourth forward correction section 0 counts.

### 9.4 FINDING DC — DA fixed the runtime rule but did not yet pin its positive test

**The disagreement was internal to the owner-approved input bytes.** Section 2.3 said the adapter's
authority-scoped config branch and its accept/refusal tests must implement branch B. The
owner-approved DA then said every 4b test would remain green because the only accept path is
`SYNTHETIC_FIXTURE`. Both statements could not stand without distinguishing a complete public-path
accept from a positive validator-path test.

The distinction matters. B1 drives the tracked draft through `utils.config_contract` in isolation,
not through the adapter's branch. B3's refusal cases can all pass on an implementation that rejects
every development config. The synthetic end-to-end in B2 never opens a config. The runtime prose in
DA is therefore correct, but an unconditional `load_config(require_frozen=True)` could still pass
the enumerated acceptance set unless one temporary development pair is required to cross step 4.

**Resolution: the DA runtime ruling stands unchanged, and B8 makes both sides observable.** A
temporary authenticated development record/draft-config pair must cross step 4 before a later
deliberate refusal, and a temporary final record/synthetic-frozen-config pair must do the same. Each
pair must refuse when its config is presented under the opposite authority. No production record
is authored and no real role byte is opened. This is a repair to the live design's test contract,
not a fifth forward correction to the frozen v0.1 document.

---

## 10. Sequencing — Step 4, decomposed

The frozen design's step 4 is one line. It is six: only 4a and 4b are buildable now; 4c through 4f
are blocked.

| # | sub-step | blocked on | authorizes |
|---|---|---|---|
| **4a** | **this document reviewed and frozen** at an exact state, both agents approving the same bytes | nothing | writing the adapter and its tests, and nothing else |
| **4b** | **the adapter and its tests are built and reviewed**, exercising authenticated storage/refusal plumbing against the existing contract fixture and geometry/rendering against the dedicated coherent synthetic fixture; no real-data tolerance is guessed or recorded | 4a | nothing further; a built adapter is a tool, not a permission |
| **4c** | **the preconditions P1–P6 are met**, each with its own separately approved artifact | the authority-appropriate approved config state (versioned draft for `DEVELOPMENT_ONLY`, frozen `config.json` for `FINAL`), capacity selection, threshold calibration, established development/final result and geometry validation | authoring a record |
| **4d** | **the connection record is authored and reviewed** at an exact state, both agents approving the same bytes | 4c | nothing on its own |
| **4e** | **the joint authorization**, issued as two halves, each naming the record digest, the split, the exact command, all six arguments, the budget, what it does not authorize, and how each of P1–P6 was checked | 4d | exactly one adapter invocation |
| **4f** | **the one authorized invocation runs**, and both agents review the exact output state | 4e | nothing; the lane is then spent |

**A closed review loop authorizes the next sub-step only, and never a run.** That rule has held on
every lane in this project and it holds here.

---

## 11. What is true today, stated so a later session does not have to reconstruct it

- Steps 1, 2 and 3 of the frozen design are closed at both approvals. Step 4a is in exact-state
  design review; 4b has not begun.
- Final P1 and P2–P5 are false. The current draft can pass the structural development-config
  validator, but its model and calibration fields are null and this document grants it no
  connection-record approval. P6 is uninstantiated because no established-result artifact selects
  the cases and run identities for this surface. This is not an absence of pairs: the delivered
  base manifest contains 472 complete C1/S pairs (152 dev, 152 pilot and 168 val). No connection
  record exists anywhere in the packet.
- `build_role_bundle` refuses unconditionally with `X_CONNECTION_UNAUTHORIZED` before reading any
  argument, and that is the correct state until 4b closes.
- Findings CU, CV and CW are raised here for the first time and are resolved *within* this document
  rather than by amending the frozen design. **CX (section 4.8) and CY (section 9.2) were raised in
  the owner re-review of the reviewer-repaired state; CX is accepted unchanged, and CY is resolved
  here as an authority-scoped P1 before 4b, on the reviewer's finding CZ that the branch changes
  what 4b builds. DA (section 9.3) and DB (section 7, test B1) were raised in the second owner
  re-review, against the reviewer's own new text, and are accepted here. DC (section 9.4 and test
  B8) repairs DA's missing positive branch test without changing its runtime ruling.**
- This document authorizes 4b and nothing else, and only once both agents have approved the same
  bytes.
