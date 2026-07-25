# Human Report — Claude Session 34

**Current date and time:** 2026-07-24 19:44 PDT
**Phase:** Phase 2 — Execution
**Session role:** Close the open Gate-2 hardening review; answer my own Gate-4 stop/go gate from development data; open an amendment proposal
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Test identity/payload rows materialized:** 0

---

## Summary

### The short version

Two things happened this session, and the second one matters much more than the first.

I closed the review loop Codex opened at the end of its Session 33 — a bounded hardening of the dataset generator — by verifying it independently and approving it. That took the first part of the session and found nothing wrong.

Then I answered the question I had blocked my own next step on: **can anything, in either sensor suite, tell a structurally damaged arm from a healthy one at the damage levels this experiment actually reserves?** The answer, measured on development data only, is **no**. At the milder of the two development damage levels neither suite does better than chance; at the more severe one both reach roughly 0.70–0.75 and neither is significant, and the structural-sensing suite does not beat the conventional one at either. A positive control run through the identical pipeline — an actuator fault — is detected at 0.86–0.89, so the pipeline works; the structural signal is simply not there.

Because of that, I opened **Amendment Proposal A2** to the Claim Sheet, covering the structural severity grid, the diagnostic excitation amplitude, and the confirmatory test contact profile. Codex has to approve or block it before any of Gates 4–7 move. Validation and test data remain untouched.

### Startup and cross-review

I read `Project Details/Project Details.md` in full, my own continuity summary, all four chat `Summary.md` files that include me, and both active transcripts. I read `Playbooks/review-cycle.md` before reviewing Codex's handoff, as the routing table requires. For cross-review I read Codex's `HumanReport33.md` and the two Session-33 turns it produced.

**Standing Lesson 5 held again.** The session-start git snapshot said `Codex Session 28`; the live HEAD was `1895084 Codex Session 33`. That is the **seventh consecutive session** in which the startup snapshot lagged reality. Verifying the live `git log` before trusting continuity is now simply part of how I start.

---

## Part 1 — Gate-2 generator hardening: reviewed and approved

Codex's Session 33 implemented the four non-blocking notes I raised in my Session 33 and handed the exact state back for genuine review.

### What I verified, independently rather than from Codex's report

All six published SHA-256 digests reproduce byte-for-byte. The full packet suite passes on my run: **399 passed in 9.66 s**.

The load-bearing claim was that the retained 3.86 GB dataset did **not** need regenerating, because the constants Codex removed resolve to the values the bound configuration now supplies. That claim is what keeps a week of generated data valid, so I checked its three legs rather than accepting it:

| bound config value | resolves to | matches |
|---|---|---|
| `timing.control_dt_s` | 0.002 | `CableModelConfig.control_dt_s` default |
| `plant.simulation_timestep_s` | 0.0001 | `CablePlant` default `1.0e-4` |
| `plant.point_count_per_link` | 17 | `CablePlant` default `point_count=17` |

`control_dt_s × f_ctrl_hz` is exactly 1.0 and the physics-step ratio is exactly 20. So the substitution is a no-op on every delivered row. I then re-ran the independent on-disk audit **under the new code** rather than reading Codex's report of it: `complete_primary_c1_s_base_dataset_audit_pass`, 472 reservations / 944 manifest rows, 472/472 byte-identical plant pairs, 472/472 bitwise-identical shared channels, **0 test identity or payload rows**.

### The check Codex's report did not contain

The hardening adds a fail-loud guard, `_step_index`, that refuses a fault-onset or trajectory-duration time not aligned to the control grid. A new guard's most dangerous property is a latent trigger: the first place this one could fire that has never been exercised is the **one-shot confirmatory test generation**. So I checked all eight trajectories, including the two test trajectories that have never been run:

```text
trajectory                     onset -> step   duration -> steps   alignment error
trajectory_dev_ordinary_a       0.80 -> 400     5.80 -> 2900        0.00e+00
trajectory_dev_diagnostic_b     1.00 -> 500     6.00 -> 3000        0.00e+00
trajectory_pilot_ordinary_c     0.90 -> 450     5.90 -> 2950        0.00e+00
trajectory_pilot_diagnostic_d   1.10 -> 550     6.10 -> 3050        4.55e-13
trajectory_val_ordinary_e       0.85 -> 425     5.85 -> 2925        4.55e-13
trajectory_val_diagnostic_f     1.15 -> 575     6.15 -> 3075        0.00e+00
trajectory_test_ordinary_g      0.75 -> 375     5.75 -> 2875        0.00e+00
trajectory_test_diagnostic_h    1.25 -> 625     6.25 -> 3125        0.00e+00
                                              tolerance 1.0e-9; misaligned 0 / 8
```

Worst case is three orders of magnitude inside tolerance. The guard has no ambush waiting at test.

### Adversarial testing of the new guards

