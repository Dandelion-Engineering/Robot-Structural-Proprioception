# Human Report 62 — Claude

**Date and time (session close):** 2026-08-02 16:34 PDT

**Phase:** Phase 2 — Execution. All Phase-1 gates in force; Schema v1.0 + Amendment A1 in force. Config deliberately unfrozen; `config.json` absent.

**Rollouts spent this session:** zero. Two MuJoCo *mechanics probes* were run — no controller, no diagnostic probe load, no fault, no sensor model, no Protocol-P scenario — and they are reported below as mechanics checks, not as rollouts. The project's Protocol-P rollout total stands unchanged at 151.

---

## Summary

One piece of work, and it is a rewrite rather than a patch.

Codex reviewed the payload-boundary extension I drafted last session and **blocked it on four findings**. I checked every one against primary sources rather than against my own memory of what I had written. **All four are real, none is contested, and one of them is a design error that would have quietly ruined the measurement.** The document is superseded by v0.2, which I approve at an exact digest and have handed back for review.

Three further changes in v0.2 came from measurements I made this session rather than from the review. Two of them are facts about the simulated robot that nobody on this project had checked, and one of them corrects a sentence I wrote last session that was simply false about the physics.

**Nothing was executed. No rollout is authorized by anything in this session. Amendment A2 remains undrafted and blocked, as does everything downstream of it.**

---

## 1. What Codex found, and why the first finding was the serious one

### Blocker 1 — payload and sensor identity moved together

v0.1 gave each of the seven payload masses its own sensor identity: both the `sensor_seed` and the `pair_id` carried the mass index. The packet's sensor random-number generator is keyed jointly on `(sensor_seed, pair_id, channel, stream)`, and this project has already measured that changing the `pair_id` alone moves the observed gauge signal by up to 6.50 µε against the distances of order 0.1–0.5 that the whole experiment is built on.

So a difference between two masses under v0.1 would have been **part payload and part sensor identity, with no way to separate them after the fact**. Worse, the closed control loop in this project is driven by a session that reads those same identity-keyed streams, so identity does not merely add observation noise — it changes the trajectory that produces the signal being measured.

The half of this I should have caught myself is the safety check. v0.1 carried an invariant (X8) requiring the seven healthy reference measurements to be pairwise distinct, and called that evidence that the payload setting had actually reached the simulated body. **With seven different sensor identities those measurements are distinct whether or not the payload setting did anything at all.** The tripwire passes in exactly the state it exists to catch. This is a lesson already written down in this project — a positive control must exercise the path the measurement uses — and I wrote the control anyway.

**The fix in v0.2 is common random numbers.** Identity is keyed on the replicate index only, so all seven masses reuse the same eight sensor identities. Across two masses the sensor streams are now identical and the only thing that moves is the body. That also makes the tripwire real: if the payload setting were dead, the same identity and the same body would produce *identical* healthy measurements, which is precisely what the check now refuses. The check grows from 21 required comparisons to 168.

I also stated what the change costs, rather than letting the reviewer find it: the seven per-mass nulls now share their identities, so they are matched rather than independent. That tightens every cross-mass comparison, which is the point, but it also means one unlucky identity draw is shared by all seven masses instead of averaging out. Nothing in the document treats them as independent, and the alternative design that would restore independence costs a full multiple of the budget.

### The consequence Codex did not name, which I found while implementing the fix

Making identities common across masses **breaks a table nobody was looking at**. The results layer records each simulation under a "physical key" — sensor seed, identity, condition, severity, probe amplitude, probe ramp — and uses that key to decide when one already-completed simulation can be cited by more than one row. **That key has no payload field.** In the original protocol that is harmless, because identity distinguished the bodies. Under common random numbers, two runs at different masses share every field in the key and collapse into one, which means the 0.025 kg simulation could have been silently reused as the 0.200 kg row.

This is a failure mode the project had already named and written into its standing requirements — key the results table on the physical body — and it took a design change to make it live. v0.2 therefore names a **second** prerequisite change, to a second already-approved file, and carries the arithmetic (7 + 70 + 49 = 126 distinct keys) so the count can be checked against the document before anything runs. The section is now titled "three prerequisites, not one".

### Blocker 2 — the outcome rules were not executable

v0.1 listed four outcome cases in prose. Codex constructed a result that fits none of them: a light mass where every severity is detectable, and a heavier mass that retains some detectable severities but none of the two its own role reserves. It is right — no rule in v0.1 reaches that result.

