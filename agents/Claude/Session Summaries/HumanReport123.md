# Human Report — Claude Session 123

**Current date and time:** 2026-08-12 00:18 PDT

## Summary

Two things happened this session, and the second is the one that matters for where the project
goes next.

First, I closed the project's one open review loop. Codex's Session-122 review of the public
README found a real defect in the entry I published in my Session 122 — my closing sentence was
literally broader than the record — appended a scope correction rather than rewriting my entry,
and approved the resulting state. I re-opened the file, checked the diagnosis and the
implementation separately, verified every published identity on disk rather than accepting the
handoff, and **explicitly approved Git blob `f00ea0d9`**. Both approvals now name the same bytes.
The public-heartbeat loop is closed.

Second — and this is the session's real work — Codex answered the direction question I put to it
in Session 122. Nothing scientific was open, and I had asked which of three lanes the next
sessions should spend themselves on. It ruled **Slot 8 first, then the Technical Report**, and
attached a hard boundary: the first Slot-8 object must be a *contract and synthetic scaffold*, not
a demo that presents the current development record as the project's result. I accepted that
without contest and wrote the first object:
**`Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md`**, blob `260e2042`,
29,089 bytes, handed to Codex for review with my explicit approval.

Slot 8 is the director's hands-on verification path — the artifact that lets Randy check the
result without reading the Technical Report end to end. It is a named completion requirement, and
until this session it was **the one such requirement with no object at all**.

The session spent zero fits, zero rollouts, zero simulations, zero analyzer invocations and zero
pilot/validation/test reads.

## What was accomplished

### 1. Owner re-review of the public README — loop closed at `f00ea0d9`

Codex's Finding BQ said my Session-122 closing sentence — *"Nothing is frozen, the final test set
remains untouched, and no research question has been answered"* — was, read literally, broader
than the record in two of its three clauses. It is right:

- **"Nothing is frozen"** is false as written. Protocol P v2.3.3, the capacity-escalation design,
  the rung-2 escalation design, the payload-boundary extension, schema v1.0 + A1 and both applied
  interpretation states are all frozen. What I meant is that no *capacity, probability threshold,
  abstention threshold or final configuration* has been selected — which is what the correction
  now says in the log.
- **"no research question has been answered"** is true only of the project's central Claim-Sheet
  question; narrower build and measurement questions have been answered by the development record.

I did not simply accept BQ's set. I checked the third clause myself: **"the final test set remains
untouched" is exactly true** (0 identities, 0 payloads), so two is the complete set of
overbreadths rather than a sample of them.

On the implementation: Codex appended a dated successor entry instead of editing the entry that
went stale. That is the standing rule on this file, and it is the rule I would have applied
myself. What I verified rather than read:

```text
diff 964231a4 -> f00ea0d9      +2 / -0, zero deleted lines; prior blob is a byte prefix
forbidden interpretive tokens  because 0 / therefore 0 / confirms 0 / which shows 0 /
                               resolves 0 / capacity-bound 0 / trend 0 / cause 0
typography vs the file         curly-quote pairs 7 -> 9 (the file already carried 7);
                               unspaced em dashes 6 -> 7 (the file already carried 6)
```

So the correction introduces no interpretive language and no new typographic convention. I accept
both the diagnosis and this implementation of it, and I approved the exact bytes.

All four identities Codex published reproduce on disk: blob `f00ea0d9`, canonical-LF sha256
`3e22e429…` at 150,506 B / 212 LF / 0 CR, working-tree raw `ede9e505…` at 150,718 B / 212 CRLF.
The `git hash-object --no-filters` value is a third number (`89d9fcac…`) that is nobody's identity
— I record it precisely so a later session does not mistake it for one.

Codex also reported against itself that its patch mechanism temporarily left five LF-only line
endings near the insertion, and that it mechanically restored the file's uniform CRLF working-tree
form. I measured the result instead of accepting it: 212 CR, 212 LF, 212 CRLF — uniform, no mixed
remainder — and the filtered blob unchanged. Repaired correctly.

### 2. Independent reproduction of Codex's result audit

Codex published an audit table it derived without importing any project module. I re-derived all
of it from the analysis artifact under a digest refusal (the script refuses unless the raw sha256
equals `604d7272…`), and every figure reproduces:

```text
rung-2 non-zero F1     healthy 0 / actuator 6 / sensor 10 / structure 0
sensor-only arms       C1 seeds 0,4; S seeds 0,3   (all four exactly at the majority baseline,
                                                    accuracy 0.631579 / macro-F1 0.193548)
actuator+sensor arms   C1 seeds 1,2,3; S seeds 1,2,4
rung-1 anchor non-zero healthy 8 / actuator 10 / sensor 10 / structure 10
paired macro sign      negative 2 / zero 1 / positive 2 = MIXED
parameter ratio        219018 / 39594 = 5.531596
```

