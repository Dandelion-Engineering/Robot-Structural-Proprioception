# Human Report — Claude, Session 116

**Date and time (measured at write):** 2026-08-11 02:16 PDT
**Phase:** 2 (Execution) — open
**Spend this session:** 0 fits · 0 checkpoints · 0 rollouts · 0 generation runs · 0 pilot/validation/test reads · 0 C7 invocations

---

## What this session was

Codex's Session 115 closed the review loop on the rung-2 executable **unchanged** — it
approved my exact bytes without editing either file — which authorized exactly one thing:
**step 4, one zero-fit plan-mode action and a review of the artifact it writes.** This
session took that step, audited the result, approved it, and handed the second review to
Codex.

It also carried one open reviewer obligation: Codex appended a new entry to the public
Live-Run README and asked me to genuinely re-open it. I did, and found one thing in it.

Three pieces of work, in the order they were done:

1. **Verified Codex's arithmetic correction** rather than conceding it.
2. **Reviewed the public README entry**, found one real defect, edited it, handed it back.
3. **Ran step 4** — the plan — and built a second, independent instrument to audit it,
   plus a mutation sweep to establish that the instrument can fail.

---

## 1. The test-count correction — accepted, and measured

Codex's Session-115 turn corrected my Session-115 report: I had written that the packet
suite stood at 2,004 tests, decomposed as 1,863 + 142. That decomposition sums to 2,005.
Codex measured 2,005 and said so.

I did not simply accept it. Re-measured this session at the same bytes:

```text
collect-only     2005 tests collected in 3.02 s
full run         2005 passed in 128.92 s
```

The correction is right and the cause was a typo in my own arithmetic, not a missing or
extra test. Every figure this session writes carries 2,005.

Codex also raised a genuine forward-looking point I accepted as written: the **concluded**
Stage-1 capacity-sweep tests still aim `main()` at the real protected checkpoint tree in
two cases, with targeted cleanup, which is the same hazard I hit and closed in my own
Session-115 mutation sweep. That shape is only safe while the guard under test is present
— which is the one condition a mutation sweep exists to remove. Neither of us reopened a
jointly approved state to fix it; it is recorded so that whoever next mutates that file
redirects the packet root into a temporary directory first.

---

## 2. The public README entry — one finding

Codex appended one entry to the root `README.md` (the public Live-Run page) reporting that
the rung-2 training program is built and jointly approved but unrun, and explicitly asked
me to re-open that state rather than read the diff.

I checked its claims against objects outside the entry. Four are exact: the one-loop /
two-factory design, the two boundaries Codex accepted, the 142-focused and 2,005-packet
figures, and the statement that a single zero-fit plan is the only next allowed action.

**The closing sentence is not.** It read:

> "No plan artifact, fit, checkpoint, rollout, data generation, reserved-role read,
> capacity choice, threshold, or final configuration exists."

That list mixes two different scopes under one absolute verb. *Reserved-role read*,
*capacity choice*, *threshold* and *final configuration* really are project-wide zeros.
*Fit*, *checkpoint*, *rollout* and *data generation* are not. I re-derived the figures
from the artifacts' own ledgers rather than from anybody's summary:

```text
fits         10 (dev_fit fits_run) + 3 (stage1-run-1) + 42 (stage1-run-2)  =  55
checkpoints  10 + 3 + 42 = 55, and `find results -name "*.pt" | wc -l`     =  55
rollouts     15 pre-run replays + 136 (Codex S57) + 127 (Codex S73)        = 278
```

And the same public log **says so three entries above**, where it describes "forty new
fits" and "the 42 training runs". A stranger reading the log top to bottom would meet a
flat contradiction.

The thing that makes this a clean finding rather than a quibble is that **every precedent
entry in this log spells the same list with *is authorized*, not *exists*** — which is
exactly the distinction that keeps it true. The entry changed the verb and kept the list.

I edited it, `+1 / -1` on that one line, rather than arguing it:

> "The only next allowed action is one zero-fit plan. This program has produced no fit and
> no checkpoint, and its approval authorizes none of what comes after: no fit, checkpoint,
> rollout, data generation, capacity choice, or threshold. The reserved comparison data
> remains untouched and the final configuration remains unfrozen."

Every strong claim Codex was making survives; the absolute the log itself refutes does
not. It has a second benefit I did not plan for: the original would have gone false
**within hours of its own date**, because of the plan produced later in this session.

```text
README.md   blob 9f6297a4243a5241fc71f425923cb0466e5670f6
            raw SHA-256 cfc814f95ee29d0122c197596189f4596632cb4f1c02c69e3db813d91cba1f33
            145,260 B / 207 LF / 199 CR  (both EOL counts unchanged)
            approved by me at these exact bytes; Codex's re-review is open
```

