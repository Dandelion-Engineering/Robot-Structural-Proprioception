# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-01 — Codex Session 57

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` does not exist. The confirmatory test split is
untouched at zero identities and zero payloads.

Protocol P Stages A/B/C have now run once under joint authorization and produced a bounded
**Case-B development result**. Codex has completed its exact-state result review and
explicitly approves the artifact; Claude owns the next review turn. Do not begin written
Amendment A2, replacement-assignment work or regeneration until the result loop closes.

Exact result state:

```text
Reproducibility Packet/results/protocol_p/stage_abc_screen.json
  git blob   209a87ae5daa171016d566e07ed14c7c71ef0f18
  SHA-256    c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756
  bytes      599,841
  Codex      APPROVED
  Claude     REVIEW REQUIRED
```

The run selected **0.10 N / ramp fraction 0.25**. Three Stage-A candidates failed the
pre-registered hard gates on their first healthy cell and were dropped immediately, so
the 168-rollout maximum spent 135 physical rollouts:

```text
Stage A                75
Stage B                32
Stage C                28
physical total        135
logical rows          147 = 135 physical + 12 reuses
rollout elapsed       4,432.155710699968 s
terminal              None
outcome               CASE_B
unsafe Stage B/C      none
```

The exact ladder boundary is:

```text
TESTABLE in all four cells       remaining EI 0.35, 0.40, 0.45
SUB_THRESHOLD by conjunction     remaining EI 0.50, 0.55, 0.60,
                                 0.65, 0.75, 0.85, 0.90
```

At 0.50–0.60, two cells pass and two fail. At 0.65 and milder damage, none pass. Do
not pool those cells. Protocol P's Stage-A/B comparison is seed-matched while Stage C is
unmatched and therefore favours S; `TESTABLE` is necessary, not sufficient. Every stamp
is `dev-`, so this result is ineligible for confirmation.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 57 is physically last. Three appends passed the transcript hard gate. The
final result-review append preserved the complete 971,007-byte / 14,159-line prior state
as a byte-identical prefix, placed its unique header at line 14,163, and left the cumulative
working diff additions-only. Final transcript state at closeout:

```text
bytes     977,580
lines     14,301
SHA-256   ae3a5d99d074818132e62aafc46660696a743c55f9ecd0c3a8be9fba40727cf7
diff      +297 / -0 versus HEAD before Session 57
```

## Session-57 decisions

### Historical physical-run count corrected to fourteen before execution

Claude returned its Session-56 progress report at thirteen prior physical runs. That count
omitted the separate all-None regression explicitly recorded in Claude `HumanReport41.md`:

```text
S39 1 + S40 1 + S41 5 + S45 4 + S46 2 + S51 1 = 14
```

Codex edited only the still-open cost paragraph and approves:

```text
agents/Claude/Progress Reports/Progress Report Session 56.md
  returned blob          1723e54558ecb58b4194763e984357c6a8b4b7f0
  reviewer-edited blob   5744b99d634296cf7419af500806767d07053203
  next gate              Claude genuine owner re-review
```

Prior human reports and dated public entries were not rewritten. This session then spent
one immediate replay plus 135 stage rollouts, so the current Protocol-P-related physical
total is **150**.

### Active-override readback uses the measurement window, not whole-run peak strain

Claude correctly flagged that the replay gate uses `overrides=None` and therefore does not
exercise the active-override physics join. Its proposed `max_abs_gauge_true` equality and
monotonicity readback was rejected because that scalar spans all 3,000 steps, including the
bit-identical healthy pre-onset prefix; a pre-onset peak may dominate it.

The accepted zero-rollout readback uses the persisted coefficient vectors that `D` actually
measures. For the selected healthy/remEI-0.75/remEI-0.35 rows in each cell it verifies:

- canonical condition and severity;
- one `link_stiffness_loss` at location 1 and onset step 500;
- matched pair id and sensor seed; and
- structural coefficients not bit-identical to healthy.

All eight structural comparisons pass. Exact equality would have produced
`INTERPRETATION_BLOCKED_PENDING_OVERRIDE_JOIN_DIAGNOSIS`; it did not. No magnitude or
monotonicity threshold was added.

### Replay and execution sequencing

The already-approved I13b focused real-physics test passed first: `6 passed in 0.71 s`.

Codex then authorized only the one-row replay gate. It passed immediately before the
screen:

```text
20/20 identity fields equal
20/20 plant fields equal
38/38 S entries equal
531 NaNs matched
3,000 steps
36.42 s
3,176 watched files; zero changed
scope: one retained row, overrides=None
```

Only after reviewing that pass did Codex post the separate Stage-A/B/C authorization.
Claude had already conditionally authorized the same run. The jointly approved driver was
then executed with no intervening code/input/config/test change.

## Exact open review states

```text
Stage-A/B/C result
  blob 209a87ae5daa171016d566e07ed14c7c71ef0f18
  Codex approved; Claude review required

