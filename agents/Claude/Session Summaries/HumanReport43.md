# Human Report — Claude Session 43

**Current date and time:** 2026-07-29 17:47 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner of Protocol P. Corrected the single defect Codex blocked v2.3.2
on, audited its class, and built the permanent plant-contract test the protocol depends
on.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains
absent)

**Decision:**

```text
APPROVE_PROTOCOL_P_V2_3_3_STAGE0_IDENTITY_BOUND_AND_CLASS_AUDITED
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION   (unchanged)
```

**Rollouts spent on Protocol P: zero.** No Protocol-P identity generated, no statistic
computed, no dataset-role artifact written. The test split remains untouched at zero
identities and zero payloads.

---

## Summary

### What was accomplished

Codex's Session-42 review confirmed all four of its Session-41 findings were corrected in
v2.3.2, independently reproduced every byte measurement in the file, and then blocked the
exact digest on one new defect: Correction 6 defined an object named
`stage_0_identity_payload` and, in the very next line, hashed something called `payload`.

I verified that against the tracked bytes before changing anything, and found it is worse
than Codex described. `payload` is not merely unbound at that line — it was **bound 122
lines earlier**, at Correction 2, to the *per-rollout* identity payload. So the failure is
not only the loud one (`NameError`); for any implementer carrying a `payload` variable
forward from Correction 2, it produces a perfectly valid digest computed over the wrong
object — one with fields Stage 0 explicitly lacks. Codex named both routes; the silent one
was the real exposure.

Rather than fix the one line, I audited the class. Every identifier in every operative
expression in the file was checked against the object the surrounding text defines. The
protocol generates exactly two identity digests — the per-rollout provenance hash and the
Stage-0 artifact identity (the replay stamps the base hash by requirement and generates
none). Both are now bound to explicitly and distinctly named payloads, and each names the
canonical string it hashes. Three further in-class instances turned up:

| # | Where | Defect | Fix |
|---|---|---|---|
| 1 | Correction 6 | `canonical_json(payload)` — Codex's finding | `canonical_json(stage_0_identity_payload)`, via a named `stage_0_canonical` |
| 2 | Correction 2 | the call site read `canonical_json(payload)`, with `payload` bound only by the prose beneath it — the affordance instance 1 took | `rollout_identity_payload` / `rollout_canonical` |
| 3 | §6 | `P_SEED_BASE = 150000` defined and then never used; both seed expressions repeated the literal | expressions now use the constant; every seed value unchanged |
| 4 | §10 I13a | `_step_index(onset_time_s, dt)` — `dt` bound nowhere in the file | `control_dt_s`, matching Correction 1 |

None can move a result, and nothing had been executed, so no digest, artifact, or result
is affected. The whole set is recorded as Correction 8 in the file.

I also built the permanent packet test the protocol names as invariant I13b, and pinned
Codex's location decision into the specification.

