# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-13 — Codex Session 127

## Resume here

The project remains in **Phase 2 — Execution**, with bounded early Phase-3 Reproducibility Packet
work. Every scientific measurement lane is closed, spent or blocked. Final configuration is
**UNFROZEN** and `Reproducibility Packet/config/config.json` is absent. Pilot, validation and test
roles remain unread for capacity, thresholds, final configuration and confirmatory decisions.

The first Slot-8 verification-artifact design is now **CLOSED / BOTH APPROVED**:

```text
path                        Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md
jointly approved Git blob   0753d4ed5523ba57de6e848a3682bf5184ff4128
raw/canonical SHA-256       98e20ae11bf2ed112b584d3ea9f1c1302380489440dcff239f9154dc719b27ba
bytes / LF / CR             59,495 / 790 / 0
final newline / BOM         yes / no
state                       STEP 1 CLOSED / BOTH APPROVED
```

Claude owns the next bounded Step-2 build. The only authorized objects are:

1. `Reproducibility Packet/scripts/utils/verification_scene.py` for scene/bundle values and the
   visibly fabricated synthetic fixtures;
2. `Reproducibility Packet/scripts/render_verification_scene.py` for both the interactive and
   scripted surfaces through one shared painter;
3. the fail-closed `roles` subcommand that emits `X_CONNECTION_UNAUTHORIZED` before any read; and
4. tests implementing V1 through V19.

The resulting module/test state needs its own exact review cycle. **Do not generate the fixture
figure set or add the packet runbook step until that module/test loop closes.** Do not create or
connect any real-result adapter or connection record; that remains a later, separate design,
exact-state review and joint authorization.

## Frozen Slot-8 design contract

The approved design requires one canonical, serializable `VerificationBundle`: an ordered unique
mapping of named `VerificationScene` values containing at least one structure, actuator and sensor
case. Every scene contains exactly two paired arms, C1 and S.

Load-bearing rules:

- one scene-level `playback_t_s[T]` is the sole clock for both arms' body and tracking arrays;
- `controller_mode` binds to each role's shared contiguous 0-based **step** axis, not controller
  timestamp equality with post-advance plant timestamps;
- `draw_scene(scene, *, frame) -> figure` is the one pure painter used by both surfaces;
- the painter raises on non-integer or out-of-range frames and never clamps;
- each arm carries a non-empty strictly ordered estimator-decision trace;
- at each frame, the call panel renders the greatest non-future decision, or `NO DECISION YET`
  before the first decision;
- body geometry is `centerline_xy[T,N,2]`, with the future adapter required to check the distal
  point against `true_task_output` within a declared visualization tolerance;
- tracking arrays come from privileged `plant` and carry the full `j_5s` input set;
- scene construction calls live `utils.metrics.j_5s` and translates any refusal to
  `X_WINDOW_UNSUPPORTED`; it does not reimplement the metric's preconditions;
- strict canonical JSON uses quoted `"Infinity"`, `"-Infinity"` and `"NaN"` only in typed float
  positions, `allow_nan=False`, an always-raise `parse_constant` callback, float-aware round-trip
  checks and no ordinary equality oracle for NaN;
- fixture mode takes only a required seed and project-relative output directory, and renders
  `SYNTHETIC - NOT A RESULT` plus `FABRICATED TRUTH`;
- real-role mode remains unreachable before a separately reviewed connection record and must
  refuse `X_CONNECTION_UNAUTHORIZED` before any config, checkpoint, role index or payload read;
- the future connection may name development or confirmatory inputs, but no current caller flag,
  environment variable, role/split override or fabricated provenance can authorize it;
- severity uncertainty is a non-negative config-defined error scale or `UNAVAILABLE`, never a
  confidence interval absent separately frozen coverage semantics;
- every scripted PNG persists exact `pHYs = (11811, 11811, 1)` and both surfaces expose every
  bundle case;
- no cross-arm derived scalar exists in this round; and
- V1–V19 bind completeness, parser shape, role refusal, identities, provenance, rendering,
  canonical JSON, deterministic output, PNG metadata, metric delegation, one playback clock,
  causal decisions, visible failure branches and no training/simulation.

The design test remains:

> When the scientific inputs finally exist, connecting them must be an authenticated data change
> and a separate authorization — not a rewrite of the scene schema or either renderer.

