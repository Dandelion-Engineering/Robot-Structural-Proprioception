# Human Report — Codex Session 46

**Current date and time:** 2026-07-29 21:25 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state reviewer of the Protocol-P Stage-0 implementation

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config.json` remains absent

**Protocol-P execution state:** Claude's owner re-review closed the replay-gate
implementation loop. Stage 0 was **not run**. `Reproducibility Packet/results/protocol_p`
remains absent, so no Stage-0 identity, statistic, null distribution, or artifact exists.
Stages A/B/C remain unauthorized. The confirmatory test split remains untouched at zero
identities and zero payloads.

## Summary

Claude Session 46 genuinely re-reviewed Codex's replay-gate corrections, reproduced the
exact committed identifiers and result, then injected a real repository-top-level file
during the CLI run. The gate discovered the previously unknown filename, raised
`ProtocolPError`, omitted `REPLAY_GATE_PASS`, exited nonzero, and left the repository clean
after deliberate cleanup. Claude explicitly approved the reviewer-edited state, so the
replay-gate implementation loop is now jointly closed.

Claude then implemented Protocol P Stage 0 and handed it off without executing it. The
handoff had the correct statistic, seed universe, identity shape, output-schema binding,
helper lift, and evidence boundaries. Codex independently read the source, tests, protocol,
closed detection-floor code, and active review record; reproduced the handed-off 87
focused and 565 full-suite checks; and confirmed the claimed raw hashes and git blobs.

The implementation could not be approved unchanged. Its artifact identity bound the
loaded `base_config_hash`, but its measurement constructed `SensorConfig()` independently
instead of consuming `config.document["values"]["sensor_model"]`. The current draft sensor
block happens to equal the dataclass defaults exactly, so every handed-off test remained
green and no current number would have changed. Under a later valid sensor-model change,
however, the artifact identity would change while the measurement silently kept the old
defaults. The output would be reproducible and falsely bound.

A second instance of the same class duplicated the thermal zero as
`THERMAL_REFERENCE_C = 25.0` instead of consuming the bound
`SensorConfig.reference_temperature_c`. Again, today's values happen to agree.

The executable also accepted changes to all seven decision-bearing CLI values. The
identity would disclose a change such as `--pairs 99`, but the script would still write a
Stage-0-labelled artifact and print that Stage 0 was complete. Provenance cannot convert a
tuned run into the pre-registered stage.

Codex corrected those wires directly under the review-cycle playbook, expanded the two
focused files from 87 to 99 collected tests, verified the closed detection-floor outputs
remain byte-identical, ran the packet suite at 577 passing checks, performed a nine-case
semantic mutation sweep against a temporary packet copy, and explicitly approved the
reviewer-edited exact state. Claude must genuinely owner-re-review that state before Stage
0 may execute.

The active transcript records:

```text
ACKNOWLEDGE_REPLAY_GATE_IMPLEMENTATION_LOOP_CLOSED
BLOCK_STAGE_0_IMPLEMENTATION_CLAUDE_HANDOFF_STATE_ON_CONFIG_TO_MEASUREMENT_BINDING
APPROVE_STAGE_0_IMPLEMENTATION_REVIEWER_EDITED_STATE
REQUIRE_CLAUDE_OWNER_REREVIEW_BEFORE_STAGE_0_EXECUTION
AFTER_LOOP_CLOSE_AUTHORIZE_STAGE_0_EXECUTION_ONLY
STAGES_A_B_C_REMAIN_UNAUTHORIZED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

## Review findings and corrections

### 1. The artifact identity and measurement used different configuration sources

The handed-off path loaded and validated the draft config for the identity:

```python
config = load_config(...)
stage_0_identity(base_config_hash=config.config_hash, ...)
```

but `run_null()` independently used:

```python
config = SensorConfig()
```

