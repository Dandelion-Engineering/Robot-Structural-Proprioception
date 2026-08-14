# Human Report — Claude Session 130

**Current date and time:** 2026-08-13 18:20 PDT

---

## Summary

Slot 8 — the Claim Sheet's commitment to build something *you* can use to check the project's
result without reading the technical report — now exists as a working, reviewed surface, and this
session put its figures and its runbook instructions into the Reproducibility Packet.

Three things happened, in this order.

1. **Codex closed the Step-2 review** in its Session 129 at the same four blobs I approved in
   mine, so the module, the fixture, both renderers and their 159 tests are jointly approved. That
   was the project's only open loop.
2. **Codex's own approval turn landed in the wrong place in the transcript**, 12,000 lines from
   the end. It caught the fault itself, preserved the misplaced copy, and appended a dated
   correction. I am the monitor for that failure mode, so I re-derived the whole thing from Git
   objects rather than from Codex's account and confirmed it: two addition-only hunks, and
   deleting exactly the inserted lines reproduces my prior state byte for byte. Nothing was lost.
3. **I built Step 3**: the scripted figure set is generated into the packet, runbook Step 32 is
   written, and the exact state is handed back to Codex for review.

I also logged the public Live-Run README heartbeat this milestone had been waiting on since
Session 122, and carried forward a correction that came from outside the two of us: the packet
test suite is **2,267**, not the degraded numbers Sessions 128 and 129 recorded during a Windows
security-policy block that has since cleared.

**Nothing scientific moved.** No fit, checkpoint, rollout, generation run, analyzer or C7
invocation. No configuration, real role index, role payload or checkpoint was opened. No pilot,
validation or test read. Every number on every figure in this session was fabricated by the
packet, and each image says so in red.

---

## What Step 3 actually is, and why it is worth a session

The verification artifact is a screen. You pick one of four named body changes from a menu, scrub
or play a timeline, and see three things at once: the two simulated arms moving against the path
they were asked to follow, what each of the two sensor suites called and how confident it was, and
the tracking error over time with the exact five-second window the project's headline number is
computed over shaded in. There is nothing to type.

Step 3 is the scripted half of that: the same drawing code, run under a non-interactive backend,
writing one 300-DPI PNG and one machine-readable scene record per case, plus the complete menu and
its fingerprint. Ten files. That set is now tracked in the packet at
`Reproducibility Packet/results/verification_fixture/`, and packet runbook **Step 32** tells a
reader how to regenerate it and how to open the interactive menu instead.

The reason the scripted half matters is that it is the half that can be checked. An interactive
demo is a claim about what someone saw; a byte-deterministic figure set is an artifact anyone can
regenerate and compare. I measured that rather than asserting it — rendered the whole bundle twice
into two scratch directories outside the repository and compared all ten files byte for byte, zero
differences, and the packet copy is identical to both.

---

## Challenges, and how each was handled

### The transcript-order fault

**What happened.** I authenticate the chat transcript's bytes before reading it. The check failed:
the 2,210,612 bytes I had written at the end of Session 129 were no longer the file's prefix.

**What it was.** Codex's Step-2 approval had been inserted at line 23,891 — in the middle of a
transcript that is now 36,000 lines long — because it placed the append with a patch anchor
(`-- Claude` plus a separator) that occurs many times in a file where two agents alternate. A
patch anchor is a search, and a search over a repeated string returns its *first* match. Verifying
the file's digest beforehand does not constrain where the anchor lands; those are two different
objects. Codex's own post-write assertions caught it in the same turn, and it appended a dated
correction at the physical tail rather than moving anything.

**What I did about it.** A line-level "nothing deleted" is a report about lines, not about bytes,
so I did the check that settles it: I reconstructed Codex's committed blob by deleting exactly the
72 inserted lines and the 46 appended lines, and it reproduces my Session-129 blob byte for byte.
Every figure Codex published reproduces independently. I posted that confirmation to the
Transcript Order Monitoring thread, which is where a reported fault belongs.

**The honest read.** This is the third recurrence of one root cause, and the rule the thread
already carries — *the whole prior file travels as an explicit asserted prefix, not a context
block* — is unchanged; this one is a narrower instance of it. What is worth noticing is that for
the second consecutive time the agent that caused the fault is also the one that detected and
disclosed it, in the same turn, before closeout. Assertions that can fail are worth writing
because occasionally they do.

### A wrong sentence I wrote and then measured

Writing runbook Step 32, I described the fixture's deliberate refusal to flatter the structural
suite as: better tracking for S on one case, for C1 on one case, "the same value to both once, and
identical arms once." I had taken that from my own continuity notes. Then I drove the project's
real metric over the fixture instead of quoting myself, and it was wrong: **two** cases are exact
ties, not one. One of them has identical tracking but *different* decisions; the other is the pair
that is identical in every recorded field but its name. I rewrote the paragraph around the
measured numbers.

This is small, and it is the reason I keep flagging it: the sentence was plausible, came from my
own file, and would have shipped in a reader-facing runbook. The habit that caught it is
mechanical — drive the thing, do not quote the note.

### One judgment call about file endings, deliberately narrow

The figure set includes a one-line file holding the menu's SHA-256. Windows checkouts of this
repository convert line endings, so I checked what a fresh clone would do to each new file rather
than reasoning about it:

| file | working tree | fresh checkout | identical |
|---|---:|---:|---|
| `verification_bundle.sha256` | 65 B | 66 B | **no** |
| `verification_bundle.json` | 340,741 B | 340,741 B | yes |
| `soften_link_2.png` | 450,826 B | 450,826 B | yes |

