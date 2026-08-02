# Human Report — Codex Session 57

**Current date and time:** 2026-08-01 23:36 PDT

**Phase:** Phase 2 — Execution

**Session role:** Close the remaining pre-execution review decisions; authorize and run
the Protocol-P replay gate and Stage-A/B/C development screen in the agreed order;
independently audit and hand off the result.

**Final config state:** **UNFROZEN**. `Reproducibility Packet/config/config.json` does not
exist. The confirmatory test split remains untouched at zero identities and zero payloads.

**Protocol-P execution state:** The one-row replay gate passed immediately before the
measurement. Stages A/B/C then ran for the first time and produced a bounded **Case-B
development result**. The tracked result is now under Claude exact-state review; it is not
a confirmatory result and does not by itself freeze a configuration.

---

## Summary

This session crossed the Protocol-P execution gate after a long implementation and review
sequence. It began with two open Claude Session-57 handoffs:

1. Claude approved Codex's packet Step-25 wording unchanged, closing that loop.
2. Claude returned its Session-56 progress report with a historical simulator-cost count
   of thirteen and raised a new concern: the replay gate exercises `overrides=None`, while
   the Stage-A/B/C measurement would be the first real MuJoCo run with an active
   `ScreenOverrides` bundle.

Both needed another correction before execution.

The historical count was fourteen, not thirteen. Claude's own `HumanReport41.md` states
that Session 41 spent five rollouts: four onset-consequence runs plus one separate all-None
regression. Claude's returned count included only the four onset runs. I edited only the
still-open cost paragraph in the progress report, changing thirteen to fourteen and the
estimated prior cost from about five and a half to about six minutes. The exact
reviewer-edited blob is `5744b99d634296cf7419af500806767d07053203`, approved by Codex and
returned for Claude owner re-review.

Claude's active-override risk was correct, but its proposed mandatory readback was not.
`max_abs_gauge_true` is a maximum over the complete 3,000-step trace, including the
bit-identical pre-onset prefix. A pre-onset peak can therefore make healthy and structural
maxima exactly equal even when softening activates correctly, and monotone whole-run peaks
are not guaranteed by a closed-loop dynamic system. I replaced that rule with a
zero-rollout measurement-window check over the coefficients the protocol's statistic `D`
actually uses. Exact equality blocks interpretation and triggers diagnosis; no magnitude
threshold or monotonicity rule is added.

After recording that decision, I authorized and ran the already-approved I13b focused
test, then the one-row replay gate. Both passed. I posted the replay evidence as its own
reviewed decision and separately authorized Stage-A/B/C, preserving the agreed sequencing.

The screen completed successfully:

```text
terminal                         None
outcome                          CASE_B
selected candidate               0.10 N / ramp fraction 0.25
planned maximum                  168 physical rollouts
actual                           135 = A 75 + B 32 + C 28
reported logical rows            147 = 135 physical + 12 reuses
Stage-A candidate drops          3
unsafe Stage-B ladder values     0
unsafe Stage-C bodies            0
recorded rollout elapsed         4,432.155710699968 s
```

The pre-registered Case-B result is narrow and clear: 0.35, 0.40 and 0.45 remaining EI
are measurable above the operative null in all four cells; 0.50 through 0.90 fail the
required all-cell conjunction. This is a development-screen result under a matched-signal
/ unmatched-null comparison that Protocol P explicitly says favours S. `TESTABLE` remains
necessary, not sufficient, and no project-hypothesis or confirmatory claim follows.

The result artifact, packet runbook update and public append are all explicitly approved
by Codex and handed to Claude for exact-state review. The written Amendment-A2 /
replacement-assignment / coherent-regeneration path should move only after that result
loop closes.

---

## Pre-execution review decisions

### 1. Historical rollout count: fourteen before this session

The primary-record recount is:

```text
Session 39   1   replay of one delivered healthy row
Session 40   1   all-None transparency regression
Session 41   5   four onset-consequence runs + one all-None regression
Session 45   4   formal replay gate twice by Claude + twice by Codex
Session 46   2   clean replay + injected-stray-write refusal
Session 51   1   replay regression after the shared-import edit
             --
total       14
```

The missed Session-41 regression is separately recorded at 27.5 seconds with 20/20
privileged fields and 30/30 S arrays identical. The dated human reports and the previous
public entry remain unchanged; the correction propagates forward.

This session then spent one immediate replay plus 135 stage rollouts, bringing the current
Protocol-P-related physical total to **150**.

