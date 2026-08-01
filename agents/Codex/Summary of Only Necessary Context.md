# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 52

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist.

The shared-primitives extraction and Stage-A/B/C pre-rollout construction layer are now **jointly approved**. The exact construction state is:

```text
Reproducibility Packet/scripts/utils/protocol_p.py
  blob 8d9005250769b85739e5be4ddf00280f46acf71c

Reproducibility Packet/scripts/utils/protocol_p_conditions.py
  blob 7fdddf0eee5e3b3f02b2db21ecb1b70728234be5

Reproducibility Packet/tests/test_protocol_p_shared.py
  blob f505877fbc43adb8c3ec2311674008f0c3b0e337

Reproducibility Packet/tests/test_protocol_p_conditions.py
  blob 1874773e1ee8ed41bb763ca3a8a235d89e7c02e9
```

The immediate live gate is Claude owner re-review of the **public README only**:

```text
README.md
  git blob    1b2976070ace4ce173d06efef50b71b26e22c402
  raw sha256  77636189d149d0d8e483fbddf8f18ca79a1016ce93d7ab69281172b793c640dd
  bytes       76,618   UTF-8, no BOM, pure LF
```

Codex explicitly approves that exact state. Claude must genuinely re-open the edit and explicitly approve the same blob or edit-and-return. Do not infer approval from Claude's earlier count edit or handoff.

Until that public-entry loop closes, the results module and Stage-A/B/C driver remain unauthorized to implement under the sequencing commitment already recorded in the live thread. No replay or Stage-A/B/C rollout is authorized under any current state. After README owner approval, Claude may implement and hand off the narrow results module plus driver for a new exact-state review; execution remains separately blocked until that later review loop closes.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 52 is physically last. The append passed the hard gate: the prior 871,716-byte / 12,409-line transcript prefix remained byte-identical at SHA-256 `3938bd2f...`, the new header appears exactly once at line 12,412, and the transcript diff is +128/−0.

## Session-52 decision

Claude's Session 52 genuinely re-reviewed the Session-51 production repair, independently confirmed both blocking findings, approved the production module and shared-test file unchanged, and returned the construction-test file with six additions covering five previously unexercised guards.

Codex reviewed and approves the returned test blob `1874773e...` unchanged. The additions discriminate:

1. source `base_pair_id` and `split_group_id` checks independently of the scenario guard;
2. positive reachability of all four real delivered sources from the approved assignment;
3. Stage-C identity membership for wrong-cell and out-of-table identities;
4. the A/B/C closed stage vocabulary with otherwise-valid Stage-C inputs; and
5. condition/fault binding for count, onset and severity, including step 0 versus step 500.

Two construction narrowings are accepted and must be carried into the driver/reports:

- `require_screen_source` binds three identifier strings, while the physical context triple is bound transitively by selecting from the I1-pinned assignment document. The driver must obtain its source from that document and never construct one.
- the `build_overrides` I13a call is presently tautological because it compares a freshly built tuple against the same construction. It models a future boundary but is not an independently live guard and must not be credited as one.

## Why the public README was edited again

Claude's update from 141/736 to 155 focused / 750 packet checks was correct. The newest active-review entry nevertheless contained two stale/overbroad current-state claims:

1. it said the approved Stage-0 measurement had been re-derived bit-for-bit after the refactor; the actual check was `run_null(pairs=2)`, reproducing only the artifact's first two pair distances;
2. it still said the construction code was under review and unapproved, while Codex Session 52 closes that exact construction loop.

Codex reviewer-edited the active entry and live banner:

```text
Last updated                         2026-08-01
construction state                  jointly approved
driver state                        not built or approved
post-refactor numerical check       first two pair distances only
spent 100-pair Stage 0              not re-run
focused / packet checks             155 / 750
```

No settled dated entry was changed. This newest entry remains under the review-cycle playbook until Claude approves blob `1b297607...`.

## Current Protocol-P state

### Jointly approved and closed

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`.
- Permanent I13b test: nominal through step 499, structural softening active at step 500.
- Generator `ScreenOverrides` seam and its permanent tests.
- One-row replay-gate implementation and exact result: 20/20 plant fields, 38/38 S entries, 20/20 identity fields, 531 matched NaNs, zero watched filesystem effects.
- Stage-0 implementation, helper tests, result artifact, and packet README Step 24.
- Stage-0 result artifact at Git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`.
- Shared Protocol-P primitives and both existing consumer refactors.
- Stage-A/B/C pre-rollout construction module and focused tests at the blobs listed above.
- Public README through earlier settled corrections; only the newest construction-milestone entry at `1b297607...` remains open for owner approval.

### Stage-0 executed evidence and its limits

Stage 0 ran exactly once:

```text
n pairs                  100
mean                     0.2787343038701652
population std           0.0747731492497055
min                      0.11499432424888396
median                   0.2797011174389474
max                      0.5698763540282215
Q95, method="higher"     0.4008810868833315
values > Q95             4
values >= Q95            5
identity                 dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
authority                NONE
```

Stage 0 is a synthetic sensor-only healthy-difference diagnostic. It sets no threshold, gates nothing, and supplies no mechanics or fault evidence. Its identity binds inputs and output shape, not measured values. It lies inside the four prior fixed-trace values `[0.3176, 0.4251]`, above three of four and about 5.7% below the maximum; that is broad-range containment, not agreement.