Reproducibility Packet/README.md
  blob 330282cd0afc725efa9cdcf7d6e1cdd38e1c69dc
  Codex approved; Claude review required

root README.md
  blob c67a00c3f719b4e04e37877588550905c73a55a5
  Codex approved; Claude review required
  Session-57 public change is +2/-0; no dated history edited

Claude Progress Report Session 56
  blob 5744b99d634296cf7419af500806767d07053203
  Codex approved; Claude owner re-review required
```

Packet Step 25 now includes the zero-rollout plan command, exact execute command, tracked
result hash, 135-actual/168-maximum accounting, Case-B boundary, active-override readback
and development-only scope. The packet current-boundary paragraph is also current.

The root Live-Run README appends one milestone recording Case B, the 135-rollout cost,
corrected readback, fourteen-before/150-now history and the non-confirmatory boundary.
Earlier dated entries remain untouched, including the statements the newest entry corrects
forward.

## Verification from Session 57

```text
result JSON                                  strict
physical ledger / distinct stamps           135 / 135
logical references / reuses                  147 / 12
references minus distinct                    12
stamps referenced exactly twice              12
missing / over-referenced stamps              0 / 0
bad dev prefixes / base collisions           0 / 0
bad 3,000-step counts / elapsed values        0 / 0
absolute drive-path leaks                     0
recorded config path                          config/draft-config-v0.1.json
full packet suite                             975 passed in 116.47 s
compileall                                    clean
config/config.json                            absent
confirmatory test identities                  0
Stage 0                                       not re-run
```

The three dropped candidates were `0.10/0.125`, `0.15/0.125` and `0.15/0.25`; each
failed on the healthy cell-4 row. Their measured failures are preserved in the result.

## Protocol-P state

Jointly approved and closed:

- Protocol P v2.3.3 at canonical digest
  `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`;
- permanent I13b step-499/step-500 test;
- generator `ScreenOverrides` seam;
- replay-gate implementation and prior one-row exact result;
- Stage-0 implementation and result artifact;
- shared primitives and construction layer;
- Stage-A/B/C results layer and driver; and
- packet README Step-25 plan wording before the Session-57 result update.

Open:

- Claude exact-state review of the Session-57 Stage-A/B/C result;
- Claude review of packet Step 25 and the root public append;
- Claude owner re-review of the fourteen-run progress-report correction;
- written Amendment A2 after result closure;
- replacement assignment/config lineage and coherent regeneration;
- Gates 4–7 and joint final config approval; and
- only then one-shot confirmatory generation/evaluation.

## Next actions

1. Claude genuinely reviews result blob `209a87ae...`, packet README blob `330282cd...`,
   root README blob `c67a00c...`, and progress-report blob `5744b99d...`; approve each
   unchanged or return a new exact state.
2. After the result loop closes, write Amendment A2 against the measured Case-B boundary.
3. Review the amendment before changing assignment/config lineage.
4. Produce the replacement assignment and coherently regenerate the superseded 3.9-GB
   development/pilot/validation dataset from zero.
5. Resume Gate-4 estimator/controller roles and Gates 5–7 only after lineage approval.
6. Keep `config.json` absent and the confirmatory split untouched until joint final freeze.

## Review and evidence rules

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence
  are not approval.
- Development screens, pilots, fixtures and diagnostics remain separate from frozen,
  confirmatory and final results.
- Keep physical rollout accounting separate from logical rows and provenance references.
- Keep detection, attribution, information/action authorization and control outcome
  separate.
- Do not re-run Stage 0 or Stage A/B/C without a new explicit decision.
- Do not use root-wide `pytest -q`; use `./venv` against `Reproducibility Packet/tests`.
- Never use bare `python` or `pip`.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: exact UTF-8 physical tail/line count/hash, verified
  unique complete EOF anchor, byte-identical old prefix, one new header after the boundary,
  and additions-only diff.
- The root Live-Run README is append-only while Phase 2 remains live; corrections propagate
  forward and dated entries are never edited.

## Closeout numbering

- Next Codex session: **58**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport58.md`.
- Next regular Codex progress report: **Session 64**, unless a phase transition or approved
  amendment triggers one sooner.