So a reader who regenerated the set and compared the digest file byte for byte against the tracked
one would see a difference the figure set does not have. I pinned that one file pattern to fixed
line endings in both `.gitattributes` files, wrote the measurement into the packet's own file, and
re-measured: identical.

I flagged this to Codex explicitly, because Codex ruled in Session 128 that no line-ending pin be
added for the Python modules. That ruling stands and I did not contest it — it rested on the
premise that nothing in the packet hashes those files at runtime, which is true of the modules and
not true of a file whose *content is a digest* that the runbook I wrote in the same session tells a
reader to compare. The JSON files carry no line breaks at all and the PNGs survive because Git
treats them as binary, so neither is pinned; pinning what does not move would be exactly the
needless enlargement Codex's ruling refuses.

### An environment fault that was not ours, and the correction it owed

Sessions 128 and 129 both recorded that the packet's full test-suite count was unmeasurable,
because MuJoCo — the physics engine the project runs on — could not load. A Repair Agent Randy
authorized for the machine problem diagnosed it to root cause: Windows Smart App Control had
refused an unsigned binary for about two hours after a Windows update, and then Microsoft's
reputation service cleared it. Nothing in the project was wrong and nothing needed repair.

The correction that owes is a number. The degraded counts Sessions 128 and 129 published (1,328
and 1,344) are honest measurements of a broken environment and worthless as measurements of the
suite. I re-measured at this session's exact checkout rather than adopting the figure I was given:
**2,267 passed, 0 failed, 0 collection errors**, which matches both the Repair Agent's and Codex's
independent runs. That number now travels; the degraded ones do not. The dated documents that
recorded them are left standing, because they are append-only records of what was true when
written.

---

## Decisions I made this session

1. **Seed 7 for the tracked figure set** — the seed the module's own docstring names and both test
   files pin. Using anything else would have created a second canonical fixture with no reason.
2. **Ten files tracked, not four.** The design specifies a machine-readable scene record beside
   each figure and the complete menu beside the set, so any figure in any later report can be
   traced to the exact scene and the exact menu that produced it. It costs about 2.4 MB; the
   traceability is the point of the artifact.
3. **The runbook writes to a separate directory.** Step 32 sends output to
   `results\verification_fixture_reproduced\` so a reader diffs against the tracked set rather than
   overwriting it, and that directory is ignored, like the packet's other reproduction outputs.
4. **The public log entry goes now, not at Step 3's approval.** Codex ruled in Session 127 that the
   milestone worth a stranger's attention is the *reviewed working* surface. That closed this
   session. The entry says plainly that the figure set and runbook step are with Codex for review
   rather than approved.
5. **The boundary correction is appended, not edited.** The packet's historical boundary paragraph
   says it "does not yet implement the confirmatory experiment or the interactive verification
   artifact." I appended a dated paragraph recording that the second half is now superseded and the
   first half is not, rather than rewriting the original sentence.

---

## Verification — what was measured, at this exact checkout

```text
focused Slot-8 suite                159 passed, 31.70 s
focused Slot-8 under python -O      159 passed, 32.71 s (one expected pytest -O warning)
packet-wide suite                   2,267 passed, 0 failed, 0 collection errors, 221.38 s
figure set rendered twice           10 files, 0 byte-differing
canonical bundle sha256             3bf51e94...5459d70  (unchanged from Sessions 128 and 129)
PNG resolution                      pHYs 11,811 px/m both axes = 300 DPI; IHDR 3,600 x 2,550
roles subcommand driven             X_CONNECTION_UNAUTHORIZED, exit 3, no directory created
fresh-checkout behaviour            measured per file with git checkout-index (table above)
runbook Step 32 run as written      exit 0, all ten files byte-identical to the tracked set,
                                    and its output directory correctly ignored
```

The bundle digest being *unchanged* is the load-bearing one. Codex's four Session-128 repairs and
my Session-129 test addition changed what the menu displays and what the two surfaces refuse; a
moved digest would have meant the underlying data moved too, which would be a different review.

---

## Files created or updated

**New (all ten, the tracked figure set):**
- `Reproducibility Packet/results/verification_fixture/verification_bundle.json` and
  `verification_bundle.sha256`
- `Reproducibility Packet/results/verification_fixture/{soften_link_2, weaken_actuator_1,
  bias_encoder_1, indistinguishable_softening}.{png, json}`

**Updated:**
- `Reproducibility Packet/README.md` — runbook Step 32 and a dated *Current boundary* paragraph
- `Reproducibility Packet/.gitattributes` and `.gitattributes` — the measured line-ending pin
- `Reproducibility Packet/.gitignore` — ignore the Step-32 reproduction directory
- `README.md` (repository root, the public Live-Run README) — one appended log entry, banner date
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — the Step-3 handoff
- `chats/Claude-Codex-Human/Transcript Order Monitoring/… - Active.md` — the monitor's
  independent confirmation
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`, and this report

**Not touched:** the four approved Step-2 blobs, every protocol document, every result artifact,
and `director_requests.md` (Codex committed the Repair Agent's append in its own session).

---

## Next steps

1. **Codex reviews the Step-3 state** — the ten figure-set files, the packet README, the two
   `.gitattributes` files and the packet `.gitignore`. If it edits or blocks, the owner re-review
   is mine and comes first.
2. **When that loop closes, Step 3 is done and Slot 8 has three of its four steps behind it.**
3. **Step 4 — connecting a real result — remains separately blocked** and cannot begin. Three of
   its inputs do not exist by governing decision: no frozen configuration, no selected capacity or
   checkpoints, and no calibrated abstention or unknown thresholds. It needs its own connection-
   record design, its own exact-state review, and its own joint authorization, none of which
   exists or is being sought.
4. **My next regular progress report is Session 136**, or sooner if a phase transition or an
   approved Claim Sheet amendment fires.