**I appended no new entry of my own, deliberately.** I re-read the playbook in full, as I
do every session where the answer turns out to be no. Nothing was finished — the plan
carries one approval, not two — no phase closed, and the step taken is the one Codex's
own same-day entry announced as next. The playbook's lean rule and its "bloated running
log" failure mode point the same way. The entry worth a stranger's attention is the one
reporting a *jointly approved* plan, or an execution.

### The finding turned around on me

Re-deriving those counters caught something in **my own** continuity file, and I would
rather report it than not.

My summary's live counter block reads `ROLLOUTS 278 | FITS 13 lifetime` and has since
Session 98. Thirteen is ten development fits plus three sweep fits — both **my** sessions.
It never absorbed the 42 fits Codex's Session 100 spent. The rollout counter sitting
immediately beside it *is* project-wide: it includes Codex's Session-57 and Session-73
runs.

So one counter was project-scope and the counter next to it was self-scope, under one
heading, for eighteen of my sessions — which is precisely the defect I had just described
in Codex's sentence. Corrected to 55 in this session's rewrite, with the derivation written
beside it so the next session re-derives rather than remembers.

---

## 3. Step 4 — the zero-fit plan

### The precondition first

Design §7.1 requires plan mode to be reproduced to at least three scratch destinations
before execution is ever authorized. I ran it to three unrelated destinations outside the
repository, then to its real destination. **All four files are byte-identical.**

```text
Reproducibility Packet/results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json
  Git blob                 61a2bd220f16edb79dd14b36dae8f90cd768f62d
  canonical == raw SHA-256 b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040
  9,751 B / one canonical JSON line / 0 LF / 0 CR / pure ASCII / no BOM
  exit X_PLAN_OK, 0 fits
```

The plan lives in `plans/<run_label>/`, a **sibling** of the execution root and not inside
it. That is not cosmetic: execute mode claims `results/rung2_escalation/rung2-run-1/` with
a single atomic create that requires the path to be absent, so writing the plan there would
make the guard refuse the run it exists to admit.

### The audit — 132 checks, none of them the executable's own

The point of a review here is not to re-read the document; it is to rebuild what the
document *should* say from sources the executable does not control, and compare. So the
audit imports nothing from `rung2_escalation`, `capacity_sweep`, `dev_fit_trainer` or
`dev_fit_contract` — including a locally reimplemented canonical digest, so the
executable's own helper is not the thing checking the executable's output. Every
expectation comes from the frozen design, the approved fit ledger, the approved readback,
the delivered assignment, or the source files themselves.

**132/132 passed.** In summary:

| group | checks | what it establishes |
|---|---:|---|
| document form | 12 | ASCII, no BOM, no CR, no LF, canonical re-emission byte-identical, the exact 27-key set |
| host leakage | 11 | no backslash, drive designator, UNC, user name or absolute POSIX path; every declared path under the namespace and **passing through the run label** |
| digests | 26 | design, ledger, readback and assignment digests all **recomputed from the files**; config hash, manifest and role index equal to what all ten approved arms carry; all twelve code-identity digests recomputed, with the eight historical ones equal to the ledger's |
| rung-2 arms | 12 | the full 2×5 grid, no duplicate, 219,018 parameters each, correct factory, write arms, names embedding their own suite and seed |
| equivalence arms | 11 | exactly (C1, seed 0) and (S, seed 4), rung-1 factory, 32 channels, inside the reserved subtree |
| anchors | 15 | ten read-only anchors, ten **distinct** digests each equal to the approved ledger's; both equivalence targets equal to the matching approved checkpoint; anchors **name** the readback fields rather than copying a number |
| band + budget | 15 | 219,018 strictly inside [100,001, 1,000,000]; 12 fits = rung-2 + equivalence; checkpoints = fits = declared write paths; rollouts, generation and non-development reads all 0; the ten anchors not charged |
| protocol | 15 | equal to the approved ledger's protocol field for field, both window-schedule entries included; origin = onset + lead and decision = origin + window **derived** rather than trusted; Protocol P's `[1000, 1768)` reproduced |
| scope | 7 | the authority string still says development-only and still disclaims held-out evidence, a capacity selection and a C1-versus-S result; no verdict, no selected capacity, no threshold, no loss or accuracy value anywhere |
| non-occupancy | 8 | the execution root absent, the plan outside it, no rung-2 checkpoint or run artifact anywhere, and both approved dev-fit documents still at their approved digests |

### The instrument that measures the instrument

A 132-check audit that passes tells you nothing until you know it can fail. So I drove **23
single-mutation controls** through it — one arm dropped, the fit budget inflated to 13, a
rollout smuggled in, four digests forged, an equivalence target swapped onto the wrong
anchor, a checkpoint redirected into the protected checkpoint tree, a checkpoint aimed at
the host filesystem, the parameter band widened, epochs doubled, the window origin moved, a
code-identity entry dropped and another made stale, the split changed to `pilot`, a
selected-capacity verdict smuggled in, the authority string softened, a seed duplicated, a
write arm marked read-only, an anchor marked writable, the run label changed alone, the
namespace changed alone, and the equivalence subtree lifted out of the run.

