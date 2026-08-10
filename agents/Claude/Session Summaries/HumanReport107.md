# Claude — Human Report, Session 107

**Date and time:** 2026-08-10 04:21 PDT

**Phase:** Phase 2 — Execution, with Phase-3 packet assembly continuing alongside it

**Progress-report session:** No. My next regular progress report is Session 112, unless a phase transition or an approved written Claim-Sheet amendment fires one sooner.

---

## Summary

This was a review session with one repair. Codex's Session 106 handed me the packet's
`.gitignore` back at a new state and asked for a genuine owner re-review. I gave it one, did
not find anything wrong with it, and approved it — which closes that loop. Then I asked the
question that the last three findings in this stretch have all turned out to be instances of,
pointed it at the file next door, and found something.

The question is **"does this rule travel?"** The Reproducibility Packet is supposed to be a
folder a stranger can take away on its own and run. A rule that the packet depends on but that
lives in a file at the repository root does not go with it. Codex's Session 105 found this for
the *ignore* rules and moved them into the packet's own file. My Session 106 found four
destinations missing from that list; Codex's Session 106 found a fifth. Three findings in a row,
each one the same shape one step further out.

Nobody had asked it of `.gitattributes` — the file that pins how line endings are stored. There
is exactly one of those in the whole repository, it sits at the root, and **all three of its
rules are about files inside the packet**. So they are lost twice over when the packet is
published on its own: the file does not travel, and its rules are written with the packet's
directory name in front of them, so they would match nothing even if it did.

That matters because one of the three pinned files is checked by a **raw byte comparison**
rather than a line-ending-insensitive one, and that check is on **Step 1** of the packet's own
runbook. I drove it end to end rather than reasoning about it: a fresh Windows-style clone
without the pin produces a `schema.json` of 15,882 bytes instead of 15,212, and the packet's own
validator then refuses with *"configuration schema_sha256 does not match schema.json bytes."*
With a packet-local pin, the file comes back byte-identical and the validator accepts. I wrote
the missing file and handed it to Codex for review.

Nothing scientific moved this session. No model was fit, no simulation run, no measurement
spent, and no result read. Stage 1 remains finished exactly as it was.

## What was accomplished

### 1. Owner re-review of the packet `.gitignore` — approved, loop closed

Codex's Session-106 addition was `/results/sensor_model/`, covering a `index.csv` that Step 20
of the runbook writes and that nothing was ignoring. I checked it and it is correct.

Rather than check its four-plus-one list against my four-plus-one list — which is how two people
converge on the same blind spot — I rebuilt the destination census from a different starting
point, taking the union of three independent extractions from the runbook:

- every path token inside every `powershell` command block;
- every backticked path anywhere in the prose, which is where the runbook declares what each
  step produces;
- **the `argparse` string defaults of all 41 scripts the runbook invokes.**

That third source is the one that mattered, and it explains my Session-106 miss precisely. I had
swept *destination arguments*. Step 20 passes no destination argument — it relies on the
parser's default. **An enumeration whose domain is "arguments present" is structurally blind to
"argument absent, default used."** Codex did not catch a step I skimmed; it caught a step my
instrument could not see. That distinction is worth keeping, because the repair for the first is
"be more careful" and the repair for the second is "change the instrument."

The union came to **93 destinations**, and `results/` is the only output root the runbook has —
no invoked script carries a path default pointing anywhere else.

### 2. The measurement that actually decides it, and why the obvious one cannot

Both Codex and I had been checking these rules with `git check-ignore` **inside this
repository**. That cannot answer the question. Two ignore files are active here — the packet's
and the root's — so a "yes, it is ignored" answer does not tell you *which file* supplied the
rule, and a rule the packet is missing can look covered because the root happens to cover it.

So I built a fresh replica: `git init` in a scratch directory outside the repository, whose only
ignore file is a byte copy of the packet's own (digest verified equal after copying), and
evaluated every destination there.

```text
targets tested                            111   a file entry as itself; a directory entry as
                                                both probe.csv and probe.npz, so a missing
                                                directory rule cannot hide behind *.npz
ignored here but NOT in the replica          0   nothing depends on the root file
uncovered in both, and not tracked           0
uncovered directory entries                  9   all nine are tracked evidence trees and are
                                                correctly visible
```

The negative control I ran exhaustively rather than by sample. Instead of picking six or seven
neighbouring directories to confirm they are *not* swallowed, I put **all 205 tracked packet
files** through the replica's matcher: none is ignored by any packet rule.

### 3. A probe defect of my own, caught by its own canary

My first negative control drove `git check-ignore --stdin` from Python, and it silently
under-reported. On Windows, text-mode standard input translates a newline into carriage-return-
newline, so every path arrived with a trailing carriage return. A path ending in `.pt\r` no
longer matches the rule `*.pt`, while a path ending in `index.csv\r` still matches a *directory*
rule — so some answers came back and some vanished, with no error anywhere.

