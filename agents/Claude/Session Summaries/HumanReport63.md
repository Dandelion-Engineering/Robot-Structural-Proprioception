# Human Report 63 — Claude

**Date and time:** 2026-08-02 20:15 PDT

**Phase:** Phase 2 — Execution

**Session type:** Owner re-review of a reviewer-edited artifact, under the review-cycle
playbook. Zero physical simulations were run.

---

## Summary

Last session I rewrote the payload-boundary extension — the pre-registered plan for the
one measurement the project still needs before it can amend its contract — and handed it
to Codex. Codex reviewed it, made five direct edits, approved its own edited version, and
handed it back with the loop deliberately left open: the rules say I have to genuinely
re-open the document and either approve that exact state or hand back a new one. Waving
through a reviewer's edits is the specific failure mode the rule exists to prevent.

This session was that re-review. I accepted all five of Codex's corrections — three of
them after checking the underlying facts in the code and configuration files rather than
taking the reasoning on trust — and found **one new defect inside Codex's own new text**,
which I fixed and handed back.

The defect is worth stating in plain terms, because it is the kind of thing that would
have been very hard to notice later. The document ends with a table of what each possible
outcome of the measurement *permits us to do next*. Codex had just tightened one of those
permissions, correctly. But the neighbouring branch still used the older, looser version
of the same rule. Because the two branches are mutually exclusive, the document ended up
granting different permissions for the same underlying evidence — and in the wrong
direction. I enumerated every outcome the classifier can reach (19,448 of them) and
measured it: in 3,185 cases, **deleting a measurement result made the document permit a
more aggressive design choice than keeping it**. In the worst case, throwing away the
heaviest mass's result raised the permitted design limit sixfold, into a band where four
of the seven test conditions fail the very requirement the option exists to guarantee.

The fix was to state the rule once and have both branches use it. Re-running the
enumeration afterwards: zero such cases remain.

Nothing was executed, nothing was authorized, and the project's blocked work stays
blocked. The document loop is now waiting on Codex.

---

## 1. What Codex found, and what I checked rather than read

Codex made five edits. Three of them rest on claims about the codebase, so I verified
those against the source instead of accepting the reasoning.

### The provenance record contained its own fingerprint

Every simulation this measurement runs has to be stamped with a record of exactly what
produced it, and that record is identified by a hash of itself. My version asked the
record to contain "all six" settings passed to the simulator — but one of those six *is*
the hash being computed. A record cannot contain its own fingerprint; there is no order
in which you could actually build it. **Confirmed at source:** the settings object has
exactly five fields and the fifth is the hash. Codex's fix names the five real inputs and
inserts the hash afterwards, which is what the existing protocol already does elsewhere.

### The zero-cost rehearsal contradicted the running order

The document promises that both agents read a **zero-simulation rehearsal** of the plan
before authorizing anything that costs simulator time. My version then put a one-rollout
verification step *before* that rehearsal. Both statements could not be true. Codex split
the executable into a genuine plan mode and an execute mode, and bound execute mode to the
digest of the plan that was actually approved — so the run cannot quietly diverge from the
thing that was authorized. Codex's version also writes a record when the rehearsal
*fails*; mine let a failed rehearsal vanish without leaving any artifact behind. That hole
was mine and I had not seen it.

### The control test could not test the thing it was added for

This is the finding I most want on record, because it is the same mistake I was fixing.

Last session Codex showed me that a safety check I had written would pass whether or not
the setting it was checking had reached the simulator. I fixed that. I then left a second
check — the "anchor," a re-measurement of a mass the project has already measured —
standing as though it proved the new payload setting was working. It does not, and the
reason is in the configuration file: the source condition the anchor copies **already
carries that exact payload mass**. So if the new setting were completely disconnected, the
anchor would still get the body it asked for and still pass.

**Verified directly from the assignment document:**

```text
scenario_dev_t01_f000_r02   payload_dev_0p050kg   0.05 kg
=> a dead payload override still hands the anchor exactly the body it requested
```

The general lesson is one I had written down the session before and then failed to apply a
second time: for every check, name the failure it exists to catch, then ask *what else in
the design produces the passing signal*. Here the answer was "the source configuration" —
something no amount of re-reading the check itself would have surfaced. Codex found it by
reading the design. Accepted without reservation, and Codex's re-ordering (all the healthy
baseline runs happen before any of the graded-damage runs) means the real liveness check
now stops the run before roughly an hour of simulation is spent on a possibly meaningless
measurement.

### Two more, both accepted

Codex also made the result file's internal cross-references into actual data rather than a
sentence promising they exist, and separated the one inherited verification rollout from
the extension's own 126 so the cost stays visible without being double-counted. And it
narrowed my "reduced coverage" rule: I had allowed a run that lost one mass to still
choose a design option for the remaining six. Codex's position is that a measurement whose
whole purpose is to settle all six unknown masses cannot settle them from five. That is
stricter than what I wrote and it is stricter *against my own convenience*, which is the
direction I want a reviewer pushing.

I additionally re-derived every number the document asserts, and they close:
126 simulations over 8 identities, 126 distinct keys, 76 internal references per mass and
532 in total, 168 comparisons in the liveness check, and the cost of every exit path.

---

## 2. The defect I found, and how I measured it rather than argued it

