# Human Report — Claude Session 126

**Current date and time:** 2026-08-12 09:15 PDT

## Summary

This session was the fourth-round **owner re-review** of the Slot-8 verification-artifact design —
the document that specifies the hands-on artifact the director will eventually use to check the
project's result without reading the Technical Report end to end.

Codex's Session-125 review had kept both of my Session-125 findings and added two of its own (CG:
the two robot arms had no single shared playback clock, so one slider position could name two
different physical times; CH: the call panel had no rule for *which* estimator decision was
available at a given moment, so it could show a diagnosis before the estimator made it). I
re-opened both, drove each against live source rather than against the document's description of
it, and **kept both diagnoses and both repairs unchanged**.

I then found **three interaction defects in the consequences of those repairs, plus one bad count**,
repaired all four, and approved the returned state:

- **CI (load-bearing).** Codex's shared-clock repair required the controller log's time array to
  equal the playback clock exactly, as a hard refusal. Measured against the live rollout loop, the
  controller's timestamp for a given step is taken *before* the plant advances and the plant's is
  taken *after*, so for the same step index the two differ by exactly one control interval. That
  clause would have refused **every** real scene the day the adapter is written — over a field no
  panel even draws. Repaired by binding to the index both roles are actually pinned to.
- **CJ.** The out-of-range-frame check was assigned to scene construction, which never receives a
  frame. Repaired by moving it to the painter and forbidding a silent clamp.
- **CK.** The new "no decision yet" display requirement could be satisfied by an arm with an empty
  decision trace — a shape the live role contract refuses outright. Repaired.
- **CL.** The section-4.1 lead-in still read "Six properties" over what had become an eight-item
  list. Fixed, and found by counting mechanically rather than by reading.

Step 1 of the Slot-8 sequencing remains open, now on Codex. Nothing was built, nothing scientific
was decided, and the session spent zero fits, rollouts, checkpoints and zero pilot/validation/test
reads.

## What the session was for

The project has exactly one open loop. Every scientific lane is spent or shut: the rung-2
escalation is finished and its two licensed sentences are published, the public README is closed at
both approvals, and no capacity, threshold or configuration has been or may be selected. The Slot-8
design is the only thing moving, and it is moving through a review cycle in which each agent must
genuinely re-open the other's edits rather than wave them through.

Four review passes have now run on a document with no code against it, and that is deliberate. This
document is the thing standing between the Reproducibility Packet and a finished-looking demo built
on a development record in which ten of ten arms scored exactly zero on two of four fault classes.
A demo is the artifact most likely to be mistaken for a result, so the contract for it is worth more
rounds than the code will be.

## What was accomplished

### 1. The handoff was authenticated before it was read

The transcript's first 2,144,529 bytes reproduce Codex's declared pre-append digest
`8924864c…`; its quoted 2,131,617-byte prefix reproduces my own Session-125 digest `9b438eeb…`;
the file carries 19,709 carriage returns before and after Codex's append, so nothing was rewritten;
and Codex's turn is physically last. The design on disk reproduced Codex's handoff exactly — blob
`968feb29`, raw == canonical `12269bd0…`, 51,766 bytes / 711 line feeds / 0 carriage returns.

This matters because the transcript has had three historical order violations, and the rule this
project settled on is that **the whole prior file travels as an explicitly asserted prefix**, not
as a context block.

### 2. Codex's Finding CG reproduced, and it is mine to have missed

My Session-125 finding CF added a `frame` argument to the shared painter so the animation and the
published still could come from one code path. Codex correctly saw that I had added the argument
without adding a clock: each arm still carried its own time array, so `frame=500` could show C1 at
one instant and S at another while every per-arm shape check passed. A side-by-side replay in which
the two sides are not at the same moment is not a side-by-side replay. Codex's repair — one
scene-level `playback_t_s` grid that everything binds to — is the right shape and it stays.

### 3. Codex's Finding CH reproduced, and was concrete rather than hypothetical

Once a frame existed, the call panel needed a rule for which decision is visible at that frame. It
had none, and I checked what a reasonable implementation would reach for: the live `EstimatorTrace`
class's own docstring says the run-level class decision **is** the last decision's probabilities and
abstention — "the settled diagnosis after the post-change window". So the obvious implementation
displays the final diagnosis at every frame, showing a call before the estimator made it and making
a pre-detection missing value visually meaningless.

The machine schema also backs the repair: `estimator_outputs` is dimensioned `[N_decisions]`, so a
real role genuinely carries a decision trace and the causal rule is reachable rather than
decorative. Kept unedited.

### 4. Finding CI — the clause that would have refused every real scene

This is the load-bearing one, and it is the same shape as my Session-124 finding CA: a rule that can
stop the write its own specification requires.

Codex's shared-clock repair required both arms' `controller_logs.t_s` arrays to equal `playback_t_s`
exactly, enforced as a fail-closed refusal at scene construction. I went to the live rollout loop:

```text
online_loop.run_online_rollout   decision_time_s = float(plant.data.time)   BEFORE plant.advance
cable_plant.advance              steps the physics 20x, THEN t_s = float(self.data.time)
=> for one step index k: the controller acts at k*dt, the plant record stamps (k+1)*dt
=> an offset of exactly one control interval (2 ms at the draft config's 500 Hz)
```

Then I drove the live role contract with a controller payload whose time array starts at `t = 0.000`
— the pre-advance convention — and it was **accepted**. Nothing in the project ties the controller's
clock to the plant's. No code writes a `controller_logs` payload yet, so the convention is genuinely
undecided, and this document — a visualization contract — would have decided it by refusal.

Three things make that a defect rather than a strict standard:

1. the natural writer produces the offset grid, so **every real scene would refuse** the day the
   adapter is written;
2. the field it refuses over, `controller_mode`, is **drawn by none of the three panels**; and
3. the repair would then be an edit to the scene contract — which is exactly what the document's own
   section-1.2 design test names as a defect in this design.

What *is* guaranteed on both sides is the index: the plant record must carry the contiguous 0-based
control grid, and the role contract requires the same of the controller log. I repaired by binding
`controller_mode` to that step axis and removing the time comparison. Body and tracking — the two
things the panels actually draw — keep the exact playback-clock binding, so Codex's real content is
untouched. Invariant V6 now additionally **drives a controller payload on the offset grid and
requires it to be accepted**, so the rule cannot be quietly re-tightened later without a test going
red.

### 5. Finding CJ — a check assigned where the thing it checks does not exist

The exit-code table fired on "`frame` is outside that grid", and V6 said scene construction "rejects
an out-of-range frame". Scene construction never receives a frame; the painter does. As written, the
clause was undischargeable where it was assigned, and the cheap resolution in a build round is a
silent clamp — a slider showing the wrong instant while every panel still looks internally
consistent. That is the precise class of silent divergence the one-shared-painter rule exists to
prevent. Repaired: the painter refuses a non-integer or out-of-range frame by raising and **never
clamps**; because a painter is a function and not a process, that refusal is an exception and the
command-line surface is what turns it into the exit code. Codex's code name is kept.

### 6. Finding CK — a requirement satisfiable by a shape no real role can produce

I drove the live role contract on an empty `estimator_outputs` payload: **refused** —
*"estimator_outputs must contain at least one decision"*. The design carried no matching rule, and
an arm with an empty decision trace is the cheapest way to make a panel read "no decision yet" at
every frame and satisfy Codex's new coverage bullet. That would have tested the pre-decision display
on a shape no real role can ever carry.

Repaired three ways: the scene table now requires **at least one** decision per arm; the fixture
must drive the pre-decision branch with an early *frame* on a case that has decisions; and the
coverage invariant no longer lists frame-dependent display states among *scene-level* coverage,
because "no decision yet" and "a decision state that later changes" are properties of a **(scene,
frame) pair**, not of a scene. The invariant that tests frames already covers them.

### 7. Finding CL — a count beside a list it does not enumerate

Codex's edits took the section-4.1 property list from six items to eight without moving the lead-in,
which still read "Six properties". This project has been bitten by that shape before, which is why I
count these mechanically instead of reading them. Fixed. The invariant count is clean: V1 through
V19 present once each and in order, with the sequencing prose matching.

### 8. Three checks that found nothing, recorded so a later session does not re-spend them

- **My own Session-125 finding CE does not break the real path, and I checked rather than assumed.**
  CE requires every scene's tracking block to be a call the project's headline metric will actually
  accept. That metric is strict: uniform grid, onset exactly on a sample, and coverage through
  onset + window. Every one of the approved assignment's eight trajectory specs has
  `duration_s = onset_time_s + 5.0` exactly, so the tolerance is the tightest it could be. I
  reconstructed the real control grid the way the generator builds it — including the physics
  engine's accumulated clock, twenty additions of 1e-4 per control step — and drove the live metric
  on all eight: **accepted, all eight**. Worth knowing for later: the last sample *is* the window
  close, so there is zero slack, and accumulated floating-point error reaches 1.2e-12 against the
  metric's 1e-9 tolerance — about 800x headroom, not a margin to erode.
- **Codex's playback-extent rule is satisfiable by real data.** With a 768-sample estimator window
  the first decision cannot precede about 1.536 s and the last lands at or before the penultimate
  control sample, so every real decision falls inside the playback extent.
- **The class order the panel prints is exactly the project's canonical order**, and the location
  sentinel the panel renders as "unlocalized" is the live `-1`.

**One scope statement measured and deliberately not raised.** Six exit codes appear only in the
exit-code table; the invariants that refuse with them refer to them collectively rather than by
name. That was equally true of Codex's state and of mine, they are all on the role path that is
unreachable this round, and I judged it not worth a review round. If a later session tightens it,
the tightening is naming each code in the invariant that refuses with it.

## Challenges, and how they were handled

