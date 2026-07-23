# Summary of Only Necessary Context

**Rewritten:** 2026-07-22 17:11 PDT

**Last completed Codex session:** 21

**Next Codex session:** 22

**Current branch:** `main`

**Project phase:** Phase 2 — Execution

**Configuration:** explicitly **unfrozen**

## Resume state

Codex Session 21 processed Claude's edited first review of the Session-20 per-class fault tracking-deficit screen. The review was not a same-state approval. Claude corrected the screen's conversion between the Claim Sheet's reduction metric and the screen's healthy-relative deficit, moved the selected actuator setting from 0.50 to 0.25 remaining gain, added a conversion regression and generated interpretation section, and handed the state back.

Codex genuinely re-opened the implementation, regression, derived artifacts, report, packet runbook, and Claim Sheet metric. The units correction is accepted:

- Claim Sheet control target: 10% reduction against the degraded arm;
- predeclared development margin: +2 percentage points in reduction units;
- required reduction target: 12%;
- equivalent healthy-relative deficit gate for exact restoration: `0.12 / (1 - 0.12) = 13.636%`.

The old 12% deficit gate admitted only a 10.714% exact-restoration reduction, so it did not preserve the stated margin. The corrected gate is conservative and data-independent.

The corrected decision is:

`ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

The mildest advancing physical condition is now **0.25 remaining actuator gain**, with disjoint mean/min deficit **23.16% / 23.03%**. No structural setting advances. The raw per-arm rows are unchanged from Session 20.

Codex made one narrow interpretation edit before approval. Claude's generated wording treated better-than-healthy performance as automatically generic command authority. The current text now says the defensible thing: performance above the exact-restoration ceiling could be fault-specific overcompensation or generic nominal-controller under-authority, and this no-action screen cannot distinguish them. The later action screen must include a healthy false-authorization arm and report the source-specific margin separately.

**Codex explicitly approves the current edited state. Claude now owes genuine re-review of Codex's wording correction.** The loop is open until Claude explicitly approves this exact state or edits and hands it back. Downstream use, silence, or continuity text is not approval.

## Current deficit-screen state

### Gate and selected condition

- `required_tracking_reduction_pct = 12.0`
- `required_tracking_deficit_pct = 13.636363636363637`
- selected actuator case: `actuator_gain_remaining_0p25`
- disjoint assessment mean deficit: 23.160934388653637%
- disjoint assessment minimum deficit: 23.031393428348363%
- exact-restoration ceiling: 18.8054% mean / 18.7199% minimum reduction
- structure: BLOCK at every remaining-EI setting
- sensor control: fixed 0.05 rad encoder bias, 15.69% mean / 15.61% minimum deficit; not a selected severity grid

### Structural result

Across the same assessment sweep:

| Remaining EI | Mean peak gauge | Mean tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

The structural signal becomes monotonically stronger as the tracking deficit falls through zero and becomes beneficial. This is the predeclared Slot-13 diagnostic-only shape measured across a 15× stiffness sweep, not a sensing failure.

### Artifact hashes

- tuning rows: `bfe0eb660e76a47702462a1bafd2477b3633bd3f32a94d8abbf0e976350c92df`
- assessment rows: `7cfcc104487d45a56ca316332dfcc563b9bdaaec94a32cf1d09d5003e680c293`
- summary: `ed265cfb1ac0cf8fa37678024203de3dcf049af70f0c85cf6fde4decec6191bf`
- candidate summary: `a7e2998d0ac986b803a6c535aa72b612960aa255f33caa7d0df259dc191e1b97`
- current report after Codex's scope edit: `f8ee1dfda070f220153fca2d5ea55e696722ac2b5e699728659ebecc2b2eaa62`

## Accepted prior structural-action state

The structural-action review loop remains closed and must not be reopened merely because later artifacts cite it.

Accepted decision:

`BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`

Robust grounds:

- global 2× action recovers about 20.37% while localized 2× recovers only 6.16%, so most apparent benefit comes through the non-localized joint;
- the underlying structural fault produces essentially no tracking deficit on this bounded task;
- the four-seed healthy/structural specificity sign is unresolved and must not carry the block;
- the fixed-severity family exercised constant capped gains, not meaningful severity conditioning.

The inverse-stiffness code seam remains reviewed and may stay, but no structural action advances.

## Control-layer shape that must constrain future work

The recorded bounded noisy information review already shows:

| Source | C1 gate | S gate | Suite-informed | S tracking change |
|---|---|---|---|---:|
| healthy | correct no action | correct no action | no | 0.0000% |
| structure | withheld actionable fault | correct actionable | yes | −18.5762% |
| actuator | correct actionable | correct actionable | no | 0.0000% |
| sensor | correct no action | correct no action | no | 0.0000% |

C1 recall is 0.083 on structure and 1.000 on actuator/sensor. S is 1.000 on all three in this development library.

The present shape is therefore:

- where S carries exclusive information (structure), there is no tracking deficit to recover;
- where control headroom exists (actuator and fixed sensor), C1 already detects the class;
- an actuator recovery action may still be useful recovery engineering, but it cannot by itself create the Claim Sheet's paired S-over-C1 control win on this library.

Do not enlarge the information claim or imply that actuator headroom opens Slot 11.

## Next technical gate after Claude's review

The next Codex-owned action review should measure **achievable source-specific reduction**, not deficit alone.

Minimum design:

1. Compare action versus no action on the same actuator fault with exact seed-paired pre-fault histories.
2. Apply the same multiplier as a false authorization on healthy and report the source-specific margin separately.
3. Put specificity into candidate selection, not only post-selection assessment.
4. Sweep the compensation cap so the screen distinguishes a controller cap from a physics limit. The current `maximum_gain_compensation = 2.0` is explicitly unfrozen.
5. Include an oracle-severity ceiling arm and a separate deployable-severity arm. Do not silently substitute true remaining gain for an unmeasured estimator output.
6. Preserve one held decision, zero pre-decision action, the full `J_5s` window, A1 safety, saturation, and contact readouts.
7. Give the disjoint source-specific margin a real paired uncertainty interval; do not use a sign-only difference of small unpaired means.
8. Keep the paired S-minus-C1 limitation explicit. A source-specific actuator recovery result is not automatically a sensor-suite result.

Claude's Session-21 exploratory action measurements are context, not tracked deficit-screen artifacts:

| Remaining actuator gain | Achieved reduction with oracle severity | Healthy false authorization | Source-specific margin |
|---:|---:|---:|---:|
| 0.50 | 10.77% | 6.11% | +4.67 pp |
| 0.25 | 10.82% | 6.11% | +4.71 pp |
| 0.10 | 3.10% | 6.11% | −3.01 pp |

These measurements show why the next gate must combine fault condition, action family/cap, and severity quality rather than advance on deficit alone. Do not copy them into a generated artifact unless the corresponding rows are recorded and reproducible there.

## Verification state

- Focused deficit screen: **16 passed**.
- Full Reproducibility Packet: **199 passed**.
- `compileall -q scripts tests`: passed.
- Generated report reproduces byte-for-byte from `summary.json` through `write_report()`.
- `git diff --check`: clean except expected line-ending conversion warnings.
- No new dependency installed.
- Root Live-Run README deliberately unchanged in Session 21; no new public milestone was produced.

## Transcript append state

The transcript-order failure mode recurred in Session 21.

Phase-2 transcript:

- original pre-write boundary: 1,673 lines;
- Codex's 17:08 turn was mistakenly inserted at line 1,331 because the applied patch used only the final two lines of a separately verified eight-line EOF block;
- no prior content was deleted, moved, truncated, or rewritten;
- correction pre-write boundary: 1,689 lines;
- correction header exactly once at line 1,693;
- Codex physically last at line 1,705;
- working-tree transcript diff after repair: +32 / −0.

Monitoring transcript:

- pre-write boundary: 27 lines;
- Codex header exactly once at line 31;
- Codex physically last at line 41;
- diff: +14 / −0.

Operational rule: read the physical UTF-8 tail, record the pre-write line count, verify a complete multi-line EOF anchor is unique, and make the **patch itself** contain that entire verified anchor. Verifying a longer anchor while applying a shorter repeated context does not satisfy the gate. After writing, assert header count, header position after the boundary, physical-last speaker, and append-only diff before any commit.

## Open / unfrozen items

- Claude's re-review of Codex's Session-21 wording correction;
- actuator action family, compensation cap, and deployable severity quality;
- sensor-fault recovery action;
- validation-sized healthy/four-class calibration and per-suite probability calibration;
- ambiguous known-class cases that make abstention bind;
- compound/OOD faults and held-out subtype/location/severity/onset grids;
- non-load-bearing sensor constants;
- class/abstention/selective/OOD thresholds;
- learned temporal attribution head plus RMA baseline;
- whole-trajectory/fault-setting split and deployable-loader leakage audits;
- role hashes, multi-run storage, and immutable config/schema gates;
- reference lifecycle beyond the scheduled one-held-decision development condition;
- task/contact/controller profile and W=768 / stride=16;
- evaluation-sized paired control comparison;
- interactive Slot-8 verification artifact and all Phase-3 deliverables.

## Required startup sequence for Session 22

1. Re-read `AgentPrompt.md` and follow it exactly.
2. Read all of `Project Details/Project Details.md`.
3. Read this file.
4. Read every Codex-channel `Summary.md`, then all active transcripts completely to physical EOF before replying.
5. Read Claude's latest Human Report and continuity.
6. Inspect git status/HEAD and actual files before trusting this summary.
7. Process Claude's re-review of the exact Session-21 deficit-screen wording first. Close only on explicit same-state approval; genuinely re-review any further edit.
8. Keep `config.json` unfrozen unless every remaining gate actually closes.

## Closeout conventions to preserve

- Active chats are append-only under the full hard gate described above.
- Rewrite this continuity file completely at every completed Codex session.
- Add the next `HumanReportN.md` and keep `agents/Codex/README.md` purpose-oriented.
- Keep the public Live-Run README lean, append-only, and milestone-based.
- Review `.gitignore`, stage only intended files, run `git diff --cached --check`, then commit exactly `Codex Session N` and push.
- Next regular Codex progress report: Session 24 unless a Claim Sheet amendment or phase transition triggers one earlier.
