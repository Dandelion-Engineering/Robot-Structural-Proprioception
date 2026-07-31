# Human Report — Claude Session 49

**Current date and time:** 2026-07-31 12:16 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review of the executed Stage-0 result artifact and of Codex's
reviewer edits to my Session-48 progress report; writing the Stage-0 runbook step into the
Reproducibility Packet

**Final config state:** **UNFROZEN**; no final `config.json` exists

**Protocol-P execution state:** Stage 0 has run **exactly once** and its result artifact is
now **jointly approved at the same exact file state** — the review loop is CLOSED.
**Protocol-P plant rollouts spent: still ONE** (the Session-45 replay); Stage 0 costs zero.
Stage 0 was **not** re-executed this session. Stages A/B/C remain unauthorized and unbuilt.
The confirmatory test split remains untouched.

---

## Summary of what was accomplished

Four things, in order:

1. **Independently re-verified and then explicitly approved the Stage-0 result artifact**,
   unchanged, at its exact committed state — closing the loop Codex correctly refused to
   close by inference.
2. **Found and recorded a scope narrowing on the artifact's identity**: it binds the run's
   *inputs and output shape*, not its measured values. Established by construction, not by
   reading. This is a documentation boundary, not a defect.
3. **Edited and returned my Session-48 progress report.** All three of Codex's corrections
   were right, and I kept every one — but two of the same claims survived elsewhere in the
   file it edited, in a director-facing artifact. I fixed those and handed the state back.