**The hardest part was resisting the pull of the document.** Codex's two findings were both correct
and both well argued, and the natural next move after confirming them is to approve and hand back.
The three defects I found are all in the *consequences* of correct repairs, and none of them is
visible from inside the document — CI required reading two source files and driving a validator, CJ
required asking which function receives which argument, and CK required driving a contract with an
empty payload. Every one of them answered the question "what happens when this runs", not "is this
sentence true".

**I broke the file's own character-set property and my own check caught it.** One of my repairs
introduced a middle-dot character into a document whose non-ASCII content has been confined to two
dash characters through every round. A mechanical character-set assertion over the finished bytes
found it; a reading would not have. I fixed it before handoff and rewrote the sentence in plain
ASCII. This is the second session running in which a mechanical sweep over my own finished work
caught something reading it would not.

## Decisions I made

1. **Keep both of Codex's repairs entirely**, and narrow only their consequences. Neither diagnosis
   was contestable and the shapes were right; the defects were downstream.
2. **Repair CI by re-binding rather than by deleting the field.** Dropping `controller_mode` from
   the scene would have been smaller, but a field added later is itself a scene-schema change, and
   the design's whole test is that connecting a real result must not require one.
3. **Keep Codex's exit-code name for the frame refusal** rather than adding a twelfth refusal code.
   The code was fine; what was wrong was the layer it was assigned to.
4. **Disclose the six table-only exit codes rather than raise them.** They are on a path that
   cannot run this round, and a round spent on them is a round not spent on the module.
5. **Do not open a second lane.** Codex ruled the direction in its Session 122 — Slot 8 first, then
   the Technical Report as an evidence map, then the Accessible Piece — and I accepted that without
   contest. The direction question is answered and is not to be re-asked.

## Reasoning paths explored

The instrument I used this session was: *for each rule the reviewer added, find the real object it
will meet and drive it.* That produced all four findings and all three null results. The variant
that paid best was asking, for each newly constrained field, **which panel draws it** — that is what
turned CI from "an unusually strict rule" into "a rule that refuses every real scene over something
nobody looks at".

The path I explored and abandoned: I initially suspected that the scripted still — always drawn at
the moment the metric's window closes — would render "no decision yet" in the published figures and
hide the call panel from the reports. Reconstructing the real grids showed the opposite: the window
closes at the *last* sample of every real rollout, so the published still always shows the settled
diagnosis. Not a defect, and recorded so it is not re-derived.

## Insights gained

**Two rounds running, the division of labour between the two reviewers has been the same, and this
round it inverted.** In Sessions 124 and 125, Codex's findings were field-level (an option that does
not exist; a payload with more members than the assertion named) and mine were interaction-level.
This round **Codex's two findings were interaction-level** — genuinely the harder kind — and the
defects left over were in how those repairs meet the rest of the system. That is a better place for
a review cycle to be: the remaining defects are getting structurally smaller each round, which is
what a converging loop looks like.

**The most valuable question this round was "which panel draws this?"** A constraint on a rendered
quantity earns its strictness. A constraint on a carried-but-unrendered quantity is pure downside
risk: it can refuse, and it can never be seen to be right.

## Files created or updated

- `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md` — edited (+71/−23). Git blob
  `ca158698734c14ed698bf5b0c08bc0570d0cc35c`, raw == canonical
  `d2afd8324fb01f80daca5a61b434f6773d525b51c5dab78eacbaa72812d4ecf1`, 56,378 bytes / 759 line feeds
  / 0 carriage returns. All 23 deleted lines attributed to the nine blocks I deliberately rewrote,
  verified from the diff with zero unattributed.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze -
  Active.md` — one appended turn, +155/−0, zero carriage returns added, prefix asserted
  byte-identical by the routine that wrote it.
- `agents/Claude/Session Summaries/HumanReport126.md` — this report.
- `agents/Claude/README.md` and `agents/Claude/Summary of Only Necessary Context.md` — updated at
  session close.

The public Live-Run README is deliberately unchanged: an open internal design review is none of the
three triggers that license a running-log entry.

## Next steps

1. **Codex re-reviews blob `ca158698`.** If it approves those exact bytes, **step 1 closes** and step
   2 is authorized and is mine: build `scripts/utils/verification_scene.py`,
   `scripts/render_verification_scene.py` and the tests carrying V1 through V19. If it edits or
   blocks, the owner re-review is mine again and comes first.
2. **Do not start a second lane.** If nothing has landed from Codex, say so in chat rather than
   starting something to fill a session.
3. My next regular progress report is **Session 128**, or sooner if a phase transition or an
   approved Claim-Sheet amendment fires.

## Boundary

Zero fits, checkpoints, rollouts, generation runs, plan invocations, analyzer and C7 invocations,
and zero pilot, validation and test reads. The project checkpoint count remains 67. I read source
and design contracts only, and drove the metric and the role contract on synthetic arrays in a
scratch directory outside the repository. No real role or payload was opened, no physics model was
built and no rollout was stepped — the grid reconstruction is pure floating-point arithmetic. No
capacity, rung, width, threshold or configuration was selected or written. The packet behavioural
suite was not run, because no executable file changed. No closed lane was reopened.
