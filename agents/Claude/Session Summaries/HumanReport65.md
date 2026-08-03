# Human Report — Claude, Session 65

**Date and time:** 2026-08-03 04:32 PDT (timestamp taken from the shell at the moment the
chat turn was posted; the session ran 04:06–05:0x PDT)

**Phase:** 2 (Execution). **Rollouts spent this session: zero.**

---

## What this session was

Codex's Session 64 built the **third and final prerequisite** for the payload-boundary
measurement — `scripts/run_payload_boundary_extension.py`, 1,626 lines, plus 517 lines of
tests — and handed it to me for first review. That was the whole assignment: read a new
2,143-line artifact against a 1,285-line pre-registration, decide whether it does what the
document says, and either approve it or say why not.

I also owed a re-review of Codex's two edits to my Session 64 progress report.

**Result: I blocked the executable on three defects that made an execute run impossible,
corrected them, added five more findings, and handed back an explicitly approved state.**

---

## The three defects that stopped the run

Each was reproduced by *running* the program, not by reading it. That distinction matters
here: all three lived in `main()`'s execute-mode paths, and **no test in Codex's 36
entered `main()` at all.** The entire region was unexercised, which is exactly where this
project keeps finding things.

### 1. The replay-failure branch crashes and writes nothing

Before the extension spends a single measurement rollout, it re-verifies itself by
rebuilding one already-delivered simulation and requiring it back bit-identically. If that
check fails, the program is supposed to write a terminal record saying so — including
whether its one rollout was actually spent.

Instead it raises `UnboundLocalError`. The handler reads two variable names that are bound
only inside a **different** exception handler, one that does not run on the path leading to
this one. I drove it end to end with a plan in a scratch directory and an absent data root:

```text
File "run_payload_boundary_extension.py", line 1609, in main
    "ran": True, "passed": False, "elapsed_s": replay_elapsed,
UnboundLocalError: cannot access local variable 'replay_elapsed'
artifacts written by that run: none
```

The design intent was right and quite careful — Codex built a custom exception class
carrying `rollout_spent` and `elapsed_s` precisely so a terminal artifact would not
hard-code a cost it might not have incurred. The wiring took those values from the wrong
scope, so the class's whole purpose was inert.

### 2. The self-verification asks for the wrong delivered run, every time

The approved verification tool exports the identifier of the run it replays,
`scenario_dev_t01_f000_r00`, and derives the file name from it. The extension **imports
that derived file name** and then re-types the identifier by hand as
`scenario_dev_t00_f000_r00` — a real but different run, the one with no diagnostic probe.

Measured at zero rollouts by driving every step of the gate that precedes its rollout:

```text
candidate scenario_dev_t00_f000_r00   (the executable's literal)
  reservations matched              1        <- the uniqueness check PASSES
  screen_pair_id(reservation, None) basepair_dev_t00_f000_r00_dataset0
  delivered row's pair_id           basepair_dev_t01_f000_r00_dataset0
  pre-rollout check PASSES          False

candidate scenario_dev_t01_f000_r00   (the approved tool's exported constant)
  pre-rollout check PASSES          True
```

So **every** execute run would have failed its own gate and then crashed in defect 1. The
uniqueness check one line earlier passes, because the wrong name is also a real run — the
failure surfaces one step later, which is why reading the code does not make it obvious.

This is a rule we already carry: a pinned literal that also lives in a bound document is
checked by **equality, never by adoption**. Here the copy disagreed with the original
inside the same file that imports the original.

### 3. An error class that can discard an hour of simulation

The measurement loop caught one exception type. The payload-override construction raises a
different one — `AssignmentGenerationError`, which is a `ValueError` and not in that
hierarchy:

```text
issubclass(AssignmentGenerationError, ProtocolPError): False
```

One of those partway through would have escaped with up to 126 already-spent rollouts —
roughly an hour of simulation — recorded nowhere. Two other execute-mode exits (an
unresolvable input, an unreadable plan) also returned without writing anything, while a
third, structurally identical exit *did* write. The document's invariant X6 says every
execute exit persists the record; three did not.

---

## Two more findings, smaller but real

**4. The guard against publishing machine paths cannot see a real error message.** The
result writer refuses any string that *is* an absolute path. No refusal sentence is one:

```text
'C:\Users\cresp\x.npz'                                     -> refused
'ProtocolPError: pinned input is absent: C:\Users\...'     -> ACCEPTED
```

The second is verbatim what my defect-1 reproduction produced, so this fires on the first
realistic failure. I deliberately did **not** strengthen the writer's guard: making it
refuse embedded paths would block the terminal write, which is the failure I had just
fixed. The reasons are scrubbed where they are formed instead, and a test inspects the
written file. The scrubber's docstring states what it does not cover.

**5. A constant that looks authoritative and drives nothing.** `TAU_ANCHOR = 0.10`
governs, in the document, which nine of the ten damage levels the instrument must
reproduce. In the code it appeared exactly twice — its definition and the field the plan
publishes — while the list of nine was typed separately beside it. Changing tau would have
published a tau that did not produce the partition. It now derives the partition, and a
test constructs both directions of the document's stability claim.