The last section of the outcome rules says which of three future design options each
possible result permits. Option B is "compress the range of payloads the project uses, so
that every test group sits inside a range we have verified." Its permission therefore has
to be capped at the heaviest mass where **every** group below it still passes its own
requirements — which is precisely the tightening Codex had just made.

But the neighbouring branch — the one that fires when some mass yields no usable result at
all — still capped at "the heaviest mass with any usable result," ignoring whether the
groups inside that range pass their own requirements. Those two branches are mutually
exclusive, so a single run gets one rule or the other, and they disagree.

Rather than argue about it, I enumerated the whole space. Because an earlier rule
guarantees the results shrink as mass increases, every reachable outcome is a
non-increasing list of seven numbers, and there are exactly 19,448 of them — the same
figure Codex's own exhaustiveness check reported, which is the point: the classifier *was*
checked for completeness, and what each branch **permits** was not checked with it.

```text
branch sizes            8,008 + 3,515 + 7,925 = 19,448
outcomes whose permitted range contained a group that fails its own
  requirement                                              4,106 of 8,008
outcomes where DELETING the heaviest result RAISED the permitted cap  3,185

worst case:  cap 0.025 kg  ->  delete the 0.200 kg result  ->  cap 0.150 kg
             the permitted range then contains four groups that fail
```

Strictly worse evidence permitting a strictly bolder choice is not a defensible property
for a pre-registration, and it is the exact direction of looseness Codex was correcting one
paragraph above. The fix is that Option B has one rule and both branches state it — an
empty result necessarily breaks the requirement chain at that mass, so the stricter rule
already covers the empty case properly. **After the fix: 0 of 3,185.**

I put the counterexample and the counts into the document itself, not just the chat, so
that a future reader who notices two branches stating the same rule finds out why before
"simplifying" one of them away.

---

## 3. Things I deliberately did not change

- **Abort-on-invalid-measurement placed early.** A run that finds an invalid statistic
  stops even if several masses measured cleanly. I read this as correct and left it: an
  invalid statistic means the *instrument* is broken, which is a different thing from a
  plant that is unsafe under load, and continuing to measure with a broken instrument does
  not produce a partial result.
- **Reduced coverage reported ahead of shape violations.** I checked whether this hides
  anything and it does not — neither permits anything, and the violations are recorded in
  a required field either way.
- **One note for the build step, not a document change.** The liveness check needs all
  eight baseline runs at all seven masses, so a mass excluded for safety must still finish
  its baseline block. The document already forces this in three independent places, so a
  wrong implementation fails loudly rather than silently — but it is worth saying out loud
  when the code is reviewed.

---

## 4. Decisions I made

1. **Hand back rather than approve.** The finding is new, verifiable, and reproducible
   from the document's own rules by enumeration, so the escalation rule (which fires when a
   round re-litigates something already settled, not when it finds a real defect) does not
   apply. I checked that explicitly rather than by counting rounds.
2. **Fix by unifying, not by adding a tolerance or a second rule.** One rule stated once
   removes the possibility of the two drifting apart again.
3. **Accept Codex's stricter reduced-coverage rule without pushing back**, even though it
   is stricter than what I proposed, because the argument for it is correct.
4. **Left the public Live-Run README unchanged.** This is an internal review handback on a
   document that is still under review, matching the reasoning Codex used for the same kind
   of turn last session. The check was made; the log stays lean by design.

---

## 5. Files created or updated

- `Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md` — the fix and its
  supporting enumeration (+30/−2). New canonical SHA-256
  `538ae06b87d0f733659ed113f3b38e0a0c1f7c7793d290358acf08d78df33b6a`, Git blob
  `d9f6e188817dc2738c1d167904fd70d98a6b9bd6`, 71,188 bytes, LF, no BOM.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — my Session 63 turn, appended (+192/−0), all four transcript
  integrity gates passed.
- `agents/Claude/Session Summaries/HumanReport63.md` — this report.
- `agents/Claude/README.md` — session index updated.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for the next session.

---

## 6. Verification run this session

```text
ScreenOverrides fields    5, provenance_hash present   -> circularity finding real
PhysicalKey fields        6, no payload field          -> mass prerequisite real
anchor source payload     0.050 kg from the assignment -> anchor cannot prove liveness
role-severity map         equals the assignment for all four splits
count closure             126 / 126 keys / 76 / 532 / 168 / 67 / 127 all reproduce
classifier state space    19,448 enumerated, partitions exactly (agrees with Codex)
Option-B anomaly          4,106 and 3,185 before the fix ; 0 after
full packet test suite    1,126 passed in 121.30 s
physical rollouts spent   0
config/config.json        still absent, as intended
```

---

## 7. Next steps

1. **Codex holds the turn.** It re-reviews the unified Option-B rule at canonical
   `538ae06b…` and either approves — closing the document loop — or hands back again.
2. If it approves, that authorizes **only** the build-and-review of the three
   prerequisites: the payload field on the simulator seam, the mass field on the results
   key, and the measurement executable itself. It does not authorize running anything.
3. After that: a zero-simulation rehearsal both agents read, then a separate explicit
   authorization, then the measurement runs once (about an hour of simulation).
4. Everything downstream — Amendment A2, the full dataset regeneration, the model work —
   stays blocked behind the measurement, as it has been since Codex's Session 60 ruling.
5. My next scheduled progress report for you is Session 64, unless an approved amendment
   or a phase change fires one sooner.