**23/23 were caught by the specific check named for them.** The two checks that fire on
*any* byte change — the pinned file digest and the canonical round-trip — were excluded
from the verdict, because a control that only trips those measures nothing. Two no-op
controls (identical content; a reversed key order that canonicalises back to the same
bytes) both pass clean, which is what shows the harness can report success at all.

**The sweep improved the audit in one place rather than confirming it.** My first version
pinned the run label and the namespace to two independent literals. That catches a
disagreement between them by accident, not by a check. Since execute mode claims
`<base>/<run_label>/`, a plan whose label and declared destinations disagreed would
authorize writes the plan does not describe. Two checks were added: the namespace must end
with the run label, and every declared path must pass through it. Changing the label alone
now fails the first; changing the namespace alone now fails the second.

### The authorization gate, driven rather than described

Separately, and importantly with **each mutant authorized under its own digest** — so the
digest comparison cannot do the work and only the content checks can refuse:

```text
the real plan                     ACCEPTED
two byte-equivalent no-op copies  ACCEPTED
23 semantic mutants               ALL REFUSED, 0 accepted
  [17] the authorized plan is not the plan this executable builds at that run label
  [ 3] the authorized plan names a different training protocol
  [ 2] the authorized plan was written by a different code state
  [ 1] the authorized plan was written against a different design document
```

A gate that accepted everything would have passed an exact-bytes check identically. This
is the same instrument shape my Session 97 used on the Stage-1 plan, and it is the reason
that check is worth running.

---

## Decisions I made this session

1. **Run label `rung2-run-1`.** No reason to burn a number; Stage 1's first label was
   consumed by a real failure, which is not the situation here.
2. **The plan goes in `plans/<run_label>/`, not in the run root.** Stage 1's precedent, and
   mechanically required by the atomic absent-root claim.
3. **Edit Codex's README sentence rather than argue it.** The defect is a scope error with
   an obvious minimal repair, and the review cycle is the place for exactly this.
4. **No new public log entry this session.** Nothing finished, no phase closed, and the
   step was already announced. Lean by design.
5. **Report my own counter defect in the chat turn, not only in my private file.** It is
   the same class of error I had just raised against Codex; saying so is cheaper than
   having Codex find it later.
6. **Did not fix the concluded Stage-1 test hazard.** Corrections propagate forward; a
   jointly approved state is not reopened for a hazard that no current work touches.

---

## Files created or updated

| path | what changed |
|---|---|
| `Reproducibility Packet/results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json` | **new** — the step-4 zero-fit plan, blob `61a2bd22` |
| `README.md` (root, public) | `+1/-1` reviewer edit to Codex's 2026-08-11 entry; blob `9f6297a4` |
| `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` | `+223/-0`, one appended turn |
| `agents/Claude/README.md` | rung-2 lane status; the plan-artifact clause; the Live-Run bullet |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten; fit counter corrected to 55 |
| `agents/Claude/Session Summaries/HumanReport116.md` | this report |

Nothing else in the repository was touched. The audit and control harnesses live in the
session scratchpad outside the repository; their results are reported here and in the chat
turn, and the plan they audited is the tracked artifact.

---

## Transcript-order check

No violation, and no entry written to the monitoring chat — an entry there needs a fault or
a proposal to close, and there is neither. Verified at the git level rather than assumed:
Codex's Session-115 commit `5b6379b` touches the Phase-2 transcript as a single tail hunk
(`@@ -31796,0 +31797,110 @@`), additions only, and does not touch the monitoring file at
all; its README change is `+2/-0` on the running-log tail. My own append is likewise a
single tail hunk, `+223/-0`.

**The cross-agent digest convention operated for the fourth time.** My pre-append digest of
the transcript — `e14dea61…6e1355`, 1,971,439 bytes — is byte for byte the post-write digest
Codex published in its own Session-115 report, measured independently, in a different
session, by a different agent. It remains standing and non-blocking: it only works when the
previous author published one, and an absent digest is not a fault.

---

## What is open, and what happens next

**Two loops are open, and both are Codex's:**

1. The public README at blob `9f6297a4` — my reviewer edit, awaiting its re-review.
2. The plan artifact at blob `61a2bd22` / SHA-256 `b51b0009…` — step 4's second half.

Closing step 4 authorizes **step 5 and nothing else**, and step 5 is itself two
authorization halves, neither of which exists. Nothing in this session authorizes an
equivalence fit, a rung-2 fit, a checkpoint, execution, the step-6 analyzer, a role read,
a capacity or threshold selection, generation, a rollout, or the configuration freeze.

A closed loop is not an authorization, and an artifact is not approved by having been
produced. Both of those have been paid for in this project already.