Three definitions were also missing, and Codex named all three. v0.1's "non-monotone beyond what the null admits" had no mathematical rule at all, so it could not classify anything prospectively; the severity sets the classifier needs were never written down; and nothing handled a result where the detectable severities are not a clean run from the most damaged rung.

v0.2 replaces the prose with **one ordered list of eleven rules, first match wins, with an unconditional catch-all last** so exhaustiveness is structural rather than asserted. The severity sets are pinned as literals, verified this session against the assignment document rather than recalled, with a test — not the measuring program — asserting equality against that document. And I removed the tolerance from non-monotonicity entirely rather than invent one: the rule is now set inclusion, which needs no threshold and cannot be argued about afterwards. A magnitude diagnostic is still recorded so a reader can tell a small flicker from a real reversal, but **it classifies nothing**.

Codex also caught a contradiction I created by misreading the protocol I was inheriting from. I checked the source: the parent protocol says that if any severity fails a safety gate, the whole outcome is terminal. v0.1 said merely that the value is excluded. I have written the deviation I actually want — exclude the *mass*, not the whole run, so one bad rollout at the heaviest payload does not discard six clean masses — and **flagged plainly that it is permissive in my own favour and is therefore Codex's call**, with the one-line reversal spelled out.

### Blockers 3 and 4 — contracts, and ordering

The provenance, plan, result and persistence sections of v0.1 were descriptions of intent rather than contracts. v0.2 names both artifact paths, enumerates the minimum fields that must be persisted on **every** exit path including every terminal one, and pins the per-rollout identity payload field by field so its hash is recomputable from the file rather than merely well-formed. It also adopts the parent protocol's existing one-rollout replay gate as a stop-or-go precondition, because the prerequisite change touches a default code path that gate exists to protect — with the standing caveat that this gate certifies the *ordinary* path and is therefore not a substitute for the experiment's own control, and vice versa.

On ordering, Codex is straightforwardly right: v0.1 budgeted all seven masses before checking the control mass that decides whether the instrument works. v0.2 runs the control mass first and alone, persists its decision, and stops there if it fails. Within every mass the healthy reference runs before the damaged ladder, so an unusable body costs 8 simulations instead of 18. The cost section now gives every exit cost — 1, 9, 19 (control-terminal), 127 (maximum) — instead of a single number.

---

## 2. Three things I found myself

### The simulated arm has no gravity, and I had described the payload as a weight

The model is compiled with gravity set to zero. I verified it three ways at zero cost: the setting in the model source, the gravity vector on the compiled model, and the gravity-bias force vector, which is exactly zero. Then I stepped the compiled model with no actuator command for three seconds of simulated time at all eight declared masses. **The arm does not deform at all, and its tip radius stays at exactly 0.80000 m, at every mass including the heaviest.**

So the payload is **not a weight hanging off the end**. It is added tip inertia. It applies no static load and consumes none of the strain safety envelope at rest. Last session I wrote that the heaviest payload is "1.157× the mass of the whole arm, hung at the tip", which carries a static reading that is false for this plant. v0.2 withdraws the phrasing and keeps the comparison as what it actually is — a large *dynamic* perturbation to a body the controller was tuned on, which is still why a terminal outcome exists for it.

### The test signal sits about a hundred times below the arm's slowest vibration

I computed a linearized estimate of the arm's natural vibration frequencies at each mass, at zero cost, from the compiled model's mass matrix and a numerically differenced stiffness. The lowest is **77.34 Hz**; the diagnostic signal the experiment uses runs at **0.8 Hz**, roughly 97 times slower.

I stated the estimate's limits before using it: it is linearized about one configuration, undamped, and its stiffness omits the elbow constraint. That omission can only push the frequencies *up*, so it is conservative for the one conclusion drawn and for nothing else, and **no verdict in the document rests on it.**

Two things follow. First, the tidiest available explanation for last session's finding — that adding payload weakens the damage signal — was that the payload shifts a vibration mode onto the test signal. **It does not.** The lowest mode does not move with payload at all, and the whole spectrum is two orders of magnitude away. So the mechanism is unidentified, and v0.2 now says so in the section listing what the experiment cannot establish. Second, the modes that *do* move with payload saturate hard: one falls 21% between the two lightest masses and only a further 5% across the whole remaining range. That is a hint and not evidence, but it is a hint pointing at the design chosen here — if the effect saturates, extrapolating a two-level ratio outward would be wrong in a direction nobody would notice.

