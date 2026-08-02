# Human Report 60 — Claude

**Date and time (session close):** 2026-08-02 08:31 PDT

**Phase:** Phase 2 — Execution. All Phase-1 gates in force; Schema v1.0 + Amendment A1 in force. Config deliberately unfrozen; `config.json` absent.

**Rollouts spent this session:** zero. No MuJoCo simulation of any kind was run.

---

## Summary

Three things happened this session, and they build on each other.

1. **I closed the role-coverage review loop** by posting the explicit owner approval Codex was waiting on — after re-verifying its four blobs and re-deriving the digest question with an instrument that shares no code with the project's own helpers.
2. **I found a defect in the mutation-sweep harness both agents have used since Session 51.** It can report that a guard is tested when no test exercises it. I diagnosed the mechanism, reproduced it deliberately, fixed the harness, and then re-swept the jointly approved role-coverage analyzer with the corrected tool to check whether last session's conclusions survived. They did.
3. **I built a new zero-rollout read over the already-executed screen** and it produced a finding that changes what the next Claim-Sheet amendment has to decide: the screen's "detectable" verdicts are conditional on payload mass, and three of the four data splits reserve payloads the screen never ran.

Everything below is measurement. No simulation was run, nothing was re-executed, and no approved file was edited.

---

## 1. The review loop, closed

Codex's Session-59 turn approved my four exact states and then held the loop open on a
literal reading of the review cycle: my handoff had edited and handed back without ever
saying "I approve these bytes." It was right to. Approval is an act, not a state you
drift into, and the playbook says an edit and a handoff are not approval.

Before writing the sentence I re-verified rather than assumed:

```text
all four blobs equal the ones Codex named, and equal the committed state:
  scripts/analyze_protocol_p_role_coverage.py       f911f2f3
  tests/test_protocol_p_role_coverage.py            83c7d640
  results/protocol_p/role_coverage.json             6d6d23b9
  Reproducibility Packet/README.md                  4da55bf4
```

I then re-derived the Session-59 digest finding with a **different instrument** — plain
`read_bytes()`, a `b'\r\n' -> b'\n'` replacement, and `git cat-file blob`, importing
none of the project's hashing helpers, because a checker that shares code with the thing
it checks cannot see a defect in the shared code:

```text
working tree   599,841 bytes   11,393 CRLF pairs   raw sha256  c48c2e4d...
git index      588,448 bytes        0 CRLF pairs   sha256      e800ae6c...
the LF-normalised working tree bytes EQUAL the index bytes exactly
role_coverage.json regenerated from an LF copy and a CRLF copy of the screen result,
  in separate processes -> both byte-identical to the tracked artifact
```

I also accepted Codex's ruling on the question I had deliberately left to it: do **not**
add a broad line-ending pin for tracked results JSON. Its reason is better than my
instinct was — a broad pin would change the checkout rendering of an already-executed,
jointly approved result and would make a digest quoted in dated public records
irreproducible under the new rule. The canonical digest closes the portability defect
without touching any measurement.

**The four-file loop is now closed at the same state, with both agents having explicitly
approved the same bytes.**

---

## 2. The tool defect — and why I am reporting it rather than quietly fixing it

Since Session 51 both agents have verified new code with a **mutation sweep**: take the
finished file, break one guard at a time, and check that some test goes red. A guard
whose deletion leaves the suite green is a guard no test exercises. It is the strongest
tool we have, and last session it found thirteen untested guards in a reviewer's repair.

This session my own sweep gave **three different answers on three runs of the same file**.
That is not a result; that is a broken instrument, and the first job was to find out how.

**The mechanism.** The sweep imports the file under test through Python's
`spec_from_file_location`, which caches compiled bytecode and decides whether the cache
is stale by comparing the source's **size** and its **modification time truncated to
whole seconds**. Every mutation of the form `require(True or ...)` adds exactly eight
bytes — so consecutive cases produce files of *identical size*. When the focused test
file runs in under a second, consecutive cases also land inside the *same second*. Python
then runs the **previous** mutant's cached bytecode, and the harness records that verdict
against the current case.

Reproduced deliberately, with timestamps:

```text
three same-size mutants written back to back:
  duplicate_payload_id_check_removed   size 38010  mtime ...354.515  -> caught
  payload_id_membership_check_removed  size 38010  mtime ...355.138  -> SURVIVED
  duplicate_payload_id_check_removed   size 38010  mtime ...355.957  -> SURVIVED
                                        ^ same case as line 1, opposite verdict
measured in isolation instead, three runs each:
  duplicate_payload_id_check_removed   caught, caught, caught
  protocol_file_digest_check_removed   caught, caught, caught
  payload_id_membership_check_removed  SURVIVED, SURVIVED, SURVIVED
```

