# Codex — Human Report, Session 113

**Date and time:** 2026-08-10 21:23 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 120 unless a
phase transition or approved Claim Sheet amendment triggers one sooner.

---

## Summary

Claude Session 113 closed the separate public README correction loop and returned the first
implementation of Slot 9's rung-2 architecture for review. I authenticated and read the frozen
design, the complete production module, the complete test file, Claude's report and handoff, and
the relevant approved rung-1/scoring seams.

The production module is correct and remains byte-for-byte unchanged:

```text
Reproducibility Packet/scripts/utils/attribution_net_rung2.py
Git blob                 ca192af0b1263fdb7d19491e09a2b5c99dc7639b
raw SHA-256              59333b48b4c9a580a165c83f672232a75cbc8220debe98a7c04748ac705ff7c7
size / physical lines    18,043 B / 362 LF
CR / BOM / final newline 0 / none / yes
review state             CLAUDE APPROVED / CODEX APPROVED
```

I found no production-code defect. I did find two test-state defects. First, Claude explicitly
asked whether its new every-parameter-gradient assertion could miss a stage that is live and
receives gradient but is still wired contrary to the design. It can: reversing the live causal
stem blocks or moving the live normalization before them preserves parameter count, shape,
causality and gradient reach while violating the declared encoder path. Second, the test and
module prologues said all four disclosed D4 limitations were pinned, but the approved
`capacity_sweep.score_arm` path was never exercised with the rung-2 module.

I added two synthetic tests and explicitly approved the reviewer-edited test state:

```text
Reproducibility Packet/tests/test_attribution_net_rung2.py
incoming Git blob        52809287496ae50705c9e8d54b78df9b1612292f
reviewer Git blob        c43d33b007701cf3c9b24c1f6a267d2329c25c1e
reviewer raw SHA-256     caaf108deab021eecfc418a93ea2ae6c6965ab771303dcae51cc4584d6017f82
size / physical lines    38,242 B / 938 LF
CR / ASCII               0 / yes
review delta             +64 / -0
review state             CODEX APPROVED / CLAUDE OWNER RE-REVIEW OPEN
```

The module/test review loop therefore remains open only for Claude's genuine owner re-review of
the current test blob. Step 2 is not yet closed, and the rung-2 executable plus its tests remain
unauthorized.

## Public README correction closure

Claude re-derived the four quantities in the Session-112 public correction and explicitly
approved the exact blob Codex had approved:

```text
README.md Git blob       bb98b66ecf4ed37f2c13bc38607fd3dd88ecdf24
Claude approval          explicit / current blob
Codex approval           explicit / current blob
review loop              CLOSED / BOTH APPROVED
```

The corrected public history remains append-only. I agreed with Claude's decision not to add a
third dated entry simply translating the correction's vocabulary. The next earned public entry
must introduce rung 2 in plain language. The Live-Run heartbeat was checked against the playbook;
this session did not update the root README because the internal module/test review remains open
and no outward-facing artifact, phase transition or public result was completed.

## Exact implementation review

The handed-off module reproduces the approved design's construction:

- 64-channel causal convolutional stem with four imported rung-1 blocks at dilations 1, 2, 4, 8;
- per-timestep channel normalization after the stem;
- a two-layer, unidirectional, bias-bearing GRU with hidden width 96;
- exact bias-bearing Q/K/V projections split over four heads, one final-state query and all-step
  keys/values, scaled by `sqrt(H / n_heads)`, with no output projection or attention dropout;
- final-state-plus-attention-context fusion through one `Linear(2H, H)` and GELU;
- the approved class, unknown, location and severity heads returning `AttributionHeads`;
- 219,018 trainable parameters, a 31-sample stem receptive field and whole-window recurrent/pool
  reach;
- the RNG fork entered before the seed is applied inside it, preserving the caller's CPU RNG;
- an unconditional last-statement rung-2 band refusal with no bypass argument; and
- unchanged runtime compatibility with the approved estimator wrapper and scoring seam.

I accepted Claude's two judgment calls. A generic `receptive_field = 31` would incorrectly name
the stem's reach as the whole network's reach, so only `stem_receptive_field` should exist.
Non-ASCII prose appears only in comments/docstrings, matches the neighbouring approved module and
does not reach a machine gate.

## Finding BK — live-but-miswired encoder stages

The incoming suite strongly covered composition and dead modules, but not the exact live encoder
wiring. A non-zero gradient establishes that a parameter contributed to the scalar output; it
does not establish that the contributing stage occupied the design's named slot.

Two concrete wrong implementations preserve every incoming high-level invariant:

1. iterate over `reversed(net.stem)` while keeping every block live; or
2. apply `stem_norm` immediately after `input_proj` and before the live stem.

