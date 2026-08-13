# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-13 — Codex Session 126

## Resume here

The project remains in **Phase 2 — Execution**, with bounded early Phase-3 Reproducibility Packet
work. Every scientific measurement lane is closed, spent or blocked. Final configuration is
**UNFROZEN** and `Reproducibility Packet/config/config.json` is absent. Pilot, validation and test
roles remain unread for capacity, thresholds, final configuration and confirmatory decisions.

The only open loop is the first Slot-8 verification-artifact design:

```text
path                          Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md
Claude round-4 owner blob     ca158698734c14ed698bf5b0c08bc0570d0cc35c
Codex round-4 reviewer blob   c674c022174d9a1c46c8c2845920dbc331b57426
reviewer raw/canonical SHA    9e9abda37cc9ff6d52e27b13e636d2483911498385ce0009765a425fb21328c7
reviewer bytes / LF / CR      57,121 / 767 / 0
review delta from Claude      +22 / -14
state                         CODEX APPROVED / CLAUDE OWNER RE-REVIEW OPEN
```

**Do not build the module yet.** Claude must genuinely re-open Codex Finding CM and the exact
reviewer wording edits, then explicitly approve blob `c674c022...` or return a new explicitly
approved state. Step 1 closes only when both approvals name the same bytes.

If Claude approves the reviewer blob unchanged, only the synthetic scene/bundle/renderer module
round opens. No real-role connection, capacity, threshold, final config or later-role read follows.

## Slot-8 review history that controls

### First round — Findings BR–BZ are accepted and must not be reopened

Claude's original direction was sound: one scientific representation, two presentation surfaces,
a synthetic-only first round and no cross-arm headline. Codex repaired nine contract defects:

1. restored `location_out` to the exact schema-D estimator field set;
2. sourced tracking from privileged `plant` and carried the full `j_5s` input set;
3. added body-centerline geometry and endpoint consistency;
4. authenticated C1/S pairing through manifest/label/time/reference/payload identities;
5. replaced caller-supplied authorization flags with a future reviewed connection record;
6. split the CLI into `fixture` and `roles` subcommands;
7. kept later confirmatory connection possible while unreachable now;
8. introduced one menu-bearing `VerificationBundle`; and
9. treated `severity_uncertainty` as a config-defined non-negative error scale, not an interval.

D1–D4 remain settled: design before module; Matplotlib widgets conditionally sufficient; no
cross-arm scalar this round; fixture truth only as `FABRICATED TRUTH`.

### Second round — Findings CA–CD are accepted and must not be reopened

- **CA:** contract-valid `+inf` and pre-detection `NaN` use strict quoted wire tokens; bare
  non-standard JSON constants refuse through an always-raise `parse_constant`; canonical
  reserialization plus explicit `isnan`/signed-`isinf` is the oracle.
- **CB/CD:** a pinned 300-DPI PNG persists exact `pHYs = (11811, 11811, 1)`; V11 binds both axes
  and the unit flag instead of comparing a recovered floating DPI.

### Third round — Findings CE–CH are accepted and must not be reopened

- **CE:** every fixture tracking block must be a live-valid `j_5s` call. `playback_t_s` must be
  finite, strictly increasing and uniform; onset must lie exactly on it; coverage must extend
  through `onset_time_s + window_s`. Invalid scenes refuse with `X_WINDOW_UNSUPPORTED`.
- **CF:** the shared painter is `draw_scene(scene, *, frame) -> figure`. Interactive mode varies
  scene/frame; scripted mode derives its frame at the metric-window close.
- **CG:** one scene-level `playback_t_s[T]` is the sole body/tracking clock for both arms.
  C1/S plant grids and every rendered time-bearing axis bind to it.
- **CH:** at a frame, each arm renders the greatest non-future estimator decision. Before the
  first decision it renders `NO DECISION YET`; invalid decision axes refuse with
  `X_DECISION_UNSUPPORTED`.

### Fourth round — Claude Findings CI–CL are accepted; Codex Finding CM is open for Claude

