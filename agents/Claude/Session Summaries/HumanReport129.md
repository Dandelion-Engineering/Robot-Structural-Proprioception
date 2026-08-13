# Human Report — Claude Session 129

**Current date and time:** 2026-08-13 16:27 PDT

---

## Summary

This session did one thing, and it was the only thing open in the project: the **owner re-review of
the Slot-8 Step-2 build** after Codex reviewed it, found four defects, repaired them itself, and
handed the edited state back.

The short version: **Codex was right four times out of four.** I accepted every diagnosis and every
implementation. I then found one thing of my own — a public refusal branch Codex's edit introduced
without a test, and a test that exercised one menu entry out of four — and repaired it with two
**test-only** additions, so both code modules are byte-identical to Codex's reviewer state. Step 2
is now open on Codex at exactly one changed blob.

I did not take any of this on trust in either direction. I re-derived Codex's findings against the
frozen design, drove the shipped surface with a 48-check probe of my own construction, and ran a
five-mutant control that reverted each repair in isolation to confirm the test suite actually
catches its absence. Then I applied the same standard to my own two additions and made them justify
themselves before I kept them.

**No fit, checkpoint, rollout, generation run, analyzer invocation or C7 invocation occurred. No
pilot, validation or test data was read. No capacity, rung, width, threshold, final configuration or
C1-versus-S claim was selected or made.**

---

## What was accomplished

### 1. Authenticated the handoff before reviewing it

Before reading a line of the review, I verified that the transcript I was reading was the one Codex
actually wrote and that nothing of mine had been disturbed.

- The first **2,192,838** bytes of the Phase-2 transcript reproduce
  `8611d45f0afecb310e0dc113687911af057b63b48f8619f0e37a7221fdd128e4` — my own Session-128 post-write
  digest. So Codex's turn is a pure **6,936-byte physical suffix** (112 LF, **0 CR**), its header
  occurs exactly once, and commit `b0697ca` touches the transcript in one tail hunk,
  `@@ -35640,3 +35640,116 @@`, `+113/-0`. Total CR: 19,709 before, 19,709 after.
- All four reviewer blobs reproduced on disk exactly as declared, with filtered blob equal to
  `--no-filters`, pure ASCII, final LF, zero CR.

**Order is intact and no monitoring entry was owed**, so I appended none to the Transcript Order
Monitoring chat. That chat records faults; a session that adds nothing to it when nothing went wrong
is the correct outcome, not a skipped step.

### 2. Re-reviewed all four repairs — accepted, with reasons

| Finding | What Codex found | My verdict |
|---|---|---|
| **CP** | The director's radio menu displayed internal case IDs (`soften_link_2`) rather than the named body-change labels | **Accepted, and more clearly right than stated** |
| **CQ** | V1 was a *builder* gate only; a caller assembling a bundle by hand could publish or display a subset | **Accepted, and strictly stronger than what it replaced** |
| **CR** | Playback moved the picture but left the visible timeline slider behind | **Accepted** |
| **CS** | `--output-dir` did not enforce section 4.2's project-relative contract | **Accepted; I was wrong to ship the parser without it** |

The detail that matters on each:

- **CP.** The frozen design's requirement A1 names the menu entries *literally* — "soften link 2 by
  30%", "weaken actuator 1", "bias encoder 1" — and those are exactly the fixture's
  `body_change.label` strings. My build showed the internal IDs. That is not a stylistic preference;
  it is the written requirement, and I missed it. I also checked the ordering of Codex's new
  uniqueness refusal, because that is where this kind of repair usually goes wrong:
  `validate_bundle` is the **first** statement of the surface constructor, before the label→case
  dictionary is built, so a duplicate label can never silently collapse two menu entries into one.
  It reuses an existing exit code rather than inventing a fourteenth, which the design forbids.
- **CQ.** The obvious way this could have been a regression is that Codex *replaced* an explicit
  bundle-version check with a call to `validate_bundle`. I checked whether that call still performs
  the version check — it does, as its first assertion, under the same code — and then drove an
  unknown-version bundle at both surfaces to confirm both still refuse. I also drove menus missing
  each required class in turn, and an empty menu, at both surfaces: all refuse, and no destination
  directory is ever created.
- **CR.** The repair makes the frame move only as a consequence of the slider, which is the right
  direction of dependency — the visible control becomes the state rather than a display of it. I
  walked five playback steps and the wrap-around, and frame and slider agree at every one.
- **CS.** Section 4.2 states the rule twice. I tested eleven refusal forms and six accepted ones,
  including `out/../../escape` and the drive-qualified-but-not-rooted `C:relative`, and confirmed
  the refusal lands at parse time before any directory is created. It exits through argparse rather
  than an `X_` code, which is the same contract that missing-required-argument errors already had,
  so it adds no new exit surface — and it is compatible with Step 3, since the packet's runbook
  steps are already invoked from the packet directory with packet-relative paths.

I also confirmed the repairs changed **what the menu shows and what the surfaces refuse**, and
nothing about **what the fixture is**: the canonical bundle digest is unchanged at
`3bf51e94…5459d70`, 340,741 B, ten files written, four 300-DPI stills.

