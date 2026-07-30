# Human Report — Claude Session 48

**Current date and time:** 2026-07-30 11:45 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review of Codex's Stage-0 test corrections; closing the
Stage-0 implementation loop; executing the one authorized Stage-0 run; regular-cadence
progress report (S41–S48)

**Final config state:** **UNFROZEN**; no final `config.json` exists

**Protocol-P execution state:** **Stage 0 HAS RUN**, once, at the pinned invocation.
`Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json` now exists.
**Protocol-P rollouts spent: still ONE** (the S45 replay) — Stage 0 costs zero rollouts.
Stages A/B/C remain unauthorized and unbuilt. The confirmatory test split remains
untouched.

---

## Summary of what was accomplished

Four things, in order:

1. **Genuinely re-reviewed Codex's two reviewer edits** to my Stage-0 test file, and
   confirmed both defects were real — by construction, not by reading.
2. **Closed the Stage-0 implementation loop** at round three with an explicit same-state
   approval, which Codex had specifically asked be made unambiguous rather than left to
   inference.
3. **Executed the single authorized Stage-0 run** and self-audited the written artifact
   independently of the console output it printed.
4. **Wrote the regular-cadence progress report** (my Session 48, covering S41–S48) and
   updated the public Live-Run README, which this session's work qualified for.

---

## The re-review, and why it was done by mutation rather than by reading

Codex's Session-47 turn approved my production file unchanged and blocked my *test*
state on two defects, correcting both directly:

- **Defect A** — `test_main_refuses_a_divergent_document_and_writes_nothing` described the
  divergent document as a "valid, schema-clean, correctly-bound" state constructible end
  to end, while the test body had to monkeypatch `validate_approved_assignment_binding`
  away to reach the guard. The claim contradicted the reachability closure I had proved
  in the same session.
- **Defect B** — `test_the_binding_gate_pins_the_blocks_both_guards_read` claimed to
  verify the production binding gate but reimplemented the parent-hash arithmetic locally
  and never called `validate_approved_assignment_binding`.

My standing lesson from S46 is that an owner re-review which only confirms the reviewer's
claims is not the review the cycle is asking for. So I rebuilt the mutation sweep against
Codex's patch — five cases, one anchor at a time, each restored from a pristine byte copy
with the restoration asserted by digest.

```text
C1  accept-all binding gate  ->  Codex's new gate test       EXPECT RED    2 failed   PASS
C2  accept-all binding gate  ->  my S47 gate test            EXPECT GREEN  2 passed   PASS
C3  refusal message changed  ->  Codex's new gate test       EXPECT RED    2 failed   PASS
C4  timing guard no-oped     ->  Codex's renamed bypass test EXPECT RED    1 failed   PASS
C5  Codex's re-stamp line cut -> Codex's new gate test       EXPECT GREEN  2 passed   PASS
                                                                          5/5 as expected
```

**C1 and C2 together are the session's cleanest result.** The same injected mutant —
replacing the reconstruction check in `validate_approved_assignment_binding` with an
unconditional pass — turns Codex's test red and leaves mine green. That is defect B
demonstrated rather than argued. **C3** confirms the new test asserts the *reason* for
refusal, not merely that a refusal happened — the exact property my own S47 parametrized
bool test lacked, and which I had written up as a lesson one session earlier. **C4**
confirms the renamed bypass test still reaches the guard it is named for.

**Defect A was confirmed by inspection**: the body monkeypatches the binding gate at what
is now line 884 and my docstring called the resulting state constructible end to end.

### The one thing I found in Codex's fix

**C5 was my audit of a line Codex added, and it found the stated justification wrong.**
Codex's review said the current document's config hash is recomputed "so the mutation is
not rejected merely as a stale self-hash." `validate_approved_assignment_binding` never
checks the current draft's self-hash on this path:

```text
assignment_binding.py:174   parent_document["config_hash"] = parent_hash   <- overwritten
assignment_binding.py:175   reconstructed_hash = expected_config_hash(parent_document)
assignment_binding.py:176   if reconstructed_hash != parent_hash:   -> the raise being matched
assignment_binding.py:190   if config.config_hash == parent_hash:   -> distinctness only,
                                                                      downstream of 176
```

C5 confirms it by measurement: delete the line and both parameters still pass.

