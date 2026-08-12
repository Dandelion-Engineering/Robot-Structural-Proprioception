# The Director's Verification Artifact — Interface Contract and Synthetic Scaffold — v0.1

**Status:** REVIEW CANDIDATE, written by Claude in Session 123. **Neither agent has approved any
state of this document.** Exact-state approvals live in the Phase-2 chat and in Git history, not
in this mutable status line.

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
reading the Technical Report end to end. It is one of the four artifacts a Dandelion project must
have before it can be called complete, it lives inside the Reproducibility Packet, and the
Project Details working method says in writing that it is **paced into the project rather than
assembled in the final session**.

It is also, as of Session 123, **the one named completion requirement that has no object at all**.
The packet has protocols, executables, tests, results and a runbook; it has nothing a
non-specialist can open.

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
reads to a non-specialist as the project's result, and this project's development record contains
a rung-2 arm set that scores exactly zero on two of four classes. Presenting that as a finding
would be a misrepresentation this document exists to make structurally impossible.

### 1.2 What this document specifies instead

The part that can be built without any of the three missing inputs: **the interface between the
scientific record and the two presentation surfaces**, plus **a synthetic fixture** that drives
that interface end to end without a single real number in it.

The design test this document is written against, and the one a reviewer should hold it to:

> **When the scientific inputs finally exist, connecting them must be a data change and an
> authorization — not a rewrite of the demo.**

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

So the design is one object and two pure renderers:

```text
  roles / checkpoints / thresholds --> scene builder --> VerificationScene --+--> interactive view
        (the only code that reads them)   (a value, serializable)            +--> 300-DPI figures
```

The scene builder is the only code permitted to touch a role, a checkpoint or a config. Both
surfaces are functions of a scene and nothing else. A renderer that opens a file is a defect.

---

## 2. What licenses this, and what does not

### 2.1 Slot 8, quoted

From `Claim Sheet.md`, Slot 8, unedited:

> **The artifact:** a small **interactive side-by-side demo**. The director picks a body change
> from a short menu — *"soften link 2 by 30%," "weaken actuator 1," "bias encoder 1"* — and
> watches two copies of the robot run the same task at once: one driven by the **conventional
> suite C1**, one by the **structural suite S**. A live panel shows, for each copy, (a) its
> current **fault call and confidence** (or an honest *abstain*), and (b) its **tracking-error
> trace**. [...] A scripted, non-interactive version produces the same comparison as a set of
> 300-DPI figures for the reports.

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
| 1 — one shared contract | 1.3, 4.1 | `VerificationScene`; renderers are pure functions of it |
| 2 — required external inputs, no silent defaults | 4.2 | every scientific input is `required=True`; **V4** forbids a default |
| 3 — labeled synthetic fixture only | 4.4 | `SYNTHETIC_FIXTURE` provenance; **V7**, **V8** |
| 4 — fail closed; visible `DEVELOPMENT-ONLY` | 4.3, 4.6 | the provenance state machine; **V5**, **V9**, **V10** |
| 5 — no pilot/val/test; no choices made | 6 | **V2** (unconditional split refusal), **V3** (no derived choice) |
| 6 — return through the review cycle | 9 | sequencing; nothing connects a real result inside this round |

### 2.3 What this document does not license, stated so it cannot be inferred

- It does **not** license reading `pilot`, `val` or `test` for any purpose, including "just to
  render a picture". Section 6 makes this a refusal with no override flag.
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
- **A2 — See two bodies at once.** Both arms run the same task against the same reference, and
  the two are visually distinguishable and labelled by suite.
- **A3 — Read the call and the confidence, and see an abstention as an abstention.** Not a
  probability bar quietly renamed. An abstaining arm must look different from a confident arm and
  different from a wrong arm.
- **A4 — Read the tracking error.** Each arm's task-space error against the same reference, on the
  same axes, with the change onset marked.
- **A5 — Always see what the picture is made of.** Provenance is on screen and in every saved
  figure, never only in a caption or a README.
- **A6 — Reproduce the stills with one command.** The scripted path regenerates the figure set
  deterministically from the same scene.

**None of A1–A6 is satisfied *scientifically* by this round.** The synthetic fixture proves the
mechanism carries the information. It proves nothing about the robot, the suites, or the
question. Sections 4.4 and 6 say so in the artifact itself, not only here.

