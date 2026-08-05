# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-04 — Codex Session 75

## Resume here

The project is in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its Stage-A/B/C development screen, role-coverage read,
payload-conditioning read, and the payload-boundary extension are development evidence,
not confirmatory or final evidence.

The lifetime Protocol-P-related physical-rollout total is **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

## Closed payload-boundary evidence

Both agents approve the frozen protocol, executable/test state, official zero-rollout plan,
and exact result. The result loop is closed:

```text
Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json
canonical SHA-256  7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04
Git blob          2cf19daa385ec3f96c91acca9de3747d7ba0f115

outcome           X_CASE_EMPTY (R10)
mass coverage     COMPLETE
replay            PASS, 1 rollout
anchor            X_ANCHOR_PASS
extension         126 rollouts
total             127 rollouts
```

The per-mass development result is:

```text
mass kg   TESTABLE_SET                 own split role retained
0.025     {0.35, 0.40, 0.45, 0.50}    false
0.050     {0.35, 0.40, 0.45}          false
0.075     {0.35, 0.40}                false
0.100     {0.35}                      false
0.125     {0.35}                      false
0.150     EMPTY                       false
0.200     EMPTY                       false
```

The sets are prefixes and never grow as mass increases. `X_CASE_EMPTY` is robust under
the pre-registered reproducibility-band audit; 0.150 and 0.200 kg are the measured empty
masses, but the adjacent 0.125/0.150-kg boundary is unresolved because the decisive
margins are inside the instrument's own `tau_anchor = 0.10` band. No write-up may call
0.150 kg a precise physical cutoff, fit a payload curve, identify a mechanism, treat the
seven CRN-matched masses as independent, or imply either independent audit re-derived the
stored harmonic coefficients from raw gauge traces (the raw traces were not persisted).

## Amendment A2 — current open exact-state review

Both agents chose **Option C**: keep both payload and severity ladders and pre-register a
payload-bounded structural non-transfer shape. Option A is not licensed by the empty-set
result. Option B has no qualifying initial role-retaining prefix.

Claude Session 75 drafted and owner-approved:

```text
Claim Sheet.md              d4c2fea2b64de359be536908c52331edc3d673af
Accessible Claim Sheet.md   5bd4a93dfcb2bba1e803d885a7cb813dfec2067b
```

Codex Session 75 verified the evidence, directly edited the two active artifacts, and
explicitly approves the returned state:

```text
Claim Sheet.md              d67d22c4df2aa5db0dc62ed854bcc6b804084cac
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
review delta                +11 / -11 across the two files
```

**A2 IS NOT YET IN FORCE.** These are reviewer-edited blobs. Claude must genuinely
re-open both files and either explicitly approve these exact blobs or edit and return a
new exact state.

## What Codex accepted and what it corrected

The two judgments Claude specifically requested both passed:

1. **Payload-matched role coverage is 0 / 0 / 0 / 0.** The original Section-9 read was
   dev 0 / pilot 0 / val 1 / test 1, but it was established only at 0.000 and 0.050 kg,
   both reserved to dev. Joining the independent assignment payload map to the extension
   sets and frozen role-severity map gives pilot 0 at 0.025/0.075 kg, val 0 at
   0.100/0.125 kg, and test 0 at 0.150/0.200 kg. This remains a development-context
   statement about scalar payload/severity values, not a verdict about held-out
   validation/test environments.
2. **Option C does not itself require regeneration.** It changes no severity, payload,
   split, trajectory, environment, contact, assignment, or fault-grid entry. The generator
   derives seeds from reservation ordinals after healthy → structure → actuator → sensor
   expansion; because A2 inserts no setting, it shifts no ordinal and by itself
   invalidates no generated datum or requires any archive move. Any future supersession
   needs its own authorization and exclusion trail.

Codex corrected one load-bearing claim boundary plus two nearby wording defects:

- **Sub-threshold is not signal absence.** At 0.150 and 0.200 kg the stored structural
  distances are nonzero; no reserved severity clears the pre-registered threshold. The
  active amendment now speaks about detectability and `TESTABLE` verdicts, not signal
  existence or removal.
- **`MONOTONE` is set inclusion.** It proves the `TESTABLE` set never grows with mass; it
  does not prove every raw distance is strictly monotonic. Two mild-rung distances rise
  slightly from 0.125 to 0.150 kg.
- Technical A2.1 now says four pieces of evidence while enumerating four. The accessible
  sheet also narrows “noise does not move at all” to “does not scale with payload” and
  calls the audited JSON the stored result file rather than a raw file.
- Both status lines are now self-resolving. Claude's draft said to replace them with the
  approvals after approval, which would create new, unapproved blobs. The current text
  says A2 enters force when both agents approve the same state and leaves the durable
  approval record in the review chat and Git history; no post-approval edit is needed.

No number, option, success bar, failure boundary, non-transfer shape, reporting rule,
no-regeneration conclusion, or downstream authorization changed.

## Next exact action

Read the physical tail of the authoritative active transcript before doing anything else:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Claude owns the next review turn. If Claude explicitly approves blobs `d67d22c4...` and
`203aab77...`, the A2 loop closes and A2 becomes in force. No document status edit is
needed. The closing session must then:

1. write the amendment-triggered progress report (event trigger, independent of the
   Session-80 regular cadence); and
2. add one lean public README milestone stating that the contract changed while every
   numerical success bar stayed fixed.

## Authorization boundary

Until the A2 two-file loop closes, and afterward absent a new separately explicit
authorization, all of the following remain blocked:

- any further payload measurement or second extension invocation;
- replacement of the assignment;
- supersession or coherent regeneration of any dataset;
- materialization of final `config/config.json`;
- pilot, validation, or test generation or outcome reads;
- confirmatory work; and
- changes to closed Protocol P v2.3.3.

Configuration stays unfrozen. Test identities/payloads remain untouched at zero.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoff, downstream use, and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, action
  authorization, and control outcome separate.
- Transcript appends require a recorded byte/line boundary and SHA-256, a complete unique
  multi-line EOF anchor actually used by the patch, one post-boundary session header, a
  byte-identical prefix, a physically last author, and an additions-only diff.
- Session 75 first appended after 1,287,549 bytes / 20,000 lines. The pre-write prefix hash
  `f7d95771...e116` remained exact and the header occurs once at line 20,004. The blob
  correction then appended against the exact 1,292,235-byte / 20,093-line intermediate
  state, preserving its `7867b381...bead` prefix hash. The correction header occurs once
  at line 20,097; Codex is physically last at line 20,126; the cumulative append is
  `+126/-0`; the pre-existing CR count stayed 19,329.
- The public README is intentionally untouched while A2 remains an open proposal.

Next Codex session/report: **76**. The next regular progress report is Session 80 unless
the approved-amendment event trigger fires sooner.
