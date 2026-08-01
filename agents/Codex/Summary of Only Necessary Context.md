# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 53

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist.

The shared-primitives extraction and Stage-A/B/C pre-rollout construction layer are jointly approved at:

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

The public README review loop is also closed. Both agents explicitly approve:

```text
README.md
  git blob    ce5e8dce3bdbef84865bbe7ba69526bfb17ad07e
  raw sha256  93046b1f470e73c16e3d49c7254977c924819dc33d4978b5f26e9ff88e152d8a
  bytes       76,726
```

Its newest entry now states the exact current boundary: no new measurement was spent; Stage 0 is the only screen stage that has run; Stages A/B/C remain unrun and unauthorized; the construction layer is jointly approved; the driver is not built or approved; config remains unfrozen; and the confirmatory split is untouched.

The immediate live task is Claude implementation of the **narrow Stage-A/B/C results module and driver**, followed by Codex exact-state review. Implementation is authorized. Execution is not. No replay or Stage-A/B/C rollout may run until the driver review loop closes explicitly on the exact executable state.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 53 is physically last. The append passed the hard gate: the 887,661-byte / 12,730-line pre-write prefix remained byte-identical at SHA-256 `373b46a1003b625bb51af5e186a295875e808a29bb50b99049c4d1fd3d6bda02`; the new header appears exactly once at line 12,734; and the transcript diff is +108/−0. The post-append file is 892,610 bytes / 12,838 lines at SHA-256 `238da6ebc296b232e2207a692fcb23641348a3bbbd1850678bc6f6eac7178045`.

## Session-53 decisions

### Public entry

Claude's returned one-sentence edit is approved unchanged. The earlier four “No screen stage has run” clauses are dated 2026-07-29 and were true when written. Only the newest active-review entry was false after Stage 0 ran. No settled dated entry required a correction.

### Reused-rollout provenance

Protocol P contains **180 logical rows but 168 physical Stage-A/B/C rollouts**. Twelve logical rows reuse Stage-A measurements:

- eight Stage-B rows: remaining-EI 0.75 and 0.35 across four cells;
- four Stage-C rows: `k=0` healthy across four cells.

The physical rollout owns provenance. A reused logical row cites the original immutable Stage-A result, including its exact `rollout_provenance` hash and canonical payload. It does not call `build_overrides`, does not call `_generate_reservation`, and does not mint a Stage-B or Stage-C hash.

The results representation must distinguish the logical consumer stage from the physical origin:

- physical ledger: 168 entries, 168 distinct provenance stamps;
- logical inventory: 180 rows, exactly twelve with fail-loud `reused_from` references;
- each reuse resolves to the correct selected Stage-A physical entry;
- the reused row's provenance hash and canonical payload equal the origin exactly;
- no Stage-A canonical payload is relabeled as Stage B or C.

This is not a Protocol-P amendment. Sections 6, 8 and 11 already declare the twelve reuses and budget 168 rollouts; section 0 and I8 require provenance per rollout. A reused logical row is not another rollout.

Codex independently rebuilt the inventory from the real approved documents/module without simulation:

```text
admissible candidates                    9
logical rows                            180
distinct physical request keys          168
distinct request stamps if all built    180
reused rows whose stage changes hash     12
derived onset index                     500
config.json                             absent
```

## Exact driver requirements

The implementation handoff must show all of the following before execution can be considered:

1. closed-vocabulary `screen_physical_faults` / exact condition construction;
2. healthy means `severity is None` and `physical_faults == ()`;
3. structural means one complete `FaultSpec` with severity in `(0,1]` and onset derived from the bound trajectory and control timestep;
4. off-grid onset refusal, plus exact equality between the derived onset and every passed fault spec;
5. I13a field-by-field equality before the rollout;
6. one complete `ScreenOverrides` bundle, never a partial bundle;
7. I3 exact reservation-difference equality plus suffix-free I4;
8. I5–I8 identity, CRN, provenance and exact canonical-payload enforcement;
9. explicit Protocol-P condition keys, never the stale assignment label;
10. I9 on-grid window origin and `w1 <= n_steps`;
11. I10 measurement-time rank/width/length;
12. I11 at least five finite valid harmonic samples;
13. I12 every hard safety gate, per cell and condition, from returned `PrivilegedRecord`;
14. source selection from the I1-pinned assignment document, never hand construction;
15. 180 logical rows resolving to 168 physical executions;
16. exactly twelve reuse references to the correct selected Stage-A results;
17. zero construction/generator calls and zero new provenance for those reused rows;
18. exact hash/canonical equality between every reused row and its physical origin;
19. Stage-A selection performed from Stage-A results, never fabricated or precomputed;
20. no persistence of `ObservedRecord`, label payload, manifest, role index, or dataset payload; and
21. a real driver integration test against an actual temporary results root that fails on an injected wrong write.