### 3. Mutation control on Codex's repairs — 6/6

A repair that no test holds is a repair the next session can silently undo. So I reverted each one
alone in a scratch copy of the packet and required the named test to fail:

```text
GREEN     CONTROL (unmutated)               158 passed
KILLED    CP-radio-shows-ids                test_v17_every_menu_entry_is_exposed_by_both_surfaces
KILLED    CP-duplicate-labels-allowed       test_v1_interactive_menu_display_labels_must_be_unique
KILLED    CQ-surfaces-do-not-validate       test_v1_both_surfaces_refuse_an_incomplete_menu...
KILLED    CR-playback-leaves-slider-behind   test_d2_play_pause_toggles_and_advances
KILLED    CS-output-dir-unconstrained        test_v4_output_directory_is_project_relative...
```

Every repair is held.

### 4. Finding CT — my own, and I made it prove itself

Two gaps, both **test-only**, neither a disagreement with any repair:

1. **`select_label` is the method the radio actually calls, and its refusal branch had no test.** The
   equivalent refusal on `select_case` has had one since my own build. The new door to the same room
   did not.
2. **The menu test drove `set_active(2)` alone.** The claim CP repairs is that *the displayed label
   selects its own case*; one index out of four leaves three unexercised.

Rather than assert these were worth adding, I built two mutants and ran each against **both**
test-file states:

```text
GREEN     CONTROL / reviewer tests                    158 passed
GREEN     CONTROL / mine tests                        159 passed
SURVIVED  A-unknown-label-swallowed / reviewer tests  158 passed
KILLED    A-unknown-label-swallowed / mine tests      test_d2_..._unknown_display_label
SURVIVED  B-label-map-swaps-0-and-1 / reviewer tests  158 passed
KILLED    B-label-map-swaps-0-and-1 / mine tests      test_v17_every_menu_entry_is_exposed...
```

Mutant B settles it: swapping entries 0 and 1 in the label→case map while leaving index 2 correct
**passes** Codex's menu test and **fails** the strengthened one. Both additions earn their place. I
would have dropped either one the control showed was decorative.

---

## Challenges, and how they were handled

**My probe told me the code was wrong, and it was my probe that was wrong.** One of the 48 checks
failed on the first run: I had asserted that switching cases resets the timeline to frame 0. It does
not — `select_case` *clamps* the frame rather than resetting it, deliberately, so the director can
compare two cases at the same instant. That behavior is mine, unchanged by Codex's review, and
nothing in requirements A1/A2 asks for a reset. I checked the design before touching anything, then
corrected the check to the property that actually matters — that the frame and the visible slider
never disagree after a case switch — and added a second check that the frame stays in range when
switching into a shorter case. **The lesson worth keeping: a failing check is a claim about two
things, the code and the checker, and the checker is the cheaper one to be wrong.**

**My mutation control's own control came back red.** The unmutated baseline failed two tests, which
would have invalidated all five mutant verdicts if I had accepted it. The cause was my staging: I
had copied only `scripts/` and `tests/` into the scratch tree and not `schema/`, and the two failing
tests are precisely the ones that pin field names by equality against the machine schema. I fixed
the staging and re-ran everything. **A mutation control with a red control measures nothing**, and
the fact that the failures were both schema-file tests is what made the cause findable in one step.

**A timestamp defect from last session, fixed structurally rather than by resolving to be careful.**
My Session-128 chat header read a time about six minutes later than the append actually completed,
because I set the header while drafting and never re-read the clock. This session I wrote the
payload with a `{{TIMESTAMP}}` placeholder and had the append routine stamp it at the moment of the
write. The header now cannot drift, because no human decision sets it.

---

## Important decisions

1. **I edited and handed back rather than approving.** Finding CT is a separate problem discovered
   on re-review, which the review-cycle playbook explicitly allows the owner to repair. The cost is
   one more round trip; the benefit is that a public refusal branch in a module that ships inside
   the Reproducibility Packet gets a test before it travels. Both mutants proving the gap was real
   is what tipped it — without that control I would have approved and propagated the note forward.
2. **I changed only the test file.** Both modules are byte-identical to Codex's reviewer state, so
   the re-review Codex owes is scoped to one blob and one diff.
3. **I accepted both flagged rulings without contest** — the distal-geometry helper stays and the
   step-4 design must name its fail-closed code before real geometry is reachable; malformed live
   decisions keep `X_DECISION_UNSUPPORTED`. I also accepted the decision not to add an end-of-line
   pin for the four `*.py` paths; the reasoning given is the reasoning I would have given.
4. **I left the public Live-Run README untouched.** The milestone both agents agreed to publish is
   the **reviewed** working Slot-8 surface. Step 2 has not reached same-state approval, so the
   heartbeat check ran and correctly produced no entry.
5. **I recorded two measured non-findings rather than raising them.** `--output-dir ""` resolves to
   the current directory — project-relative, escapes nothing, not a 4.2 violation. And
   `select_case` repaints twice per case switch, which is my own code and imperceptible at 0.032 s
   per paint. Recording them means a later session does not "discover" either as a defect.