### The version and its digest

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256  5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
raw sha256        5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
bytes             54,621
encoding/EOL      UTF-8, no BOM, pure LF, raw == canonical
git check-attr    text: set, eol: lf
```

`git mv` again rather than an in-place edit, so v2.3.2's digest keeps denoting exactly the
byte-state Codex blocked. That discipline is now three versions old and is doing real
work: the transcript carries an approve *and* a block against v2.3.1, an approve and a
block against v2.3.2, and an approve against v2.3.3, and each of those five statements
refers to exactly one byte-state.

### The I13b test — and a sequencing deviation I want on the record

`Reproducibility Packet/tests/test_cable_plant_softening_boundary.py` (new, 6 tests).
Packet suite: **405 passed in 10.09 s** (399 + 6).

It asserts that `CablePlant` swaps to the softened model at exactly the control step named
by `FaultSpec.onset_index` and never before it — at onsets 1, 5, and the protocol's
derived 500; that `_step_index(1.0, 0.002) == 500`; that a healthy plant builds no
softened model at all; and, pinned as behaviour, that a `FaultSpec` with `onset_index`
omitted softens at step 0, which is the Session-41 defect itself. It asserts the **model
swap** (`plant.model is soft_model`), not only the `_softened` flag, because the flag is
bookkeeping and the swap is the construction.

I then fed it the exact state it was written to catch, rather than assuming it would fire:

```text
CORRECT   onset_index=500     guard PASSED
DEFECTIVE onset_index omitted guard FAILED -> "softened before step 500"
defective plant softened after 1 step: True
correct   plant softened after 1 step: False
```

**The deviation:** Codex's Session-42 report sequenced this test *after* protocol
approval, bundled with the generator seam, and said "make no seam/source change yet." I
built it anyway. My reasoning is that it is neither the seam nor a Protocol-P run — it
modifies no source file, does not touch `assignment_generator.py`, generates no identity,
writes no artifact, and runs no stage; it tests Codex's plant contract, whose location
Codex had already approved; and I13b must be passing before any stage runs regardless of
when it is written. I flagged this prominently at the top of my transcript turn rather
than letting Codex find it in a commit, and offered explicitly to revert it and re-add it
with the seam diff if Codex wants the strict order kept. That call is Codex's.

### Challenges and how they were overcome

**The reported defect had to be verified before being fixed, and its class before being
called fixed.** Both held. The first check (raw bytes, occurrence audit) confirmed Codex's
finding and sharpened it — the competing referent 122 lines up is what makes the silent
route real. The second check found three more instances. Fixing only the reported line
would have been the necessary-not-sufficient half-fix my own standing lesson warns about,
and would have left the generic `payload` sitting in an operative expression as exactly
the affordance that produced the defect in the first place.

**The test would not run as first written.** `CablePlant.rollout()` builds a
`PrivilegedRecord` whose validator requires a contiguous 0-based step grid, so it cannot be
called twice on the same plant to cross a boundary — the second call raised. Rewritten to
step with `advance()` under zero commanded torque, which is also the cheaper and more
explicit path. Not a defect in the plant; a property of the record contract I had not
needed before.

**Cost had to stay low for a permanent test.** The activation boundary is a control-step
index comparison and does not depend on mesh resolution or physics timestep, so the tests
run at reduced fidelity: all six take 0.59 s, of which the onset-500 case is 0.37 s. A
permanent guard that made the suite noticeably slower would eventually be deleted by
someone.

**My previous session's scratchpad did not survive.** The append-only transcript gate had
to be rebuilt from scratch. It was, and it recorded a clean append.

### Important decisions

1. **Audit the class rather than patch the instance**, and accept the resulting diff
   expansion — declared explicitly to Codex, itemized, so its re-review can be scoped.
2. **Rename Correction 2's `payload`.** Codex's own diagnosis named the generic per-rollout
   payload as the thing the Stage-0 expression could bind to. Removing the instance without
   removing the affordance leaves the trap armed for the next writer.
3. **Bind the canonical string as a named object** (`stage_0_canonical`) rather than
   describing it in prose, so the artifact records the *same* string it hashed rather than
   a second call that ought to agree.
4. **Pin Codex's I13b location decision into the specification**, with its rationale.
   Without it in the file, a reader cannot find the precondition the protocol depends on.
5. **Build the I13b test now, and flag the sequencing deviation loudly** rather than
   quietly conforming or quietly deviating.
6. **Do not update the public README this session.** The heartbeat check ran; the answer
   was no. Reasoning below.
7. **No progress report.** Next regular is my Session 48; no phase transition and no
   approved *written* Claim Sheet amendment occurred. Approving a protocol revision is not
   an amendment trigger.

### Reasoning paths explored

**Whether to keep the diff to Codex's one token.** Considered seriously, because expanding
a diff after a reviewer has bounded its re-review costs review cycles and risks
introducing new defects — my own Session-42 lesson is that generalizing a fix is making a
new claim about a new domain. I expanded it anyway, but kept every item in the same defect
class, made each one a token-level change, and enumerated all four for Codex with the
reason each is in class. The discipline that makes expansion safe is declaring its exact
extent, not avoiding it.

**Whether the README should carry an entry.** The running log is lean by design, and the
last three entries are each "another review round found another defect." A fourth would
turn a log into a journal. The genuinely new thing this session is the permanent test —
but it is not yet reviewer-approved, and announcing it publicly ahead of the review
inverts the order the reviewer set. Codex reached the same conclusion for its own session
independently. The requirement is that the check happens every session, not that the file
changes.

**Whether the I13b test should test at the protocol's real onset of 500 or only at a small
onset.** A plant-contract test should be parameterized rather than hard-wired to one
screen's constant, but I13b explicitly names the step-499/step-500 boundary and the derived
onset is part of the chain the defect broke. Measurement settled it: the onset-500 case
costs 0.37 s, so there was no tradeoff to make — it tests onsets 1, 5, and 500.

### Insights gained

**A pre-registration's variable names are part of its executable surface, and retiring
ambiguous abbreviations does not audit them.** Session 42's Correction 5 removed two
ambiguous *abbreviations* from the prose and declared the file free of tokens whose
meaning lives outside it. It was right about abbreviations and never looked at variable
names. The same defect class simply moved from prose into an executable expression — where
the consequence is a wrong digest rather than a wrong reading, and where a reader who
resolves it "helpfully" gets a valid-looking answer.

**A generic name in an operative expression is an open invitation, and something usually
accepts it.** `payload` was fine where it was written, and became a defect 122 lines later
when a second payload appeared and the writer's fingers reached for the short name. This
is the same shape as Session 42's `canonical_file_sha256`, which invited exactly one wrong
use and got it within a single session from its own author. Two sessions running, the
repair was "give it a name that says which one," and both times the old name was
demonstrably the affordance.

**A constant that looks authoritative and drives nothing is the same trap pointed the
other way.** `P_SEED_BASE` was defined and then ignored by both expressions that should
have used it. Nothing was wrong with the seeds, but anyone changing the constant to move
the band would have changed nothing and been told so by no one.

**A guard is worth committing only after it has been shown to fail.** The I13b test passes
on the correct construction and fails with a clear message on the exact Session-41 defect
state. That is precisely what the Session-41 safety gates could not do — they passed with
roughly 70x margin under *both* the correct and the defective onset. Six rounds of review
have been finding construction defects; this is the first committed artifact that catches
one automatically.

### Files created or updated

- `Reproducibility Packet/protocol/protocol-p-v2.3.3.md` — **renamed** from
  `protocol-p-v2.3.2.md` via `git mv` and corrected. Canonical sha256
  `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`, 54,621 bytes.
- `Reproducibility Packet/tests/test_cable_plant_softening_boundary.py` — **new.** The
  permanent I13b plant-contract guard, 6 tests.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — appended my Session-43 turn, **+137 / −0**, header at line 8,748,
  occurring exactly once, prior bytes an exact prefix.
- `agents/Claude/Session Summaries/HumanReport43.md` — this report.
- `agents/Claude/README.md` — updated.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

Not changed: any packet source module, the config, the schema, the assignment, any result
file, the public README, `.gitignore`, `director_requests.md`, or the monitoring chat.

### Verification performed

```text
protocol v2.3.3    54,621 bytes; BOM no; CRLF pairs 0; raw == canonical
                   5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
                   git check-attr -> text: set, eol: lf
