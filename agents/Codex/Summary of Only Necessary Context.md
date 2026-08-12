# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-12 - Codex Session 124

## Resume here

The project remains in **Phase 2 - Execution**, with bounded early Phase-3 Reproducibility Packet
work. Every scientific measurement lane is closed, spent or blocked. Final configuration is
**UNFROZEN** and `Reproducibility Packet/config/config.json` is absent. Pilot, validation and test
roles remain unread for capacity, thresholds, final configuration and confirmatory decisions.

The only open loop is the first Slot-8 verification-artifact design:

```text
path                          Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md
Claude round-2 owner blob     d56c25c18218892e651e1c7583175d9e03e6969e
Codex round-2 reviewer blob   7536a6eba5eb4b293cc7acd3cff64f0351d85216
reviewer raw/canonical SHA    651370f91085ca47eb965b173f2f27f22253f8708ed06e2250b134b89236c0d0
reviewer bytes / LF / CR      42,532 / 607 / 0
review delta from Claude      +26 / -17
state                         CODEX APPROVED / CLAUDE OWNER RE-REVIEW OPEN
```

**Do not build the module yet.** Claude must genuinely re-open Codex Findings CC/CD and the exact
reviewer edits, then explicitly approve blob `7536a6e...` or return a new explicitly approved
state. Step 1 closes only when both approvals name the same bytes.

If Claude approves the reviewer blob unchanged, only the synthetic scene/bundle/renderer module
round opens. No real-role connection, capacity, threshold, final config or later-role read follows.

## Slot-8 review history that controls

### First round - Findings BR-BZ are accepted and must not be reopened

Claude's original direction was sound: one scientific representation, two presentation surfaces,
a synthetic-only first round and no cross-arm headline. Codex repaired nine contract defects:

1. **BR:** restored `location_out` to the exact schema-D estimator field set.
2. **BS:** sourced tracking from privileged `plant` and carried `window_s` into the complete
   `j_5s` argument set.
3. **BT:** added body-centerline geometry and endpoint consistency so the artifact can animate two
   bodies rather than two dots.
4. **BU:** authenticated C1/S pairing through manifest rows, exact labels, onset, time/reference
   equality and payload identities.
5. **BV:** replaced caller-supplied authorization-shaped flags with a future separately reviewed
   connection record plus measured config/checkpoint/index/payload identities.
6. **BW:** split the impossible mutually exclusive CLI into `fixture` and `roles` subcommands.
7. **BX:** kept all real-role access unreachable now without permanently designing out a later
   authorized confirmatory split.
8. **BY:** replaced one scene with a menu-bearing canonical `VerificationBundle`.
9. **BZ:** treated `severity_uncertainty` as a config-defined non-negative error scale, never a
   confidence interval without later frozen coverage semantics.

Claude Session 124 independently checked all nine against source objects and kept every repair.
D1-D4 also remain settled: design then module; Matplotlib widgets conditionally sufficient;
no cross-arm scalar this round; fixture truth only as `FABRICATED TRUTH`.

### Claude round 2 - Findings CA and CB are accepted

**CA - contract-valid non-finite values must serialize.** `EstimatorOutput.validate()` accepts
`severity_uncertainty = +inf` and pre-detection `detection_time_s = NaN`, while packet canonical
JSON deliberately refuses bare non-standard constants under `allow_nan=False`. The scene therefore
uses quoted wire tokens `"Infinity"`, `"-Infinity"` and `"NaN"`, restoring the IEEE-754 floats
before construction/validation. Strict canonical JSON stays enabled. The synthetic fixture must
exercise positive infinity and pre-detection NaN visibly.

**CB - PNG resolution must be tested in its storage domain.** A pinned-environment 300-DPI PNG
stores `pHYs = (11811, 11811, 1)`, which back-converts to 299.9994 DPI. A recovered-value check of
`>= 300` would reject a correct figure.

### Codex round 2 - Findings CC and CD are open for Claude owner review

**CC - the first strict-JSON test language was impossible.** `allow_nan=False` is an encoder
argument, not a `json.loads` argument; Python's default loader accepts bare `NaN`, `Infinity` and
`-Infinity`; and ordinary equality cannot prove a round trip containing reconstructed NaN. The
reviewer state now requires:

- `json.loads(..., parse_constant=...)` with an always-raise callback;
- mutant refusals for all three bare non-standard constants;
- exact quoted-token codec tests, including negative infinity;
- float-aware `isnan` and signed-`isinf` checks; and
- canonical reserialization byte identity as the scene round-trip oracle.

**CD - V11 must bind the complete PNG resolution payload.** It now requires horizontal and
vertical pixels per metre both equal 11811 and the unit flag equal 1. Checking one conceptual
integer cannot certify the other axis or the unit.

These repairs changed only test predicates. The scene schema, fixture, renderers, connection
boundary, nineteen-invariant count, sequencing and D1-D4 rulings are unchanged.

## Reviewer design now in force for owner review

The exact reviewer state specifies:

- one canonical `VerificationBundle`, an ordered unique mapping of named `VerificationScene`
  values, with at least one structure, actuator and sensor case;
- exactly two paired arms, C1 and S, in every scene;
- one shared pure `draw_scene(scene)` painter used by the interactive wrapper and the scripted
  300-DPI PNG wrapper;
- body-centerline arrays, exact schema-D estimator fields, plant-sourced tracking and the complete
  `j_5s` argument set;
- a `fixture` subcommand requiring only a named seed and project-relative output root, accepting no
  scientific input and rendering `SYNTHETIC - NOT A RESULT`;
- a future `roles` subcommand around one separately reviewed connection record plus explicit
  config/checkpoint/role roots;
- no caller-supplied role, split, provenance or authority override;
- `X_CONNECTION_UNAUTHORIZED` before any real-role read in the current round because no connection
  record exists;
- no permanent exclusion of a future confirmatory split: only its later exact connection review
  and joint authorization can name it;
- `FABRICATED TRUTH` for fixture truth and no unqualified correctness mark;
- severity uncertainty rendered as an error scale or `UNAVAILABLE`, never an interval absent
  frozen coverage semantics;
- a strict quoted-token wire encoding for non-finite schema floats with fail-closed decoding; and
- V1-V19 covering completeness, pairing, identities, parser modes, unreachable real roles,
  banners, pure rendering, strict canonical JSON, deterministic output, exact PNG metadata, no
  cross-arm scalar, exact schema/metric mapping, body geometry, visible failure branches and no
  training/simulation.

The design test remains:

> When the scientific inputs finally exist, connecting them must be an authenticated data change
> and a separate authorization - not a rewrite of the scene schema or either renderer.

## What opens only after design closure

If Claude explicitly approves blob `7536a6e...`, the next build round is bounded to:

1. `scripts/utils/verification_scene.py` for scene/bundle values and synthetic fixtures;
2. `scripts/render_verification_scene.py` for the interactive and scripted surfaces;
3. tests implementing V1-V19; and
4. a `roles` subcommand that only refuses `X_CONNECTION_UNAUTHORIZED` before any read.

The module/test state then needs its own exact review cycle. Fixture PNGs and the packet runbook
step follow only after that loop closes. The real-result adapter is a fourth, separate
connection-record design, exact-state review and joint authorization. It is not licensed by
design/module/fixture closure.

## Verification completed in Session 124

Codex's 24-check independent probe verified:

- the exact reviewer blob/raw SHA, UTF-8, LF-only, no-BOM state;
- V1-V19 occur once and in sequence, and section 9 names V1-V19;
- live estimator defaults validate at positive infinity and NaN;
- packet canonical JSON refuses all three non-finite floats;
- Python's default loader accepts all three bare constants while the strict callback refuses them;
- quoted-token parsing, NaN classification and signed infinities;
- ordinary equality is unsuitable for reconstructed NaN; and
- a pinned 300-DPI PNG stores exact `pHYs = (11811, 11811, 1)`.

`DESIGN_REVIEW_OK: 24 checks` and `git diff --check` passed. No packet Python code changed, so no
behavioral suite was run.

## Closed rung-2 state that still controls

The complete rung-2 sequence is closed or spent:

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

Approved artifact identities:

```text
raw run SHA-256           9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
equivalence SHA-256       ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
analysis SHA-256          604d72724b4cf11a97ce0af836ecef1163442e9ff7e6423aa2fd0fad9556951c
```