The arm-by-arm partition is a decomposition Codex published for the first time this session — it
names *which* arms are which — and it is exactly right. It is also consistent with the coarser
statement both agents had already approved.

### 3. Transcript-integrity check — clean, so the monitor got nothing

I re-ran the monitoring thread's own checks against primary objects. The first 2,094,915 bytes of
the Phase-2 transcript reproduce my Session-122 post-write digest `386b1433…` exactly; Codex's
suffix is 5,588 bytes carrying 104 LF and **zero CR**; its session header occurs once in the whole
file; the commit delta is `+104/-0`. **No fault occurred, so I appended nothing to the monitoring
chat.** A clean check is not a reason for an entry — that is the standard the thread has run under
since Session 113, and it is why the thread has stayed short enough to be read.

### 4. The Slot-8 design document — the session's substantive output

`Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md`, blob `260e2042`,
raw == canonical sha256 `abff8af8…`, 29,089 B / 465 LF / 0 CR, LF-pinned by the packet's
`.gitattributes` rule for `protocol/*.md`.

**The problem it starts from.** Slot 8 commits the agents to build an interactive side-by-side
demo: the director picks a body change from a short menu, watches two copies of the robot run the
same task — one on the conventional sensor suite, one on the structural suite — and reads each
copy's fault call, confidence (or honest abstention), and tracking-error trace. That artifact
cannot be built at its final form today, and the reason is not effort. Three of its four inputs do
not exist:

| Slot 8 needs | current state |
|---|---|
| a frozen `config.json` naming the run being shown | absent by governing decision |
| a selected capacity and its fitted checkpoints | undecided — nothing has been selected |
| calibrated abstention and unknown/OOD thresholds | undecided, validation-owned, gate shut |
| a rendering mechanism | does not exist |

Only the fourth is available. A demo built now would have to either invent the first three or
silently adopt whatever the development record happens to contain — and the second is the more
dangerous, because a development artifact rendered in a finished-looking demo reads to a
non-specialist as the project's result. Our development record currently contains a rung-2 arm set
that scores exactly zero on two of four classes. Presenting that as a finding would be a
misrepresentation, and the document exists to make it structurally impossible rather than merely
discouraged.

**What it specifies instead.** The interface between the scientific record and the two
presentation surfaces, plus a synthetic fixture that drives that interface end to end with no real
number in it. The design test I wrote it against, and the one I asked Codex to hold it to:

> When the scientific inputs finally exist, connecting them must be a data change and an
> authorization — not a rewrite of the demo.

**The shape.** One object and two pure renderers. `VerificationScene` is the complete, serializable
description of exactly one side-by-side comparison. A single builder is the only code permitted to
touch a role, a checkpoint or a config. The interactive view and the scripted 300-DPI figure path
are both functions of a scene and nothing else; a renderer that opens a file is a defect. Slot 8's
own words are that the scripted version produces *"the same comparison"* — and sameness has to be
a single source, not a property maintained by hand across two code paths, or the first divergence
between them will be silent and will land in a published figure.

Three design points I expect Codex to press on, and which I flagged as such:

1. **The scene carries the schema's own structs, not translations of them.** The per-decision
   block renders the schema's `estimator_outputs` fields verbatim, and the tracking block carries
   *precisely* the arguments the project's headline tracking metric takes. That makes the panel
   the director reads and the number the Technical Report reports provably the same quantity,
   because the plot and the metric take the same inputs.
2. **Provenance is computed from the inputs, never supplied** — a caller-supplied provenance label
   is a label that can lie. Three states (`SYNTHETIC_FIXTURE`, `DEVELOPMENT_ONLY`, `FINAL`);
   anything else is a refusal with its own exit code and no scene is produced. `FINAL` is currently
   unreachable — the only config hash in the packet is `dev-712abf27…` — and an invariant requires
   a **test asserting it is unreachable**, so the day that changes the suite goes red and the
   decision has to be taken deliberately rather than noticed afterwards.
3. **No cross-arm derived number appears anywhere this round.** Both arms' quantities sit side by
   side, which is exactly what Slot 8 asks for, but no C1-minus-S difference, ratio or reduction
   is emitted. A single reduction figure rendered under two robots reads as a headline, and the
   confirmatory comparison that would license one has not been run.

The fixture has to render the *unflattering* branches or it is not a fixture: a confident wrong
call, an abstention, a high unknown score, and **at least one scene in which the two arms are
indistinguishable**. Slot 8 names that outcome by name — "the honest negative shown *as* a result"
— and a demo that cannot draw it is a demo that can only show a win.

Fourteen invariants, each stated as a refusal a test can fail rather than as a behaviour. Codex's
six bounds are quoted verbatim and mapped one-to-one to the section and invariant that discharges
each, so the reviewer can check the mapping instead of taking it on trust.

## Challenges, and how they were handled

### The honest tension in Slot 8, and where I put it

Slot 8's entire purpose is a *comparison* between the two sensor suites, and this project's
scientific gates forbid saying anything about C1 versus S. Those two facts pull against each
other, and the pull is real rather than a technicality.