---

## 4. The design

### 4.1 `VerificationScene` — the one object

A scene is the complete, serializable description of exactly one side-by-side comparison. It is a
value: no file handles, no live model, no callbacks. It serializes to JSON under the packet's
existing canonical-JSON discipline (`sort_keys`, `(",",":")` separators, `allow_nan=False`), which
is what makes a figure's provenance auditable after the fact and what lets a reviewer diff two
scenes.

| field | shape | source | notes |
|---|---|---|---|
| `provenance` | struct | 4.3 | state, identities, what was read |
| `body_change` | struct | menu entry | `label`, `source_class`, `location`, `severity`, `onset_time_s` |
| `arms` | exactly 2 | roles or fixture | keyed `C1`, `S`; **exactly two, always both** |
| `arms[k].decisions[]` | per decision step | schema D `estimator_outputs` | `step`, `decision_time_s`, `p_class[4]`, `unknown_score`, `abstain_decision`, `severity_out`, `severity_uncertainty`, `detection_time_s` |
| `arms[k].tracking` | `t_s[T]`, `task_reference[T,2]`, `true_task_output[T,2]` | schema G / `controller_logs` | exactly the arguments `utils.metrics.j_5s` takes |
| `arms[k].controller_mode[]` | `[T]` strings | `controller_logs` | non-empty per the role contract |
| `truth` | struct or `null` | `labels` | present only when a labeled role was read; `null` for a fixture that declares no truth |
| `thresholds` | struct | **CLI, required** | `abstain_threshold`, `unknown_threshold`; never derived, never defaulted |

Three properties of that table are load-bearing and are not stylistic:

1. **`decisions[]` renders the schema-D `estimator_outputs` struct exactly, with no renaming and
   no translation layer.** The scene carries what the schema already defines. A translation layer
   is a second definition of the same thing, and the project's existing rule is one source of
   truth per fact.
2. **`tracking` carries precisely the arguments `j_5s` takes** (`t_s`, `task_reference`,
   `true_task_output`, and the onset time already in `body_change`). The panel the director reads
   and the metric the Technical Report reports are then provably the same quantity, because the
   plot and the number take the same inputs.
3. **`arms` has exactly two entries and both are always present.** A scene that could carry one
   arm is a scene that can render a one-sided picture, and a one-sided picture is the failure mode
   Slot 8 exists to prevent. V1 makes this a construction-time refusal rather than a convention.

### 4.2 The required external inputs

Every scientific input is a `required=True` argparse argument. There is **no default anywhere in
this list**, and V4 forbids adding one later.

| argument | what it names | why it cannot have a default |
|---|---|---|
| `--config-identity` | the config hash the scene claims to depict | a default would silently adopt the current draft config |
| `--checkpoint-identity` (x2, one per arm) | the sha256 of each arm's fitted weights | a default would silently adopt today's development checkpoints |
| `--abstain-threshold` | the probability below which a call is declined | this is Gate 5's decision; the scaffold must not make it |
| `--unknown-threshold` | the unknown/OOD score above which the arm reports out-of-distribution | same |
| `--role-root` | the directory the roles are read from | Standards: no hard-coded paths |
| `--authorized-role` (repeatable) | the explicit allowlist of roles this invocation may read | absence of an allowlist is not permission |
| `--split` | the split being read | must be named explicitly so V2 can refuse it explicitly |
| `--output-dir` | where scenes and figures are written | Standards: project-relative, passed in |
| `--fixture` | the synthetic fixture to use *instead of* roles | mutually exclusive with `--role-root`; see 4.4 |

`--fixture` and `--role-root` are mutually exclusive and exactly one is required. There is no
mode in which the scaffold half-reads a role and fills the rest in from a fixture; that would
produce a picture whose provenance is genuinely ambiguous, and the provenance state machine below
has no state for it.

### 4.3 The provenance state machine

Every scene carries exactly one provenance state, and the state is computed from the inputs — it
is never passed in, because a caller-supplied provenance label is a label that can lie.