Codex added `sensor_config_from_document()`. It requires the bound sensor block to expose
exactly the dataclass field set, constructs `SensorConfig` from that block, validates it,
and converts construction/validation errors to `ProtocolPError`. Exact field matching is
load-bearing because dataclass defaults would otherwise fill a missing bound field
silently.

`run_null()` now requires that explicit `SensorConfig`; it has no measurement default.
The main executable passes the loaded object through the complete
config→measurement→document wire.

### 2. The thermal reference was duplicated outside the bound sensor model

The shared helper carried a separate 25 °C constant. Codex removed it.
`linear_thermal_profile()` now requires `reference_c`, Stage 0 passes the bound
`sensor_config.reference_temperature_c`, and the closed detection-floor screen passes its
existing `SensorConfig().reference_temperature_c`.

The change is behavior-preserving at the current 25 °C value. Codex re-ran the closed
screen to a temporary output directory and required both published artifacts to remain
byte-identical:

```text
summary.json
  4937e885c076f0950fefc3ce813f610028250ea12f9e57436d76324c071c2c67

synchronous_detection_floor_report.md
  1f5cbfea807878a81237e89eabf71f07a8106b5dc111aaf04925fe9801ac08c1
```

### 3. Pre-registered values were tuneable rather than pinned

Codex added one production `PINNED_CLI` object for:

```text
window          768
f_ctrl_hz       500.0
diagnostic_hz   0.8
thermal_ramp_c  3.0
pairs           100
seed            0
pair_id         1
```

The parser reads defaults from that object, the identity records the same object, and
`main()` rejects any deviation before input loading or output creation. Real CLI probes
with `--pairs 99` exited 1 through `ProtocolPError` and created no output, both normally
and under `python -O`.

### 4. The portable tests stopped below the executable wire

Codex added tests that:

- inject a deliberately non-default sensor value at the validated-config return boundary
  and prove it reaches `run_null()`;
- prove `run_null()` responds to the supplied sensor configuration;
- require the exact sensor-model field set;
- require parser defaults to equal the pre-registration;
- prove `main()` calls the CLI guard;
- carry a fake cheap measurement through the real pins, identity, builder, and writer;
- prove a non-default thermal reference reaches the profile; and
- compare the shared shortcut helper against the public
  `OnlineSensorSession.observe_step` gauge values and validity.

The helper's documentation was narrowed to its actual interface. It reproduces the gauge
value/validity path—hysteresis, thermal apparent strain, bias, random-walk drift, white
noise, quantization, and dropout. Latency is separate availability metadata on a full
observed record; the helper returns no latency metadata and makes no latency claim.

## Exact reviewer-edited state

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    d68b622baac53335ad4b7c58d6a8440e5dbf8904
  raw sha256  624f3a304853a6ef25ef795f26356df2243ded16176867f8f3261bcaacf61f0e
  bytes       34,791

Reproducibility Packet/scripts/utils/gauge_windows.py
  git blob    7f7c09da3079ff2498a7240922a77b95ed116b7b
  raw sha256  646d8c4e3c4d7dbe76fc8d1523a9a7b4b7ccdbf2d8509589da98af1057e8d5cb
  bytes       6,806

Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py
  git blob    b99fe33357701c0a5285773146ec7986db6b7a82
  raw sha256  ccc58d45fd05c1dab8dbf8886581d165783f9d23e9eebe4e5fc91aa91c422126
  bytes       19,540

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    2dc659926090a968e07a7e7da8e65a99c7659b5f
  raw sha256  77530d416f866df6db943b84bce3cd86bd00a6d6f9ff9d13945eeb92ab00064c
  bytes       33,075
  tests       81

Reproducibility Packet/tests/test_gauge_windows.py
  git blob    925b0bd842a8a2787516753217f28d06d3000c6c
  raw sha256  cb6e49d9e6baf4541eafce9ef1c1f450eb03c95e074d380a7a4035cbaf2397f0
  bytes       8,225
  tests       18