I resolved it by separating *showing two things side by side* from *emitting a number that
compares them*. The first is what Slot 8 contracts and what the director actually needs; the
second is what would smuggle a conclusion into a picture. So the design shows both arms fully and
emits no cross-arm scalar at all, enforced by an invariant rather than by care. I deliberately did
**not** rule on whether such a number appears later, once a real result is connected — that
belongs to whatever authorization connects it, and I handed the question over rather than settling
it quietly in a design document.

### Design first, or design and module together?

Codex's ruling said "contract and synthetic scaffold," which can be read as one round producing
both. Every prior lane in this project froze a design before building anything, and I followed
that — but I flagged the ambiguity as an explicit handed-over decision rather than assuming my
reading. My argument for splitting: the field table and the no-cross-arm-number rule are cheap to
contest in prose and expensive to contest after a module and its tests exist. If Codex reads its
own ruling as one round, I will build both next session.

### Choosing the smallest sufficient surface

The interactive requirement invites a web viewer. I chose `matplotlib.widgets`, with the scripted
path being the same code under a non-interactive backend, because matplotlib is *already pinned*
in the packet and this therefore adds **no dependency at all**. A browser stack would cost the
packet a build step and a whole class of "it doesn't run on my machine" that the fresh-environment
validation exists to prevent. That is the Efficiency standard applied to a presentation artifact
rather than to a model, and it is the load-bearing dependency choice in the document — so I named
it as the one most worth contesting now rather than after the build.

## Insights

- **The deferral shape keeps paying.** Sessions 118–121 each declined to publish the rung-2
  heartbeat for a written reason with a named trigger, and Session 122 published without having to
  reconstruct why it had been waiting. This session's equivalent is the handed-over decision list:
  four questions written down with my leaning and my reasoning, so the next session does not have
  to re-derive why they were open.
- **A correction can be right and still need checking on both axes.** BQ's diagnosis and BQ's
  implementation are separate questions, and the review-cycle playbook is explicit that accepting
  the first while silently swallowing the second is a real disagreement in disguise. I checked
  them separately and accepted both — but I checked the third clause of my own sentence
  independently, which is the part that turns "the reviewer is right" into "the reviewer's set is
  complete."
- **I walked into my own documented trap again.** My first derivation script crashed on
  `arms[].classification.per_class_f1`. That path is a *template string* the artifact carries to
  name where a value came from — not the shape of the array — and my own continuity file records
  that in capital letters from one session earlier. It cost nothing because it raised loudly, which
  is precisely the argument against writing a tolerant accessor (`.get()`, a try/except fallback)
  over an artifact you did not write: a tolerant accessor would have returned a wrong number
  silently, and this project publishes what those accessors return.

## Files created or updated

- `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md` — **created**; the Slot-8
  interface contract and synthetic-scaffold design, blob `260e2042`, open on Codex for review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my owner re-review and approval of `f00ea0d9`, the independent audit reproduction, and
  the Slot-8 handoff (`+170/-0`, zero deleted lines, zero CR added).
- `agents/Claude/README.md` — updated the root-README bullet to its closed state and added the
  Slot-8 design bullet.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 124.
- `agents/Claude/Session Summaries/HumanReport123.md` — this report.

No code, checkpoint, result artifact, packet runbook or configuration was changed. The root
`README.md` was not touched this session.

## Verification and resource boundary

- Codex's four published README identities reproduced on disk; the `+2/-0`, zero-deleted-lines
  property verified at the Git level.
- The rung-2 audit figures re-derived from the analysis artifact under a digest refusal, importing
  no project module for the derivation.
- Transcript prefix, suffix-CR, header-uniqueness and additions-only checks all passed;
  `git diff --check` clean.
- Packet test suite collected at **2,108**, unchanged (35.80 s, collect-only).

Zero fits, checkpoints, rollouts, generation runs, analyzer or C7 invocations, plan-mode
invocations and pilot/validation/test reads. Checkpoint count unchanged at 67. Both rung-2
authorizations remain spent; both section-5.4 applications remain closed and spent; no
configuration was frozen or drafted.

## Next steps

1. **Codex reviews the Slot-8 design at blob `260e2042`** — approving those exact bytes or handing
   back edits. If it edits or blocks, the owner re-review is mine.
2. **It should rule on the four handed-over decisions**, and D1 in particular: whether its own
   Session-122 ruling means one round or two. If one, I build the module and its tests next
   session instead of waiting.
3. Once the design loop closes: build `verification_scene.py`, the renderer, and the tests
   carrying the fourteen invariants, then generate the fixture figure set and add the packet
   runbook step.
4. After the Slot-8 scaffold loop closes, begin the Technical Report as an evidence map and
   section scaffold — Codex's stated order, which I accept.
5. My next regular progress report is **Session 128**, unless a phase transition or an approved
   Claim-Sheet amendment fires sooner.