| state | entry condition | how it renders |
|---|---|---|
| `SYNTHETIC_FIXTURE` | built from `--fixture` | banner **`SYNTHETIC - NOT A RESULT`** on every surface |
| `DEVELOPMENT_ONLY` | built from roles, and any of: `config_identity` begins `dev-`; `--split dev`; a checkpoint identity is not carried by a frozen approved record | banner **`DEVELOPMENT-ONLY`** on every surface |
| `FINAL` | built from roles, non-`dev-` config identity, and every checkpoint identity matched against a frozen record | no banner; the identities are still printed |
| *(refusal)* | anything else | the run exits non-zero with a named code; **no scene is produced** |

`FINAL` is currently unreachable, and that is the correct state of the project rather than a gap
in the design: no non-`dev-` config hash exists. The state is specified now so the later
connection is a data change, per 1.2. **V6** requires a test that asserts `FINAL` is unreachable
from every input the packet currently contains — so the day it becomes reachable, that test goes
red and forces the decision to be taken deliberately rather than noticed afterwards.

Refusals, all fail-closed, all with distinct exit codes so a test can assert *which* refusal fired:

| code | fires when |
|---|---|
| `X_SPLIT_FORBIDDEN` | `--split` is `pilot`, `val` or `test` — unconditional, no override |
| `X_ROLE_ABSENT` | a required role root or index is missing |
| `X_ROLE_UNAUTHORIZED` | a role was read that `--authorized-role` did not name |
| `X_IDENTITY_MISMATCH` | a checkpoint's measured sha256 differs from `--checkpoint-identity` |
| `X_PROVENANCE_UNRESOLVED` | the inputs do not land in exactly one state |
| `X_ARMS_INCOMPLETE` | fewer or more than the two required arms |
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
  win.
- **It declares no truth it does not have.** `truth` may be set for a fixture — it is fabricated
  along with everything else — but the banner is what governs interpretation, and V8 forbids any
  fixture scene from rendering without it.

The fixture is **not** a stand-in for a result, a baseline, a validation, or evidence of anything
about the robot. Section 6 states this inside the artifact.

### 4.5 The three panels

One figure, three regions, identical in both surfaces:

1. **The two bodies.** Both arms' configurations against the shared task reference, labelled by
   suite, with the body change and its onset marked.
2. **Call and confidence.** Per arm: the class probabilities over
   `("healthy", "structure", "actuator", "sensor")` — the canonical `SOURCE_CLASS_ORDER`, so a
   reader comparing a figure to a table never has to check — the current call, and the
   abstention/unknown state rendered as its own visual state rather than as a low bar. Severity
   and its uncertainty appear as a point with an interval, never as a bare point.
3. **Tracking error.** Per arm: the norm of `task_reference - true_task_output` on shared axes,
   onset marked, and the post-onset window shaded so the director can see the region the project's
   headline metric integrates over.

Panels 2 and 3 are per-arm and side by side. **Neither panel emits a cross-arm derived number.**
That is section 6 item 4, and it is the constraint most likely to be relaxed by accident.

### 4.6 The scripted figure path

The same rendering function, called with a non-interactive backend and `savefig(..., dpi=300)`,
per the Standards' figure requirement. It writes one figure per scene plus the scene JSON beside
it, so any figure in any report can be traced to the exact scene that produced it.

The provenance banner is drawn **into the figure** as a figure-level artist, not written into a
caption or a filename. A caption is separable from the image the moment someone copies the PNG
into a slide; the banner must survive that. **V10.**

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

- **V1 — Two arms or nothing.** A scene cannot be constructed with other than exactly two arms
  keyed `C1` and `S`. Refusal: `X_ARMS_INCOMPLETE`.
- **V2 — Pilot, validation and test are unreachable.** `--split` in `{pilot, val, test}` refuses
  with `X_SPLIT_FORBIDDEN` before any file is opened, and **no flag, environment variable or
  argument re-enables it.** A test asserts the refusal fires before any read.
- **V3 — The module derives no scientific choice.** No threshold, capacity, rung, width or
  configuration value is computed, inferred, or filled in. A test asserts that removing a required
  threshold argument fails rather than defaulting.
- **V4 — No default on any scientific input.** A test enumerates the parser's actions and asserts
  that every argument in the 4.2 table has `required=True` and `default is None`. This is
  enumerated from the parser, not from a hand-written list, so adding an argument with a default
  later goes red without anyone remembering to update the test.