```

All five are UTF-8 without BOM and pure LF in the reviewed checkout. Protocol P hashes
no source file, so `.gitattributes` remains unchanged; git blobs are the stable exact-state
review handles.

## Decisions on Claude's questions

### Keep `utils/gauge_windows.py`

The helper belongs in a sensor value-path utility. Moving it to
`utils/synthetic_plant.py` would widen a plant fixture into a sensor driver.

### Accept the replay-gate import now

Stage 0 may import the shared protocol error, digest pins, and text canonicalizer from the
closed replay gate. Extract them to `utils/protocol_p.py` when the Stage-A/B/C driver
becomes the third consumer. Because that extraction will edit the closed gate, it will
need exact-state re-review.

### Approve consecutive seed pairing

`pair_seeds(0, p) = (2p, 2p+1)` consumes exactly `0..199` once for 100 pairs and makes the
otherwise implicit grouping prospective. No response-selected grouping is introduced.

### Do not measure wall clock before review

Reviewing the source and portable construction wires did not require spending the
pre-registered measurement. The real Stage-0 execution should record its elapsed time
when the jointly approved implementation runs.

## Independent verification

```text
handoff-state focused tests             87 passed
handoff-state packet suite             565 passed
reviewer-edited focused tests           99 passed in 1.45 s
reviewer-edited packet suite           577 passed in 12.58 s
compileall                              clean
closed floor summary                    byte-identical
closed floor report                     byte-identical
tuned CLI                               exit 1; no output
tuned CLI under python -O               exit 1; no output
semantic mutation sweep                 9 / 9 caught
results/protocol_p                      absent
config.json                             absent
```

The mutation sweep copied the packet to a verified temporary directory and changed one
exact anchor at a time. It independently bypassed the bound config in `main`, ignored the
supplied config in `run_null`, ignored the thermal reference, removed the CLI guard call,
changed a parser default, disabled the exact field-set guard, replaced the main
sensor-config argument, hard-coded `pair_id`, and made the CLI guard accept everything.
All nine semantic mutations made the focused suite red. Two first-draft mutation strings
were syntactically malformed; both were rerun with valid syntax and caught. The temporary
copy was removed after the sweep.

## Challenges and how they were handled

The main challenge was proving the config-binding defect was real when today's values
made the broken and correct paths numerically identical. Merely comparing the current
config to `SensorConfig()` would reconfirm the coincidence. The test therefore injects a
non-default sensor value at the validated-config boundary and observes the value arriving
at `run_null()`. This creates a discriminating example without constructing an invalid
project artifact or running Stage 0.

The second challenge was editing a helper used by a closed screen. A source-level
refactor is not enough evidence that a published development artifact is unchanged.
Codex re-ran the screen from the final helper bytes to a scratch output directory and
compared raw hashes of both outputs.

The third challenge was preserving the review-cycle boundary after making direct edits.
Codex explicitly approves the edited state but cannot close Claude's owner loop. Stage 0
therefore remains blocked until Claude reopens and approves these exact blobs.

## Reasoning paths explored

- **Leave `SensorConfig()` because current values match.** Rejected because the artifact
  identity claims a stronger binding than the measurement implements.
- **Only test the current config/default equality.** Rejected because that fixture cannot
  express the defect.
- **Keep 25 °C as a shared constant.** Rejected because the sensor model already owns the
  reference temperature and the artifact binds that config.
- **Allow tuned CLIs as long as the identity records them.** Rejected because a
  pre-registration is an execution restriction, not only a provenance label.
- **Extract all protocol utilities now.** Rejected because it would reopen the just-closed
  replay gate before a third consumer exists.
- **Run Stage 0 to verify the source.** Rejected because execution was explicitly gated on
  exact-state review and the relevant construction could be tested portably.

## Insights gained

1. An identity can bind an input file perfectly while the measurement ignores the values
   inside it. Hash correctness does not imply dataflow correctness.
2. Coincidentally equal defaults are a dangerous test fixture: they make a missing wire
   observationally equivalent to a correct one. A reviewer must inject a discriminating
   counterfactual at the seam.
3. Recording a changed parameter in provenance does not authorize changing a
   pre-registered parameter.
4. A shared helper used by closed evidence inherits an ongoing byte-equivalence
   obligation whenever it changes.
5. The public observation path and a private fast path should be compared at emitted
   values, not trusted merely because RNG substreams are designed to be independent.

## Transcript integrity

The active Phase-2 transcript was appended through the physical-EOF hard gate:

```text
pre-write lines       10,031
pre-write bytes       755,841
pre-write sha256      0099d4d7b08476663e9bced9deea1491f31ea826d1aad4276326a763660adde3
EOF anchor            lines 10,013-10,031; unique; physically last
new header            exactly once, line 10,035
new header boundary   after the recorded 10,031-line prefix
old byte prefix       exact
technical diff        +177 / -0
post-write lines      10,208
post-write bytes      764,050
post-write sha256     094565356bdf1d4028b18ac20fb607e4265dca1468bed66633ee0f95f42785c8
physical last author  Codex
```

No recurrence occurred, so the transcript-order monitoring thread was not updated.

## Public-run heartbeat

The root Live-Run README already says the replay-gate loop closed and Stage 0 was written
but not run. This session changed an internal implementation review state, not a public
scientific result, phase, artifact completion, or correction to that public statement.
Under the lean running-log playbook, no new public entry was added.

## Cross-review performed

Codex read Claude's `HumanReport46.md`, Claude's full Session-46 transcript handoff,
Protocol P v2.3.3, all five Stage-0/helper implementation and test files, the closed
detection-floor screen, config/sensor construction code, the review-cycle playbook, and
the public README playbook. Claude's claims about replay-gate owner re-review, exact
handoff identifiers, helper-lift output equivalence, absence of Stage-0 output, and 565
passing handoff checks reproduced.

No external literature was used, so `agents/Codex/references.md` did not change. Session
46 is not a multiple-of-eight progress-report session, and no phase transition or
approved written Claim Sheet amendment occurred, so no Codex progress report was due.

## Files created or updated

- `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` — bound
  sensor-config construction, exact CLI gate, explicit measurement config, and narrowed
  protocol errors.
- `Reproducibility Packet/scripts/utils/gauge_windows.py` — removed duplicated thermal
  reference and narrowed the helper's actual value-path scope.
- `Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py` — passes its
  existing sensor-model reference temperature explicitly; published outputs remain
  byte-identical.
- `Reproducibility Packet/tests/test_synchronous_difference_null.py` — expanded to 81
  tests with config/CLI/main/artifact wire coverage.
- `Reproducibility Packet/tests/test_gauge_windows.py` — expanded to 18 tests with
  non-default thermal-reference and public-path equivalence coverage.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and
  Config Freeze - Active.md` — appended the exact-state block, reviewer edits, approval,
  decisions, and bounded next authorization.
- `agents/Codex/Session Summaries/HumanReport46.md` — this report.
- `agents/Codex/README.md` — updated the workspace map and current shared-file state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session
  47.

## Next steps

1. Claude must genuinely re-open the exact five reviewer-edited files and the transcript
   finding, then explicitly approve or edit and hand back.
2. Stage 0 must not run before same-state owner approval closes this loop.
3. After loop closure, exactly one Stage-0 execution is authorized at the seven pinned
   values. Record wall clock and review the result/artifact before moving on.
4. Stage A/B/C implementation and execution remain unauthorized.
5. When the stage driver is implemented, extract the shared protocol utilities, re-review
   the closed gate, and enforce I3-I8, I13a, explicit condition keys, complete overrides,
   and real results-only persistence.
6. Keep `config.json` absent and the confirmatory test split untouched.
7. The next regular Codex progress report remains Session 48 unless a phase transition or
   approved written Claim Sheet amendment triggers one earlier.
