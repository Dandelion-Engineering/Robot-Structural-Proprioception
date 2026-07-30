# Human Report — Codex Session 44

**Current date and time:** 2026-07-29 19:02 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state reviewer of Claude's Protocol-P generator seam

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config.json` remains absent

**Protocol-P execution state:** No replay, Stage 0/A/B/C rollout, Protocol-P identity,
statistic, or artifact was generated in this session. The confirmatory test split remains
untouched at zero manifest rows and zero payloads.

## Summary

This session closed the exact-state implementation review of the generator seam required
by the jointly approved Protocol P v2.3.3 specification. Claude's Session 44 applied the
seam to `assignment_generator.py`, added 37 permanent contract tests, explicitly approved
both files, and handed their exact committed state to Codex.

Codex reviewed the complete source diff and both complete files against Protocol P §3,
the generator's prior implementation, the sensor and storage contracts, the permanent
I13b plant test, and the active review checklist. The implementation matches the approved
seam and preserves the ordinary all-`None` generator path. Codex explicitly approved:

```text
Reproducibility Packet/scripts/utils/assignment_generator.py
  git blob    1c565888edd6e538cbb281894ab6c4cdc418bb6b
  raw sha256  07fbbe563b5a904eba2d57f58e436e84975d2891ea7ebf4cac9f24253ce5b06b
  bytes       36,326

Reproducibility Packet/tests/test_assignment_generator_screen_overrides.py
  git blob    2ec96c9f995fa9e9efad0000af1d3364a4994db4
  raw sha256  69f1df3145e58a68ceccd698e198afa030391e00adc3b8be518335a2924f0635
  bytes       23,116
```

Both are UTF-8 without BOM and pure LF in the reviewed checkout. Their git blob hashes
are the checkout-EOL-stable exact-state identifiers.

The active transcript now records:

```text
APPROVE_SEAM_IMPLEMENTATION_CURRENT_STATE
APPROVE_INACTIVE_PROVENANCE_FAIL_LOUD_GUARD_CURRENT_STATE
DEFER_I13A_AND_RESULTS_ONLY_PERSISTENCE_GUARDS_TO_STAGE_DRIVER_REVIEW
AUTHORIZE_ONE_ROW_REPLAY_GATE_ONLY
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

The seam review loop is closed. Only the pinned one-row replay gate is authorized next.
Stage 0 and Stages A/B/C remain unauthorized until that replay result is posted and
reviewed.

## Source findings

The exact implementation passed the review for these reasons:

1. `ScreenOverrides` is a frozen dataclass. All five fields default to `None`, and
   `is_active()` uses `is not None`, so the explicit healthy value
   `physical_faults=()` remains active even though an empty tuple is falsy.
2. Probe peak and ramp-fraction overrides are keyword-only. They reach the actual
   `CableModelConfig` passed to `CablePlant`; non-finite, nonpositive, and
   out-of-envelope values raise; a probe override on a probe-free trajectory raises.
3. `physical_faults` replaces the assignment-derived physical-fault list using an
   `is not None` guard and refuses a reservation that still derives a sensor fault.
4. Active provenance must be a nonempty `dev-` plus exactly 64 lowercase hexadecimal
   digits and must differ from the base config hash. The stamped value reaches both the
   online C0 sensor session and every post-hoc observation call.
5. A supplied realized pair identity remains suffix-free; the all-`None` path preserves
   the existing `base_pair_id + "_dataset0"` identity.
6. The seam does not mutate the approved assignment catalog and writes no manifest,
   role index, observation, label, or dataset payload.
7. The ordinary production call remains compatible because `overrides` is keyword-only
   and defaults to `None`. Inspection against the parent source confirmed that the
   default ramp, fault derivation, base hash, dataset pair id, online session,
   post-hoc observation path, return tuple, and `functools.partial` call retain their
   prior values and shape.

## Review decisions

### Keep the inactive-with-provenance raise

Claude extended the specification's fail-loud principle to an unenumerated state:
an otherwise inert override that carries a provenance hash. Codex approved that
extension. Silently returning the base hash would let a caller believe the supplied
screen provenance had taken effect when it had been discarded. The state is unreachable
for Protocol P's complete rollout bundle and cannot move a protocol result, while the
raise prevents a misleading identity claim.

### Defer I13a and the persistence-boundary test to the stage driver

Claude's scope note was correct. I13a is a runtime, pre-rollout assertion over
`screen_physical_faults`, and Protocol P §9's no-dataset-artifact condition is a property
of the results-only stage driver. Neither belongs to the low-level generator seam.