A separate results module is acceptable, but unit tests of that module are necessary and insufficient. The real driver wire must be observed against a real temporary output root. Tests may inject physical-run fixtures; they must not execute Protocol-P plant rollouts before authorization.

Two construction narrowings remain load-bearing:

- `require_screen_source` binds three identifier strings, while payload/environment/contact are bound transitively by selecting the source from the I1-pinned assignment document. The driver must select from that document and never hand-construct a source.
- the `build_overrides` I13a call presently compares a freshly built tuple against the same construction. It models a future boundary but is not an independently live guard and must not be credited as one.

## Protocol-P state

### Jointly approved and closed

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`.
- Permanent I13b: nominal through step 499, structural softening active at step 500.
- Generator `ScreenOverrides` seam and permanent tests.
- One-row replay gate and exact result: 20/20 plant fields, 38/38 S entries, 20/20 identity fields, 531 matched NaNs, zero watched filesystem effects.
- Stage-0 implementation, helper tests, result artifact, and packet README Step 24.
- Stage-0 result artifact at Git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`.
- Shared Protocol-P primitives and both consumer refactors.
- Stage-A/B/C pre-rollout construction module and focused tests.
- Public README through current blob `ce5e8dce...`.

### Stage-0 evidence and limits

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

Do not describe that as re-derivation of the 100-pair result or its Q95.

Protocol-P plant rollouts remain one original replay for protocol accounting. Later replay reruns were regression checks, not new stage evidence. Stages A/B/C have not run.

## Stage design that remains fixed

```text
Universe       dev diagnostic trajectory t01, cells 4/5/6/7
Ordinary t00   probe-free negative control
Candidates     peak {0.05..0.40 by 0.05} x ramp {0.125,0.25,0.5} = 24
Torque gate    inclusive; admits peaks {0.05,0.10,0.15} x 3 ramps = 9
Stage A        9 x 4 cells x {healthy, remEI .75, remEI .35} = 108 rollouts
Selection      maximize worst-cell D at remEI .75; 1% tie -> lower peak -> longer ramp
Stage B        ten remaining-EI values; .75/.35 reused; 32 new rollouts
Stage C        eight healthy identities per cell; k=0 reused; 28 new rollouts
Logical rows   108 + 40 + 32 = 180
Physical runs  108 + 32 + 28 = 168
Verdict        D(v,c) >= 2 * Q95_c for every cell; Q95 method="higher"
Total budget   replay 1 + stages 168 = 169 protocol rollouts
```

Stage A hard-gates every cell/condition: zero seven-channel safety flags; `max|qd_true| <= 8`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 microstrain`; inclusive torque gate; no increase in saturated steps versus zero probe.

Selection, terminal branches, role coverage, OOD handling, matched-signal/unmatched-null asymmetry disclosure, and success bar remain exactly as Protocol P v2.3.3 states. Do not redesign them in the driver.

## Downstream project gates

Even after driver review and the development screen, the project still requires:

- written Amendment A2 and a replacement approved assignment/config lineage if Protocol P supports it;
- coherent regeneration of dev/pilot/validation roles;
- Gate 4 estimator artifacts;
- Gate 5 controller protocol;
- Gate 6 end-to-end seed smoke;
- Gate 7 immutability/frozen-config audit;
- joint final config approval; and only then
- one-shot confirmatory test generation/evaluation.

The current pre-A2 local dataset remains development scaffolding: 472 dev/pilot/validation pairs, zero test rows. Do not treat it as frozen or confirmatory.

## Session-53 verification

```text
independent inventory construction       180 logical / 168 physical / 12 reused
full packet suite                         750 passed in 13.28 s
compileall                                clean
git diff --check                          clean (checkout-EOL warning only)
config.json                               absent
Stage-0 result artifact                   unchanged; not re-executed
Protocol-P replay/stage rollouts          none in Codex Session 53
confirmatory test split                   untouched
```

## Review and evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence are not approval.
- Development screens, pilots, fixtures, diagnostics and regression checks remain separate from frozen, confirmatory or final results.
- Keep detection, attribution, information/action authorization, and controller outcome separate.
- Public README running history is append-only once settled; only the newest active-review state may be reviewer-edited under the review-cycle playbook.
- Packet README is an outsider-clean runbook: no local paths, agents, sessions, or internal history.
- Do not use root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute collection. Use:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

- Do not use bare `python` or `pip`; use the project venv.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture physical UTF-8 EOF bytes/count/hash, patch only the complete verified unique EOF block, then assert old prefix exact, one new header after the boundary, and additions-only diff.

## Closeout numbering

- Next Codex session: **54**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport54.md`.
- Next regular Codex progress report: **Session 56**, unless a phase transition or approved amendment triggers one sooner.
