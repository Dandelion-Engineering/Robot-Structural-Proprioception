# The Director's Verification Artifact — Interface Contract and Synthetic Scaffold — v0.1

**Status:** REVIEWER-EDITED CANDIDATE, ROUND 3. Claude approved the Session-123 draft
`260e2042c6b857c2d07cf1f9619cf54af86e5015`; Codex reviewed it in its Session 123, found nine
contract defects, repaired them and approved `0fabe54741741f7a86c121859bd7110d8664d39d`; Claude's
Session-124 owner re-review kept all nine repairs unchanged, added two findings of its own and
approved `d56c25c18218892e651e1c7583175d9e03e6969e`; Codex's Session-124 re-review kept both new
repairs, narrowed their test contracts and approved `7536a6eba5eb4b293cc7acd3cff64f0351d85216`.
Claude's Session-125 owner re-review kept both of those narrowings and added two findings of its
own (the fixture's tracking block was never required to be a valid `j_5s` call, and the shared
painter had no time argument for the animation it is required to drive). Codex's Session-125
re-review kept both repairs and found two interaction defects exposed by the new frame argument:
the two arms had no single shared playback grid, and the painter had no causal rule for which
estimator decision was available at a frame. Codex repaired both and approved the returned state;
Claude's owner re-review is open. Exact-state approvals live in the Phase-2 chat and in Git
history, not in this mutable status line.

**Nothing in this document authorizes a fit, a checkpoint, a capacity choice, a probability or
abstention threshold, a configuration freeze, a generation, a rollout, or any pilot, validation or
test read.** It is a design under review, in the same shape as Protocol P, the payload-boundary
extension, the capacity escalation and the rung-2 escalation: the document is reviewed and frozen
first; the module and its tests are built and reviewed second; connecting any real scientific
input is a third and separate joint authorization that this document does not grant and does not
pre-approve.

**Version discipline (inherited).** This document has never been jointly approved, so any revision
before approval is an in-place edit of an unapproved draft. **Once both agents approve a state, a
later correction bumps the version and `git mv`s; an approved version is never edited in place.**

**Provenance of the request.** In Session 122 I asked Codex which of three lanes the next sessions
should spend themselves on, since nothing scientific was open. Its Session-122 turn ruled Slot 8
first, then the Technical Report, and attached a hard boundary to the Slot-8 round. That boundary
is the origin of this document and is quoted in full in section 2.2 rather than paraphrased, so a
reader does not have to find the transcript.

---

## 1. What this document is for

Claim Sheet Slot 8 commits the agents, before execution, to build a hands-on artifact that lets
the director — and anyone who downloads the Reproducibility Packet — verify the result without
reading the Technical Report end to end. It is a required component of the Reproducibility
Packet — itself one of the four artifacts a Dandelion project must have before it can be called
complete — and the Project Details working method says in writing that it is **paced into the
project rather than assembled in the final session**.

It is also, as of Session 123, **the one named completion requirement that has no object at all**.
The packet has protocols, executables, tests, results and a runbook; it has nothing a
non-specialist can open as the Slot-8 surface.

### 1.1 The problem, stated plainly

The artifact Slot 8 describes cannot be built at its final form today, and the reason is not
effort. Three of its four inputs do not exist:

| Slot 8 needs | current state |
|---|---|
| a frozen `config.json` naming the run being demonstrated | **absent by governing decision** — `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION` |
| a selected model capacity and its fitted checkpoints | **undecided** — no rung and no width has been selected; Slot 9's ladder has two of three rungs built and nothing chosen |
| a calibrated abstention threshold and an unknown/OOD threshold | **undecided and validation-owned** — Gate 5, and validation must not be touched until Gate 4 closes |
| a rendering mechanism | **does not exist** |

Only the fourth is available. A demo built now would have to either invent the first three or
silently adopt whatever the current development record happens to contain. The second failure is
by far the more dangerous, because a development artifact rendered in a finished-looking demo
reads to a non-specialist as the project's result, and this project's development record has zero
healthy and structure per-class F1 in all ten rung-2 arms. Presenting that as a finding would be a
misrepresentation this document exists to make structurally impossible.

### 1.2 What this document specifies instead

The part that can be built without any of the three missing inputs: **the interface between the
scientific record and the two presentation surfaces**, plus **a synthetic fixture** that drives
that interface end to end without a single real number in it. The real-result entry path is
specified as an authenticated connection record but remains mechanically unreachable until that
record exists and has passed its own exact-state review and authorization.

The design test this document is written against, and the one a reviewer should hold it to:

> **When the scientific inputs finally exist, connecting them must be an authenticated data
> change and a separate authorization — not a rewrite of the scene schema or either renderer.**

If a reviewer can find a place where connecting a real result would require editing rendering
code, that is a defect in this design, not a detail of the later build.

### 1.3 The two surfaces, and why they must share one object

Slot 8 asks for two artifacts that must agree. The interactive demo is the director's; the
scripted 300-DPI figures are the Technical Report's and the Accessible Piece's. Slot 8's own words
are that the scripted version "produces **the same comparison**".

"The same comparison" is a contract, not a coincidence. If the interactive view and the figure
script each reach into the roles and assemble their own picture, then sameness becomes a property
maintained by hand across two code paths, and the first divergence between them will be silent
and will land in a published figure. This project has already paid for that lesson in a smaller
denomination: standing lesson S56 — *every check must be given a source independent of the thing
it checks* — and its converse here is that every two things required to be identical must be
given a **single** source.

So the design is one bundle and two pure surfaces. A `VerificationBundle` contains the named
`VerificationScene` objects in the short menu. Two mutually exclusive construction paths produce
the bundle: the synthetic generator now, and an authenticated real-result adapter only after its
connection record is jointly approved.

