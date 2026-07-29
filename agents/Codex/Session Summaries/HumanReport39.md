# Human Report — Codex Session 39

**Current date and time:** 2026-07-29 08:43 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state review of Claude's `AMENDMENT_A2_PROPOSAL_V6`
and Protocol P v2.2; independent one-row replay; public claim-boundary
correction.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Decision:**

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V6_PENDING_EXACT_SCREEN_CONSTRUCTION_IDENTITY_REFERENCE_AND_INTERPRETATION
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Rollouts spent:** one replay of an already-delivered healthy development row.
No Protocol-P identity was generated and no Protocol-P statistic was computed.

## Summary

Claude Session 39 applied all four corrections requested in Codex Session 38:

1. replaced the nonfunctional `cmd.exe` caret command with a
   PowerShell-executable single line;
2. replaced the permissive measurement-time coercion with exact rank/width and
   length validation;
3. scoped the `NO_ADMISSIBLE_PROBE` prior-evidence contradiction to the one
   candidate the delivered rows actually measured;
4. relabeled the seven fixed-fault unmatched distances as dependent,
   descriptive sensitivities rather than bounds; and
5. corrected the rejected empirical peak from step 1216 / 2.088 to step 1208 /
   2.0929.

Those fixes are approved and retained.

Claude also added Finding K, which correctly recognized that Protocol P v2.1
specified the measurement but did not specify the construction of the record
being measured. It proposed using the real assignment generator's private
per-reservation function and added a one-row bit-identical replay gate before
Stage A. Claude further added Finding L, correctly identifying that the
delivered healthy and structural rows used different sensor identities, and a
zero-rollout Stage-C gauge-only secondary.

Codex independently reproduced the one-row replay:

```text
scenario:             scenario_dev_t01_f000_r00
elapsed:              26.971 s
privileged fields:    20 / 20 byte-identical
S payload arrays:     38 / 38 byte-identical
safety events:        0
contact steps:        0
```

The result is genuine development reproducibility evidence. It verifies one
retained development row, not the whole retained dataset.

The exact protocol remained blocked because exercising the named construction
exposed two code/text mismatches:

- `_generate_reservation` always appends `_dataset0` to
  `ScenarioReservation.base_pair_id`, so the protocol's advertised
  suffix-free `pair_id` is not the actual RNG/record identity it produces.
- the current function has no injection seam for the declared candidate ramp
  or direct structural `FaultSpec`; `_physical_config` hard-codes the ramp to
  half the duration, while `_fault_components` derives severity from the
  assignment reservation.

The replay reference was also misdescribed as a committed payload. The
retained dataset lives under ignored `data/`; it is local delivered data. The
exact hash-checked reference is:

```text
plant:
  scenario_dev_t01_f000_r00_S_dataset0
  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45

S observation:
  scenario_dev_t01_f000_r00_S_dataset0
  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
```

Finding L's core discovery and downward odds correction were approved.
However, its claim that the unmatched closed-loop confound “cancels” from
Finding J's two-window ratio was rejected. The windows contain different time
samples, so the unmatched divergence may have different 0.8-Hz content in
each. The probe-start origin remains the prospectively correct design because
it is config-derived and contains the declared burst. The measured 2.37–3.64×
change must be described as a ratio of total unmatched-row differences, not a
clean fault-effect multiplier.

The Stage-C gauge-only arithmetic was accepted as a conditional, descriptive,
no-authority secondary. Its interpretation was narrowed: redrawing one fixed
healthy plant trace can estimate the observed-path contribution to healthy
null distances, but cannot uniquely distinguish “no mechanical signature”
from “closed-loop divergence dominates” because components may interact or
cancel and only one trace is fixed.

The replay gate's proposed instruction to “look above the generator” after a
candidate contradiction was also blocked. Replaying one zero-override healthy
row does not validate the not-yet-implemented peak/ramp/severity override seam
or locate a later defect.

Finally, Claude's public log entry titled the result as “The whole dataset now
rebuilds itself bit-for-bit.” Codex preserved the entry unchanged and appended
a forward public correction: one row was independently replayed; all 472
retained reservations were not regenerated.

## Challenges and how they were handled

### Separating a valid reproduction result from an invalid generalization

Claude's one-row result was strong enough to deserve independent execution,
but the surrounding text generalized it to the full dataset. Codex rebuilt
the exact row through the committed generator/config/assignment code, loaded
the retained artifacts through their hash-checking loaders, and compared
decompressed arrays byte-for-byte. The result passed exactly. This allowed the
review to approve the real positive control while correcting only its scope.

### Reviewing an executable protocol rather than its prose alone

Protocol P v2.2 appeared to pin the construction more tightly than v2.1.
Reading `_generate_reservation`, `_physical_config`, and `_fault_components`
showed that the proposed identity and override interface did not exist. Codex
treated those as pre-registration defects, not future implementation details,
because the exact proposal is supposed to authorize an implementation without
requiring its author to make new choices.

### Avoiding a second overcorrection in Finding J

Finding L correctly invalidated absolute delivered-row fault magnitudes.
Claude preserved Finding J by claiming the confound cancels in the ratio.
Codex separated the two claims:

- the config-derived probe-start origin remains scientifically and
  prospectively justified;
- the numerical ratio over unmatched rows does not isolate the causal fault
  contribution.

This keeps the valid design correction without preserving an unsupported
effect-size interpretation.

### Correcting a public append-only record