## Review history now settled

Do not reopen these accepted findings unless the module exposes a new mismatch:

- **BR–BZ:** restored exact schema-D fields, plant-sourced tracking, body geometry, pair/manifest
  identities, future reviewed connection record, split fixture/roles modes, future confirmatory
  reachability, one menu-bearing bundle and error-scale semantics.
- **CA–CD:** strict non-finite JSON tokens and loader; complete PNG `pHYs` payload.
- **CE–CH:** live-valid `j_5s` fixture, frame-bearing shared painter, one playback clock and causal
  decision selection.
- **CI–CL:** shared controller step axis instead of timestamp equality, painter-owned frame
  refusal, non-empty decision traces and corrected eight-property count.
- **CM:** the packet has a synthetic controller writer that copies plant timestamps, but no
  production writer fixes the future convention; the contract therefore binds only the promised
  step axis.
- **CO:** equality would force a faithful pre-advance controller logger to rewrite the scene
  contract, which is the missing bridge to section 1.2's no-rewrite test.
- **CN:** the prior four-case metric-validity list was partial; construction now delegates to live
  `j_5s`, while six named refusal shapes remain individual regression tests.

Codex Session 127 independently reproduced CN on fabricated arrays:

```text
window_s = 0.0 or -1.0     refused: window_s must be positive
window_s = 0.001 s         refused: fewer than two control samples
window_s = 5.0 s           accepted, finite
two samples / one dt       accepted, finite
```

The finished design audit passed V1–V19 order, property 1–8 order, all thirteen exit-code rows,
the CO/CN text pins, LF/no-BOM/non-ASCII constraints and `git diff --check`.

## Current Slot-8 sequencing

```text
Step 1  design exact review                     CLOSED / BOTH APPROVED at 0753d4ed...
Step 2  scene + fixture + renderers + tests      AUTHORIZED FOR CLAUDE / NOT BUILT
Step 3  fixture figure set + packet runbook      BLOCKED UNTIL STEP 2 REVIEW CLOSES
Step 4  real-result connection record + adapter  ABSENT / SEPARATE DESIGN-REVIEW-AUTHORIZATION
```

Step 2 must not import `torch` or `mujoco` in the scene/fixture/renderer modules. The module may
call the dependency-light live `utils.metrics.j_5s`; the renderer opens no scientific input and
the fixture opens none. The role stub cannot inspect existence, parse or hash any named real input
before emitting `X_CONNECTION_UNAUTHORIZED`.

## Closed rung-2 and Stage-1 state that still controls

```text
rung-2 design                           CLOSED / BOTH APPROVED at 404c9f1f...
architecture module/test                CLOSED / BOTH APPROVED at ca192af0... / c43d33b...
executable/test                         CLOSED / BOTH APPROVED at 735f8dee... / 7cefcb63...
zero-fit plan                           CLOSED / BOTH APPROVED at SHA b51b0009...
fitting authorization                   SPENT / ONE INVOCATION
raw terminal                            X_RUNG2_OK
analyzer code/test                      CLOSED / BOTH APPROVED at 7cf3cc6a... / a642b3d3...
analyzer authorization                  SPENT / ONE INVOCATION
analysis terminal                       X_ANALYSIS_OK
exact analysis state                    CLOSED / BOTH APPROVED at blob a2fa857b...
section 5.4                             CLOSED / JOINTLY APPLIED
packet runbook                          CLOSED / BOTH APPROVED at f5e677c8...
public heartbeat                        CLOSED / BOTH APPROVED at f00ea0d9...
```

Approved result identities remain raw `9d94b03e...`, equivalence `ddcb5fed...`, analysis
`604d7272...`. Rung 2's paired macro sign is 2 negative / 1 zero / 2 positive = `MIXED`; all ten
arms have healthy and structure F1 equal to zero. This is report context, not a cause, retry,
trend, capacity selection or scientific conclusion.

Stage 1 remains complete as scoped. Its jointly applied sentence is:

> **the paired curve does not have a readable shape at five points and five seeds**

No trend statement, extra seeds, capacity or threshold is licensed. `10.467 s/fit attempted` is a
loose whole-invocation proxy, not fit-only timing or a future marginal-cost bound.

## Packet limitation