v2.3.2 as reviewed 50,169 bytes; 9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5
                   (recomputed before editing; matches Codex's reviewed digest exactly)
identifier sweep   only remaining bare `payload` is canonical_json's formal parameter
packet suite       405 passed in 10.09 s
I13b negative test guard FAILS on the omitted-onset construction, PASSES on onset 500
transcript append  +137 / -0; 8,744 -> 8,881 lines; header unique at 8,748
Codex S42 append   +107 / -0 at the git level -> no transcript-order recurrence
config.json        absent
test identities    0 / 0 payloads
Protocol-P rollouts 0
```

### Cross-review performed

Read Codex's `HumanReport42.md` in full, its Session-42 transcript turn, and its commit
delta at the git level. Its report is accurate: it did independently reproduce all four
byte measurements (I recomputed the protocol digest and reached the same value), its
architectural reason for the I13a/I13b split matches the return statement I read in
Session 42, and its commit touched only its own workspace files plus the transcript. Its
transcript append was **+107 / −0**, purely additive — no transcript-order recurrence, so
the director-visible monitoring chat needed no entry this session. I verified that at the
git level rather than taking the report's own assertion for it.

One point of substance where I went past Codex rather than disagreeing with it: Codex
characterized the defect as "either an undefined-name failure or a route to hashing the
generic per-rollout payload." Verifying it showed the second is not merely a possible
misreading but the *likely* implementation outcome, since `payload` is a live bound name
earlier in the same document. That raised my assessment of the finding's severity, not
lowered it, and is why I audited the class instead of patching the line.

### Next steps

**Codex owns the next turn.** Two items: (1) review v2.3.3 at canonical digest
`5689dad7…8bdf421f` and either approve that same digest or edit and hand back; (2) decide
whether the I13b test stays where it is or is reverted and re-added with the seam diff.

Once — and only once — both agents have approved the same protocol digest:

1. apply the seam patch to `assignment_generator.py` in the working tree, post the exact
   diff plus focused tests for Codex's separate implementation review;
2. nothing runs until that review closes;
3. then the one-row replay gate; a passing replay authorizes Stage 0, then Stages A/B/C;
4. then Codex reviews the implementation, result, and terminal branch;
5. then the written Amendment A2 and replacement assignment, both agents approving;
6. then full dataset regeneration from zero, re-audit, and the Gate-4 model work.

The written Amendment A2, the replacement assignment, from-zero regeneration, the
remaining Gate-4-to-Gate-7 work, the final `config.json`, and all confirmatory execution
remain unauthorized.

**Nothing is blocked on the director.** `director_requests.md` entry 1 (Claim Sheet review)
remains open and non-blocking by design.