### 2. Active-override join readback

I accepted Claude's diagnosis: the replay gate verifies the shared ordinary path but not
the first real active-override join. I rejected only the proposed evidence rule.

The accepted readback, applied after the artifact was written and before its outcome was
accepted, was:

1. For the selected candidate in each cell, parse the persisted canonical healthy,
   remEI-0.75 and remEI-0.35 records.
2. Verify one structural `link_stiffness_loss` fault at location 1, the requested severity,
   onset step 500 derived from the bound document, matched pair id and matched sensor seed.
3. Compare the persisted post-onset coefficient vectors bit-for-bit against the matched
   healthy vector.
4. If either structural vector is exactly identical, block all scientific interpretation
   pending diagnosis. Do not call it a construction failure and do not call it a
   scientific null without further evidence.

All eight comparisons passed:

```text
cell   remEI   canonical check   coefficient identity   D
4      0.75    PASS              DIFFERENT              0.485680373098988
4      0.35    PASS              DIFFERENT              2.676840231281948
5      0.75    PASS              DIFFERENT              0.474623319584314
5      0.35    PASS              DIFFERENT              2.683073436805542
6      0.75    PASS              DIFFERENT              0.255447066416752
6      0.35    PASS              DIFFERENT              1.352761082606397
7      0.75    PASS              DIFFERENT              0.246403927812380
7      0.35    PASS              DIFFERENT              1.336862627334846
```

Whole-run peak strain was inspected only as a descriptive diagnostic. No equality,
magnitude or monotonicity rule was imposed on it.

---

## Authorization and execution sequence

The first transcript turn approved the fourteen-run progress-report correction, ruled on
the readback, and authorized only the replay gate. Stages A/B/C remained unauthorized.

The approved I13b real-physics boundary test then passed:

```text
6 passed in 0.71 s
```

The Section-7 replay gate then passed at its exact narrow scope:

```text
protocol / assignment pins        exact
plant / observation binary pins   exact
identity                          20 / 20 fields equal
plant                             20 / 20 fields equal
S observation                     38 / 38 entries equal
matched NaNs                      531 across 5 entries
steps                             3,000
rollout wall clock                36.42 s
watched filesystem                3,176 files
added / modified / removed        0 / 0 / 0
result                            REPLAY_GATE_PASS
scope                             one retained row, overrides=None
```

Only after reviewing that evidence did I append the separate Stage-A/B/C authorization.
The approved command was then launched immediately:

```powershell
..\venv\Scripts\python.exe scripts\run_protocol_p_screen.py `
  --output-dir results\protocol_p --mode execute
