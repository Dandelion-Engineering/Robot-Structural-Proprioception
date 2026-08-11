# Progress Report — Codex, Session 112

**Written:** 2026-08-10 19:14 PDT
**Covers:** my Sessions 105–112 (previous regular report: Session 104)
**Phase:** 2 — Execution, with limited Phase-3 packet assembly
**Written for:** Randy

---

## The short version

The previous report ended with Stage 1 complete but deliberately inconclusive: five model sizes
and five random seeds did not support a readable curve. This eight-session stretch did not try to
force a stronger result out of that curve. It did three quieter things that determine whether the
next result will be trustworthy.

First, we tested whether the Reproducibility Packet really travels by itself. It did not. Its
runbook depended on files outside the packet for ignore rules and line-ending rules, and one
displayed recovery command could not do what its own prose promised. Those defects are repaired.

Second, we measured the precision of the Stage-1 instrument itself. At five seeds, the pooled
pointwise minimum detectable difference is **0.263**, while the project’s predeclared effect scale
is **0.05**. That does not make the Stage-1 result wrong. It means five repeats are much too coarse
for a 0.05 pointwise comparison under the measured dispersion. The exact calculation uses the
[noncentral Student-t distribution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nct.html),
which is the distribution needed to solve the stated 80%-power question rather than approximate
it.

Third, we decided not to deepen the current Stage-1 measurement. The authority for what happens
next comes from the Claim Sheet’s capacity ladder, not from a story about the unreadable curve.
Claude designed the literal second rung—a recurrent-plus-attention model about 5.5 times the size
of rung 1—and the two agents took that design through exact-state review. The design is now
jointly approved. It authorizes writing the model module and its tests, and nothing later.

No model fit, checkpoint, simulation, generation, rollout, plan execution, reserved-role read,
capacity choice, threshold, or final configuration was spent in these eight sessions.

## Three ideas that explain this stretch

### A packet is self-contained only if its rules travel too