It was caught only because I had seeded three known-ignored paths as a liveness canary and two
of the three came back. The fix was to pass the paths as ordinary command-line arguments, which
have no such translation.

This is the third time this project has been bitten by parsing a tool's output instead of asking
it a question with an unambiguous answer, and my own summary already carries the lesson in those
words. I wrote the parsing version anyway. It is in the record because a probe that mis-scores a
property that is passing is one edit away from mis-scoring one that is failing.

### 4. Finding BB — the line-ending pins do not travel, and one of them is a gate

A `.gitattributes` file tells Git how to store and check out particular files. This project uses
it to pin three files to Unix line endings, because their exact bytes are hashed and a Windows
checkout would otherwise silently rewrite every line ending and change the hash.

There is one `.gitattributes` in the repository, at the root, and every rule in it names a path
inside the Reproducibility Packet. There is no packet-local copy.

**The consequence, driven rather than inferred.** `scripts/utils/config_contract.py` compares
the draft configuration's declared `schema_sha256` against a **raw** digest of `schema.json` —
raw meaning the bytes exactly as they sit on disk, with no allowance for line-ending
differences. I committed `schema.json` into a scratch repository configured the way a Windows
clone is configured by default, deleted it, checked it out again, and then called the packet's
own validator on the result:

```text
tracked schema.json                15,212 B   670 LF     0dae0dd0…   what the draft config declares
clone WITHOUT .gitattributes       15,882 B   670 CRLF   b11fd1d8…
  packet's own validator says      REFUSED — "configuration schema_sha256 does not match schema.json bytes"
clone WITH a packet .gitattributes 15,212 B   670 LF     0dae0dd0…
  packet's own validator says      ACCEPTED
tracked file, control              ACCEPTED
```

That comparison sits on **Step 1** of the runbook, so a Windows reader who clones a published
packet meets it at the first validation command in the document.

**How far the problem reaches — bounded by measurement, not by argument.** I swept all 205
tracked packet files for those that are line-ending sensitive (123 of them) and whose raw digest
appears as a literal anywhere in the packet. Sixteen came back. Fifteen of those sixteen are
compared in the *canonical* domain, which folds line endings before hashing and is therefore
immune; the project already knew this and says so in the code's own comments, citing the
sessions where it was learned. I then enumerated **every raw-domain hash call site in the
packet's scripts** — thirteen — and exactly one takes a tracked text file:

```text
config_contract.py:216   schema/schema.json   tracked text, and a gate
the other twelve         checkpoints, numeric payloads, and generated CSV files in the data
                         root — binary or never version-controlled, so Git never rewrites them
```

So the root file's own structure turns out to have been right all along: its first rule stands
alone under a comment about the byte-hashed schema, and the other two sit under a comment
calling pinning defence in depth. That reading is now measured rather than assumed.

**Repaired.** New file `Reproducibility Packet/.gitattributes` — 1,693 bytes, Unix line endings,
no byte-order mark, plain ASCII. It carries the same three rules with the packet-name prefix
removed, and its comments record which rule is load-bearing and why the other two are not, so a
future reader does not have to re-derive that distinction.

### 5. Two things I deliberately did not do

**I did not touch the repository-root `.gitattributes`.** The precedent from the ignore-file
finding would suggest *moving* the rules rather than duplicating them. I considered that and
declined, for two reasons. The two files protect two different things — a full-repository
checkout and a packet-only checkout — and the packet's rule already wins where both apply, so
the duplication is behaviour-neutral. More decisively, the ruling that produced the root
`.gitattributes` is on my standing "escalate rather than reopen" list. Editing it inside a
review is exactly the move that list exists to prevent. If Codex judges the root lines should
go, that is an escalation, not a repair either of us should apply on our own.

**I did not reopen the packet README.** It is closed with both agents' approval on the same
bytes, no runbook step changes, and a reader never invokes a `.gitattributes` directly. If Codex
judges the runbook owes a reader a sentence about it, that is a forward revision for it to
propose.

## Challenges and how they were overcome

**The instrument both of us were using could not answer the question we were asking it.**
`git check-ignore`, run inside this repository, conflates "the packet covers this" with "the
root covers this". Every check either of us had run over three sessions had that ambiguity in
it. The fix was to build a repository where the ambiguity does not exist — one file, no tracked
history — and re-ask there. That is also what made the exhaustive negative control meaningful:
inside this repository, a rule that swallowed a tracked file could hide behind Git's habit of
not re-evaluating files it already tracks; a repository that tracks nothing removes the question
entirely.

**My own probe failed silently, in the exact manner my notes warn about.** Described above. The
canary was the only reason I noticed, and I would not have written a canary if the summary had
not made a point of the earlier incident. That is the argument for keeping the lesson list.

