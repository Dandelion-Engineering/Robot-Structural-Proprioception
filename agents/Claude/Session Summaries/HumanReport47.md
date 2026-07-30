# Human Report — Claude Session 47

**Current date and time:** 2026-07-30 10:52 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review of Codex's reviewer-edited Protocol-P Stage-0 implementation

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config.json` remains absent

**Protocol-P execution state:** Stage 0 was **not run**. `Reproducibility Packet/results/protocol_p/`
remains absent, so no Stage-0 identity, statistic, null distribution, or artifact exists.
Stages A/B/C remain unauthorized. Protocol P has still spent exactly **one** rollout — the
one authorized in Session 45. The confirmatory test split remains untouched at zero
identities and zero payloads.

---

## Summary

Last session I built Protocol P's Stage 0 and handed it to Codex without running it.
Codex reviewed it, **blocked it**, found a real defect, fixed it across five files, and
handed the corrected state back for my owner re-review. This session was that re-review.

The short version: **Codex's defect was real, its fix is correct, and the same defect has
a second member that its patch did not reach.** I found the second member, fixed it,
tested it, and handed the extended state back rather than approving. Stage 0 therefore did
not run this session, which was the cost of the finding and is the honest outcome.

Underneath that, the session produced a finding I did not expect and that matters more
than either fix: **both config-binding guards — Codex's and mine — defend code rather than
present-day data.** The architecture makes the state they reject unconstructible today. I
established that by measurement, wrote it into the code, and pinned it with tests, because
it bounds what the Technical Report will be allowed to claim about either guard.

---

## What Codex found in my Session-46 work, and whether it was right

Codex's block was on one wire. My Stage-0 script computed the artifact's identity from the
loaded configuration document — stamping `base_config_hash` into it — but the measurement
itself never consumed that document's sensor block. It built `SensorConfig()` from
dataclass defaults instead.

Today those two things are identical, which is why all 565 of my handoff-state checks
passed and no number would have changed. That coincidence is exactly what made it
dangerous: a later sensor-model change would move the artifact's identity while `D` quietly
kept using the old defaults, producing a file that is internally consistent and falsely
bound to a configuration it did not use.

**I verified the premise before accepting the fix**, rather than taking it on trust:

```text
values.sensor_model  vs  dataclasses.asdict(SensorConfig())
  key sets equal        True
  value differences     0
  => the blocked defect changed NO current number
```

Codex's characterization was accurate. I then confirmed its fix is a real wire rather than
a plausible-looking one, by moving a bound value and watching the statistic move:

```text
control                            D = [0.17764883, 0.18949149]
gauge_noise_microstrain 1.0 -> 2.0 D = [0.28163672, 0.40648718]    moved
```

Codex also caught two related things I had gotten wrong: a duplicated thermal-reference
constant that should have come from the bound config, and — fairly — that my module called
seven CLI values "pins" while cheerfully accepting `--pairs 99` and still labelling the
output Stage 0. All three fixes are correct and I approved them.

## The second member of the same class

Codex's own framing is what led me to it. The defect is *"the identity binds X, but the
measurement does not consume X."* Having agreed with that, I asked what else the identity
binds, and enumerated every value the measurement uses against the bound document.

**Three of the seven pinned CLI values also exist in that document**, and nothing connected
them:

```text
window         768    <->  values.timing.window_steps
f_ctrl_hz      500.0  <->  values.timing.f_ctrl_hz
diagnostic_hz  0.8    <->  values.timing.diagnostic_probe.frequency_hz
```

I demonstrated it the same way rather than arguing it:

```text
timing mutated (window 768->512, f_ctrl 500->250, probe 0.8->1.6)
  config hash   dev-712abf27... -> dev-c2d06af1...    moved
  D             [0.17764883, 0.18949149]              UNCHANGED, bit for bit
  raised        nothing
```

Same shape, one layer over. I was careful about the boundary: the other four pins are
genuinely protocol-only. `pairs`, `seed` and `pair_id` have no counterpart in the document.
`thermal_ramp_c = 3.0` *does* have a numeric match in the config, and it is **not** the
same object — that entry is a sinusoidal plant-side environment profile for the validation
split, while ours is an imposed linear per-window excursion on the sensor path. I checked
the environments table rather than trusting the coincidence, and the three-member boundary
is now pinned by a test so a later edit cannot quietly move a pin in either direction.

**The fix is equality, not adoption.** I deliberately did not make the measurement read
these values from the document. That would have punched a hole through the very guard
Codex had just added: the configuration could then silently move a pre-registered quantity
while the pin check still reported clean. The new guard requires the document to *agree*
and refuses when it does not, so the protocol stays the authority and a protocol/config
divergence fails loudly instead of resolving in the document's favour.

## The finding that matters more

While establishing whether my new guard is reachable, I found that **it is not — and
neither is Codex's**, for the same architectural reason neither of us had stated.

The assignment-binding gate runs before both guards and reconstructs the approved parent
hash from the entire document with one block nulled out. That means every other
configuration block — including both `timing` and `sensor_model` — is pinned by a chain
that terminates in an assignment file whose bytes are themselves pinned:

```text
values.timing / values.sensor_model
  -> parent reconstruction -> parent_draft_config_hash
  -> must equal assignment.draft_config_hash
  -> assignment bytes pinned by invariant I1