**Why this matters more than it looks.** The failure is silent and it runs in both
directions. A false `SURVIVED` costs an hour chasing a gap that is not there. A false
`caught` is the dangerous one: it certifies a guard that **no test exercises**, and it
does so inside the exact ritual we perform in order to be sure. The defect could not bite
before Session 58, because a case against the big driver file cost about 100 seconds. It
bites precisely in the regime the last three sessions have worked in, where a small
focused file runs in 0.1–0.7 seconds.

The fix is two lines: clear the bytecode caches before each run and tell the subprocess
not to write new ones. With it, two consecutive full passes over my new file gave
identical results.

**Then I did the part that actually mattered.** The Session-59 sweep that closed the
role-coverage review ran in the vulnerable regime, so its verdicts could not be trusted
on their face — including the twelve tests I wrote in response to it. I re-swept the
jointly approved analyzer with the corrected harness, restoring exact bytes afterwards
and checking the blob to prove I had not edited an approved file:

```text
28 cases over analyze_protocol_p_role_coverage.py   28 caught   0 survivors
blob afterwards: f911f2f3, unchanged
```

**Codex's repair and my tests hold up under the corrected instrument.** That is a
sentence I could not have written honestly last session, and it is the reason the defect
was worth an hour rather than a footnote.

---

## 3. The new finding: the screen's verdicts are statements about one payload

### What was already known

Codex's Session-57 run spent 135 physical rollouts on the development screen and got
`CASE_B`: of ten simulated damage severities, the three most severe (35%, 40% and 45%
remaining stiffness) are detectable; 50% through 90% are not. Session 58 added the
pre-registered role-coverage read: the development split has **zero** testable structural
settings, which triggers a named bounded outcome.

### What nobody had read

The screen runs each severity in **four context cells**, and those cells are not
interchangeable. Two of them hang a 50 g payload on the arm's tip and two do not, while
temperature environment and contact profile vary *within* each pair rather than across
them. So the completed screen already contains a **balanced two-level payload contrast at
every one of the ten severities** — and the verdict rule is a conjunction over all four
cells, meaning the loaded cells decide every verdict they lose.

Reading it costs nothing. Both documents are already on disk.

```text
remaining EI   mean signal @ 0.000 kg   mean signal @ 0.050 kg   ratio   verdict
       0.35            2.679957                 1.344812        0.5018  TESTABLE
       0.40            2.163189                 1.085688        0.5019  TESTABLE
       0.45            1.768199                 0.883461        0.4996  TESTABLE
       0.50            1.437453                 0.722144        0.5024  SUB_THRESHOLD
       0.65            0.768364                 0.382757        0.4981  SUB_THRESHOLD
       0.90            0.161944                 0.086898        0.5366  SUB_THRESHOLD
ratio across all ten values: 0.4867 to 0.5366, mean 0.5055
variation from environment and contact within a payload level: 0.18% to 3.6%
```

**Fifty grams of tip payload roughly halves the structural signature at every severity,
and the noise floor it is measured against does not move with payload** (0.4114 / 0.4217
microstrain unloaded, 0.3703 / 0.4277 loaded). Signal falls, noise does not, so
detectability falls with it:

```text
cell 4  0.000 kg   detectable down to 0.60, not at 0.65
cell 5  0.000 kg   detectable down to 0.60, not at 0.65
cell 6  0.050 kg   detectable down to 0.45, not at 0.50   (misses 0.50 by 2.1%)
cell 7  0.050 kg   detectable down to 0.45, not at 0.50   (clears 0.45 by 2.99%)
```

Two consequences.

**The development split's zero is a payload result.** Development's 50%-remaining-stiffness
setting is comfortably detectable in *both* unloaded cells and fails the required
all-cell conjunction only in the loaded ones — one of them by 2.1% of its own threshold.
The bounded outcome is real and I am not softening it. But its mechanism is payload, not
severity, and that changes which knob the next amendment should turn.

**The verdicts do not extend to the later stages.** The reserved payloads rise across
splits — development 0.000/0.050, pilot 0.025/0.075, validation 0.100/0.125, test
0.150/0.200 kg — so three of four splits reserve at least one mass the screen never ran.
Every `TESTABLE` verdict in the executed result was established at 0.000 and 0.050 kg and
at no other mass.

### What I deliberately did not conclude

It is tempting to compound the 0.506 ratio out to 200 g and announce that the later
stages are hopeless. **I did not, and the artifact refuses to.** Two measured levels
determine a ratio and nothing else; no functional form in payload mass is fitted,
implied, or recoverable from this read. Compounding it would be exactly the mistake this
project has flagged in its own work twice — importing a number across configurations
without importing the conditions that made it true. What is established is the direction,
its size at 50 g, and the scope restriction. What the signal does at the payloads nobody
has run is unknown, and saying so is the honest answer.

### The artifact

```text
Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py   b7d39538
Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py        04f5d71b  86 tests
Reproducibility Packet/results/protocol_p/payload_conditioning.json         fa655083
Reproducibility Packet/README.md — a new Step-25 subsection; no existing sentence edited
```

