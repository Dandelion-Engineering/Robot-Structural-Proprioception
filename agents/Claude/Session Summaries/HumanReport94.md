# Claude — Human Report, Session 94

**Date and time:** 2026-08-08 00:20 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts: 0. Data generated: 0. Pilot / validation / test reads: 0.** The test suite reads two approved development documents (`dev_fit_result.json`, `dev_fit_analysis.json`) through its fixtures; no delivered observation payload and no approved `.pt` checkpoint was opened.

**Progress-report session:** no. My next regular progress report is Session 96; no phase transition and no Claim-Sheet amendment occurred this session.

---

## Summary in one paragraph

This was round three of the review loop on the capacity-sweep executable. Last session I handed
Codex a state; Codex found one real defect in it, repaired the defect itself, and handed back an
edited state for me to approve. My job this session was to genuinely re-open that state, check
Codex's finding from my own side rather than trusting the diff, and either approve it or find
something. I did both: I confirmed Codex's finding was real and its repair correct — with a
piece of evidence I did not expect to get, described below — and then found one further place
where a rule the design states was being carried by an accident rather than by the code. I
repaired that, added a test that would have caught it, and handed the new state back. The
executable loop is open for Codex's fourth pass. Nothing was executed: no fits, no checkpoints,
no plan run, no data generated.

---

## What I was reviewing, and what it is for

The program under review is the one that will run the **capacity sweep** — the experiment that
asks whether the first result we measured (one sensor suite fitting slightly worse than the
other at one network size) survives when the network is made larger and smaller. It is 2,200
lines and it will eventually spend 42 model fits of real compute. Because that is the most
expensive single action this project has queued, both agents review it adversarially before it
is allowed to run at all, and nothing about it is taken on trust.

The review has a fixed shape: whoever owns a file hands over an exact set of bytes it approves;
the reviewer re-reads it, may edit it, and hands back an exact set of bytes *it* approves; the
owner must then genuinely re-open the file and either approve the same bytes or edit again. The
loop closes only when both agents have explicitly approved **the same state**. Approval is never
inferred from silence, from a passing test suite, or from the fact that someone made an edit.

---

## Codex's finding, and the evidence I got for free

Codex's finding — labelled AR — was this. The program has one guard whose job is to refuse to
write anything into the directory holding ten already-approved model checkpoints. Those ten
files are the sole provenance record for work already done, so overwriting them would destroy
evidence that cannot be regenerated. The guard takes the destination it was given, resolves it
to a full absolute path, compares *that* against the protected directory, and returns it.

In the half of the program I had written last session, the guard was called — and its return
value thrown away. The later write then used the original, unresolved spelling of the path.
Codex's point is that a check and the thing it authorizes have to be the same object: if
anything moves underneath the original spelling between the check and the write, the guard's
conclusion is stale. It demonstrated this concretely inside a temporary directory, and showed
the program reporting success while depositing its output somewhere the guard had never
approved. The repair is one line: keep the value the guard returns.

I accepted the diagnosis and the implementation. What I want to record is *how* I checked it,
because it produced a stronger result than I planned. Rather than read the diff, I reverted
Codex's one-line change and re-measured the file's fingerprint. It came back **bit-for-bit
identical to the fingerprint I had published for my own version last session**. That is a much
better guarantee than reading a diff: it proves the reviewer changed exactly that one line and
nothing else anywhere in a 2,200-line file, and I did not have to trust anyone's summary of it.
With the line reverted, Codex's new regression test fails; with it restored, it passes. The
finding is real and the repair works.

I also accepted a correction Codex made to my Session-93 wording. I had written that my session
did not read a tracked results file at all; that was too wide, because the test suite reaches
two approved development documents through its fixtures. Codex corrected it forward in the live
transcript rather than editing my report, which is the project's rule, and this report uses the
narrower wording.

---

## What I found — and the judgment call I had to make about it

The program has a rule, written into the frozen design, that each network size gets its own
output directory and that the program must refuse to run if it finds leftover files from an
earlier attempt in one. Carrying that rule requires two things to name the same directory: the
guard that inspects it, and the code that writes the checkpoint into it.

They did name the same directory. But each of them built the name from **its own separate copy**
of the same formatting expression, and nothing anywhere compared the two. I tested whether that
agreement was actually held in place by anything, by changing only the guard's copy — so the
guard would inspect a directory no arm ever writes into — and running the tests:

```text
focused test suite      203 passed
full packet suite     1,754 passed
```

Everything passed. The rule was being carried by a coincidence between two strings, and the
project had no way to notice if that coincidence ever broke.

**The honest severity is low, and I want to say so plainly rather than dress it up.** Nothing
misbehaves today, because the two copies currently agree. The guard is also already documented
as unreachable during a normal run, since the output directory is created fresh each time — it
is a second line of defence, not the first. So this is a gap in *coverage*, not a live bug.

That created a real judgment call, because I had told Codex in writing last session that a
review round which finds only coverage gaps should close the loop rather than hunt for one more
thing. By my own stated rule, the correct move here was arguably to approve and move on.

I repaired it anyway, and I told Codex exactly why so it can overrule my reasoning and not just
my code. The rule about closing assumes the cost of deferring a small finding stays flat. Here
it does not. The very next step after this loop closes is a "plan" run that produces a document
binding this program's fingerprint into the authorization for the 42 fits. After that point, a
twenty-line cleanup stops being a twenty-line cleanup and becomes an invalidated authorization.
The window for cheap changes closes at the next gate, and that asymmetry — not the severity — is
why I moved.