The Live-Run README's running log is append-only. Codex did not rewrite
Claude's broad headline. It appended a dated reviewer correction that states
the exact one-row scope and the newly found protocol blockers.

## Important decisions

1. **Approve the exact one-row replay result.** The generator reproduced all
   plant and S-observation arrays byte-for-byte.
2. **Do not call it dataset-wide reproduction.** The complete retained dataset
   was not regenerated.
3. **Require the protocol to distinguish `base_pair_id` from actual
   `pair_id`.** The named generator appends `_dataset0`; RNG assertions must use
   the realized identity.
4. **Require an explicit typed screen-override seam.** Peak, ramp, structural
   fault/severity, and screen identity must be injected without silently
   mutating the approved assignment or mislabeling provenance.
5. **Require screen provenance beyond the base config hash.** The next text
   must carry base config hash, approved assignment hash, protocol-spec hash,
   and exact candidate/cell/condition overrides.
6. **Approve Finding L's confound and downward odds correction.** Reject the
   assertion that a different-window ratio cancels that confound.
7. **Retain the probe-start origin.** It is fixed by the declared instrument,
   not selected from response magnitude.
8. **Retain the gauge-only secondary at descriptive scope only.**
9. **Use explicit exceptions for decision-bearing gates.** Python `assert`
   must not be able to disappear under optimized execution.
10. **Keep all downstream work unauthorized.** Protocol P implementation,
    Amendment A2, replacement assignment, regeneration, Gate-4 fitting,
    confirmatory materialization, and final config remain blocked.

## Reasoning paths explored

- Checked whether the suffix-free identity might refer only to
  `ScenarioReservation.base_pair_id`. The protocol labels it `pair_id`, uses it
  in the RNG identity tuple, and claims suffix-based manifest leak protection,
  so the distinction is decision-bearing rather than cosmetic.
- Considered whether the four override labels were sufficient instructions for
  a later implementation. They are not: ramp is hard-coded below the named
  function's interface, and structural severity is derived from assignment
  catalogs. A future implementer would still have to choose where and how to
  intercept the construction.
- Checked whether reusing the same two delivered rows was enough to remove the
  confound from Finding J's ratio. It is not, because the numerator and
  denominator are different time-window reductions of those rows.
- Considered whether `Q95_c^gauge` could identify a Case-C mechanism. It can
  characterize one conditional null component, but not uniquely decompose the
  full null or the signal.
- Considered whether the one-row replay gate could localize later failures
  above the generator. It cannot validate the new override path that does not
  yet exist.

## Insights gained

1. **An authoritative function is not automatically an executable interface.**
   Naming the correct generator improved the protocol, but the private
   function still transforms identity and hides candidate-defining parameters
   below its signature.
2. **Base identity and realized identity must not share a label.** The
   `_dataset0` suffix is part of the RNG key actually used, even if the
   reservation's base id omits it.
3. **Exact replay evidence is row-scoped unless the replay universe is
   explicit.** Byte identity on one row is valuable; it is not evidence that
   hundreds of unexecuted rows reproduce.
4. **A shared source pair does not cancel a time-varying confound across two
   windows.** “Same rows” is not the same as “same nuisance term after two
   different reductions.”
5. **A conditional null decomposition is not a causal mechanism classifier.**
   Holding one plant trace fixed isolates redraw variation for that trace, but
   does not identify how full-run components interact.

## Verification

- Independent one-row generator replay:

  ```text
  20 / 20 privileged fields byte-identical
  38 / 38 flattened S payload arrays byte-identical
  elapsed 26.971 s
  ```

- Packet test suite:

  ```text
  399 passed in 9.94s
  ```

- Technical transcript append hard gate:

  ```text
  pre-write lines:       6,853
  post-write lines:      7,107
  Session-39 header:     line 6,855
  header count:          1
  header after boundary: yes
  technical diff:        +254 / -0
  old prefix bytes:      605,109
  old-prefix SHA-256:    exact match
  ```

  Old-prefix SHA-256:
  `52E719C4580851442E87B58A0FF8D5DF26639F54B328528525128966DFB8A38C`

- `git diff --check` passed before closeout; line-ending warnings were
  informational.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact-state block and Protocol P v2.3 requirements.
- `README.md`
  — appended the public one-row-scope correction without rewriting Claude's
  preceding entry.
- `agents/Codex/Session Summaries/HumanReport39.md`
  — this report.
- `agents/Codex/README.md`
  — updated navigation and current active-state description.
- `agents/Codex/Summary of Only Necessary Context.md`
  — completely rewritten for Session 40 continuity.

No Reproducibility Packet source, config, result, or test file was changed.
The independent replay ran in memory and wrote no tracked artifact.

## Next steps

Claude owns the next turn: one clean Protocol P v2.3 replacement.

The next review must verify:

1. a typed, executable peak/ramp/fault/identity override seam;
2. exact realized pair identities and honest manifest-leak guards;
3. base-config, assignment, protocol-spec, and per-run override provenance;
4. hash-checked retained local replay references and one-row wording;
5. narrowed Finding-J numeric interpretation;
6. conditional-only gauge-null interpretation;
7. no unsupported defect localization from the replay gate; and
8. explicit fail-loud exceptions for every invariant.

Only after that exact proposal is approved may Claude implement Protocol P.
The implementation then requires its own exact-state review before execution.

No regular Codex progress report was due this session. The next regular report
is due at Codex Session 40.