```

No code, input, configuration or test state changed between the replay and the
measurement.

---

## Case-B result

The three Stage-A drops were `0.10/0.125`, `0.15/0.125` and `0.15/0.25`. Each failed the
hard gates on the first healthy row in cell 4. The fail-fast driver preserved each measured
failure, then avoided the other eleven planned bodies for that candidate. That accounts
exactly for the 33-rollout difference between the 168 maximum and 135 actual.

The selected candidate was the unique best candidate at the protocol's selection
severity:

```text
selected                       0.10 N / 0.25 ramp fraction
best worst-cell D at 0.75 EI  0.24640392781237982
1% tie threshold              0.24393988853425602
tied candidates               selected candidate only
```

The ten-value ladder was:

```text
remaining EI   verdict          minimum all-cell margin
0.35           TESTABLE          0.4815189074132872
0.40           TESTABLE          0.2180535059726273
0.45           TESTABLE          0.025560866297681284
0.50           SUB_THRESHOLD    -0.13610606188409746
0.55           SUB_THRESHOLD    -0.27702315785103915
0.60           SUB_THRESHOLD    -0.3785056765197888
0.65           SUB_THRESHOLD    -0.47441764187927826
0.75           SUB_THRESHOLD    -0.608939792109179
0.85           SUB_THRESHOLD    -0.7327344736095494
0.90           SUB_THRESHOLD    -0.7714063785537557
```

At 0.50–0.60, two cells pass and two do not. At 0.65 and milder damage, none pass. The
protocol uses an all-cell conjunction, so none of those values can be pooled or averaged
into a pass.

---

## Artifact verification

The exact result state is:

```text
path       Reproducibility Packet/results/protocol_p/stage_abc_screen.json
git blob   209a87ae5daa171016d566e07ed14c7c71ef0f18
SHA-256    c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756
bytes      599,841
```

Independent artifact checks:

```text
strict JSON                                      PASS
physical ledger / distinct stamps               135 / 135
logical references / reuses                      147 / 12
references minus distinct stamps                 12
stamps referenced exactly twice                  12
references over twice / missing references       0 / 0
bad dev prefixes / base-hash collisions          0 / 0
bad 3,000-step counts / negative elapsed values  0 / 0
absolute Windows drive-path leaks                 0
recorded config path                              config/draft-config-v0.1.json
full packet suite                                 975 passed in 116.47 s
compileall                                        clean
config/config.json                                absent
confirmatory test identities                      0
```

The result file contains only `dev-` provenance and is permanently ineligible for
confirmatory analysis.

---

## Documentation updates

### Packet README

Step 25 now gives an outsider:

- the zero-rollout plan command;
- the exact execute command;
- the tracked result link and SHA-256;
- the 168-maximum versus 135-actual fail-fast accounting;
- the selected candidate, Case-B ladder boundary and recorded runtime;
- the active-override coefficient readback; and
- the explicit development-only / necessary-not-sufficient boundary.

The packet's current-boundary paragraph now records Case B and points forward to the
Amendment-A2 / replacement-assignment / coherent-regeneration path without implying
freeze or confirmation. Codex approves packet README blob
`330282cd0afc725efa9cdcf7d6e1cdd38e1c69dc`; Claude review is open.

### Public Live-Run README

One new milestone entry was appended, `+2/−0`. No dated entry was edited. It reports the
selected candidate, the 135-rollout actual cost, the three-value testable boundary, the
corrected construction readback, the fourteen-before / 150-now cost correction, and the
development-only scope. Codex approves root README blob
`c67a00c3f719b4e04e37877588550905c73a55a5`; Claude review is open.

### Active transcript

Three appends passed the hard gate:

1. review/readback/replay authorization;
2. replay evidence and separate Stage-A/B/C authorization; and
3. result audit and exact-state handoff.

The final transcript retains the complete 971,007-byte / 14,159-line pre-result state as
a byte-identical prefix. The result-review header occurs once after that boundary, and the
working diff is additions-only.

---

## Challenges and how they were handled

### A correction to a correction to a correction

The simulator-cost number had moved from one to four to thirteen. Re-reading the same
primary report Claude cited showed that thirteen still omitted one explicitly recorded
run. The correction was made only in the still-open progress report and propagated
forward elsewhere; dated records were not rewritten.

### A plausible readback that checked the wrong time domain

Claude correctly identified the first active-override physics join as unexercised, but
the proposed whole-run peak-strain scalar included the healthy pre-onset prefix. The fix
was not to invent a threshold after seeing the data; it was to read the already-persisted
post-onset coefficient vectors that the pre-registered statistic actually uses and to
block only exact identity pending diagnosis.

### Long buffered execution

The screen writes its result and stdout summary only after the measured branch completes.
The process was kept attached for 4,441.8 seconds of wall time and monitored only through
read-only liveness snapshots. No project file changed while it was running.

### Public-log verifier mismatch

My first public-README check incorrectly demanded that the old file be a complete EOF
prefix. The append-only running log sits above a preserved footer, so that invariant was
inapplicable. The actual git diff is `+2/−0`, proving no prior line was edited. This was a
verification-instrument error, not a README mutation error.

---

## Files created or updated

### Created

- `Reproducibility Packet/results/protocol_p/stage_abc_screen.json`
- `agents/Codex/Session Summaries/HumanReport57.md`

### Updated

- `agents/Claude/Progress Reports/Progress Report Session 56.md`
- `Reproducibility Packet/README.md`
- `README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No Protocol-P code, test, specification, assignment, draft config, Stage-0 artifact,
retained dataset payload or confirmatory material was changed.

---

## Next steps

1. Claude genuinely reviews and either approves or returns:
   - result blob `209a87ae...`;
   - packet README blob `330282cd...`;
   - public README blob `c67a00c...`; and
   - progress-report blob `5744b99d...`.
2. After the result loop closes, write and review Amendment A2 at the measured Case-B
   boundary.
3. Produce the replacement assignment/config lineage and regenerate the superseded
   development/pilot/validation payloads coherently from zero.
4. Resume Gates 4–7 only after that lineage is approved.
5. Keep `config.json` absent and the confirmatory split untouched until the joint final
   freeze gate closes.

The next regular Codex progress report is Session 64 unless a phase transition or an
approved amendment triggers one sooner.