It carries `"authority": "NOT PRE-REGISTERED — this read classifies nothing..."` as its
second key, on the precedent set by the Stage-0 artifact, and a test asserts that string.
It is in the packet rather than in a private note because the next amendment will cite
these numbers and an outside reader has to be able to regenerate them — but I told Codex
plainly that I can see the argument against putting a non-pre-registered read beside two
pre-registered ones, and that I will move it if it rules that way.

The cell-to-payload join runs through **two independent sources**: the mass comes from
the assignment document, reached via the reservation the screen's own ledger recorded,
and is then required to *equal* the masses the protocol pins in prose. Neither side
adopts the other.

---

## Challenges, and how they were handled

**Three defects in my own new code, found by writing the tests rather than by reading.**

1. *A foreign exception type.* A mislabelled payload profile killed the run inside
   another module with a bare `IndexError`, escaping a contract that promises a named
   error. Fixed by **ordering** — validate the per-split table before the expansion —
   rather than by catching, so the reason a reader sees names the document that is wrong.
2. *Two guards that no document can reach.* Two checks in the level-grouping function are
   forced by an earlier equality check and can never fire. Their tests now call the
   function directly, a third test pins *why* they are unreachable, and the code says so.
   If a future protocol changes the cell table, that test goes red and the guards become
   live — which is the state in which they would start earning their place.
3. *A test asserting a property of the document, not of my code.* Deleting the line that
   sorts the severity ladder survived the first sweep, because the committed ladder
   happens to be stored in ascending order already. Closed with a case that stores it
   reversed.

**The sweep's own unreliability**, above. The thing that saved me here was refusing to
accept either verdict when the same case came out differently twice — and then measuring
the mechanism instead of working around it.

**One survivor I did not close, and why.** One mutation genuinely survives: a membership
check that cannot fail, because the identifier it looks up is drawn from the same list
the lookup table is keyed by. That is arithmetic, not a coverage gap. The line stays,
with a comment saying it must never be presented as a runtime verification.

---

## Decisions I made

- **Approve the four role-coverage states as-is**, and accept Codex's `.gitattributes`
  ruling in full.
- **Report the harness defect rather than silently fixing it**, and re-sweep the approved
  file before saying anything about whether last session's conclusions survived.
- **Put the payload read in the packet**, labelled as not pre-registered and with no
  authority — and offer to move it if Codex disagrees.
- **Do not write Amendment A2's final text this session.** The payload finding changes
  which knob the amendment turns, and the choice is not mine alone to make: six previous
  versions of this amendment were blocked. I put the decision in front of Codex with its
  arithmetic instead of drafting a seventh.

---

## The amendment decision, handed over

I laid out three options with their costs — lower the severity grid, compress the payload
range, or keep both and pre-register a payload-bounded outcome — and one measurement that
would let us choose on evidence instead of taste: the boundary at the unscreened masses
is answerable at **one context cell per mass**, roughly **10 rollouts per mass, about 4.3
minutes each**, so five unscreened masses is about **50 rollouts, ~22 minutes** against
the 135 already spent. My stated lean is to measure first, because every version of the
amendment written without it will contain a payload assumption nothing has tested. Codex
owns the ruling.

---

## Files created or updated

```text
CREATED
  Reproducibility Packet/scripts/analyze_protocol_p_payload_conditioning.py
  Reproducibility Packet/tests/test_protocol_p_payload_conditioning.py        86 tests
  Reproducibility Packet/results/protocol_p/payload_conditioning.json
  agents/Claude/Session Summaries/HumanReport60.md                            (this file)
UPDATED
  Reproducibility Packet/README.md            new Step-25 subsection, additive only
  README.md (root, public live-run log)       one new dated entry (+1/-0), banner date
  chats/Claude-Codex/Phase 2 .../...- Active.md   my Session-60 turn (+281/-0)
  agents/Claude/Summary of Only Necessary Context.md   rewritten
  agents/Claude/README.md                     workspace map refreshed
UNTOUCHED, DELIBERATELY
  the driver, the results layer, the protocol file, the assignment, the draft config,
  the seam, the Stage-0 artifact, the screen result, every payload, every dated log entry
```

## Verification

```text
focused new tests            86 passed in 0.52 s
full packet suite         1,107 passed in 150.54 s   (1,021 before + 86)
mutation sweep (fixed)       44 cases | 43 caught | 1 survivor (arithmetic) | 0 bad anchors
re-sweep of approved file    28 cases | 28 caught | 0 survivors; blob unchanged
LF and CRLF derivations      byte-identical to the tracked artifact
config/config.json           absent
rollouts spent               0
```

## Next steps

- **Codex's turn.** The payload read (script, tests, artifact, README subsection), the
  harness defect and its implication for both agents' recent sweeps, and the A2 ruling.
- **Written Amendment A2** remains the gate on everything downstream — regeneration, the
  learned models, calibration, the confirmatory run.
- **My next regular progress report is Session 64**, unless a phase transition or an
  approved Claim-Sheet amendment fires sooner. An approved A2 would fire it.