### My own control test was built to fail on noise

v0.1 required the control mass to reproduce the previous experiment's crossing point exactly. I re-derived the previous experiment's own margins from its result file rather than trusting my summary of them, and the crossing it is being asked to reproduce **sits 2.1% from the line**. Requiring a fresh run at a new identity to reproduce the sign of a 2.1% margin is requiring it to reproduce noise, and a terminal failure obtained that way would have meant nothing while stopping the whole measurement.

v0.2 constrains the nine rungs whose original margins are at least 10% of threshold and leaves the one borderline rung unconstrained. The number 10% does no work and I said so in the document: the smallest constrained margin is 19.6% and the largest unconstrained one is 2.1%, so **any cut anywhere in that gap produces the identical rule.** It is fixed from already-published values, before any data from the new experiment exists.

---

## 3. Decisions I made

- **Accept all four blockers without argument, and rewrite rather than patch.** Three of the four touch the design rather than the wording, and a patched document would have hidden how much moved.
- **Version-bump and `git mv` rather than edit in place**, matching the discipline the parent protocol established. v0.1 was never executed and authorized nothing; its bytes remain recoverable from last session's commit.
- **Pin the permissive exclusion rule rather than offer a menu.** Codex asked for one exact state to review. I wrote the rule I think is right, labelled the direction it favours as favouring me, and named the one-line reversal.
- **Drop the non-monotonicity tolerance instead of inventing one.** A threshold I chose would have been arguable after the result; set inclusion is not.
- **Report the two mechanics probes as mechanics probes.** They stepped the physics engine, so calling them "zero simulation" would be false; they ran no scenario, so calling them rollouts would inflate a cost figure this project has already misreported once.

---

## 4. Reasoning paths explored and set aside

- I tried to calibrate the heaviest payload's safety risk from **static sag**, expecting the strain to be a meaningful fraction of the 500 µε limit. It is exactly zero, which is how I found the gravity setting. The intended measurement failed and produced a better finding than it was aiming at.
- I tried a **modal analysis using the model's joint stiffnesses** and got an empty result, because the cable's elasticity comes from a plugin rather than from joint parameters. Falling back to a numerically differenced stiffness worked and made the omitted elbow constraint explicit, which is what let me state the estimate's direction of bias honestly.
- I considered making the non-monotonicity tolerance a fraction of the operative null, which is at least an inherited unit rather than an invented one. I dropped it because any tolerance in a *classifying* rule invites the argument that it was chosen to produce the outcome, and the same information is available as a non-classifying diagnostic.

---

## 5. Files created or updated

```text
Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md   (git mv from v0.1, rewritten)
  canonical sha256 e734c498fa661afa68f9407d79ba6539244efdf848489eb8a5a4abd4469932e9
  blob c7facc13c6148f824b7f86bb962e80ef164ae825 ; 60,815 bytes ; LF ; raw == canonical
chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md   (+256 / −0)
README.md                                                                (+2 / −0, one log entry)
agents/Claude/Session Summaries/HumanReport62.md                         (this file)
agents/Claude/README.md                                                  (state paragraph)
agents/Claude/Summary of Only Necessary Context.md                       (rewritten)
```

No code file was created, edited, or deleted. The full packet test suite was re-run and is green at **1,126 passed in 111.94 s**.

---

## 6. Next steps

**Codex owns the next turn.** It holds the review of v0.2 at canonical `e734c498…`. The four things I specifically asked it to judge are the cost statement for common random numbers, the second prerequisite against its own approved results module, the permissive exclusion rule, and whether the nine-rung control is right or whether it wants the strict version back.

Nothing downstream may start before that. In order: v0.2 approved by both agents → the two seam changes and the executable built, reviewed, approved, and mutation-swept → a plan-mode run producing a zero-rollout plan artifact both agents read → a separate explicit execution authorization → the measurement runs once → both agents read it → Amendment A2 is finally drafted → full regeneration of the dataset from zero.

**For the director:** nothing here needs you, and nothing is blocked on you. The one open request in `director_requests.md` — your review of the Claim Sheet — remains non-blocking and still open. The short version of this session is that the plan to measure something we had been assuming got sent back, and rebuilding it surfaced a design flaw that would have made the measurement unreadable, plus two facts about the simulated robot that had gone six months without anyone checking them.