```

Measured, not asserted:

```text
committed draft reconstructs its parent                          True
change timing.window_steps       -> matches pinned parent?       False
change sensor_model.gauge_noise  -> matches pinned parent?       False
re-stamped divergent config, real CLI       refused at the binding gate, exit 1
same under python -O                        refused at the binding gate
```

So both guards defend **code** — a reordering of the main routine, a caller that skips the
binding gate, a future driver that assembles the configuration differently — not a data
state anyone could construct today. They become live data guards at exactly one moment:
when a new draft configuration is authored for the pre-confirmatory build and the lineage
is legitimately re-derived. That moment is on our roadmap, which is why both guards should
stay.

What it changes is what may be *written*. Codex's report says a later valid sensor-model
change would produce a falsely bound artifact; that needs the qualifier that such a change
cannot happen inside this lineage at all — it requires a new assignment and therefore a new
protocol pin. I put the reachability paragraph into the code itself, referencing Codex's
guard as well as mine, and pinned the underlying architectural fact with two tests, so if
that gate ever stops pinning these blocks both docstrings go red and have to be rewritten.

This is the third time the project has hit this shape (Session 42's principle, Session 46's
invariant I8), and it is now a carried limitation for the Technical Report.

## Challenges, and how they were resolved

**A false alarm I nearly reported.** My standing obligation from Session 46 is that any
change to the shared gauge-window helper requires re-verifying a *closed* screen's
published artifacts byte-identical. Codex changed that helper's signature, so I re-ran the
screen — and my comparison harness reported the closed screen had **MOVED**. It had not.
The harness was wrong: a POSIX-style path reached Python on Windows, the regenerated file
read as missing, and my script folded "could not find the file" into "differs." I checked
the alarm before reporting it, found the bug, and re-verified correctly — both artifacts
byte-identical, Codex's claim confirmed independently.

The lesson generalizes an existing one. Session 45 taught that a *clean* report must
disclose its denominator. This is the mirror: a **dirty** report must be verified too,
because a broken comparator fails in the alarming direction and looks like diligence. A
comparison must distinguish "these differ" from "I could not compare them."

**A test of mine that would have passed on unguarded code.** I wrote one parametrized test
covering non-numeric and non-finite configuration values, asserting only that the guard
raised. Asking the standard question — *what exact state would make this red?* — showed the
boolean case was vacuous: with the type guard removed, `True` compares as `1.0`, still
fails the equality check, still raises, still passes. I split it into two tests that assert
the *reason* for refusal. That change is the only reason my mutation sweep caught "accept
bools as numbers."

**Reachability had to be established by construction, not argument.** My first two attempts
to build a falsely-bound configuration were refused by *earlier* gates — the config's own
hash self-check, then the assignment binding. Rather than conclude "unreachable" from two
failed attempts, I traced the pinning chain to its terminus and proved the closure
explicitly. That is what produced the finding above.

## Verification performed

```text
Codex's handed-back state, focused              99 passed
Codex's handed-back state, packet suite        577 passed
extended state, focused                        117 passed in 1.40 s
extended state, packet suite                   595 passed in 12.68 s
compileall                                     clean
mutation sweep over the new guard              12 / 12 caught, control green, restore verified
closed detection-floor screen re-run           BOTH artifacts byte-identical
                                               summary.json  4937e885...c2c67
                                               report        1f5cbfea...ac08c1
re-stamped divergent config, CLI + python -O   refused, no output directory created
results/protocol_p                             absent
config.json                                    absent
Codex's five declared blob hashes              all five reproduced exactly
Codex's transcript append                      +177 / -0, at the physical tail
```

## Decisions I made

1. **Hand back rather than approve.** Approving a state containing the same defect class
   Codex had just blocked me for would have been inconsistent with the reasoning I had
   just accepted. Stage 0 costs zero rollouts, so nothing is burning while the round runs.
2. **Equality over adoption**, for the reason given above — adoption would have defeated
   Codex's new guard.
3. **Keep both guards despite unreachability**, and document the boundary honestly in the
   code rather than quietly shipping a guard whose value is overstated.
4. **Assert the architectural fact in a test rather than only in prose**, so the
   reachability claim cannot rot silently.
5. **Do not touch the Live-Run README.** The heartbeat check ran; no artifact finished and
   no phase closed, and an unclosed review round does not meet the playbook's bar.
6. **Do not add a note to the transcript-order monitoring chat.** Codex's append was clean
   (+177/−0, at the physical tail); the duty is to flag recurrences. Streak is now
   thirteen.

## Files created or updated

- `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` — added
  `CLI_TO_BOUND_TIMING_PATH` and `require_bound_timing_matches_cli`, wired into the main
  routine with disclosure of what was compared; reachability documented.
  git blob `8435c764a76cb091278ffa47f14584dbf43b40ce`, 40,098 bytes, UTF-8, no BOM, LF.
- `Reproducibility Packet/tests/test_synchronous_difference_null.py` — 99 → 117 tests.
  git blob `85354c762c16f0e3268909b75ce13cb3b87c3762`, 44,032 bytes, UTF-8, no BOM, LF.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-47 turn appended at the physical tail (+206 / −0, header at line 10,212).
- `agents/Claude/Session Summaries/HumanReport47.md` — this report.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — updated.

Not touched: `gauge_windows.py`, the detection-floor screen, `test_gauge_windows.py` (all
approved at Codex's exact state), the replay gate, the protocol file, `.gitattributes`, and
every dataset payload.

## Next steps

1. **Codex reviews the two extended files at exact state.** If it approves, the
   implementation loop closes and one Stage-0 execution is the next authorized action. If
   it would rather ship without the timing guard, I have said I will not re-argue it — but
   the reachability paragraph should survive either way, because it governs what we may
   claim about both guards.
2. **When Stage 0 runs**, its packet README step gets written in that same session (a
   runbook step should describe an executed, reviewed step), and it is worth recording that
   unlike the replay gate, Stage 0 needs no dataset and no physics engine — it is the first
   Protocol-P step an outside reader can run end to end.
3. **Then** the Stage-A/B/C driver, against Codex's enumerated requirements, followed by the
   written amendment and full regeneration.
4. My next regular progress report is due at **Session 48**.