**I did not block on this and did not remove the line.** It is harmless, and it makes the
rejected document fully coherent rather than merely stale — which is the *harder* case for
the gate and is exactly the `restamped-divergent-config.json` construction I built in S47.
The line is right; the reason given for it is not. I recorded the correction so it cannot
propagate into the Technical Report as a claim that this gate validates a draft's
self-hash. It does not.

This was a deliberate judgment call about the escalation trigger. Blocking a third round
over an inaccurate justification for a correct line would have been exactly the
re-litigation spiral the review cycle warns about, against Codex's explicit request for an
unambiguous approval. Correct-forward, do not reopen.

### One count correction accepted

Codex was right and I was wrong: the Stage-0 test file collects **99** tests, not 117.
`test_gauge_windows.py` collects 18, and 117 is the two-file focused total. My S47
per-file description `99 -> 117` conflated the two. Verified by `--collect-only`.

---

## Stage 0 — the run

Posted the approval turn **first**, then executed, specifically so the record cannot be
read as an approval contingent on the outcome.

```powershell
Set-Location "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```

All three shared pins agreed with the bound document; the sensor model was constructed
from that document rather than from dataclass defaults (Codex's S46 fix, live).

```text
n pairs            100        (sensor_seeds 0..199 consumed once, consecutive pairing)
mean               0.278734
std                0.074773
min                0.114994
median             0.279701
max                0.569876
q95_method_higher  0.400881   <- the reported statistic

Stage-0 identity   dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
I8                 PASS
```

### The corroboration, narrowed

```text
real-plant per-cell Q95   c6 0.3176   c4 0.3555   c7 0.3854   c5 0.4251
Stage 0                                                0.400881
```

Containment holds — and that is the pre-registered claim. But **Stage 0's Q95 exceeds
three of the four real-plant cell values**, sitting below only cell 5 with about 5.7%
of headroom. "Inside the range" is true; "agrees with the real-plant null" would be
stronger than the numbers support, and I put that qualifier on the record myself rather
than leave it for a reviewer.

Separately, §8 describes the expected synthetic value as "roughly `0.39`"; the executed
value is `0.400881`, +2.8%. I read this as requiring **no protocol change** — §8 says
"roughly," the operative claim is containment, and the spec pins no Stage-0 value. I
flagged it to Codex explicitly rather than settle it unilaterally, because the protocol
is jointly approved and its version discipline forbids editing in place.

### Self-audit of the artifact

Per the standing rule that a clean report must disclose what it examined, I re-derived
the numbers from the written file rather than trusting its own printed summary:

```text
distances recorded                            100
Q95 recomputed (method higher)                0.4008810868833315  == reported   True
mean recomputed                                                   == reported   True
identity recomputed as dev- + sha256(canonical)                   == recorded   True
first two distances       0.17764883, 0.18949149
S47 sensor-config control 0.1776,     0.1895
```

Two things worth carrying. **The identity reproduces from the artifact's own 650-character
canonical string**, so §8's promise that provenance is recomputable from the file alone is
now measured rather than asserted. And **the first two distances reproduce my S47 wire
demonstration exactly**, which is independent evidence that the sensor block is being read
from the bound document rather than defaulted — the pinned run and the S47 control agree.

One near-miss worth recording: the artifact's `samples` key returned length 6, which
looked briefly like a catastrophic sample-count defect. It is a metadata dict with six
keys, one of which (`distances`) holds the 100 values. I checked the type before reporting
anything — the S47 lesson that a *dirty* report needs verifying as much as a clean one,
applied one session later.

---

## Challenges and how they were overcome

- **The temptation to accept a correct-looking fix on authority.** Codex's edits read as
  obviously right. Reading them would have produced the same approval with none of the
  evidence. The sweep is what converted "this looks correct" into "the same injected fault
  turns one test red and the other green." Cost: about 40 seconds of compute.
- **My first mutation anchor did not exist.** C4's anchor text was invented from memory
  rather than read from the file, matched zero times, and the harness said so and refused
  to run. That fail-loud behaviour is why the sweep is trustworthy; I grepped the real call
  site (`analyze_synchronous_difference_null.py:842`) and re-ran.
- **Deciding whether to block on the inert line.** Resolved by asking what the escalation
  trigger actually says: it fires on re-litigation of settled points, not on new verifiable
  findings, and this finding did not affect the correctness of any shipped code. Recorded,
  did not block.

---

## Important decisions

1. **Approved the exact two-file state** at Codex's blobs and stated it unambiguously —
   the loop is closed at round three.
2. **Did not remove or edit Codex's re-stamp line**; recorded the narrowing instead.
3. **Posted approval before execution**, as two separate turns, so the approval stands on
   the record independently of the result.
4. **Did not edit Protocol P** over the 0.39 vs 0.4009 gap, and handed the reading to
   Codex rather than settling it alone.
5. **Deferred the Stage-0 packet README step a third time** — a runbook step describes an
   executed *and reviewed* step, and Codex has not yet reviewed the result.
6. **Updated the Live-Run README**, which this session's work genuinely qualified for
   (a loop closed and the project's first pre-registered measurement ran).

---

## Reasoning paths explored

- **Whether Codex's new gate test lost coverage my version had.** My version asserted
  `wrapper["parent_draft_config_hash"] == wrapper["assignment"]["draft_config_hash"]`
  explicitly; Codex's drops it. Traced it: `assignment_binding.py:160-161` performs exactly
  that check, and the test's control call requires the unmutated binding to pass. Coverage
  is preserved *through the production gate*, which is strictly better. No loss.
- **Whether `match="reconstruct the exact"` is discriminating.** Grepped every
  `AssignmentBindingError` raise site; the phrase appears in exactly one message
  (`:177-178`). C3 then confirmed it behaviourally.
- **Whether the float-doubling mutation is a real mutation.** `float(768) * 2.0` makes
  `window_steps` the float `1536.0`, which serializes differently from `1536` — the hash
  moves either way, so the test is sound.

---

## Insights gained

1. **A reviewer's correct fix and a reviewer's correct reasoning are separable, and both
   are reviewable.** Codex's line was right and its justification was wrong. The owner
   re-review that only asks "is the code correct" would have passed both through.
2. **The mutation sweep is now the load-bearing instrument of this collaboration.** Across
   S44, S46, S47 and S48 it has found every defect that mattered, including three rounds of
   defects in fixes to defects. Reading found none of them.
3. **A lesson written down is not a lesson applied.** My S46 note against test helpers that
   reimplement production arithmetic sits a few lines above the test where I did exactly
   that. Codex caught it. The value of the second agent is highest precisely where I
   believe I already know the rule.

---

## Files created or updated

**Created**
- `Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json` — the
  Stage-0 artifact (6,765 bytes, tracked by design)
- `agents/Claude/Progress Reports/Progress Report Session 48.md` — regular cadence, S41–S48

**Updated**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — two clean tail appends, `+252 / −0` (approval at line 10,577; Stage-0 result at 10,707)
- `README.md` — Live-Run banner date and one running-log entry
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout

**Deliberately not touched:** both Stage-0 files, `scripts/utils/gauge_windows.py`,
`analyze_synchronous_detection_floor.py`, `test_gauge_windows.py`, the replay gate, the
protocol file, the assignment, `.gitattributes`, `config.json` (still absent), and any
payload. No new dependency. No transcript-order note (Codex's append was clean,
`+159 / −0` — streak fourteen).

**Scratchpad (not committed):** `append_turn.py` (copied forward unchanged, sha256
`3cf26db9…`, now surviving a sixth session), `verify_s48_mutations.py` (the five-case
sweep), `old_test_s47.py` (my S47 test file extracted from commit `5514a60` for C2),
`turn_s48_approval.md`, `turn_s48_stage0.md`.

---

## Verification

```text
reviewer-edited two-file focused run     117 passed in 1.48 s   (99 + 18)
full packet suite                        595 passed in 12.32 s
mutation sweep                           5/5, all restorations digest-verified
working tree after the sweep             clean
files written by Stage 0                 exactly 1
.npz under results/                      0
config.json                              absent
Protocol-P rollouts spent                1 (unchanged)
```

---

## Next steps

1. **Codex reviews the Stage-0 result** and gives its read on the 0.39 vs 0.4009 question.
2. **I write packet README Step 24 for Stage 0** once that review lands, noting that Stage 0
   — unlike the replay gate — *is* fully runnable from a clean checkout with no dataset and
   no MuJoCo. The two Protocol-P steps have opposite reader-reproducibility status and the
   packet must say so.
3. **The Stage A/B/C driver**, against Codex's enumerated requirements, which I carry verbatim.
4. **Write amendment A2**, get both approvals, regenerate the dataset from zero, re-audit.
5. Then Gate 4/5 (models + calibration), the joint immutable freeze, and the confirmatory run.

**Open director dependency:** `director_requests.md` entry 1 (Claim Sheet review) remains
open and **non-blocking**. Nothing else is blocked on the director.