I also added the equality check the anchor's ten pinned screen values never had. **That
test is green against Codex's state too, and I said so in the chat** — the numbers are
correct; what was missing was anything that would notice if they stopped being.

---

## What I changed, and one deviation I flagged

Under the review cycle the reviewer may edit directly. I did, in both files, and handed
back an explicitly approved state.

One change is structural rather than corrective: I lifted the whole pre-rollout half of the
verification gate into its own function, `resolve_replay_source`, so it can be exercised by
a test at zero cost. Without that, nothing in that branch is testable without the 3.9 GB
retained dataset, and the branch had no test of any kind. That is a change to Codex's
structure, so I led with it in the chat and handed it the decision rather than sliding it
in.

---

## Verification

```text
focused extension suite            45 passed   (36 -> 45)
focused suite under python -O      45 passed
full packet suite               1,181 passed in 117.19 s   (1,172 before)
compileall                         clean
new tests red against the reviewed state
                                   7 of 9, in an isolated packet copy carrying Codex's
                                   blob and my test file; Codex's 36 all still pass
mutation sweep                    17 cases | 13 caught | 4 survivors | 0 bad anchors
                                  fresh isolated packet copy per case, bytecode writes
                                  disabled, __pycache__ cleared per case, no -x,
                                  two passes required to agree
```

The sweep found a gap in **my own** repair: narrowing the measurement handler back to the
original exception type survived, because nothing drove the other kind through it. Closed
with a test that raises a real `AssignmentGenerationError` mid-run and requires the five
rollouts already recorded to survive into the census.

It also caught a fault in my own harness. I had embedded pytest's timing line in each
case's verdict, so "run the sweep twice and require identical results" — the detector we
adopted in Session 60 after the mutation harness was found to give false verdicts —
reported a disagreement on every clean sweep. That is precisely the way to train yourself
to ignore your only detector for a whole class of fault. Fixed before I trusted a verdict.

All four surviving mutations are characterised in the chat and annotated in the source as
code guards. None is a coverage gap; none may be counted as coverage either.

---

## Progress-report re-review

Codex reviewed my Session 64 director report and made two edits. I verified both against
primary records rather than accepting them on authority, and both are right:

1. I wrote that a colliding results key would have "quietly filed one run as another." My
   own Session 64 reproduction had established the narrower truth — the ledger refuses the
   duplicate **loudly**, about nine simulations in. I measured that and then wrote the
   stronger sentence anyway.
2. I wrote "151 rollouts, about 70 minutes," which contradicted line 14 of my own report,
   where the audited figure of 4,432.16 s (74 minutes) for the screen already appeared.

I accepted both diagnoses and both implementations, and moved one clause: Codex's replacement
said the follow-up "still cannot run until payload mass is part of the key," which was true
when the defect was found and is no longer true — the field landed in Sessions 63 and 64. I
put it in the past tense, named where it was fixed, and handed the blob back with an explicit
approval and an offer to take Codex's wording instead.

---

## Files created or updated

| Path | Change |
|---|---|
| `Reproducibility Packet/scripts/run_payload_boundary_extension.py` | `+193/−52`; blob `ff0cdbe63bf527cb21fe499b84e45a86e1dee0af` |
| `Reproducibility Packet/tests/test_payload_boundary_extension.py` | `+214/−0`; blob `ebdfdf837035e3a0049a2a68e78c102717d8ac92` |
| `agents/Claude/Progress Reports/Progress Report Session 64.md` | `+4/−3`; blob `b0ff74969f42bc6b7d45eb72bf8576dfe0020f64` |
| `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` | `+214/−0`, header unique, physically last, pre-write prefix retained byte for byte |
| `README.md` (Live-Run) | `+2/−0`, one log entry; banner already carried today's date |
| `agents/Claude/README.md` | Session-65 entry |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten |
| `agents/Claude/Session Summaries/HumanReport65.md` | this file |

Nothing under `Reproducibility Packet/results/` was created, changed, or read for
modification. `config/config.json` remains absent.

---

## Where things stand

- **Step 2 is still incomplete.** Two of three prerequisites are jointly approved. The
  third — this executable — is in review, at my corrected state, awaiting Codex.
- **Nothing is authorized to run.** Not plan mode, not the replay gate, not the
  measurement, not amendment A2, not the configuration freeze.
- **Lifetime simulation cost is unchanged at 151 rollouts.**

## Next steps

1. Codex re-reviews the two corrected blobs. If it approves them, Step 2 closes.
2. Then, and only then, plan mode runs — zero rollouts — and both agents read the plan.
3. A separate written authorization naming that plan's digest is required before the
   measurement's 127 rollouts (roughly an hour) may be spent.
4. Amendment A2 stays blocked until the measurement is read.

## What I would tell the director in one paragraph

The last piece of machinery for the payload measurement got built, and reviewing it found
that it could never have run: it was checking itself against the wrong reference run, and
when that check failed it crashed instead of writing down what happened. Both are the sort
of thing that looks like nothing on the page — one mistyped character in an identifier, two
variable names read from the wrong place — and both were only visible by running the
program rather than reading it. All three of the serious defects lived in the one part of
the program no test had ever entered. That is now the second session in a row where the
defect sat one layer below the layer being worked on, which is becoming a reliable place
to look.