Following Standing Lesson 8 — test a guard by feeding it the exact state it was written to catch — I ran 23 cases. All behaved as required: the required-pin API refuses omission at the boundary; the self-consistently re-hashed assignment swap that motivated the fix is refused when the tracked file is pinned; non-reciprocal timing, a non-integer physics ratio, a degenerate point count, zero/negative/missing constants, misaligned or non-finite onsets, and every `test`-containing split tuple are all refused.

**One thing I learned that I did not know before.** I also tested the case the pin *cannot* cover — an attacker who pins their own swapped bytes — and the wrapper still refuses, because the embedded assignment is re-validated against the reconstructed parent by `validate_assignment`. So the binding has two independent layers, not one. Along the way I twice reported a "leak" to myself that turned out to be a bug in my own test harness (a no-op mutation), which is Standing Lesson 8's corollary — check a flaw is real before reporting it — earning its keep for the second session running.

**Verdict:** `APPROVE_GATE2_GENERATOR_HARDENING`, no edits, with two non-blocking forward notes (an uninformative `TypeError` when `expected_assignment=None` is passed explicitly, and a leftover `point_count=17` in the Phase-0 spike script, which is outside the generation path).

---

## Part 2 — The structural separability screen: the substance of the session

### Why this existed

In my Session 33 I measured, for the first time on real generated physics rather than on the written plan, that the strain signature produced by a link-stiffness loss falls below the project's own 2.0× synchronous detection margin at **every** structural severity the experiment reserves. That bounded the interpretable rung only. The learned rung reads the raw sensor tensor and was genuinely untested. Rather than build the Gate-4 model ladder on data that might not contain the signal, I imposed a gate on myself — `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK` — with three pre-committed outcomes. This session answered it.

### The design, and a piece of luck in the delivered data

New packet script `Reproducibility Packet/scripts/screen_structural_separability.py`; results under `Reproducibility Packet/results/structural_separability/`. It refuses any split but `dev` **in code**, and never opened a pilot, validation or test payload.

The delivered assignment turned out to give me a stronger instrument than I expected. Every fault setting's eight development runs sit in the *same eight background-condition cells*, run for run. So the healthy run and the structure run of a given cell share trajectory, payload, temperature profile and contact profile, and differ **only in the fault and the sensor seed**. Three consequences:

- every contrast is context-matched rather than context-confounded;
- cross-validation holds out a whole *cell* — both of its runs — so a model is never scored on a run whose context twin it trained on;
- the per-cell difference is a paired statistic, giving an exact 2^8 = 256-pattern permutation null.

Two rungs ran on the identical window set (W = 768 steps, stride 64, 28 fully post-onset windows per run): the interpretable `CoefficientReferenceDetector` with its healthy reference fitted on the seven training cells, and a small L2 logistic probe reading the raw `[W, D]` tensor reduced to 16 mean-pooled time bins plus per-column standard deviation and valid fraction. The learned number is the **maximum over a regularisation grid** — an optimistic bound, deliberately, because the screening question is whether *any* separability exists — and the permutation null applies the identical maximisation so the selection sits inside the null.

### Result

Held-out run-level AUROC, both development trajectories pooled (8 runs versus 8):

| contrast | suite | interpretable | learned (best over grid) | permutation p |
|---|---|---|---|---|
| structure, remaining EI 0.75 | C1 | 0.453 | 0.250 | 0.914 |
| structure, remaining EI 0.75 | S | 0.469 | 0.172 | 0.945 |
| structure, remaining EI 0.50 | C1 | 0.469 | 0.750 | — |
| structure, remaining EI 0.50 | S | 0.578 | 0.703 | — |
| **actuator, remaining gain 0.50** | C1 | 0.594 | **0.891** | — |
| **actuator, remaining gain 0.50** | S | 0.500 | **0.859** | — |

Restricted to the diagnostic trajectory, where the 0.8 Hz probe actually exists and the synchronous rung is in its proper regime (4 versus 4):

| contrast | suite | interpretable | learned |
|---|---|---|---|
| structure, remaining EI 0.75 | C1 / S | 0.375 / 0.500 | 0.000 / 0.000 |
| structure, remaining EI 0.50 | C1 / S | 0.375 / 0.625 | 0.375 / 0.500 |
| **actuator, remaining gain 0.50** | C1 / S | 0.875 / 0.875 | 0.875 / 0.750 |

At remaining EI 0.75 the learned probe is at or below chance in both suites, and its exact paired permutation p is 0.914 and 0.945 — the observed value is not merely non-significant, it sits near the bottom of its own null distribution. At 0.50 both suites reach roughly 0.70–0.75 pooled, neither significantly, and **S does not beat C1 at either severity**.

### The part I think matters most

I also ran a per-column paired comparison across all 18 registry channels, with no classifier in the loop:

| contrast | column | S-exclusive? | median change | effect / healthy spread | sign p |
|---|---|---|---|---|---|
| structure 0.75 | `imu_obs[2]` | no | −12.34% | 0.223 | 0.0078 |
| structure 0.50 | `imu_obs[0]` | no | −9.37% | 0.597 | 0.0078 |
| structure 0.50 | `imu_obs[2]` | no | −29.34% | 0.502 | 0.0078 |
| actuator 0.50 | `tau_cmd[1]` | no | +62.82% | 6.027 | 0.0078 |
| actuator 0.50 | `current_proxy_obs[1]` | no | +55.12% | 7.430 | 0.0078 |
| structure 0.75 | best gauge `gauge_obs[1]` | **yes** | — | 0.134 | 0.2891 |
| structure 0.50 | best gauge `gauge_obs[0]` | **yes** | — | 0.111 | 0.2891 |

**No gauge column reaches significance in any arm.** The one consistent structural signature in the delivered development data is the distal IMU's z accelerometer — which is a **C1** channel, present in the conventional baseline this project is trying to beat. At the severities we reserved, the conventional suite sees the structural fault and the structural suite does not.

### How far the signal is from where it would need to be

To find out whether an amendment has anywhere to go, I ran a matched-seed ladder below the reserved grid — same trajectory, payload, environment, sensor seed and pair identity, with only the structural severity varying — and measured both the privileged differential (the quantity the safe-probe screen's 0.405 µε floor and 2.0× margin were defined on) and what the deployable suite can actually see through the sensor model:

```text
matched seed 110802, trajectory_dev_diagnostic_b, nominal payload, W=768 from onset
rem EI   privileged ue   margin   clears 2.0x   observed ue   obs/priv
 0.75        0.0604       0.15x       no           0.0677       1.12
 0.50        0.1867       0.46x       no           0.1972       1.06
 0.40        0.2784       0.69x       no           0.2832       1.02
 0.30        0.4318       1.07x       no           0.4342       1.01
 0.25        0.5552       1.37x       no           0.5575       1.00
 0.20        0.7396       1.83x       no           0.7230       0.98
 0.15        1.0486       2.59x      YES           1.0523       1.00
 0.10        1.6653       4.11x      YES           1.6684       1.00
                     floor 0.405 ue; required 2.0x = 0.810 ue
```

Three things fall out of this.

**The margin is first met between remaining EI 0.20 and 0.15** — an 80 to 85%
loss of bending stiffness. The reserved grid is dev {0.75, 0.50}, pilot
{0.85, 0.60}, val {0.90, 0.40}, test {0.65, 0.35}. **Every reserved severity is
between 2x and 14x too mild**, and the mildest reserved severity, val's 0.90, is
roughly forty times too mild. This is not a grid that needs nudging; it sits in
a different regime from the one the mechanism lives in.

**The sensor model is not the bottleneck.** Observed and privileged distances
agree to within 0 to 12% at every severity, because the matched-seed noise
cancels in the difference. Whatever is missing is missing in the *mechanics*,
not in the strain instrumentation. That is worth knowing before anyone proposes
a quieter gauge.

**The same severity varies by context.** My Session-33 measurement gave 0.1614
at remaining EI 0.75; this cell gives 0.0604. Different payload, environment,
contact and seed. Both are far below 0.810, so the conclusion is unchanged, but
the spread is real and I would not quote either number as *the* value for a
severity without naming its cell.


### Boundaries on all of this

n is 8 per arm pooled and 4 diagnostic-only. The probe is linear on a pooled tensor, so it is a lower bound on the learned rung; a temporal model could do better. The positive control establishes sensitivity to effects around 2–7× the healthy across-context spread, not to effects at 0.1–0.5× it. And the per-column statistic is post-onset mean |value|, which for the gauges includes payload bending and the thermal term and therefore *understates* the gauges relative to the synchronous statistic — which is precisely why the interpretable rung is reported beside it, and it says the same thing.

**Outcome:** the second of the three I pre-committed to. Neither suite separates structure at 0.75, and neither separates it convincingly at 0.50. Per the pre-decision, that requires an amendment before validation or test are consumed.

---

## Part 3 — Amendment Proposal A2

Posted to the Phase-2 chat for Codex to approve or block. Four parts:

1. **Keep the existing severity grid and the delivered 472 runs** as a pre-registered *mild band*, and report their negative result as a finding rather than dropping it: at remaining EI ≥ 0.50, under this task and this excitation, distributed strain adds nothing over a matched conventional suite, and the structural signature that exists is in the distal IMU.
2. **Add a second, more severe structural band per split**, drawn from the measured ladder, preserving split-exclusivity and the disjoint difficulty ordering. The headline confirmatory comparison moves to this band.
3. **Re-derive the diagnostic probe amplitude** against the new mildest reserved severity by a bracketed grid on the 0.405 µε floor at 2.0×, with the A1 angular-rate envelope as the hard safety ceiling. 0.05 N was selected against remaining EI 0.50 under 50% task torque and 1.0 N was rejected as unsafe; the interval between them has never been searched against the *reserved* severities.
4. **Decide the confirmatory test contact profile deliberately** rather than inheriting `contact_test_sustained` — my Session-33 Finding 2, folded in here so both levers move once.

New Slot 11–13 shapes: success keeps its form but is stated per band, with the severe band carrying the headline; a new failure shape makes "S fails to beat C1 where the margin *is* met" a clean hypothesis failure; a new Slot-13 non-transfer shape, **severity-bounded**, pre-declares "structural sensing helps only above a measured severity threshold."

**Why this is not designing around the answer.** The gate being failed is one we declared before execution — the safe-probe screen's 2.0× synchronous margin. The mild band stays in the design with its negative result reported. And if nothing inside the A1 safety envelope clears the margin at any admissible severity, the honest conclusion is that this plant cannot test the hypothesis, and we say so. It is also explicitly **not** the task/score redesign the director withdrew in `chats/Claude-Codex-Human/Better Suited Task/`; the joint-space task, controller and tracking score are untouched.

**One implementation constraint I raised for Codex to decide.** `expanded_fault_settings` expands healthy → structure → actuator → sensor per split, so extending the structure severities inserts settings *ahead* of every actuator and sensor setting, shifting their ordinals and therefore their seeds — which invalidates the delivered 472 runs. The honest options are a full regeneration under one coherent rule, or a change to the expansion order. I recommended the regeneration: it keeps one rule and one assignment, and changing a jointly approved expansion rule to save a few hours of compute is optimizing the wrong axis. Codex owns the generator and gets the call.

---

## Cross-review note

Codex's `HumanReport33.md` renders my Session-33 severity table with its first row as `0.95 | 0.0090 µε | 0.02x | development`. The row I measured and posted was `0.90 | 0.0544 | 0.13x | validation`. 0.95 is not a reserved severity, and development is `{0.75, 0.50}`. Concluded record, so I did not ask for an edit — I flagged it in the chat so the wrong value does not walk into the Technical Report's limitations section, where this table is going.

---

## Files created

- `Reproducibility Packet/scripts/screen_structural_separability.py` — the development-only structural separability screen.
- `Reproducibility Packet/results/structural_separability/pooled_trajectories/` — JSON + markdown report, both trajectories.
- `Reproducibility Packet/results/structural_separability/diagnostic_trajectory_only/` — JSON + markdown report, diagnostic trajectory only.
- `agents/Claude/Session Summaries/HumanReport34.md` — this report.

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — append-only Session-34 turn.
- `README.md` (Live-Run) — running-log entry and banner date.
- `agents/Claude/README.md` — workspace index through Session 34.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

## Files deliberately unchanged

The approved assignment JSON; `Reproducibility Packet/config/draft-config-v0.1.json`; every review-target file in Codex's hardening (approved with no edits); the retained dataset; the Claim Sheet and its companions (A2 is a *proposal*, not yet an amendment); `director_requests.md`; the transcript-order monitoring thread; `references.md` (no external sources were read this session — it was measurement and review).

## `.gitignore` review

The root `/data/` rule still correctly excludes the 3.86 GB dataset. The new results artifacts total 140 KB of JSON and markdown, which belong in the repository as the reproducible evidence behind the screen, so no new ignore rule was needed. No secret, credential, environment or large binary file appeared in `git status`.

## Claim boundaries

This session:

- closes the Gate-2 generator hardening review at exact state;
- answers the development-only structural separability stop/go gate; and
- opens an amendment proposal.

It does **not**: complete Gate 2; establish or refute the research hypothesis; fit any model that is carried forward; select any hyperparameter that enters the confirmatory protocol; touch validation or test data; create `config.json`; or close Phase 2.

## Next steps

1. Codex reviews Amendment Proposal A2 and returns approval or a specific block.
2. If approved, the amendment is written into the Claim Sheet, appended and dated, and the affected slots (3, 5, 7, 9, 11–13) are updated; that approval fires a progress report at whichever session writes the approving turn.
3. Codex decides the regeneration-versus-expansion-order question and re-derives the probe amplitude against the new mildest reserved severity.
4. Gate 4 stays blocked on A2 rather than on the separability check, which is now answered.
5. Validation and test remain untouched until A2 settles.

## End state

```text
Gate 1: complete and jointly approved
Gate 2 base roles: exact-state review closed
Gate 2 generator hardening: exact-state review CLOSED this session
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved
Gate 4: BLOCKED on AMENDMENT_A2 (the separability check is answered)
Gates 5-7: open
Final config: UNFROZEN
Research result: none
Test identity/payload materialized: 0
```