```text
  synthetic case set + seed --------------------------+
                                                        +--> VerificationBundle --+--> interactive menu
  connection record + config + checkpoints + roles -->+    (value, serializable)  +--> 300-DPI PNG set
             (future, separately authorized adapter)
```

The real-result adapter is the only code permitted to touch a role, a checkpoint or a config.
Both surfaces are functions of a bundle and nothing else. They share one pure painter with the
exact signature

```text
draw_scene(scene, *, frame) -> figure
```

**The frame argument is load-bearing and is not an implementation detail.** A2 and section 4.5
panel 1 require an *animated* two-body view with play/pause and a timeline, and V16 requires each
case to carry two *time-varying* centerlines. A painter whose entire input is a scene has no lever
the timeline can move, so a wrapper that may only choose *which scene* cannot animate anything;
naming the frame here is what keeps the animated view and the published still on one source
instead of two. `frame` is an integer index into the scene's one shared `playback_t_s` control
grid; it cannot mean one time for C1 and another for S. The interactive wrapper varies both the
scene (radio menu) and the frame (slider / `FuncAnimation`); the scripted wrapper iterates the
same scenes at a frame **derived from the scene** (section 4.6), so the scripted surface remains a
function of the bundle alone. The painter itself is pure in both: it takes a value and a frame
index and returns a figure. A renderer that opens a scientific input is a defect; the scripted
wrapper may write only its declared output set.

---

## 2. What licenses this, and what does not

### 2.1 Slot 8, quoted

From `Claim Sheet.md`, Slot 8, unedited:

> **The artifact:** a small **interactive side-by-side demo**. The director picks a body change
> from a short menu — *"soften link 2 by 30%," "weaken actuator 1," "bias encoder 1"* — and
> watches two copies of the robot run the same task at once: one driven by the **conventional
> suite C1**, one by the **structural suite S**. A live panel shows, for each copy, (a) its
> current **fault call and confidence** (or an honest *abstain*), and (b) its **tracking-error
> trace**. The director sees directly whether the structural robot names the right cause
> **sooner and more often** and **tracks better after the change** — or whether the two are
> indistinguishable, which is the honest negative shown *as* a result. A scripted,
> non-interactive version produces the same comparison as a set of 300-DPI figures for the
> reports.
>
> What the director does: trigger a few changes, watch which robot correctly says *what* happened
> and *keeps doing the task*, and read the confidence/abstain behavior to see the system decline
> to guess when the signals are genuinely ambiguous. Naming this artifact now also disciplines
> the build — the experiment has to be designed so that this comparison is possible and legible.
> If results reshape what the artifact should show, the Slot-8 entry is amended through the normal
> protocol.

Slot 8 also says, and this document takes it as binding: *"If results reshape what the artifact
should show, the Slot-8 entry is amended through the normal protocol."* Nothing here proposes an
amendment. Everything specified below is inside what Slot 8 already contracts.

### 2.2 The Session-122 boundary, quoted

Codex's Session-122 turn, verbatim:

> The first Slot-8 round should:
>
> 1. define one packet-local input/output contract shared by the interactive side-by-side view and
>    the scripted 300-DPI figure path;
> 2. keep final config, checkpoint identities, class/abstention thresholds and result roles as
>    required external inputs, with no defaults that silently select today's development state;
> 3. use only an explicitly labeled synthetic fixture to prove the two-copy visualization,
>    confidence/abstain panel and tracking traces work;
> 4. fail closed if a role is absent or not authorized, and carry a visible `DEVELOPMENT-ONLY`
>    state whenever a non-final fixture is loaded;
> 5. read no pilot, validation or test outcomes and make no capacity, threshold or configuration
>    choice; and
> 6. come back through the normal review cycle before any real result is connected.

Each bound is discharged by a named section, and a reviewer should check the mapping rather than
take it on trust:

| bound | discharged by | mechanism |
|---|---|---|
| 1 — one shared contract | 1.3, 4.1 | one `VerificationBundle` of `VerificationScene` values; both surfaces share `draw_scene` |
| 2 — required external inputs, no silent defaults | 4.2 | mode-specific parsers; real-result mode requires one authenticated connection record plus explicit roots; **V3**, **V4** |
| 3 — labeled synthetic fixture only | 4.4 | `SYNTHETIC_FIXTURE` provenance; **V7**, **V9**, **V17** |
| 4 — fail closed; visible `DEVELOPMENT-ONLY` | 4.2, 4.3, 4.6 | authenticated connection record, identity/pair checks and provenance state machine; **V2**, **V5**, **V6**, **V9**, **V11** |
| 5 — no pilot/val/test; no choices made | 4.2, 6 | no connection record exists in this round, so all real-role access refuses before a read; **V2**, **V3** |
| 6 — return through the review cycle | 9 | sequencing; nothing connects a real result inside this round |

### 2.3 What this document does not license, stated so it cannot be inferred

- It does **not** license reading `pilot`, `val` or `test` for any purpose, including "just to
  render a picture". Section 4.2 and V2 keep every real-role path unreachable in this round.
- It does **not** license selecting a capacity, a rung, a width, a probability threshold, an
  abstention threshold or an unknown/OOD threshold. Every one of those is an *input*.
- It does **not** license writing, freezing or drafting `config.json`.
- It does **not** license a fit, a checkpoint, a generation run or a rollout. The scaffold runs
  no physics and trains nothing.
- It does **not** license a C1-versus-S statement of any kind. See section 6, item 4, which is the
  one a reader is most likely to expect this document to have quietly relaxed.
- It does **not** re-open any closed lane, artifact or approval.

---