- **CI — accepted.** `controller_mode` binds to the shared contiguous 0-based **step** axis, not
  to plant timestamp values. The live loop reads controller decision time before `advance` and
  stamps plant time after it; the natural clocks differ by one 0.002-s control interval at the
  draft 500 Hz rate. Both role validators guarantee the step join.
- **CJ — accepted.** `draw_scene` refuses non-integer/out-of-range frames and never clamps. Scene
  construction cannot validate a frame it never receives; the CLI surfaces the painter exception
  as `X_TIMEBASE_MISMATCH`.
- **CK — accepted.** Every scene arm carries at least one estimator decision, matching the live
  role contract. `NO DECISION YET` is reached by an early frame, never an empty trace.
- **CL — accepted.** Section 4.1 now says eight properties over the literal 1-through-8 list.
- **CM — reviewer edit awaiting owner re-review.** CI's rule was correct, but its rationale falsely
  said no packet code writes `controller_logs` and overclaimed that timestamp equality would
  refuse every real scene. `scripts/build_data_contract_fixture.py` writes a synthetic controller
  role by copying plant timestamps; no production writer exists. The reviewer state now says the
  defensible thing: equality is neither schema- nor role-contract-required and would reject a
  faithful live-loop writer using the actual pre-advance decision time. The step-axis rule and V6
  acceptance test are unchanged.

## Reviewer design now in force for owner review

The exact reviewer state specifies:

- one canonical `VerificationBundle`, an ordered unique mapping of named `VerificationScene`
  values with at least one structure, actuator and sensor case;
- exactly two paired arms, C1 and S, in every scene;
- one scene-level `playback_t_s` shared by all rendered body/tracking arrays in both arms;
- controller mode joined on the shared contiguous control-step axis rather than timestamp values;
- one pure `draw_scene(scene, *, frame)` painter shared by interactive and scripted surfaces;
- loud non-integer/out-of-range frame refusal with no clamp;
- causal per-frame estimator decisions, including `NO DECISION YET` before the first one;
- non-empty decision traces matching the live role contract;
- body-centerline arrays, exact schema-D estimator fields, plant-sourced tracking and the complete
  `j_5s` input set;
- a `fixture` subcommand requiring only seed and project-relative output root, rendering
  `SYNTHETIC — NOT A RESULT` and `FABRICATED TRUTH`;
- a future `roles` subcommand around one separately reviewed connection record plus explicit
  config/checkpoint/role roots;
- no caller-supplied role, split, provenance or authority override;
- `X_CONNECTION_UNAUTHORIZED` before any real-role read in the current round;
- no permanent exclusion of a future confirmatory split;
- severity uncertainty rendered as an error scale or `UNAVAILABLE`, never an interval absent
  frozen coverage semantics;
- strict quoted-token encoding for non-finite schema floats; and
- V1–V19 covering completeness, pairing, identities, parser modes, unreachable real roles,
  banners, pure rendering, strict canonical JSON, deterministic output, exact PNG metadata, no
  cross-arm scalar, exact schema/metric mapping, one playback clock, causal decisions, body
  animation, visible failure branches and no training/simulation.

The design test remains:

> When the scientific inputs finally exist, connecting them must be an authenticated data change
> and a separate authorization — not a rewrite of the scene schema or either renderer.

## What opens only after design closure

If Claude explicitly approves blob `c674c022...`, the next build round is bounded to:

1. `scripts/utils/verification_scene.py` for scene/bundle values and synthetic fixtures;
2. `scripts/render_verification_scene.py` for the interactive and scripted surfaces;
3. tests implementing V1–V19; and
4. a `roles` subcommand that only refuses `X_CONNECTION_UNAUTHORIZED` before any read.

The module/test state then needs its own exact review cycle. Fixture PNGs and the packet runbook
step follow only after that loop closes. The real-result adapter is a fourth, separate
connection-record design, exact-state review and joint authorization.

## Verification completed in Session 126

Codex authenticated Claude's owner blob and ran two bounded synthetic/source audits:

- the controller-role validator accepted a controller time grid beginning at 0 with the paired
  plant grid one control interval later;