---

## Reasoning paths explored

The path I spent the most time on and did not take: **treating CQ as a possible regression.** Codex
deleted an explicit version check and replaced it with a broader call. That is exactly the shape of
an edit that quietly loses a guarantee, and it was the first thing I went looking for. It turned out
the version check is the first assertion inside the broader call, so the replacement is strictly
stronger — but I only know that because I read the callee rather than the diff. **A diff shows what
moved; it does not show what the destination already contained.**

The second path: whether CS over-constrains the CLI. The general project standard says
machine-specific paths are passed in via arguments, which could be read as arguing for accepting
absolute paths. I resolved it by reading the frozen design rather than reasoning from the general
standard, and the design settles it twice in the same table. **When a project-wide standard and a
frozen project-specific contract appear to disagree, the contract is the one that was written with
this artifact in view.**

---

## Insights gained

- **A reviewer's repair deserves a mutation control as much as an original build does.** Five
  repairs, five mutants, five kills — but I did not know that until I ran it, and "the suite is
  green" would not have told me.
- **The strongest evidence that a test addition is worth its bytes is a mutant that survives the
  other version.** Running the same mutant against both test-file states converts "this seems
  under-tested" into a measurement. It is a cheap instrument and I expect to reuse the shape.
- **A requirement stated with literal example strings is a requirement about those strings.** A1
  listed the three menu entries verbatim and I read them as illustrative. Codex read them as the
  specification. Codex was right, and the general form of the mistake — reading a concrete example
  as decoration — is worth carrying.

---

## Files created or updated

**Updated (the one artifact edit this session):**
- `Reproducibility Packet/tests/test_render_verification_scene.py` — blob `ba7d135a` → **`1833a472`**,
  33,822 → 34,780 B, 859 → 878 LF, 0 CR. Two test-only additions (Finding CT).

**Unchanged and re-verified byte-for-byte against Codex's declared reviewer state:**
- `Reproducibility Packet/scripts/utils/verification_scene.py` — blob `c12745ab`
- `Reproducibility Packet/scripts/render_verification_scene.py` — blob `0ae5b19d`
- `Reproducibility Packet/tests/test_verification_scene.py` — blob `cf61e5aa`

**Appended:**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one turn, 10,838 payload bytes, 175 LF, 0 CR, prior `98ab2f37…` → post `7b27df5e…`, prefix
  and payload both asserted byte-identical after the write. *(The Git delta reads `+175/-1`, not
  `+175/-0`, and nothing was deleted: Codex's turn ended `---` with no final newline and my append
  added one after it, so Git scores that line as changed. The byte assertion is the authority and
  it passed.)*

**Rewritten / updated as session closeout:**
- `agents/Claude/Session Summaries/HumanReport129.md` (this file)
- `agents/Claude/README.md` — the Step-2 bullet updated in place to current state
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten

**Deliberately not touched:** the root `README.md` (heartbeat check ran, no trigger fired),
`chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (no fault occurred),
`director_requests.md` (entry 2 re-measured and still accurate; no new entry owed),
`agents/Claude/references.md` (no external sources read).

**Scratch only, outside the repository:** the 48-check owner probe, the five-mutant reviewer-repair
control, the two-mutant own-addition control, the transcript prefix checker, and the asserting
append routine.

---

## Verification

```text
focused normal                     159 passed, 25.17 s
focused under python -O            159 passed (one expected pytest -O warning), 26.40 s
independent 48-check owner probe   48/48
reviewer-repair mutation control   6/6 (control green, five mutants killed)
own-addition mutation control      both mutants survive reviewer tests, both killed by mine
packet-wide fallback               1,344 passed, 1 failed, 28 collection errors
py_compile / git diff --check      PASS
```

The packet-wide count moved 1,343 → 1,344, which is exactly my one added test.

**The MuJoCo block persists and it is not ours.** `import mujoco` still fails at the interpreter
level because a Windows Application Control policy blocks `mujoco._functions`. I re-measured it: the
string "Application Control policy has blocked" appears **29** times across the run — once per
affected module — accounting for all 28 collection errors and the single test failure. **The
packet's true full-suite count remains unmeasurable while that policy holds, and 1,344 is not it.**
This is logged as `director_requests.md` entry 2 and only Randy can resolve it, since nobody else
can change a machine security policy.

---

## Next steps

1. **Codex re-reviews `1833a472`.** If it approves that blob as it stands, both approvals name the
   same state, **Step 2 closes**, and **Step 3 becomes authorized and is mine**: generate the fixture
   figure set into the packet and add the runbook step. If it edits or blocks, the owner re-review
   returns to me and comes first.
2. **When Step 2 closes, log the Live-Run README entry.** That is the milestone both agents agreed
   is publishable, and it is currently the only pending README obligation.
3. **Step 4 — connecting a real result — remains a separate joint authorization** that neither the
   design nor Steps 1–3 grants. Nothing in this session moved toward it, and the design's own reason
   still holds: three of Slot 8's four real inputs do not exist.
4. **My next regular progress report is Session 136**, unless a phase transition or an approved
   Claim-Sheet amendment fires sooner.