Both keep all 219,018 parameters, every expected shape, strict causality and non-zero gradient
reach. Both violate design section 4.2's exact
`input_proj -> stem[1,2,4,8] -> stem_norm -> GRU` path.

I added `test_encode_is_the_declared_stem_norm_gru_path_in_order`. It independently reconstructs
`encode` from the named components in the named order and drives both wrong-order forms as
negative controls. This complements rather than replaces the gradient assertion: gradient reach
is the broad detector for dead stages; direct reconstruction pins the live wiring the design
actually specifies.

## Finding BL — the untested approved scoring seam

The incoming module/test prose claimed all four disclosed D4 limitations were pinned. It covered:

1. the identity-bound capacity ladder's still-false rung-2 `built` flag;
2. the estimator wrapper's narrow annotation but rung-agnostic runtime behavior; and
3. the deliberate absence of a misleading generic receptive-field property.

It did not test the fourth claim: `capacity_sweep.score_arm` has a narrow rung-1 annotation but a
rung-agnostic runtime contract. That function is also the approved scorer the later executable is
required to import.

I added `test_the_approved_score_arm_accepts_a_rung_2_network_unedited`. It constructs two
synthetic eight-step `TrainingExample` instances, scores them through the approved function with
the real rung-2 module and requires exactly the approved `accuracy`, `macro_f1` and
`per_class_f1` mapping. It reads no project data and performs no fitting.

## Verification

Verification at exact module blob `ca192af0...` and reviewer test blob `c43d33b...`:

```text
focused normal       71 passed in 1.65 s
focused python -O    71 passed, 1 expected pytest assertion warning in 1.65 s
packet-wide          1,863 passed in 147.20 s
git diff --check     clean
```

The optimized-mode warning is Pytest's standing warning that Python assertions outside test
modules/plugins are disabled under `-O`; the focused tests themselves all passed.

## Transcript integrity

The Phase-2 handoff append used Claude's complete, programmatically verified unique physical EOF
block. The old bytes were rehashed from the post-write prefix rather than inferred from Git.

```text
pre-write transcript       1,937,332 bytes / 31,270 LF / 19,456 CR
pre-write SHA-256          ee9fadff4e43aa93ae4f6cc91b5d5aab494f0cddc35e9bb338c067f2ad081258
old prefix                 byte-identical
Codex header               unique at physical line 31,272
transcript diff            +95 / -0
last agent                 Codex
post-write transcript      1,942,223 bytes / 31,365 LF / 19,456 CR
post-write SHA-256         614e48ae8e0c4b45970431b4e1bd77fee386e0d08e0c02ce6860ac8b7273fb63
```

No Transcript Order Monitoring entry was needed. Claude did not publish the `ee9fadff...`
post-write digest, so the standing prior/post cross-agent comparison was simply unavailable and
did not become a blocker.

## Files created or updated

- `Reproducibility Packet/tests/test_attribution_net_rung2.py` — added the exact encoder-wiring
  reconstruction and approved scorer compatibility tests; reviewer-edited state awaits Claude.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended README closure acknowledgement, findings BK/BL, exact approvals and the resource
  boundary.
- `agents/Codex/Session Summaries/HumanReport113.md` — this report.
- `agents/Codex/README.md` — updated the workspace index and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 114.

Deliberately unchanged: the production rung-2 module, the frozen rung-2 design, root public
README, every Stage-1 executable/plan/result/artifact/checkpoint, Claim Sheet, both
`.gitattributes` files, both `.gitignore` files, `director_requests.md`, and the absent final
configuration.

## Resource and evidence boundary

This session used synthetic tensors and synthetic `TrainingExample` objects only. It opened no
manifest, `.npz`, label payload, model checkpoint, pilot outcome, validation outcome or test
outcome. It ran no fit, wrote no checkpoint, generated no data, spent no rollout, invoked no C7
reader or analyzer, ran no plan mode, selected no capacity, set no threshold and materialized no
final configuration.

Rollouts remain 278. The lifetime fit counter remains 13. Stage 1 remains complete as scoped and
licenses only its no-readable-shape sentence.

## Next steps

1. Claude genuinely re-opens reviewer test blob
   `c43d33b007701cf3c9b24c1f6a267d2329c25c1e`, reviews findings BK/BL and either explicitly
   approves the state or returns another test state.
2. If Claude approves the same test blob, module/test Step 2 closes because both agents already
   approve unchanged module blob `ca192af0...`. Only then does Step 3 — writing
   `scripts/utils/rung2_escalation.py` and its tests — become authorized.
3. The executable, plan mode, fits, analyzer, role reads, capacity selection, thresholds and final
   configuration remain separately gated.
4. The 55-checkpoint clean-machine recovery/distribution limitation remains open for Phase 3.
5. Codex Session 120 is the next regular progress-report session.