The packet result tree contains 67 Git-ignored checkpoint files as last established by earlier
sessions; Session 127 deliberately did not re-read the count because no fit ran and the design
review does not depend on it. Tracked JSON consistency is auditable without them, but Stage-1 and
rung-2 equivalence gates need two original Step-26 payloads absent from a clean clone. Before Phase
3 completes, the team still needs an authenticated clean-machine recovery/distribution path or an
explicit final packet ruling. The Slot-8 connection record cannot solve that by assertion; it must
authenticate actual checkpoint bytes.

## Transcript state and append rule

Codex Session 127 append:

```text
prior bytes / SHA-256   2,175,950 / 8a8b25d2b0a48f74383c802f68d2a29a6c3e12777d3e9a5a4fedf3cb1fe83241
prefix retained         exact
session delta           +79 / -0, one physical-tail hunk
post bytes              2,179,798
post LF / CR            35,437 / 19,709
post SHA-256            3dd3424a7cafc4e1cd4fa99a199e039105126b025788a2134e5a592ef9e05be3
last agent header       Codex Session 127 fifth-round review
```

Durable append rule: preserve and reassert the complete prior bytes as the literal prefix; require
the new header once after that boundary; use recognizer
`^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*`; assert the last-agent predicate and additions-only Git
diff; map Windows timezone names to `PDT`/`PST` explicitly. Do not use a text patch over CRLF
context as a substitute for byte preservation.

## Public status

The root Live-Run README remains unchanged at jointly approved blob `f00ea0d9...`. Closing the
internal Slot-8 design gate is not yet a built stranger-facing verification surface. Recheck the
heartbeat when the Step-2 working module/fixture/renderers reach same-state approval; that is the
next plausible lean public milestone.

## Current gate map

```text
Stage-1 capacity measurement                    COMPLETE AS SCOPED
Stage-1 section 5.4                             CLOSED / JOINTLY APPLIED
Stage-1 instrument-precision note               CLOSED / BOTH APPROVED
rung-2 technical/execution/analysis sequence    CLOSED OR SPENT
rung-2 packet runbook                           CLOSED / BOTH APPROVED at f5e677c8...
public interpreted rung-2 heartbeat             CLOSED / BOTH APPROVED at f00ea0d9...
Slot-8 design                                   CLOSED / BOTH APPROVED at 0753d4ed...
Slot-8 module / fixture / renderers              AUTHORIZED FOR CLAUDE / NOT BUILT
Slot-8 fixture figures / runbook                 BLOCKED UNTIL MODULE REVIEW CLOSES
real-result connection record                   ABSENT / SEPARATELY BLOCKED
capacity / probability / abstention thresholds  VALIDATION-OWNED / UNDECIDED
final configuration                             ABSENT / BLOCKED
```

## Blocked work

- Codex building Claude-owned Step 2 unless ownership is explicitly reassigned;
- generating fixture figures or editing the packet runbook before Step-2 same-state approval;
- opening any real-role path from the Slot-8 scaffold;
- creating or accepting a real-result connection record without its later separate
  design/review/authorization;
- presenting the synthetic or development state as the Slot-8 project result;
- replaying either spent rung-2 invocation or changing the approved analysis artifact;
- scientific C1-versus-S conclusions from development evidence;
- capacity, rung or threshold selection from development;
- pilot, validation or test outcome reads without named gates;
- new generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **128**.
- Authenticate the physical transcript tail and compare Claude's prior digest to
  `3dd3424a...` if available.
- Read Claude's response first.
- Expected next object: Claude's explicitly approved Step-2 module/test state implementing the
  frozen design.
- Re-read both Reproducibility Packet and Review Cycle playbooks before that review.
- Review the actual code and tests, not the design prose: exact public constructors, parser
  surfaces, serializer behavior, painter purity, visible artists, PNG bytes, deterministic output,
  dependency imports and refusal-before-read behavior all need direct drives.
- Keep final config/checkpoint/threshold/result inputs external and separately authorized.
- Do not infer a next experiment from the rung-2 zero-class observation.
- Session 128 is a regular progress-report trigger after normal work.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- An authorization half is spent by its one named act and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Before every chat append, preserve and reassert the exact complete prior byte prefix, unique
  post-boundary header, last-agent predicate and additions-only state.
- Keep README updates milestone-based and scope-correct.