## 3. What the artifact must let the director do

"The director can verify the result" is not checkable. These six are, and the module's tests are
expected to exercise the mechanism behind each one.

- **A1 — Choose without typing.** The director selects one body change from a short named menu
  (Slot 8's examples: *soften link 2 by 30%*, *weaken actuator 1*, *bias encoder 1*). No path, no
  hash, no flag, no code edit.
- **A2 — See two bodies at once.** Both arms replay the same paired task against the same
  reference, and the two animated planar bodies are visually distinguishable and labelled by
  suite. Play/pause and timeline controls require no typing.
- **A3 — Read the call and the confidence, and see an abstention as an abstention.** Not a
  probability bar quietly renamed. An abstaining arm must look different from a confident arm and
  different from a wrong arm.
- **A4 — Read the tracking error.** Each arm's task-space error against the same reference, on the
  same axes, with the change onset marked.
- **A5 — Always see what the picture is made of.** Provenance is on screen and in every saved
  figure, never only in a caption or a README.
- **A6 — Reproduce the stills with one command.** The scripted path regenerates the figure set
  deterministically from the same bundle and shared scene painter.

**None of A1–A6 is satisfied *scientifically* by this round.** The synthetic fixture proves the
mechanism carries the information. It proves nothing about the robot, the suites, or the
question. Sections 4.4 and 6 say so in the artifact itself, not only here.

---

## 4. The design

### 4.1 `VerificationBundle` and `VerificationScene` — one surface contract

A scene is the complete, serializable description of exactly one side-by-side comparison. A
bundle is an ordered, non-empty mapping of unique `case_id` values to scenes; it is the one object
both surfaces consume and the source of the interactive menu. Every bundle contains at least one
structure, actuator and sensor case, and every scene in it agrees on bundle version, provenance
state, config identity, thresholds and connection-record identity. Both are values: no file
handles, no live model, no callbacks. The bundle serializes to JSON under the packet's existing
canonical-JSON discipline (`sort_keys`, `(",",":")` separators, `allow_nan=False`), which is what
makes a figure's provenance auditable after the fact and what lets a reviewer diff two bundles.

**Non-finite floats are part of the schema, so the scene encodes them rather than being unable to
write them.** `EstimatorOutput.severity_uncertainty` defaults to `+inf` and `detection_time_s` is
`NaN` before detection, and `EstimatorOutput.validate()` accepts both — they are contract-valid
values a real `estimator_outputs` role will contain, not corruption. Measured this session:
`json.dumps` under `allow_nan=False` refuses all three of `inf`, `-inf` and `nan`, and the
packet's own `protocol_p.canonical_json` docstring says that refusal is deliberate. Left
unaddressed, the bundle write fails on exactly the value section 4.5 promises to render as
`UNAVAILABLE`, and connecting a real result would require rewriting the scene serialization —
which is the one thing section 1.2's design test forbids. Therefore **every float position in a
scene encodes as a JSON number when finite and as one of the three JSON strings `"Infinity"`,
`"-Infinity"`, `"NaN"` when not.** `allow_nan=False` stays on and no non-standard JSON token is
ever emitted; the mapping is total and exactly invertible; it is unambiguous because a finite
float never encodes as a string. This is a wire encoding, not a second estimator schema: decoding
restores the three strings to their IEEE-754 float values before scene construction and validation.
The decoder calls `json.loads` with a `parse_constant` callback that always raises, because
Python's default loader accepts the bare non-standard tokens `NaN`, `Infinity` and `-Infinity`;
only the three quoted strings in typed float positions are decoded. Any other string in a float
position is a loud decode failure, never a silent zero. **V19.**

| field | shape | source | notes |
|---|---|---|---|
| `provenance` | struct | 4.3 | state; connection-record identity; config/checkpoint identities; per-arm run, pair, role-index and payload identities; exact roles read |
| `body_change` | struct | menu plus fixture/`labels` | `case_id`, display `label`, and the exact schema-D label fields: `source_class`, `subtype`, `location`, `severity`, `onset_index`, `onset_time_s`, `compound_flag`, `ood_flag` |
| `playback_t_s` | `[T]` | fixture, or authenticated C1/S schema-B `plant` roles | the one shared, finite, strictly increasing uniform control grid; every frame-bearing array in both arms is indexed by it |
| `arms` | exactly 2 | roles or fixture | keyed `C1`, `S`; **exactly two, always both** |
| `arms[k].body` | `centerline_xy[T,N,2]` | fixture, or derived read-only from schema-B `plant` + authenticated config | the body animation on `playback_t_s`; final centerline point must agree with `true_task_output` |
| `arms[k].decisions[]` | per decision step | schema D `estimator_outputs` | strictly increasing `step`/`decision_time_s`; exact fields `p_class[4]`, `unknown_score`, `abstain_decision`, **`location_out`**, `severity_out`, `severity_uncertainty`, `detection_time_s` |
| `arms[k].tracking` | `task_reference[T,2]`, `true_task_output[T,2]`, `window_s` | schema-B `plant`; window from fixture or authenticated config | with `playback_t_s` and onset in `body_change`, the complete argument set for `utils.metrics.j_5s` |
| `arms[k].controller_mode[]` | `[T]` strings | `controller_logs` | non-empty and indexed by `playback_t_s`; source `controller_logs.t_s` must match exactly |
| `truth` | exact schema-D label struct or `null` | fixture or `labels` | fixture truth is visibly marked **`FABRICATED TRUTH`**; real truth requires an authorized label role |
| `thresholds` | struct | fixture or authenticated connection record | `abstain_threshold`, `unknown_threshold`; never derived and never silently defaulted |

Six properties of that table and bundle are load-bearing and are not stylistic:

1. **`decisions[]` renders the schema-D `estimator_outputs` struct exactly, including
   `location_out`, with no renaming and no translation layer.** The scene carries what the schema
   already defines. A translation layer is a second definition of the same thing, and the
   project's existing rule is one source of truth per fact.
2. **`tracking` comes from the privileged schema-B `plant` role, not `controller_logs`, and the
   scene carries the complete argument set `j_5s` takes** (`playback_t_s`, `task_reference`,
   `true_task_output`, `window_s`, and the onset time already in `body_change`). The panel the
   director reads and the metric the Technical Report reports are then provably the same quantity,
   because the plot and the number take the same inputs.
3. **A frame names one physical time in both arms.** Scene construction requires the C1 and S
   `plant.t_s` arrays, each arm's body and tracking leading dimension, and both
   `controller_logs.t_s` arrays to agree exactly with the one `playback_t_s` grid. The fixture is
   held to the same rule. A per-arm time grid would let `frame=500` show different physical times
   in C1 and S while still passing every per-arm shape check; that is not a side-by-side replay.
4. **The call panel is causal in the playback frame.** At `playback_t_s[frame]`, each arm renders
   the greatest `decision_time_s` that is no later than the frame time. Before the first decision
   it renders **`NO DECISION YET`**, with no probability, call, severity or unknown state borrowed
   from the future. Decision steps and times are strictly increasing and every decision lies
   inside the playback extent. The final decision may not be shown at every frame merely because
   it is the persisted run-level summary.
5. **`arms` has exactly two entries and both are always present.** A scene that could carry one
   arm is a scene that can render a one-sided picture, and a one-sided picture is the failure mode
   Slot 8 exists to prevent. V1 makes this a construction-time refusal rather than a convention.
6. **The body panel has body geometry.** Endpoint traces alone do not satisfy Slot 8's promise
   that the director can watch two robot copies. The synthetic generator emits analytic
   centerlines. The future adapter derives planar centerlines read-only from authenticated
   `q_true`, `deform_coords` and config geometry, without stepping MuJoCo, and checks every distal
   point against the recorded `true_task_output` within a declared visualization tolerance.
7. **The two arms are a real pair, not merely two suite labels.** The adapter authenticates the
   C1/S `pair_id`, case identity, onset, shared playback grid and `task_reference`; any mismatch
   refuses.
8. **The menu is data, not renderer state.** Unique case labels and order live in the bundle. Both
   surfaces must expose every bundle scene; a scripted figure set or interactive menu that drops a
   case refuses rather than silently publishing a subset.

### 4.2 The two mode-specific input contracts

The CLI has two subcommands rather than one parser with contradictory requirements.

**`fixture` mode — the only executable data path in this round**

| argument | rule |
|---|---|
| `--fixture-seed` | required; no default seed |
| `--output-dir` | required, project-relative |

Fixture mode builds the complete named fixture bundle from one seed; individual cases are selected
inside the interactive menu, not on the command line. It accepts no config, checkpoint, role,
split or caller-supplied provenance argument. The generator supplies visibly synthetic identities
and round fabricated thresholds as fixture data.

**`roles` mode — specified now, unreachable until a separate connection review**

| argument | what it names | why it cannot have a default |
|---|---|---|
| `--connection-record` | the reviewed JSON that names every allowed case, role and scientific input | a caller-authored allowlist is not authorization |
| `--connection-record-sha256` | the exact record identity named by the joint approval | prevents a different record from travelling under the same path |
| `--config` | the exact frozen config file | the adapter measures it; a hash string alone does not authenticate bytes |
| `--checkpoint-root` | root for the relative C1/S checkpoint paths in the record | the adapter measures both files against the record |
| `--role-root` | root containing `manifest.csv`, `plant/`, `labels/`, `estimator_outputs/<suite>/`, and `controller_logs/<suite>/` | manifest rows establish pair/split; role paths and payload identities are measured against the record |
| `--output-dir` | where scenes and figures are written | Standards: project-relative, passed in |

The connection record is data, not a permission-shaped CLI flag. It contains: record version and
authority (`DEVELOPMENT_ONLY` or `FINAL`); config semantic identity and file SHA-256; analysis
window; both thresholds; manifest SHA-256 and exact row identities; render geometry and its
derivation version; exact split; selected model/rung/width identities; and, per menu case, the
pair/case identifiers, C1/S run IDs, relative checkpoint paths and SHA-256s, and the role-index and
role-payload SHA-256s for `plant`, `labels`, `estimator_outputs` and `controller_logs`. Paths
inside it are packet-relative. The
runtime authenticates those facts; it does **not** claim that digest matching proves social
approval. Exact-state approval of the record in the chat is the authorization.

No connection record exists in the packet in this round. Therefore `roles` mode must refuse with
`X_CONNECTION_UNAUTHORIZED` **before opening any config, checkpoint, role index or payload**. The
later jointly approved record is what makes the already-specified adapter reachable; no
`--authorized-role`, `--split`, environment variable or override flag can substitute for it.
There is no mode in which a scene mixes fixture and role data.

### 4.3 The provenance state machine

Every scene carries exactly one provenance state, and the state is computed from the construction
path plus authenticated inputs — it is never passed in, because a caller-supplied provenance
label is a label that can lie.

| state | entry condition | how it renders |
|---|---|---|
| `SYNTHETIC_FIXTURE` | built by the fixture subcommand | banner **`SYNTHETIC - NOT A RESULT`** on every surface |
| `DEVELOPMENT_ONLY` | an exact approved development connection record authenticates the roles, and the config is `dev-` and split is `dev` | banner **`DEVELOPMENT-ONLY`** on every surface |
| `FINAL` | an exact approved final connection record authenticates the named split, non-`dev-` config, checkpoints, pair and all role bytes | no warning banner; identities and **`FINAL RESULT INPUTS`** remain printed |
| *(refusal)* | anything else | the run exits non-zero with a named code; **no scene is produced** |

`DEVELOPMENT_ONLY` and `FINAL` are both currently unreachable, and that is the correct state of
the project rather than a gap in the design: no connection record exists and no non-`dev-` config
hash exists. The states are specified now so the later connection is an authenticated data change,
per 1.2. **V8** requires a test that asserts both are unreachable from every input the packet
currently contains — so the day either becomes reachable, the suite goes red and forces the
connection record to be reviewed deliberately.

Exit codes. Every refusal below is fail-closed and carries its own distinct code, so a test can
assert *which* refusal fired; the last row is the success code and is the only zero exit:

| code | fires when |
|---|---|
| `X_CONNECTION_UNAUTHORIZED` | role mode was requested without the exact separately approved connection record; fires before any read |
| `X_SPLIT_FORBIDDEN` | the record names a split its exact authorization does not permit, or any role/index disagrees with that split |
| `X_ROLE_ABSENT` | a required role root or index is missing |
| `X_ROLE_UNAUTHORIZED` | a role is not named by the authenticated connection record |
| `X_IDENTITY_MISMATCH` | a measured config, checkpoint, index or payload SHA-256 differs from the record |
| `X_PAIR_MISMATCH` | C1/S pair, label fields, onset, time grid or task reference differs |
| `X_TIMEBASE_MISMATCH` | C1/S plant grids, body/tracking/controller leading axes or controller-log grids do not all bind to one `playback_t_s`, or `frame` is outside that grid |
| `X_DECISION_UNSUPPORTED` | decision steps/times are not strictly increasing, a decision lies outside the playback extent, or a call panel cannot apply the causal at-or-before rule |
| `X_PROVENANCE_UNRESOLVED` | the inputs do not land in exactly one state |
| `X_BUNDLE_INCOMPLETE` | case IDs are duplicated, a required source case is absent, or a surface omits a bundle case |
| `X_ARMS_INCOMPLETE` | fewer or more than the two required arms |
| `X_WINDOW_UNSUPPORTED` | an arm's `tracking` block is not a valid `utils.metrics.j_5s` call at that scene's onset and `window_s` — a non-uniform or non-increasing grid, a non-finite sample, an onset that is not exactly a control sample, or a grid that ends before `onset_time_s + window_s` |
| `X_SCENE_OK` | success (exit 0) |

### 4.4 The synthetic fixture

The fixture is a small, explicitly fabricated scene generator. It exists to prove that the
mechanism carries the information — two arms, four classes, an abstention, an onset, two tracking
traces — and for no other reason.

Requirements on it:

- **It is generated by code in the packet from a named seed, not shipped as data.** A checked-in
  `.npz` of plausible numbers is indistinguishable from a real result at a glance; a generator
  named `synthetic_fixture` in a file that says what it is, is not.
- **Its numbers must be visibly artificial where that costs nothing.** Tracking traces are
  analytic; probabilities are round; onset is at a round time. The fixture is not trying to look
  real, and a fixture that looks real is a defect.
- **It must exercise every branch the director can see**, because a panel whose abstention path is
  never rendered in this round is a panel whose abstention path is untested when it matters. The
  fixture set must therefore include, at minimum: a confident correct call; a confident **wrong**
  call; an abstention; and a high `unknown_score`. It must include at least one scene in which the
  two arms are **indistinguishable**, because Slot 8 names that outcome explicitly as "the honest
  negative shown *as* a result" and a demo that cannot render it is a demo that can only show a
  win. It must also include at least one arm whose `severity_uncertainty` is `+inf` and whose
  `detection_time_s` is `NaN` before detection — those are the schema's own defaults, they are what
  a real role will carry, and without them section 4.5's `UNAVAILABLE` branch and the 4.1
  non-finite encoding are both unrendered and untested in the only round that can test them.
- **Its animation has one clock and a visible decision history.** Every body, tracking and
  controller array in both arms is indexed by the fixture scene's one `playback_t_s` grid. At
  least one case has two or more strictly ordered decisions that change a visible call-panel
  state, and the grid begins before the first decision, so the fixture drives both
  `NO DECISION YET` and the causal at-or-before decision selection. Otherwise a moving body could
  coexist with a call panel that quietly displays the run's final diagnosis at every frame.
- **Every arm's `tracking` block must be a valid `j_5s` call, and this is a hard fixture
  requirement rather than an aspiration.** Section 4.1's property 2 claims the panel the director
  reads and the number the Technical Report reports are the same quantity *because they take the
  same inputs*. That claim is only checkable if the inputs are ones `j_5s` will actually accept,
  and the function's preconditions are strict — measured this session against the live
  `utils.metrics.j_5s`: `playback_t_s` must be strictly increasing and uniform, every tracking sample
  must be finite, `onset_time_s` must land on a control sample to within `1e-9`, and the grid must
  extend through `onset_time_s + window_s` or the call raises *"the analysis window is truncated
  before onset + window_s"*. **A perfectly ordinary fabricated trace fails this**: 1,000 samples
  at 100 Hz from 0 s, with a deliberately round onset at 5.0 s, is refused, because that grid ends
  at 9.99 s and the 5 s window needs a sample at 10.0 s. `linspace(0, 10, 1001)` at the same onset
  is accepted. The fixture generator must therefore emit grids that cover
  `onset_time_s + window_s`, and scene construction refuses with `X_WINDOW_UNSUPPORTED` when they
  do not. Without this, the only round that can exercise property 2 never exercises it, and
  section 4.5 panel 3 shades a window that extends past the end of the data it is drawn over —
  the picture and the number disagreeing in exactly the way property 2 exists to prevent. This is
  the same shape as finding CA: a fixture that cannot reach a branch leaves that branch untested
  in the only round that can test it.
- **It declares no truth it does not have.** `truth` may be set for a fixture — it is fabricated
  along with everything else — but it is rendered as **`FABRICATED TRUTH`**, never as an
  unqualified green correctness mark, and the banner governs interpretation. V9 forbids any
  fixture scene from rendering without both labels.

The fixture is **not** a stand-in for a result, a baseline, a validation, or evidence of anything
about the robot. Section 6 states this inside the artifact.

### 4.5 The three panels

One figure, three regions, identical in both surfaces:

1. **The two bodies.** Both arms' planar centerlines at the painter's `frame` argument on the one
   shared `playback_t_s` grid, drawn
   against the shared task reference and over the faint full sweep of that arm's centerlines
   across time, labelled by suite, with the body change and its onset marked. Radio-button menu
   selection selects the scene and play/pause and timeline controls drive `frame`, which is what
   satisfies A1/A2 without typed input.
2. **Call and confidence.** Per arm: the class probabilities over
   `("healthy", "structure", "actuator", "sensor")` — the canonical `SOURCE_CLASS_ORDER`, so a
   reader comparing a figure to a table never has to check — the current call, and the
   abstention/unknown state rendered as its own visual state rather than as a low bar. The known
   call follows the packet scorer exactly: stored `abstain_decision=True` renders `ABSTAIN`;
   otherwise it is `SOURCE_CLASS_ORDER[argmax(p_class)]`. Confidence is `max(p_class)`.
   `unknown_score >= unknown_threshold` is shown as a separate high-unknown state and does not
   silently rewrite the stored abstention decision. The thresholds are display/audit references
   from fixture data or the authenticated connection record, never re-estimated here.
   The displayed decision is the last decision whose `decision_time_s` is at or before
   `playback_t_s[frame]`; before the first decision the panel displays `NO DECISION YET` and no
   future probability, call, unknown, location or severity value. `location_out` is shown as the
   location call or `UNLOCALIZED`. Severity appears beside its
   non-negative, config-defined **error scale**; the renderer must not call that scale a confidence
   interval unless a later frozen contract gives it coverage semantics, and an infinite scale
   renders as `UNAVAILABLE` rather than as a plot extent.
3. **Tracking error.** Per arm: the norm of `task_reference - true_task_output` on the shared
   `playback_t_s` axes —
   the same per-sample quantity `j_5s` integrates — with onset marked and the shaded band spanning
   exactly `[onset_time_s, onset_time_s + window_s]`, so the director can see the region the
   project's headline metric integrates over. The shaded band is the metric's window and not an
   approximation of it; a scene whose grid cannot support that band never reaches the renderer,
   because scene construction already refused it with `X_WINDOW_UNSUPPORTED`.

Panels 2 and 3 are per-arm and side by side. **Neither panel emits a cross-arm derived number.**
That is section 6 item 4, and it is the constraint most likely to be relaxed by accident.

### 4.6 The scripted figure path

The scripted wrapper iterates the bundle through the same `draw_scene(scene, *, frame)` painter
under a non-interactive backend and calls `savefig(..., format="png", dpi=300)`, per the
Standards' figure requirement. It writes one PNG and canonical scene JSON per case plus the
canonical bundle JSON and its SHA-256, so any figure in any report can be traced to both the exact
scene and complete menu that produced it.

**The frame the still draws is derived from the scene, never passed in**, so the scripted surface
stays a function of the bundle alone and V13's byte-identical requirement has something
deterministic to bind. It is the index of the shared `playback_t_s` control sample at
`onset_time_s + window_s` — the last sample the headline metric integrates, which section 4.4 now
guarantees exists. That choice ties panel 1 to
panel 3: the body pose the reader sees is the pose at the moment the shaded window closes, rather
than an arbitrary frame that happens to be first or last in the array. The interactive surface is
the only place `frame` is free.

The provenance banner is drawn **into the figure** as a figure-level artist, not written into a
caption or a filename. A caption is separable from the image the moment someone copies the PNG
into a slide; the banner must survive that. **V11.**

### 4.7 Dependencies — nothing new

The interactive surface is built on `matplotlib.widgets`, and the scripted surface is the same
code under a non-interactive backend. `matplotlib==3.11.0` is already pinned in the packet's
`requirements.txt`.

**This adds no dependency to the packet, and that is a design choice made against the Efficiency
standard rather than a convenience.** A browser-based viewer would render more prettily and would
cost the packet a web stack, a build step and a class of "it doesn't run on my machine" that the
fresh-environment validation exists to prevent. The smallest sufficient surface is one the
existing pinned dependency already draws. If a reviewer thinks the interactive requirement cannot
be met inside `matplotlib.widgets`, that is worth contesting now, in this round, rather than after
the module is written — see section 8, decision D2.

---

## 5. Invariants the module must carry

Each is a property a test must be able to fail. "The module does X" is not an invariant; "the
module refuses, with code Y, when Z" is.

- **V1 — A complete menu, with two arms per case, or nothing.** A bundle requires unique case IDs,
  at least one structure, actuator and sensor case, and every scene has exactly two arms keyed
  `C1` and `S`. Refusals: `X_BUNDLE_INCOMPLETE`, `X_ARMS_INCOMPLETE`.
- **V2 — Real roles are unreachable in this round.** Without the exact separately approved
  connection record, role mode refuses with `X_CONNECTION_UNAUTHORIZED` before any config,
  checkpoint, index or payload is opened. No caller-supplied role/split flag or environment
  variable re-enables it. This prevents a later approved test result from being permanently
  designed out while keeping pilot/validation/test unread now.
- **V3 — The module derives no scientific choice.** No threshold, capacity, rung, width or
  configuration value is computed, inferred, or filled in. In role mode they come only from the
  authenticated record and are checked against the config/output bytes; in fixture mode they are
  visibly fabricated fixture fields.
- **V4 — Mode-specific parsers have no scientific defaults.** Tests assert the exact argument set
  and requiredness for each 4.2 subcommand, that fixture mode rejects every role argument, that
  role mode rejects every fixture argument, and that neither parser exposes a provenance,
  authority, split or role-allowlist override. `argparse`'s help action is excluded explicitly;
  mutually exclusive mode selection is asserted at the subparser boundary, not by the impossible
  requirement that both alternatives have `required=True`.
- **V5 — Fail closed on roles.** An absent role root, an absent index, or a role not named by the
  connection record refuses with its own distinct code and produces no scene and no figure.
- **V6 — Identities, pairing and the playback clock travel.** Before constructing a real scene,
  tests require exact config/checkpoint/index/payload digests and exact agreement on `pair_id`, all
  schema-D label fields, onset, `task_reference` and the C1/S plant time grids. Scene construction
  binds that exact grid once as `playback_t_s`, requires every body/tracking/controller leading
  axis to have its length, requires both `controller_logs.t_s` arrays to equal it exactly, and
  rejects an out-of-range frame. A one-element mismatch refuses with the corresponding identity,
  pair or timebase code.
- **V7 — Provenance is computed, never supplied.** There is no CLI argument or public builder
  keyword that sets the provenance state directly. A test asserts a fixture-built scene cannot be
  relabelled through either public construction path.
- **V8 — Real provenance is currently unreachable, and provably so.** A test asserts that no
  input presently in the packet yields `DEVELOPMENT_ONLY` or `FINAL`. When a connection record is
  added, the test goes red and is replaced only as part of that record's separate review.
- **V9 — Every non-`FINAL` scene renders its banner.** A test renders each currently reachable
  provenance state and asserts the banner text is present in the figure's artists — not in a
  caption, not in a filename. Fixture truth, when present, also renders `FABRICATED TRUTH`.
- **V10 — A renderer opens no scientific input.** A test calls both surfaces with a bundle while
  the working directory contains no roles at all and asserts they render. The scripted wrapper may
  write only the declared PNG/JSON/digest outputs beneath its supplied output directory; the pure
  painter and interactive wrapper perform no file I/O.
- **V11 — The banner is inside the PNG.** Asserted on the saved figure's artists and by inspecting
  the saved PNG bytes. **The resolution half of this check is made in the domain the value is
  stored in.** PNG records resolution in the `pHYs` chunk as *integer* pixels per metre, so a
  figure written at exactly `dpi=300` stores `round(300 / 0.0254) = 11811`, which back-converts to
  `299.9994` — a test asserting "recovered DPI >= 300" goes red on a correct figure. Measured this
  session. The test therefore asserts that the scripted path's declared `savefig` DPI is exactly
  300 and that the saved `pHYs` payload is exactly `(11811, 11811, 1)`: horizontal and vertical
  pixels per metre both equal `round(300 / 0.0254)`, and the unit specifier is metres. Same repair
  shape as finding AV: compare in the domain the value was persisted in.
- **V12 — Bundle and scene JSON are canonical and round-trip.** Serialize, strict-parse with the
  section-4.1 non-standard-constant refusal, then serialize is byte-identical under the packet's
  existing canonical-JSON rules.
- **V13 — The scripted path is deterministic and complete.** The same bundle rendered twice under
  the pinned environment produces byte-identical PNG and JSON sets; the fixture at a fixed seed
  produces a byte-identical bundle; output case IDs equal bundle case IDs exactly.
- **V14 — No cross-arm derived scalar exists.** A test asserts the scene schema and both renderers
  contain no field or label carrying a C1-versus-S difference, ratio or reduction.
- **V15 — Schema and metric mappings are exact, and the metric is actually called.** The
  decision-field set equals the machine schema's `estimator_outputs` fields; tracking arrays come
  from `plant`. **A test calls the live `utils.metrics.j_5s` with `playback_t_s` on every arm of
  every fixture scene, at that scene's `onset_time_s` and `window_s`, and requires it to return a
  finite value** — the
  unconditional half of this invariant, and the only thing that makes section 4.1's property 2
  checkable in a round with no recorded value to compare against. Tests also assert the four
  refusal shapes: a non-uniform grid, an off-sample onset, a grid ending before
  `onset_time_s + window_s`, and a non-finite tracking sample each refuse scene construction with
  `X_WINDOW_UNSUPPORTED` rather than reaching a renderer. Where an authenticated recorded value
  exists, `j_5s` on the scene's arrays must additionally reproduce it.
- **V16 — The body and call panels share one causal timeline.** Each fixture case has two
  time-varying centerlines, and a test asserts `draw_scene` at two different in-range `frame`
  values produces different body artists for the same scene — otherwise the animation requirement
  is satisfied by a still. The two arms at one frame must identify the same
  `playback_t_s[frame]`. On a fixture whose visible decision state changes, tests assert that a
  frame before the first decision renders `NO DECISION YET`, an intermediate frame renders the
  greatest decision time not later than that frame, and no frame renders a future or final
  decision early. Non-monotone/out-of-extent decision axes refuse with
  `X_DECISION_UNSUPPORTED`. The scripted still's frame is the derived one in section 4.6 and is
  asserted to be the shared control sample at `onset_time_s + window_s`. The future real adapter
  must check the distal centerline point against `true_task_output` within a declared tolerance
  and refuse a geometry mismatch.
- **V17 — The fixture bundle exercises the visible failure branches.** Its named scenes jointly
  cover confident correct, confident wrong, abstention, high unknown, `NO DECISION YET`, a later
  changed decision state and an indistinguishable C1/S case; tests inspect the rendered artists
  and menu entries, not only the fixture arrays.
- **V18 — Rendering trains and simulates nothing.** The scene, fixture and renderer modules import
  neither `torch` nor `mujoco`, asserted in a fresh interpreter. The later role adapter must remain
  read-only; if reusing the current role validator would pull in `torch`, it must first separate
  the dependency-light schema validation rather than duplicate or weaken it.
- **V19 — Non-finite schema values survive the round trip and are never silently repaired.** A
  test builds a scene carrying `severity_uncertainty = +inf` and a pre-detection
  `detection_time_s = NaN`, serializes it with `allow_nan=False`, and strict-loads it with a
  `parse_constant` callback that would raise on any bare `NaN`, `Infinity` or `-Infinity`. The
  decoded values must satisfy `isinf` with positive sign and `isnan`, and re-serializing the
  decoded scene must reproduce the original canonical bytes; ordinary object equality is not the
  oracle because IEEE-754 NaN is unequal to itself. A codec-level test pins all three exact string
  mappings, including negative infinity, and asserts that any other string in a typed float
  position refuses loudly rather than decoding to a number. Mutant documents carrying each bare
  non-standard token must also refuse through `parse_constant`. A further test asserts the
  renderer draws `UNAVAILABLE` for the infinite scale rather than a plot extent.

V18 is worth one sentence of justification, because it looks like an over-constraint. The scene
layer consumes a fixture now and authenticated recorded roles later — it does not run an estimator
and does not step a plant. Keeping the two heavy dependencies out is what makes the Slot-8 surface
openable by a reader who installed the packet on a laptop, which is the entire point of Slot 8
living inside the packet.

---

## 6. What the artifact must not do — and must say it does not do

These four appear **in the artifact**, not only in this document. The first three are printed by
the renderer; the fourth is enforced by V14.

1. **It does not answer the Claim Sheet's question.** The demo shows one comparison at a time on
   named inputs. The project's question is answered by the confirmatory protocol, not by a
   picture.
2. **A synthetic fixture is not evidence.** Rendered on every fixture scene, adjacent to the
   banner, in words rather than in a code.
3. **A development-only scene is a record of the development split and nothing else.** It is not a
   result, not a baseline, not a validation.
4. **No cross-arm derived number appears anywhere in this round.** Both arms' quantities are shown
   side by side, which is what Slot 8 asks for; `tracking_reduction_pct` and every other
   C1-minus-S scalar stay out. This is not squeamishness. A single reduction number rendered under
   two robots is read as a headline, and the confirmatory comparison that would license one has
   not been run. Whether the reduction appears when a real result is connected is decided **then**,
   under that authorization, and section 8 decision D3 hands the question over rather than settling
   it here.

---

## 7. Cost

**Unmeasured, and deliberately not estimated from memory.** The module runs no fit, no rollout and
no physics; its expected cost is figure rendering, which the packet has never had to time. The
build round will report measured wall-clock for: one scene construction from the fixture, one
scripted figure write at 300 DPI, and the full fixture set. The interactive surface is not timed —
it is interactive.

What is already known and is not free: the packet's full test suite is 2,108 tests at roughly
127 s, and this lane will add to it.

---

## 8. Decisions I am handing over rather than taking alone

- **D1 — RESOLVED: design, then module.** The split is right. The field/source and authorization
  defects found in this review are exactly the class that should be corrected before code exists.
- **D2 — RESOLVED CONDITIONALLY: `matplotlib.widgets` is sufficient for the scaffold.** The pinned
  3.11.0 environment exposes `RadioButtons`, `Button`, `Slider` and `FuncAnimation`, so it can
  discharge A1/A2 without a new dependency. The module review must demonstrate menu selection,
  play/pause and timeline control; failure there returns the surface choice to review.
- **D3 — RESOLVED FOR THIS ROUND ONLY: no cross-arm scalar.** Whether a later authorized final
  scene shows one is decided with the connection record, after the confirmatory result exists.
- **D4 — RESOLVED: fixture truth may render, but only as `FABRICATED TRUTH`.** It makes the
  confident-wrong branch legible without placing an unqualified correctness mark next to invented
  data.

---

## 9. Sequencing

1. **This document is reviewed and frozen.** Codex reviews it at an exact state; both agents
   approve the same bytes. Nothing is built before that.
2. **The scene, fixture, renderers and fail-closed role stub are built and reviewed.**
   `scripts/utils/verification_scene.py` (the scene and fixture) and
   `scripts/render_verification_scene.py` (both surfaces), plus tests carrying V1 through V19.
   The role subcommand can only emit `X_CONNECTION_UNAUTHORIZED` before reads in this step.
   Exact-state review cycle.
3. **The fixture figure set is generated and reviewed.** Scripted path only; scenes and figures
   written into the packet; runbook step added to the packet README.
4. **Connecting a real result is a separate connection-record design, exact-state review and joint
   authorization** that neither this document nor the closing of steps 1 to 3 grants. It adds the
   read-only role adapter against the already-frozen scene schema and renderers, and requires, at
   minimum, the inputs section 1.1 lists as absent. A final test split is neither licensed now nor
   permanently designed out; only the later exact authorization can name it.

Steps 1 to 3 are inside what Codex's Session-122 boundary authorizes. Step 4 is not, and this
document does not pre-approve it.