**The session-tooling writer had expired again.** The gated chat-append writer, which refuses to
write a message whose timestamp disagrees with the clock, lives in scratch space and does not
survive between sessions. This is the second time I have had to rebuild it. It rebuilt correctly
this time, and the reason is that after the *first* rebuild came out weaker than what it
replaced, I moved the improved description into the block that owns the lesson rather than
leaving it in that session's notes. The mechanism worked on its second test.

## Decisions and reasoning

1. **Approve the `.gitignore` at Codex's exact bytes.** Its addition is correct, and my
   independent census found nothing further. Approving the same bytes is what closes a loop;
   returning a cosmetic change would not.
2. **Rebuild the census from a different starting point rather than check Codex's list.**
   Checking someone's list against your own reproduces the shared blind spot. Deriving it from
   the scripts' own defaults is what exposed why the blind spot existed.
3. **Measure in a fresh replica, not in this repository.** The only domain where "does the
   packet's rule cover this" has an unambiguous answer.
4. **Repair the `.gitattributes` gap rather than only report it.** It is one file, it changes no
   behaviour here, and the alternative is leaving a known first-step failure in a packet whose
   whole purpose is that a stranger can run it.
5. **Duplicate the rules; do not move them.** Two publication surfaces, behaviour-neutral here,
   and the root file's ruling is on the escalate-don't-reopen list.
6. **Do not update the public Live-Run README.** This is packaging. It changes no scientific
   result, completes no artifact, and closes no phase. Codex made the same call for the same
   reason last session, and the running log is lean by design.

## Insights gained

- **A finding's mechanism is more portable than its fix.** "Rules that must travel with the
  packet belong inside the packet" was learned about ignore rules. Applied as a *question* to
  the next file over, it found a defect with a harder consequence — a refusal at the first step
  rather than a stray file in a status listing. The three previous findings in this stretch were
  all the same shape, each one step further out; this is the fourth, and it is the first to
  cross into a different file.
- **An enumeration is only as complete as its domain.** Sweeping arguments cannot see a command
  that omits the argument. This is the general form of the miss, and it is more useful than the
  specific one.
- **A measurement taken where two sources could supply the answer is not a measurement of
  either.** The replica is the instrument; the repository is the confound.
- **Canaries pay for themselves.** Three seeded known-positive inputs turned a silent
  under-report into an immediate, obvious failure.

## Files created or updated

- `Reproducibility Packet/.gitattributes` — **new**; packet-local line-ending pins, blob
  `76976c108853b5a9ff6712b8e5aac4345606f0bb`.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the Session-107 owner re-review, the approval, Finding BB and the handback.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — appended the session's transcript-integrity entry.
- `agents/Claude/Session Summaries/HumanReport107.md` — this report.
- `agents/Claude/README.md` — session index and current-state text.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for the new open state.

**Not changed:** the packet README, the repository-root `.gitignore`, the repository-root
`.gitattributes`, any script, test, protocol, plan, result, or checkpoint, the Claim Sheet, the
director requests file, the final configuration, or the public Live-Run README.

## Verification and resource boundary

```text
full packet suite                     1,792 passed in 128.39 s   (count unchanged)
git check-attr on the three pinned     text: set / eol: lf, all three, after the edit
digests of the three pinned files      unchanged byte for byte after the edit
root .gitattributes                    identical to the blob at HEAD
working tree                           clean before; one new untracked file after
every probe write                      under the session scratch directory, outside the repository
```

No fit, no checkpoint, no simulator generation, no physical rollout, no invocation of the
capacity-sweep reader, no plan publication, and no pilot, validation or test read. No
observation payload, no label payload and no checkpoint file was opened at all — the
line-ending experiment copies one tracked 15 KB JSON file and nothing else. Lifetime physical
rollouts remain **278**; the lifetime fit counter remains **13**. Stage 1 is finished as scoped;
nothing here selects a capacity, sets a threshold, opens Stage 2, or licenses any additional
statement about the paired capacity curve.

## Next steps

1. Codex genuinely re-opens `Reproducibility Packet/.gitattributes` at blob `76976c10…` and
   either approves those same bytes or returns a corrected state. Two questions I asked it to
   rule on rather than simply accept: whether the packet file should duplicate the root's rules
   or whether the earlier precedent requires a move (I think a move escalates rather than gets
   applied), and whether the two defence-in-depth lines belong in the packet file at all given
   that no gate refuses without them.
2. Keep the packet README closed unless a genuinely new finding requires a forward revision.
3. Preserve the disclosed clean-machine checkpoint limitation, which is unrelated to this
   finding and is still open by design rather than by oversight.
4. Do not infer capacity selection, threshold selection, Stage 2, later-role reads, or a final
   configuration from any of this packaging work.
5. My next session is 108. My next regular progress report is Session 112.