The repair is the same shape as one I made last session: extract the name into a single function
and have both sides call it. The new test checks four things: that the format now exists in
exactly one place in the program, that it lives in that function, that both users reach it
through the function rather than through a literal of their own, and that the writer's path
agrees with it for all forty arms. I re-ran the mutation that had survived before; it is now
caught.

---

## Verification

```text
focused suite                      204 passed in 3.65 s   (203 before + 1 new)
focused suite under python -O      204 passed in 3.91 s
full packet suite                1,755 passed in 120.73 s (1,754 before + 1 new)
mutation sweep                     4 real cases / 4 CAUGHT, 2 negative controls SURVIVED
compileall                         clean
git diff --check                   clean
frozen design                      UNTOUCHED, and the program's own digest check agrees
production files                   trainer, contract, network, analyzer, both result
                                   artifacts, both READMEs: ALL UNCHANGED
packet artifacts                   no plan, result or equivalence artifact anywhere in the
                                   packet; config/config.json still absent
fits 0 | checkpoints 0 | plan artifacts 0 | generation 0 | rollouts 0
```

Every mutation ran under a harness that restores the original bytes in a `finally` block and
then verifies the restore by fingerprint before continuing. All six restores verified. Two
negative controls — a changed docstring word and a changed status message — survived, which is
what tells me the new test fires on the thing it is aimed at rather than on any edit at all.

**Rollout count unchanged at 278.**

---

## The exact state I handed over

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 937ab73c960ac4d5e6ffcbcd1c869f071c47a8b5
  canonical/raw SHA-256    9ceb1298bad4247086d42d9fd08a01e1460647af91603a3391e5f4347fbfe489
  physical state           95,248 B / 2,222 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 0a8f8b71fccae95d9e0648bc45bea14902d9cb14
  canonical/raw SHA-256    dbee9c98e786a5cd2a5adaf189b3b56d95a76bf5710d31011dc33581a6535a19
  physical state           82,127 B / 2,019 lines / LF / no BOM / 204 tests
```

I explicitly approve those exact bytes. Codex owes the fourth pass. I restated the closing
condition in the transcript so that a fifth round does not happen by drift: **if Codex's next
pass finds only coverage, it should approve.**

---

## Decisions I made this session

1. **Accepted Codex's finding AR and its one-line implementation**, after reproducing the defect
   from my own side rather than reading the diff.
2. **Accepted Codex's correction to my Session-93 wording** about tracked-file reads, and carried
   the narrower phrasing forward instead of reopening the report.
3. **Repaired the unbound directory name rather than approving around it**, against my own stated
   closing heuristic, on the cost-asymmetry argument above — and said so explicitly in the
   transcript so Codex can rule against the reasoning.
4. **Pinned the current directory spelling in the new test, not merely the count.** The design
   makes those names part of what the plan document binds, so renaming one is a contract-visible
   change that should require touching a test. I flagged this as the one place I would accept an
   edit without argument.
5. **Left `.gitattributes` alone**, though Git warns that both reviewed files are LF in a
   working tree configured to produce CRLF. The committed bytes are LF either way and no
   fingerprint in this project is taken from a raw `.py` file, so pinning every Python file in
   the repository would be a repository-wide decision made as a side effect of a code review.
   Recorded in the transcript instead.
6. **Left the public Live-Run README untouched.** No artifact finished, no phase moved, no result
   exists. The running log is milestone-based by design.

---

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport94.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — one new function giving the
  capacity-point directory a single definition; both users now consume it.
- `Reproducibility Packet/tests/test_capacity_sweep.py` — one new test binding the guard's
  directory to the writer's.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only owner re-review turn and exact-state handoff.
- `agents/Claude/README.md` — Session-94 navigation and current exact-state pointer.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` (frozen)
- `README.md`, `Reproducibility Packet/README.md`
- `.gitattributes`, `.gitignore`

---

## Transcript hard gate

```text
pre-write bytes          1,608,413
pre-write lines          25,733
pre-write SHA-256        430a0751d60e52472ec8410f49e41c67d6cc49b21ccc42708656b73ee9a3aa43
final bytes              1,619,145
final lines              25,918
Claude header line       25,734; unique and after the boundary
final SHA-256            25a8926b0ced660810703e31d8ffc86b7e15e4d9ea167db0400aa86024865d14
diff                     +185 / -0
last agent               Claude
```

The pre-write fingerprint equals the one Codex published at the end of its Session 93, which
independently confirms the transcript was untouched between the two sessions. The append is a
byte append rather than a patch, which is what lets the prefix check promise byte-identity.

---

## Cross-review

I read Codex's `HumanReport93.md`, its full Session-93 transcript turn, and both files it
returned. Its report describes its own change accurately and does not overstate it. Its
correction to my Session-93 wording is correct and I accepted it. I found nothing in its work
that needs carrying forward as a correction beyond the one finding above, which is in my own
code rather than its.

---

## Next steps

1. Codex owner-reviews the exact blobs `937ab73c...` and `0a8f8b71...`. If it approves them
   unchanged, the executable loop closes.
2. Only after closure may the agents separately authorize one deterministic zero-fit plan run
   and review the artifact it produces.
3. The two equivalence fits and the forty curve fits remain a later, separate, joint
   authorization naming the approved plan's fingerprint.
4. The read-only analysis script, every later-role read, Stage 2, the final config, data
   generation and all rollouts remain blocked.

— Claude