4. **Wrote Step 24 of the packet README** — the Stage-0 runbook step, deferred three times,
   whose remaining condition (Codex's review of the result) was met this session.

---

## 1. The owner approval, and how I earned it rather than asserted it

Codex's Session-48 review approved the Stage-0 artifact unchanged as reviewer, but refused
to treat my Session-48 result turn as owner approval. It was right to: under the review
cycle, creating an artifact, self-auditing it, and handing it off are three things, and none
of them is approval. Approval is never inferred.

The risk in that situation is that the owner re-review becomes a formality — re-read the
reviewer's audit, agree, sign. That produces the same word with none of the evidence.

So I recomputed the distribution by a route neither of us had used. My Session-48 self-audit
and Codex's Session-48 audit both went through NumPy, which is also what produced the
result. This time I used **pure Python** — the standard-library `statistics` module and
hand-indexed order statistics, no NumPy anywhere:

```text
n = 100, all values finite and nonnegative, 100 distinct values (no ties)
ceil((n - 1) * 0.95) = 95  ->  0-based index 95  ->  the 96th ordered value
  s[95]                        0.4008810868833315   == reported q95    EXACT
  count strictly above q95     4
  count at or above q95        5
  median / min / max           EXACT match
  statistics.pstdev            0.0747731492497055   == reported std    EXACT
  statistics.stdev (sample)    0.075149842561975    != reported std
  statistics.fmean             0.27873430387016523  vs reported 0.2787343038701652
                               -> 1 ULP apart; np.mean reproduces the reported value exactly
```

Two things fell out of that which are worth having on the record. The reported `std` is the
**population** standard deviation, not the sample one — the artifact does not say which, so
a reader could not have told, and Step 24 now says it. And the only non-exact agreement in
the entire distribution is a one-unit-in-the-last-place difference on the mean between two
different float summation orders, which is a property of floating-point addition rather than
of the artifact.

I also re-derived both text-domain digests from the files themselves (`5689dad7…` for the
protocol, `76255a80…` for the assignment), recomputed the identity from the artifact's own
650-character canonical string, and ran the full packet suite at HEAD: **595 passed in
12.23 s**.

Codex's order-statistic correction — that 5 values are at or above the reported figure and 4
exceed it, rather than "only 5 in 100 exceed it" — is correct, and so is its stated reason.
I checked both halves separately, per the lesson from Session 48 that a reviewer's correct
fix and a reviewer's correct reasoning are separable claims.

**Approved, unchanged, at git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`.**

## 2. The finding: the identity certifies the inputs, not the numbers

The Stage-0 artifact carries a cryptographic identity, `stage_0_identity`, recomputable from
a canonical string the file also records. It would be natural — and wrong — to read that as
a tamper seal on the file.

I established what it actually covers by construction rather than by reading the
specification and reasoning about it. In memory, I set one recorded distance to `999.0` and
the headline 95th percentile to `0.05`, left the `inputs` block untouched, and re-applied
the identity rule and the production validator:

```text
tampered artifact still satisfies identity == dev- + sha256(stage_0_canonical)   TRUE
require_valid_stage_0_identity(tampered)                                        ACCEPTS
canonical key set: assignment_canonical_sha256, assignment_hash, base_config_hash,
                   cli, output_schema, protocol_spec_sha256, stage
```

The canonical payload contains the stage label, the base configuration hash, both assignment
digests, the protocol digest, the seven pinned command-line values, and the sorted list of
top-level output keys. It contains **no measured value**.

**This is not a defect.** The protocol's Correction 6 pins exactly that seven-key payload,
and the only claim the specification makes for it is that the digest is independently
recomputable from the artifact alone — which is true, and which I re-measured. What the
finding changes is what may be *written* about it: `stage_0_identity` is a provenance
identity over the run's inputs and output shape, and it is not a seal over its results. Two
files with identical inputs and different numbers carry the same valid identity.

This is the third object in this project whose name promised more than its mechanism
delivers — invariant I8 guards the code rather than present-day data, and both
configuration-binding guards defend the code rather than the data. The consistent shape is
that **our provenance objects certify what went in**, and the write-up has to say so. It is
now recorded as a carried limitation, and Step 24 states it in those terms for an outside
reader.

I deliberately did not propose a protocol change. Adding the result to the identity payload
would mean editing an approved specification to solve a documentation problem, and the
project's version discipline exists precisely to stop that from happening casually. I said
so explicitly and handed the judgment to Codex rather than settling it alone.

## 3. Edit and return on the progress report

Codex made three corrections to my Session-48 director progress report and explicitly
approved its edited state. All three were right, I verified each against the artifact rather
than accepting them, and I reverted none of them:

- "noise floor / any smaller signal is invisible" → the actual no-threshold boundary. The
  artifact's `authority` field reads literally `NONE`, and the operative null for the
  screen's verdict is Stage C's per-cell figure, which has not been measured.
- "two routes agree" → broad-range containment. Confirmed: the value exceeds three of the
  four real-plant cells.
- "only 5 in 100 exceed it" → 5 at or above, 4 exceeding. Confirmed numerically above.

**What the re-review found is that two of those same claims survived elsewhere in the file
Codex had just edited.** It corrected the section that introduces Stage 0 and corrected the
public log for calling the binding gate a safety check, but inside the report itself:

```text
line 198        "Stage 0 measures the noise floor; it deliberately decides nothing."
lines 158-159   "break the security check  ->  ..."      (the mutation-sweep table)
line 172        "...a claim about a safety check that the code does not actually perform."
```

The first is the exact phrase the earlier edit removed forty lines above it. The second and
third are the exact miscategorization the public correction names — and "safety" is a
load-bearing technical word in this project, attached to the A1 envelope, the seven-flag
safety array, and the Stage-A gates. A director reading "safety check" in a robotics report
will read it as physical safety. What was actually broken in that mutation sweep is the gate
that ties the program to its approved input files: an integrity check on inputs, not a check
on whether a motion is safe.

A correction pass that fixes a heading and leaves the same claim standing in "What isn't
working" has not corrected the record the reader actually reads. So I edited and returned
rather than approving:

```text
agents/Claude/Progress Reports/Progress Report Session 48.md
  reviewer state Codex approved   36ba0221540582b04f7f35029f7a38f3649a60ff
  my returned state               f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f
  owner diff                      +9 / -4
```

That loop is now open on Codex's side. It is separate from the result-artifact loop, which
is closed.

## 4. Step 24 — the Stage-0 runbook step

This step had been deferred three times, each time for the same reason: a runbook step
should describe a step that has been executed **and reviewed**, and until this session the
result had not been reviewed. That condition is now met.

```text
Reproducibility Packet/README.md
  HEAD blob   516348935e2ce0d400be255aac08cb83b3eac242
  my state    e525c7bea92eb259f62368b75c5ecb950e5fd370      +37 / -1
```

Step 24 carries the pre-registered seven-flag invocation, the recorded result, the zero
rollout cost, and four boundaries drawn from the artifact itself: it sets no threshold, so a
smaller signal is not thereby invisible; its corroboration is upper-tail containment and
explicitly not agreement; its `dev-` prefix makes it permanently ineligible for confirmatory
analysis; and its identity binds inputs and schema rather than numbers.

It leads with the contrast against Step 23, because the two Protocol-P steps have **opposite
reader-reproducibility status**. Step 23 cannot be run from the distributed packet — it needs
the retained development dataset and one MuJoCo rollout. Step 24 needs neither a dataset nor
MuJoCo and runs end to end on a clean checkout after Step 1. That makes it the first
Protocol-P step an outside reader can actually execute, which is worth saying plainly rather
than leaving for them to discover.

Two reader traps are named: `len(samples)` returns 6, not 100, because `samples` is a
metadata dictionary whose `distances` key holds the values (this looked briefly like a
catastrophic sample-count defect in Session 48 and was not); and `std` is the population
standard deviation. And it refuses to claim cross-platform bit-identical output, because we
have not measured that — it states determinism given the pinned seeds and pinned dependency
versions, and tells a reader to compare against the recorded values.

One line outside Step 24, in the packet's **Current boundary** section, records that the
replay gate has passed and Stage 0 has executed once at zero rollout cost with no authority
over any verdict, while Stages A/B/C are unbuilt and unauthorized.

Step 24 is handed to Codex for review; it is not approved yet.

---

## Challenges, and how they were handled

**The main risk this session was ceremonial approval.** Codex had already audited the
artifact thoroughly and found it correct. The path of least resistance was to read that
audit, agree, and sign. That produces an approval with no independent evidence behind it,
and it is exactly the failure the review cycle is built to prevent. The remedy was to pick a
verification route with no shared machinery — pure Python instead of NumPy — so that an
error in the producing library could not hide inside the check.

**The second was knowing when a finding is worth a round and when it is not.** I found two
things this session. The identity-scope narrowing changes no shipped behaviour and no
number, so under the rule the project settled last session, I recorded it and approved. The
surviving "noise floor" and "safety check" phrases in the progress report *do* change what a
director reads, in the artifact whose whole purpose is to keep the director able to judge the
work, so I edited and returned. The distinction that decided both was not severity in the
abstract — it was whether leaving it alone would leave a false claim in front of a reader.

**Elapsed time.** Codex found that the first-run wall clock was promised in Session 47 and
never captured, and that it cannot honestly be reconstructed. I agree, and I did not re-run
Stage 0 to manufacture a figure. One narrowing for exactness: my private summary of
necessary context does carry an informal "≈7 s" note in a timings list, but I can no longer
distinguish whether that was measured on the authorized execution or estimated from a
two-pair test run, and an approximation of unknown provenance is not a measurement. Step 24
therefore records `first-run elapsed time: not captured`, notes that an informal
order-of-magnitude figure exists and is not being quoted as a measurement, and requires any
later timing to be labelled a separately authorized reproduction.

---

## Important decisions

1. **Approve the result artifact unchanged**, after independent re-derivation rather than
   after reading the reviewer's audit.
2. **Record the identity-scope narrowing rather than propose a protocol amendment.** Editing
   an approved specification to fix a documentation problem is the failure mode version
   discipline exists to prevent; the judgment was handed to Codex explicitly.
3. **Edit and return the progress report** rather than approve it with two of the corrected
   claims still standing in it.
4. **Write Step 24 now**, since its stated blocking condition was met, rather than defer a
   fourth time.
5. **Do not re-execute Stage 0** for any reason, including to obtain a timing figure.
6. **Do not reopen any earlier dated public log entry.** Codex's forward correction is the
   right mechanism and remains the operative record; corrections propagate forward.

---

## Reasoning paths explored

- **Whether the identity gap was a defect worth blocking on.** Traced to the specification:
  Correction 6 pins exactly the seven-key payload the implementation writes, and its only
  claim is recomputability from the artifact alone, which holds. The gap is between what the
  mechanism does and what a reader would assume from the phrase "artifact-level identity" —
  a write-up boundary, not a code or specification error.
- **Whether "security check" was worth changing.** On its own it is defensible; an integrity
  check is a kind of security check. It was changed because it sits three lines from a
  "safety check" that is not defensible, in a project where "safety" names a specific
  physical envelope, and leaving one of the pair would have preserved the confusion.
- **Whether to publish a public log entry this session.** The bar is a finished artifact, a
  closed phase, or something genuinely noteworthy. The result artifact reaching joint
  approval is a finished artifact, and the identity finding is a concrete, checkable instance
  of a verification object protecting something narrower than its name. Both clear it.

---

## Insights gained

1. **A provenance identity has a scope, and the scope is the claim.** Three objects in this
   project now protect something narrower than their names suggest. The pattern is not
   carelessness in any one case — each was specified correctly. It is that names travel into
   write-ups faster than mechanisms do.
2. **When you re-verify someone else's verification, change the instrument.** Recomputing
   with the same library the producer used checks arithmetic; recomputing with a different
   one also checks the library. It cost about a minute here and produced two facts the
   original audit did not surface.
3. **A correction pass has a completeness question of its own.** The right question after a
   reviewer corrects a claim is not "is this correction right" but "does this claim appear
   anywhere else in this artifact." Two of three did, and a search took seconds.

---

## Files created or updated

**Created:**
- `agents/Claude/Session Summaries/HumanReport49.md` — this report.

**Updated:**
- `Reproducibility Packet/README.md` — **Step 24** (the Stage-0 runbook step) plus one
  sentence in *Current boundary*. `+37 / -1`. Handed to Codex for review.
- `agents/Claude/Progress Reports/Progress Report Session 48.md` — three owner edits
  propagating Codex's own corrections to their surviving instances. `+9 / -4`. Returned to
  Codex for re-review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-49 turn, appended at the physical tail. `+190 / -0`, header once at line
  10,999, after the recorded 10,995 boundary.
- `README.md` (root, the public Live-Run page) — banner date to 2026-07-31, plus one running
  log entry: the result is jointly approved, re-derived without the original's numerical
  libraries, and the identity does not seal the numbers.
- `agents/Claude/README.md` — workspace guide brought current.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten, as every session.
- `.gitignore` — `.agent-session.lock` added to the agent coordination lock-file block.

**Deliberately not touched:** the Stage-0 result artifact; the Stage-0 implementation and
its tests; the three approved helper and detection-floor files; the replay gate; the protocol
file; the assignment; the draft configuration; `.gitattributes`; any payload; the test split.
No new dependency.

---

## Next steps

**Codex owns the next two turns:** re-review of the returned progress report (blob
`f01aa7d7…`) and first review of packet README Step 24 (blob `e525c7be…`). It may also give
a read on the identity-scope narrowing, though nothing is blocked on it.

**Then, in order:** the Stage-A/B/C driver, which must be handed off and approved at an exact
state before any execution, and which has to satisfy Codex's six enumerated fail-loud
requirements plus the accumulated driver constraints; Codex's review of that implementation,
its result, and its branch; the written Amendment A2 and a replacement assignment approved by
both agents; full regeneration of the dataset from zero; re-audit; then the Gate-4 model and
calibration work, the two remaining data roles, the controller protocol, the joint immutable
configuration freeze, and finally the one-shot confirmatory generation and evaluation.

**Progress report cadence:** the regular Session-48 report is done. The next regular one is my
Session 56, unless a phase transition or an approved written Claim-Sheet amendment fires
first.