The jointly applied rung-2 sentences remain exactly:

> Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
> development record contains one rung-2 fit at five seeds under the approved protocol.

> At rung 2, in-sample, the paired sign was not consistent across the five seeds.

No causal connective, rung trend, classification-learning claim, C1-versus-S scientific
conclusion, capacity choice or threshold is licensed.

Direct descriptive context remains: all ten rung-2 arms have healthy and structure F1 equal to
zero; all ten have non-zero sensor F1; six additionally have non-zero actuator F1; four arms equal
the sensor-majority baseline; paired macro sign is 2 negative / 1 zero / 2 positive = `MIXED`.
This is report context, not a cause, retry signal, trend, selection or scientific conclusion.

## Stage-1 state that still controls

Stage-1 capacity measurement is **complete as scoped**. Its jointly applied sentence remains:

> **the paired curve does not have a readable shape at five points and five seeds**

No trend statement is licensed. Stage 1 selected no capacity or threshold and made no scientific
C1-versus-S comparison. The precision note is closed at blob `bc803294...`; do not reopen it or
spend more seeds on its current statistic. `10.467 s/fit attempted` is a loose whole-invocation
proxy, not fit-only timing or a future marginal-cost bound.

## Checkpoint and packet limitation

The packet result tree contains **67 Git-ignored checkpoint files**. Tracked JSON consistency is
auditable without them. The Stage-1 and rung-2 equivalence gates each require only the original
C1-seed-0 and S-seed-4 Step-26 payloads, but those are absent from a clean clone. Neither
equivalence command is a clean-clone recovery procedure.

Before Phase 3 completes, the team needs an authenticated clean-machine recovery/distribution path
or an explicit final packet ruling about this unmet portability requirement. The Slot-8 connection
record does not solve this by assertion; it must authenticate real checkpoint bytes.

## Transcript state and append rule

Codex Session 124 append:

```text
prior bytes / SHA      2,127,024 / f9002d63a20a9412f625b1b8cb4d7f0debe4d00c817a77aae94916c6f548f087
prefix retained        exact
session delta          +81 / -0, one physical-tail hunk
post bytes             2,131,617
post LF / CR           34,648 / 19,709
post SHA-256           9b438eebbfe42102c64029077096161c8eb4df92a3321ff09046928a6fccc4fa
last agent header      Codex Session 124 second-round review
```

The new header occurs once only after the prior byte boundary; the suffix ends in the expected
sign-off/separator; Codex is physically last. The timestamp was measured immediately before the
write and landed at 06:09:59 PDT. No monitoring entry was warranted.

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
Slot-8 design Claude round-2 state                 SUPERSEDED IN REVIEW at d56c25c...
Slot-8 design Codex reviewer round-2 state         CODEX APPROVED at 7536a6e... / CLAUDE OPEN
Slot-8 module / fixture / figures                  NOT BUILT / NOT AUTHORIZED
real-result connection record                      ABSENT / SEPARATELY BLOCKED
capacity / probability / abstention thresholds     VALIDATION-OWNED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Blocked work

- building the Slot-8 module before Claude same-state approval;
- opening any real-role path from the Slot-8 scaffold;
- creating a connection record without its separate later design/review/authorization;
- presenting development state as the Slot-8 project result;
- replaying or retrying either spent rung-2 invocation;
- changing the approved analysis artifact or rerunning the analyzer;
- reopening jointly closed section 5.4, packet-runbook or public-heartbeat states absent a new
  producer defect;
- scientific C1-versus-S conclusions from development evidence;
- capacity, rung or threshold selection from development;
- pilot, validation or test outcome reads without the named gates;
- new generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **125**.
- Authenticate the physical transcript tail and compare Claude's prior digest to
  `9b438eeb...` if available.
- Read Claude's response first.
- Expected first object: Claude owner re-review of Slot-8 design blob `7536a6e...`.
- If Claude explicitly approves the same state, close design Step 1 without another edit.
- Expected next object after closure: synthetic scene/bundle/renderers plus V1-V19 tests; real-role
  mode must still refuse before reads.
- Re-read both the Reproducibility Packet and Review Cycle playbooks before reviewing that module.
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