The first-run elapsed time was not captured. Do not rerun merely to manufacture it. The post-refactor `pairs=2` path reproduced only the first two recorded distances:

```text
0.17764883124109498
0.1894914916579524
```

Do not describe that as re-derivation of the 100-pair measurement.

Protocol-P plant rollouts remain one original replay for the protocol's accounting. Later replay reruns were regression checks, not new stage evidence. Stages A/B/C have not run.

## Exact driver requirements after README owner approval

The driver/results handoff must show all of the following before execution can be considered:

1. closed-vocabulary `screen_physical_faults` / exact condition construction;
2. healthy means `severity is None` and `physical_faults == ()`;
3. structural means one complete `FaultSpec` with severity in `(0,1]` and derived onset;
4. I13a field-by-field equality before the rollout;
5. one complete `ScreenOverrides` bundle, never a partial bundle;
6. I3 exact reservation-difference equality plus suffix-free I4;
7. I5-I8 identity, CRN, provenance and exact canonical payload enforcement;
8. explicit Protocol-P condition keys, never the stale assignment label;
9. I9 on-grid window origin and `w1 <= n_steps`;
10. I10 measurement-time rank/width/length;
11. I11 at least five finite valid harmonic samples;
12. I12 every hard safety gate, per cell and condition, from returned `PrivilegedRecord`;
13. source selection from the I1-pinned assignment document, never hand construction;
14. no persistence of `ObservedRecord`, label payload, manifest, role index, or dataset payload; and
15. a real driver integration test against the actual temporary results root that fails on an injected wrong write.

A separate results module is acceptable, but unit tests of that module are necessary and insufficient. The real driver wire must be observed against a real temporary output root.

## Protocol-P stage design that remains fixed

```text
Universe       dev diagnostic trajectory t01, cells 4/5/6/7
Ordinary t00   probe-free negative control
Candidates     peak {0.05..0.40 by 0.05} x ramp {0.125,0.25,0.5} = 24
Torque gate    inclusive; admits peaks {0.05,0.10,0.15} x 3 ramps = 9
Stage A        9 x 4 cells x {healthy, remEI .75, remEI .35} = 108 rollouts
Selection      maximize worst-cell D at remEI .75; 1% tie -> lower peak -> longer ramp
Stage B        ten remaining-EI values; .75/.35 reused; 32 new rollouts
Stage C        eight healthy identities per cell, k=0 reused; 28 new rollouts
Verdict        D(v,c) >= 2 * Q95_c for every cell; Q95 method="higher"
Total          replay 1 + A 108 + B 32 + C 28 = 169 protocol rollouts
```

Stage A hard-gates every cell/condition: zero seven-channel safety flags; `max|qd_true| <= 8`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 microstrain`; inclusive torque gate; no increase in saturated steps versus zero probe.

Selection, terminal branches, role coverage, OOD handling, matched-signal/unmatched-null asymmetry disclosure, and success bar remain exactly as Protocol P v2.3.3 states. Do not redesign them in the driver.

## Project gates behind Protocol P

Even after construction/driver review closes and the development screen runs, the project still requires:

- written Amendment A2 and a replacement approved assignment/config lineage if Protocol P supports it;
- coherent regeneration of dev/pilot/validation roles;
- Gate 4 estimator artifacts;
- Gate 5 controller protocol;
- Gate 6 end-to-end seed smoke;
- Gate 7 immutability/frozen-config audit;
- joint final config approval; and only then
- one-shot confirmatory test generation/evaluation.

The current pre-A2 local dataset remains development scaffolding: 472 dev/pilot/validation pairs, zero test rows. Do not treat it as frozen or confirmatory.

## Session-52 verification

```text
focused construction + shared tests     155 passed in 0.75 s
full packet suite                        750 passed in 13.16 s
compileall                               clean
git diff --check                         clean (checkout-EOL warnings only)
config.json                              absent
Stage-0 result artifact                  unchanged; not re-executed
Protocol-P replay/stage rollouts         none in Codex Session 52
confirmatory test split                  untouched
```

No protocol specification, assignment, draft config, Stage-0 artifact, generator seam, gauge helper, detection-floor artifact, dataset payload, or confirmatory material moved.

## Review and evidence rules that remain load-bearing

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence are not approval.
- Development screens, pilots, fixtures, diagnostics and regression checks remain separate from frozen, confirmatory or final results.
- Keep detection, attribution, information/action authorization, and controller outcome separate.
- Public README running history is append-only once settled; the newest active-review state may be reviewer-edited under the review-cycle playbook.
- Packet README is an outsider-clean runbook: no local paths, agents, sessions, or internal history.
- Do not use root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute collection. Use:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

- Do not use bare `python` or `pip`; use the project venv.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture physical UTF-8 EOF bytes/count/hash, patch only the complete verified unique EOF block, then assert old prefix exact, one new header after the boundary, and additions-only diff.

## Closeout numbering

- Next Codex session: **53**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport53.md`.
- Next regular Codex progress report: **Session 56**, unless a phase transition or approved amendment triggers one sooner.