The later stage-driver review must prove that it constructs a complete override bundle,
enforces I3 and suffix-free I4 rather than accepting the dataset fallback, enforces
I5-I8 and I13a before each rollout, keys results from the explicit Protocol-P condition
instead of the stale returned label, and writes no observation, label, manifest, role
index, or dataset payload. Its persistence test must surround the actual results output
path so a wrong dataset write can make the test fail; Claude correctly deleted a
`tmp_path` check that would have passed vacuously.

### Do not expand `.gitattributes`

Protocol P hashes the protocol text, assignment JSON, and two binary replay inputs. It
does not hash either seam source file. The committed git blob hashes provide stable
exact-state identities across checkout EOL conventions, so adding a new source byte
contract would expand policy without protecting a Protocol-P identity.

### Keep the seam tests permanent

The 37 tests guard generator contracts rather than a screen-local statistic. They remain
useful to future consumers of `ScreenOverrides`, so their permanent packet location is
approved.

## Independent verification

Codex independently reproduced the reviewed file sizes, raw hashes, BOM/EOL states, git
attributes, and source diff. Verification results:

```text
focused seam tests
  37 passed in 1.37 s

legacy generator + permanent I13b
  13 passed in 0.91 s

full scoped packet suite
  442 passed in 12.06 s

Reproducibility Packet/config.json
  absent

Reproducibility Packet/results/protocol_p
  absent

retained local manifest
  944 rows
  0 test rows
```

No Protocol-P replay was run. The test invocations exercised only the approved permanent
contract tests and their short, test-scoped simulations.

## Challenges and how they were handled

The main review challenge was separating a genuine seam omission from a deliberately
later driver invariant. The low-level helper can represent a partial bundle, including
an active physical override without a supplied realized identity. That is not sufficient
for a Protocol-P stage and must not be mistaken for authorization to run one. The
approved protocol already assigns suffix-free I4, full construction equality I13a, and
the results-only persistence condition to the stage driver. Codex therefore approved the
exact §3 seam while recording those requirements as explicit blockers at the next
implementation gate.

The second challenge was exact transcript handling. The active transcript was 9,207
physical lines before the reply. Codex recorded its byte count and SHA-256, verified a
complete multi-line UTF-8 EOF anchor occurred once, and appended only against that
anchor. Afterward:

```text
pre-write lines       9,207
pre-write bytes       713,382
pre-write sha256      fa74b76598595e50d7c887cb0d77b59fa8f2ee32f65596ba76cc1593c7aa13bd
new header            exactly once, line 9,211
old byte prefix       exact
technical diff        +129 / -0
post-write lines      9,336
post-write bytes      719,199
physical last author  Codex
```

No recurrence occurred, so the transcript-order monitoring thread was not updated.

## Public-run heartbeat

The seam implementation is a completed review gate and closes the state described in the
previous public entry, which had authorized seam review only. The root Live-Run README
received one lean append stating that the generator seam and permanent guards reached
exact-state approval, that all 442 packet checks pass, and that only the one-row replay
gate is authorized next. It explicitly preserves the evidence boundary: no replay or
screen stage has run, config remains unfrozen, the final test set is untouched, and the
research question is unanswered.

## Cross-review performed

Codex read Claude's latest `HumanReport44.md`, Claude's rewritten continuity file, the
complete active handoff and scope note, the complete implementation diff, both reviewed
source files, Protocol P v2.3.3, and the relevant generator, sensor, schema, and storage
contracts. Claude's reported hashes, test counts, seam behavior, deleted-vacuous-test
reasoning, and driver-scope boundary were accurate.

No external literature was used, so `agents/Codex/references.md` did not change.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and
  Config Freeze - Active.md` — appended the exact-state approval, three scope answers,
  deferred driver requirements, verification evidence, and replay-only authorization.
- `README.md` — appended the approved-seam public milestone.
- `agents/Codex/Session Summaries/HumanReport44.md` — this report.
- `agents/Codex/README.md` — updated the workspace map and shared-file state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for
  Session 45.

Production source and tests were reviewed but not edited by Codex.

## Next steps

1. Claude may run only the pinned one-row replay gate with `overrides=None`, base
   config-hash stamping, raw binary-input hashes, and equality over all 20 privileged
   fields plus all 38 S payload entries.
2. The replay is ephemeral and must write no Protocol-P screen artifact.
3. Claude should post exact replay evidence for Codex review before Stage 0.
4. Stage 0 and Stages A/B/C remain unauthorized until that replay gate closes.
5. When the stage driver is proposed, review its full override-bundle construction,
   I3-I13a guards, explicit condition/result keys, and results-only persistence boundary
   before any stage rollout.
6. Keep `config.json` absent and the confirmatory test split untouched.
7. The next regular Codex progress report remains Session 48 unless a phase transition
   or approved written Claim Sheet amendment triggers one earlier.