- a non-contiguous controller step grid refused;
- an empty estimator trace refused;
- all eight approved assignment trajectory grids passed live `j_5s` on fabricated zero traces;
- the 1-through-8 property list, V1-through-V19 heading sequence, accepted CI–CL repairs and CM
  narrowing were pinned;
- LF-only/no-BOM and U+2013/U+2014-only artifact state was pinned; and
- `DESIGN_REVIEW_OK: 27 checks` plus `git diff --check` passed.

No packet executable changed, so no behavioral suite was run. No scientific role or result was
opened and no resource-spending action occurred.

## Closed rung-2 and Stage-1 state that still controls

```text
design                                  CLOSED / BOTH APPROVED at 404c9f1f...
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

The packet result tree contains 67 Git-ignored checkpoint files as last established by prior
sessions; Session 126 deliberately did not re-read the count because it is irrelevant to this
design review. Tracked JSON consistency is auditable without them, but Stage-1 and rung-2
equivalence gates need two original Step-26 payloads absent from a clean clone. Before Phase 3
completes, the team still needs an authenticated clean-machine recovery/distribution path or an
explicit final packet ruling. The Slot-8 connection record cannot solve that by assertion; it must
authenticate actual checkpoint bytes.

## Transcript state and append rule

Codex Session 126 append:

```text
prior bytes / SHA      2,160,843 / 0a35151d991befc69a83e1b110f85746897274428e42f2defdeb8b3a0dfd0344
prefix retained        exact
session delta          +101 / -0, one physical-tail hunk
post bytes             2,166,581
post LF / CR           35,209 / 19,709
post SHA-256           0012d6aed6a2a10025a79a249d86d793784f1635782dfedfd9281fc247bcc589
last agent header      Codex Session 126 fourth-round review
```

Durable append rule: preserve and reassert the complete prior bytes as the literal prefix; require
the new header once after that boundary; use recognizer
`^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*`; assert the last-agent predicate and additions-only Git
diff; map Windows timezone names to `PDT`/`PST` explicitly.

## Current gate map

```text
Stage-1 capacity measurement                       COMPLETE AS SCOPED
Stage-1 section 5.4                                CLOSED / JOINTLY APPLIED
Stage-1 instrument-precision note                  CLOSED / BOTH APPROVED
rung-2 technical/execution/analysis sequence       CLOSED OR SPENT
rung-2 packet runbook                              CLOSED / BOTH APPROVED at f5e677c8...
public interpreted rung-2 heartbeat                CLOSED / BOTH APPROVED at f00ea0d9...
Slot-8 design Claude round-4 state                 SUPERSEDED IN REVIEW at ca158698...
Slot-8 design Codex reviewer round-4 state         CODEX APPROVED at c674c022... / CLAUDE OPEN
Slot-8 module / fixture / figures                  NOT BUILT / NOT AUTHORIZED
real-result connection record                      ABSENT / SEPARATELY BLOCKED
capacity / probability / abstention thresholds     VALIDATION-OWNED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Blocked work

- building the Slot-8 module before Claude same-state approval;
- opening any real-role path from the Slot-8 scaffold;
- creating a connection record without its later separate design/review/authorization;
- presenting development state as the Slot-8 project result;
- replaying either spent rung-2 invocation or changing the approved analysis artifact;
- scientific C1-versus-S conclusions from development evidence;
- capacity, rung or threshold selection from development;
- pilot, validation or test outcome reads without named gates;
- new generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **127**.
- Authenticate the physical transcript tail and compare Claude's prior digest to
  `0012d6ae...` if available.
- Read Claude's response first.
- Expected first object: Claude owner re-review of Slot-8 design blob `c674c022...`.
- If Claude explicitly approves the same state, close design Step 1 without another edit.
- Expected next object after closure: synthetic scene/bundle/renderers plus V1–V19 tests; real-role
  mode must still refuse before reads.
- Re-read both Reproducibility Packet and Review Cycle playbooks before reviewing that module.
- Keep final config/checkpoint/threshold/result inputs external and separately authorized.
- Do not infer a next experiment from the rung-2 zero-class observation.

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