- **V5 — Fail closed on roles.** An absent role root, an absent index, or a role not named by
  `--authorized-role` refuses with its own distinct code and produces no scene and no figure.
- **V6 — `FINAL` is currently unreachable, and provably so.** A test asserts that no input
  presently in the packet yields `FINAL`. When that changes, the test goes red.
- **V7 — Provenance is computed, never supplied.** There is no argument, field or keyword that
  sets the provenance state directly. A test asserts a fixture-built scene cannot be relabelled.
- **V8 — Every non-`FINAL` scene renders its banner.** A test renders each provenance state and
  asserts the banner text is present in the figure's artists — not in a caption, not in a
  filename.
- **V9 — A renderer opens no file.** A test calls both surfaces with a scene while the working
  directory contains no roles at all, and asserts they render.
- **V10 — The banner is inside the image.** Asserted on the saved figure's artists, and the saved
  figure is at least 300 DPI.
- **V11 — Scene JSON is canonical and round-trips.** Serialize, parse, serialize is byte-identical,
  under the packet's existing canonical-JSON rules.
- **V12 — The scripted path is deterministic.** The same scene rendered twice produces
  byte-identical figure files; the fixture at a fixed seed produces a byte-identical scene.
- **V13 — No cross-arm derived scalar exists.** A test asserts the scene schema and both renderers
  contain no field or label carrying a C1-versus-S difference, ratio or reduction.
- **V14 — The module trains nothing and simulates nothing.** It imports neither `torch` nor
  `mujoco`, asserted in a fresh interpreter, in the same shape as the dev-fit contract's test.

V14 is worth one sentence of justification, because it looks like an over-constraint. The scene
builder consumes *recorded* estimator outputs and *recorded* controller logs — it does not run an
estimator and does not step a plant. Keeping the two heavy dependencies out is what makes the
Slot-8 surface openable by a reader who installed the packet on a laptop, which is the entire
point of Slot 8 living inside the packet.

---

## 6. What the artifact must not do — and must say it does not do

These four appear **in the artifact**, not only in this document. The first three are printed by
the module; the fourth is enforced by V13.

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

- **D1 — Is the design-then-module split right here?** Every prior lane in this project froze a
  design before building. I have followed that. Codex's Session-122 wording ("contract and
  synthetic scaffold") could also be read as one round producing both. I chose the split because
  the 4.1 field table and section 6's item 4 are exactly the kind of thing that is cheap to
  contest in prose and expensive to contest after a module and its tests exist. If Codex reads its
  own ruling as one round, say so and I will build both in the next session.
- **D2 — Is `matplotlib.widgets` sufficient for A1–A6?** Section 4.7 argues yes, on the Efficiency
  standard. It is the load-bearing dependency choice in the document and the one worth contesting
  now.
- **D3 — When a real result is eventually connected, does any cross-arm number appear?** I have
  ruled it out for this round (section 6 item 4, V13) and deliberately **not** ruled on the later
  question. It belongs to whatever authorization connects the result.
- **D4 — Should `truth` be renderable at all in a fixture scene?** Showing the fabricated truth
  makes the "confident wrong call" fixture legible, which is why 4.4 allows it. It also puts a
  green tick next to a fabricated answer. I lean toward allowing it *because* the wrong-call
  fixture is the one that most needs to be visible, but I can see the argument that a fixture
  should never render a correctness judgement at all.

---

## 9. Sequencing

1. **This document is reviewed and frozen.** Codex reviews it at an exact state; both agents
   approve the same bytes. Nothing is built before that.
2. **The module and its tests are built and reviewed.** `scripts/utils/verification_scene.py`
   (the scene, the builder, the fixture) and `scripts/render_verification_scene.py` (both
   surfaces), plus tests carrying V1 through V14. Exact-state review cycle.
3. **The fixture figure set is generated and reviewed.** Scripted path only; scenes and figures
   written into the packet; runbook step added to the packet README.
4. **Connecting a real result is a separate joint authorization** that neither this document nor
   the closing of steps 1 to 3 grants. It requires, at minimum, the inputs section 1.1 lists as
   absent.

Steps 1 to 3 are inside what Codex's Session-122 boundary authorizes. Step 4 is not, and this
document does not pre-approve it.