The packet is supposed to survive being copied into a clean directory or published as its own
repository. That promise includes invisible repository rules. Git can normalize line endings when
files move between Windows and Unix; the official
[Git attributes documentation](https://git-scm.com/docs/gitattributes) explains how `text` and
`eol` rules control that behavior. If a packet authenticates a file by its raw-byte checksum but
the line-ending rule lives outside the packet, a clean Windows checkout can change the checksum
and make a correct verification command refuse.

The packet now carries its own `.gitignore` and `.gitattributes` rules. We verified the
line-ending repair in scratch repositories under both positive and negative conditions: without
the packet-local rule the schema fingerprint changes and validation refuses; with the rule it
stays stable and validation passes.

### Measurement resolution is not the same as a result

The Stage-1 precision note asks a planning question: given the disagreement across five seeds,
how large would a paired mean difference need to be before this five-repeat design had 80% power
to detect it?

The pooled answer is 0.263. Reaching a pointwise MDD near 0.05 under the same dispersion model has
a point estimate of 79 seeds, with a wide uncertainty range of 47–162 because the dispersion
estimate is itself based on little data. Those figures characterize pointwise development
precision. They do not measure curve-shape power, choose a model, or become confirmatory evidence.

The timing estimate has the same honesty boundary. The only recorded rate divides 439.594 seconds
of whole-invocation elapsed time by 42 attempted fits. It includes non-fit work and has no
per-width timing, so projected runtimes may be too high or too low. The approved table’s rough
estimate for extending all five widths to 79 seeds is **740 additional fits and about 2.15
hours**, not a guaranteed duration.

### A capacity ladder separates “nothing there” from “model too small”

Rung 1 is the existing temporal-convolutional network. Rung 2 adds a two-layer unidirectional
[GRU](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html)—a recurrent component that
carries state forward through the sequence—and a final-query attention pool that can weight
earlier moments in the window. It has 219,018 parameters versus rung 1’s 39,594.

Trying rung 2 does not prove that capacity caused the Stage-1 deficit. Architecture family,
parameter count, and optimization behavior all change together. It satisfies a narrower
commitment: before the project makes its later held-out C1-versus-S comparison, validation will
have more than one real model rung from which to select.

## What happened in Sessions 105–112

### 1. The packet runbook and portability controls closed

Session 105 found that the displayed “new run” command still authenticated the already-spent
`stage1-run-2` plan, so changing the visible label could not create the fresh run the prose
described. The runbook now shows the full fresh-plan sequence and states the harder limitation:
the approved sweep is bound to the exact original anchor checkpoints. A clean clone cannot
recreate those exact bytes merely by refitting.

The same review found that scratch-output ignore rules lived at repository root and would vanish
from a packet-only copy. Sessions 106–107 completed a destination census, added the missing sensor
model output directory, and installed the packet-local line-ending rules described above. Those
review loops are closed at jointly approved states.

### 2. The precision note needed four review rounds

Claude’s first note extracted the right paired dispersions but called a common central-t planning
approximation an exact 80%-power answer. Codex replaced it with the exact noncentral-t solution.
The review also separated pointwise precision from curve-shape interpretation, corrected a
candidate fit count, and narrowed a five-pair observation that had been generalized too far.

Claude’s owner re-review then found three more issues: a truncated confidence-interval constant,
an ambiguous pooled-SD definition, and a contaminated elapsed-per-fit denominator. Two repairs
held unchanged. The third initially called the contaminated rate an upper bound on future fit
cost; Codex corrected that because unmeasured wider models can be slower. Claude accepted the
same bytes in Session 110, closing the note.

The useful lesson is not that the note took four rounds. It is that nearly every defect was in a
number that looked cautious or familiar. “Conservative” is not the same as “supported.”

### 3. The design direction was decided separately from the curve

After the precision note closed, Codex ruled three questions:

1. do not add seeds into the preserved 32-channel anchor;
2. do not spend more seeds on the current Stage-1 in-sample statistic; and
3. build the literal rung 2 already named by Claim Sheet Slot 9.

That third decision is not an interpretation of the Stage-1 curve. The curve remains unreadable.
It is the next action required by a contract written before those points existed.

### 4. The rung-2 design is now closed at one exact state

Claude returned a zero-data, zero-fit design. Codex’s first review repaired seven blocking
contract defects: the source of authority, exact attention parameterization, architecture-versus-
size semantics, an overclaiming objective label, overlapping outcome rows, impossible refusal
persistence, and incomplete producer identity.

Claude genuinely re-opened that edited state, accepted all seven repairs, and added two narrow
clarifications. One makes the RNG order explicit: enter the fork first, seed inside it, then build
the parameters. The other distinguishes persisting a signed rung-to-rung primitive from asserting
a direction that the interpretation table never licenses.

Codex independently reproduced the RNG behavior and approved Claude’s exact returned blob. Both
agents now approve the same design state. The next licensed act is only the model module and its
tests, owned by Claude’s estimator lane.

## What was unexpected

- A packet that looked portable still depended on root-level rules invisible to a packet-only
  consumer.
- The five-seed instrument was about five times coarser than the project’s 0.05 effect scale.
- The stock PyTorch multi-head attention module would have added an output projection and silently
  produced 228,330 parameters while still sitting inside the declared rung-2 size band. The exact
  architecture count, not the band, is what catches the wrong implementation.
- An apparently harmless ordering phrase around random seeding admitted both the correct and
  incorrect construction. Both produced the same parameter shapes; only the caller-RNG invariant
  distinguished them.
- Claude’s new public entry called the 79-seed extension “a lunch break away.” That did not follow
  from the jointly approved note. Codex appended a public forward correction: the rough table says
  about 2.15 hours and 740 new fits, with uncertainty in both seed count and elapsed time. The
  decision not to run it is unchanged.

## What is working

- Exact-state review is catching specification defects before code makes them expensive.
- The packet’s portability claims are increasingly tested in packet-only copies rather than
  inferred from the full repository.
- The project preserves failed and superseded states rather than making the history look cleaner.
- Scientific interpretation, development measurement, code approval, plan approval, execution,
  and later-role reads remain separate gates.
- The design’s outcome table is an ordered partition: every terminal condition lands in one
  status branch, and only a fully successful run opens one sign description.

## What is not working or remains open

- The final configuration is still absent, and validation-owned capacity and thresholds remain
  undecided.
- Pilot, validation, and test outcome roles remain unread for capacity, threshold, and final
  claims.
- Fifty-five Git-ignored checkpoints still lack an honest clean-machine distribution or recovery
  path. Rebuilt checkpoints are new artifacts, not restoration of the authenticated originals.
- Claude must re-review Codex’s forward correction to the public README at the exact returned
  blob. This is a documentation loop only; it does not reopen the rung-2 design.
- `director_requests.md` entry 1—the director’s non-blocking Claim Sheet review—remains open.
  Nothing new is required from Randy for the technical sequence to continue.

## Verification artifact

The Slot-8 hands-on verification artifact did not change in this interval. Inventing an update
would confuse internal design closure with a user-visible result, so none is reported.

## What happens next

1. Claude re-opens and either approves or edits the public README correction.
2. Claude writes `scripts/utils/attribution_net_rung2.py` and its tests under the now-approved
   design. No executable or fit is implied.
3. The module/test state goes through its own exact-state review.
4. Only later, under separate gates, may the executable be built, plan mode run, execution
   authorized, the read-only analyzer built, and the terminal artifact interpreted jointly.

The important state is simple: the design is ready; the experiment is not authorized.

— Codex
