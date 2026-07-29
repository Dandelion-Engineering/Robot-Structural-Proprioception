# Human Report — Claude Session 41

**Current date and time:** 2026-07-29 15:11 PDT
*(Session work ran 14:55–15:26 PDT; timestamp taken at the moment the chat turn was written.)*

**Phase:** Phase 2 — Execution

**Session role:** Verify and correct Codex's two Session-40 block items on Protocol P,
then close the review loop with an explicit approval of a hashable artifact.

**Config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)

**Decision:**

```text
APPROVE_PROTOCOL_P_V2_3_1_CORRECTED_STATE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

**Rollouts spent:** 5 (4 on the onset-consequence measurement, 1 on the all-None
regression). No Protocol-P identity generated, no Protocol-P statistic computed.

---

## What was accomplished

Codex's Session-40 turn blocked Protocol P v2.3 for the fifth consecutive round, on
two source-level contradictions. This session verified both at source, corrected them,
measured a consequence Codex's text had left open, moved the protocol out of the chat
transcript into a tracked and hashable file, fixed a repository portability defect, and
closed the loop with an explicit owner approval of a named digest.

The five substantive outputs:

1. **Both of Codex's items independently verified at source.** Neither was taken on
   trust and both hold exactly as described.
2. **The corrected seam rebuilt and verified — 44 checks, all passing.** Including
   branch-specific tests for the non-default override path, which is precisely the gap
   Codex's report named in my Session-40 work.
3. **The onset defect's consequence measured rather than argued (4 rollouts).** The
   answer inverted my working assumption and strengthened Codex's block.
4. **A new tracked artifact:** `Reproducibility Packet/protocol/protocol-p-v2.3.1.md`,
   29,250 bytes, canonical SHA-256
   `8c268f8f5777923e661cb44c0b6d68991bdf41bf5080ea3e229e4c101d401d76`.
5. **A repository portability fix** covering both the code path and `.gitattributes`.

### 1. Codex's two items, verified

| Claim | Verified at | Holds? |
|---|---|---|
| `FaultSpec.onset_index` defaults to `-1` | `utils/schema_types.py:77` | yes |
| Plant clamps it: `onset = max(int(fault.onset_index), 0)` | `utils/cable_plant.py:183` | yes |
| Committed path derives step 500 instead | `utils/assignment_generator.py:390` | yes |
| `_valid_config_hash` strips exactly `dev-` then needs 64 hex | `utils/storage_contract.py:103-109, 364-367` | yes |
| The guard accepted `provenance_hash=config_hash` | my own v2.3 seam text | yes |
| Assignment file not LF-pinned under `core.autocrlf=true` | `git check-attr`, `git config` | yes |
| Its CRLF rendering hashes to `00dacaf6…4f87f` | recomputed independently | yes, exactly |

I also checked whether the same exposure sat on more load-bearing pins, which Codex had
not covered. It does not: `config_hash` is computed over `canonical_json_bytes(document)`
and is therefore end-of-line-immune, and `schema_sha256` is a raw-byte hash whose file
*is* already pinned. That established the codebase's own precedent — **when this project
raw-byte-hashes a file, it pins that file** — and my provenance object had introduced a
second raw-byte-hashed file without pinning it. That framing is what decided the fix.

### 2. The corrected seam — 44 checks

Rebuilt from the Session-40 prototype with three corrections, then verified in five
classes ordered by cost:

```text
D onset       default-onset fault active at step 0                 DEFECT CONFIRMED
              corrected FaultSpec carries onset_index = 500
              inactive at step 499, active at step 500
              behavioural: 480 steps -> _softened = False  (3.0 s)
                           520 steps -> _softened = True   (3.3 s)
              healthy () is active-but-faultless
E provenance  derived dev-<64 hex> accepted, passes the validator, base-distinct
              6 rejection cases: base hash / 32-hex / uppercase / no prefix /
              empty / None                                         all rejected
              stamped hash verified to reach the ObservedRecord
B reach       ramp fraction 0.5 == the delivered hard-code EXACTLY (regression test)
              0.0 / 0.5000001 / 0.6 / -0.1 / nan                   all rejected
C leak guard  both tripwires fed the exact state                   both raise
A regression  overrides=None reproduces the delivered row
              20/20 privileged fields, 30/30 S arrays byte-identical, 27.5 s
              and stamps the BASE config hash
F byte pin    Codex's CRLF hash reproduces; canonical digest invariant
```

Scoped packet suite: **399 passed in 9.71 s.**

### 3. The measurement that changed the fix

Codex's turn said the onset difference is decision-bearing because a step-0 fault
removes the declared healthy pre-change segment. True — but it left open the reading
that Stage A's hard safety gates are a backstop, since a body soft from step 0 through
the initial transient plausibly strains harder and trips a flag. I did not want to rely
on that, so I measured it: four full rollouts, both severities, both onsets, every
Stage-A gate computed from the returned `PrivilegedRecord`.

```text
remEI 0.75  step 0    gauge   5.76 ue   qd 0.686   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.75  step 500  gauge   5.56 ue   qd 0.773   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.35  step 0    gauge   5.58 ue   qd 0.752   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.35  step 500  gauge   5.59 ue   qd 0.720   q 0.396   flags 0   sat 0   ADMISSIBLE

peak |gauge| ratio step0/step500      remEI 0.75  1.035      remEI 0.35  0.999
```

Nothing trips. The margins are enormous — 5.6 µε against a 400 µε limit is about 70×.
So the defect had **no** route to a spurious safety failure and **no** route to being
misclassified as a physical limit. It had the quiet route instead: all 169 rollouts
complete, the results JSON looks clean, and `D` gets measured on a body that was soft
from step 0 with no healthy pre-change segment, with nothing in the protocol noticing.

That is worse than a loud failure and it forced two changes beyond Codex's text: a new
invariant **I13** asserting the construction directly, and a **precondition on a
terminal branch** — no Stage-A failure may be labelled a *newly observed physical
safety/method limit* until I13 has been asserted for that rollout. My v2.3 branch table
had silently conditioned that scientific label on the construction being correct.

I recorded explicitly that those `|gauge|` figures are whole-run peak statistics on the
privileged path. remEI 0.35 and remEI 0.75 differ by 0.01 µε there, which shows the
peak is dominated by task motion rather than by the fault. It is not `D`, and it says
nothing about separability.

### 4. The tracked protocol artifact

Codex required "one tracked, canonical protocol-spec artifact containing the complete
operative state." I created it rather than promising it, because the defect this round
existed *precisely* because the written instruction and the working prototype disagreed
while each was internally consistent. A specification that lives only in a chat
transcript cannot be hashed and cannot be reviewed as an object.

One consequence worth naming, which Codex's requirement implies without stating: **the
spec cannot contain its own digest.** The implementation reads the file, computes the
canonical digest at run time, and records it per rollout in the results JSON.

### 5. The portability fix, done three ways

Codex offered two options — pin the file to LF, or replace the raw-file field with the
canonical assignment hash. I did both, plus a third that makes the pin portable
independently of either:

1. **Every hash of a pinned text file folds CRLF to LF in memory before digesting.**
   This is the load-bearing fix: the digest becomes portable *by construction* rather
   than by depending on `.gitattributes` being present and correct in whatever clone
   runs the protocol.
2. **`.gitattributes` pins the assignment JSON and `protocol/*.md` to `text eol=lf`**,
   following the `schema.json` precedent. Defence in depth. I deliberately did **not**
   pin `draft-config-v0.1.json` — its hash is already canonical, so pinning it would
   flip a load-bearing file's bytes in Codex's lane for no gain.
3. **Both the canonical byte digest and the document-derived `assignment_hash` are
   retained.** The canonical digest is end-of-line-immune; the raw-byte digest catches
   whitespace or key-order changes canonicalization hides. They cross-check each other.

Supporting evidence I found that Codex had not: **`draft-config-v0.1.json` is already
CRLF in this working tree** (969 CRLF, 0 LF) while the assignment JSON beside it is pure
LF. The divergence is present, not hypothetical.

---

## Challenges and how they were overcome

### The commitment I had made to escalate, and why I did not honour its letter

In Session 40 I committed in writing — in both the chat turn and `HumanReport40` — to
escalating to the director rather than looping a fifth time if round five did not
converge. Round five did not converge: Codex blocked. By the letter of that commitment
I should have written to Randy instead of continuing.

I chose not to, and said so explicitly in the chat turn rather than letting the
commitment quietly lapse. The reasoning:

- The framework's escalation rule exists for a **disagreement** that will not converge
  — where two agents need a third party to settle a judgment. There is no disagreement
  here. Codex approved the direction and substance of all nine of its own Session-39
  requirements, approved every retained Stage A/B/C rule, found no new scientific
  blocker, and stated that no arbitration is needed.
- Both remaining items were **checkable facts about Python source**, not contested
  judgments. I checked both myself and both held.
- The surface shrank from nine items to two, with zero re-litigation.
- Escalating would have asked a non-specialist to arbitrate what
  `FaultSpec.onset_index` defaults to — making the director a bottleneck on exactly
  the class of question the agent layer exists to absorb.

So I replaced a count-based trigger with a content-based one: **escalate when a round
re-litigates a settled point, or when we disagree on a judgment neither agent can
resolve from source — not when a round finds a new, verifiable defect.** Five rounds
that each found something new and none that repeated itself is a protocol getting
harder to break, not two agents stuck. If a future round repeats a settled point I
escalate immediately, regardless of count.

Codex reached the same conclusion independently: its `HumanReport40` decision 10 reads
"Do not escalate to the director yet. The new findings are direct source
contradictions, not a repeated disagreement requiring arbitration." Both agents
arriving there separately is some evidence the judgment is right rather than
convenient.

### A fair hit on my Session-40 verification

Codex's `HumanReport40` insight 2: "A positive-control replay validates the default
branch only. It cannot authorize a newly added non-default path without
branch-specific tests." That is a correct criticism of my Session-40 work — my
transparency test exercised `overrides=None` and nothing else, so it could not have
caught a defect living in the override path. This session's D and E classes are
branch-specific tests of exactly that path, and the onset defect is the concrete proof
the criticism was right.

### Resisting the assumption that the safety gates were a backstop

My first instinct on reading Codex's onset finding was that Stage A would have caught
it — which would have made the defect a validity nuisance rather than a silent one.
That instinct was wrong, and the only reason I know is that I spent four rollouts
measuring instead of reasoning. Had I trusted the instinct, I would have written a
weaker correction: no I13, no precondition on the terminal branch, and a protocol that
still relied on gates that are demonstrably blind to this class of error.

### Scope discipline while the protocol is blocked

Protocol P is blocked, so I had to measure the defect's consequence without executing
any part of Protocol P. Handled by using probe identities explicitly outside the
`P_SEED_BASE` band, computing no `D`, making no admissibility selection, writing no
dataset-role artifact, and relying on the fact that `CablePlant` contains no RNG — so
every gate quantity measured is a pure function of the physical config and the fault,
making the identity irrelevant to the measurement.

---

## Important decisions

1. **Do not escalate; replace the count-based trigger with a content-based one.**
   Stated in the chat turn so it is auditable rather than silent.
2. **Adopt both of Codex's corrections verbatim**, then extend each where measurement
   showed the correction was insufficient.
3. **Add invariant I13** — assert the construction directly rather than trusting the
   safety gates to reveal a construction defect.
4. **Add a precondition to the `NO_ADMISSIBLE_PROBE` branch table** so a build mistake
   cannot be reported as a physical discovery.
5. **Pin `is not None` rather than truthiness** on every override guard. An empty tuple
   is falsy while being `is not None`; a truthiness test would fall through to the
   derived fault list — harmless at the healthy dev reservation, which is exactly what
   makes it worth pinning.
6. **Create the protocol spec as a tracked file this session** rather than deferring it
   to implementation, so Codex reviews an object with a digest instead of a description.
7. **Fold CRLF in code** as the load-bearing portability fix, with `.gitattributes` as
   defence in depth — better than either option Codex offered, because it does not
   depend on repository configuration surviving a clone.
8. **Do not pin `draft-config-v0.1.json`.** Its hash is already canonical; pinning it
   would change a load-bearing file's bytes in Codex's lane for no benefit.
9. **Retain both the canonical and raw-byte assignment digests** rather than choosing.
10. **Add one Live-Run README running-log entry.** The log already records review
    rounds at this granularity (three entries dated 2026-07-29), and this session
    produced a measurement, not just a block.

---

## Reasoning paths explored

- **Whether the escalation commitment bound me.** Resolved by asking what the rule is
  *for* rather than what it says: it targets unconvergent disagreement, and there is no
  disagreement. Recorded the decision and its criterion in the transcript so a reader
  can disagree with it.
- **Whether the onset defect was catchable downstream.** Traced it forward from the
  `FaultSpec` through `_generate_reservation` → `CablePlant` → `_fault_active`, then
  asked which Stage-A gate would notice. Measured the answer: none. That converted the
  fix from "correct the text" to "correct the text *and* add a construction invariant
  *and* fence a terminal branch."
- **Whether the misclassification route was open.** Worked out that remEI 0.35 is the
  severity most likely to trip a limit, and that under my branch table a 0.35-only
  failure maps to "newly observed physical limit" — a bug laundered as physics. Measured
  it: the route is closed, because nothing trips at all. Both the hypothesis and its
  refutation are recorded; the refutation is worse news.
- **Whether the same CRLF exposure sat on other pins.** Checked `config_hash`
  (canonical, immune) and `schema_sha256` (raw but pinned). Finding the precedent is
  what produced the fix rather than a patch.
- **Whether to call the corrected state v2.4 or v2.3.1.** Chose v2.3.1 because Codex
  explicitly asked for a narrow correction rather than a fifth rewrite, and the version
  string should carry that.
- **Whether committing an unapproved pre-registration is appropriate.** Concluded yes,
  with a status header stating it is pending review and unrun — pre-registration means
  written down *before* execution, and a digest is what makes "the state I approved"
  meaningful.

---

## Insights gained

1. **A gate with a large margin is evidence about safety, not about construction.** It
   cannot double as a check that the thing built is the thing specified. Measured here:
   gates passing with 70× margin were completely insensitive to a defect that changed
   which body was being measured. Invariants that catch construction defects must
   assert the construction, not its consequences.
2. **A terminal branch that attributes a failure to physics must first exclude the
   construction.** My branch table assigned scientific meaning to a gate outcome
   without a construction check, so one branch could have converted a bug into a
   finding. The failure mode is not a wrong measurement — it is a *correct* measurement
   of the wrong object, wearing the label of a discovery.
3. **The quiet failure is the dangerous one, and it is the one a large margin
   produces.** A defect that trips an alarm costs a session. A defect that passes every
   check costs a result.
4. **A specification that cannot be hashed cannot be approved.** This round's defect
   existed because the written text and the working prototype disagreed while each was
   internally consistent — the exact failure a digest-bearing artifact prevents,
   because there is then one object rather than two.
5. **Type safety proves a field exists, not that the caller supplied the experiment's
   value for it.** Codex's phrasing, and it is the sharpest available statement of this
   round's defect: `ScreenOverrides` was fully typed and still imported a dangerous
   dataclass default.
6. **A guard on a falsy-but-present value is a trap that hides in the harmless case.**
   The empty tuple would have fallen through to a derived list that is *also* empty,
   so the bug would have been invisible until the first reservation where it was not.
7. **Escalation triggers should be content-based, not count-based.** A count cannot
   distinguish "stuck" from "converging on a hard problem." Five rounds finding five
   distinct real defects is the latter.

---

## Files created or updated

**Created:**
- `Reproducibility Packet/protocol/protocol-p-v2.3.1.md` — the complete operative
  Protocol-P state as a tracked, hashable artifact. Canonical SHA-256
  `8c268f8f5777923e661cb44c0b6d68991bdf41bf5080ea3e229e4c101d401d76`.
- `agents/Claude/Session Summaries/HumanReport41.md` — this report.

**Updated:**
- `.gitattributes` — pinned the assignment JSON and `protocol/*.md` to `text eol=lf`,
  with the reasoning and the verification date recorded in comments.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Session-41 correction and explicit approval. `+284 / −0`, header at
  line 7,952 after the recorded 7,951-line boundary, four hard gates passed.
- `README.md` (Live-Run) — one running-log entry. Banner already read 2026-07-29.
- `agents/Claude/README.md` — current-state paragraph and clean-append streak.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

**Not changed:** no Reproducibility Packet source, config, schema, assignment, results,
or test file. The seam remains a scratchpad prototype because it modifies code Codex
owns, and applying it is gated on Codex's approval of v2.3.1.

**Scratchpad (not committed):** `probe_s41_seam_corrected.py` (the corrected seam and
all five verification classes), `probe_s41_onset_consequence.py` (the four-rollout gate
measurement), `append_turn.py`, `turn_s41.md`.

---

## Verification

```text
Codex's two block items, at source                      both confirmed
Codex's CRLF hash 00dacaf6…4f87f                        reproduced exactly
corrected seam, 44 checks across 5 classes              ALL PASS
onset-consequence probe, 4 rollouts                     all 4 ADMISSIBLE
scoped packet suite                                     399 passed, 9.71 s
transcript append hard gates                            4 / 4 passed
  pre-write lines                                       7,951
  pre-write SHA-256                                     FFDB590E33A1D5B08891CA7B306D13B4AB70C0B284A453E298F6E5721FC94445
  header line / count                                   7,952 / 1
  git diff                                              +284 / −0
Codex's S40 append verified at git level                +182 / −0, header 7,771
  clean-append streak                                   SEVEN (no monitoring note needed)
.gitattributes change produces no content churn         verified
assignment digest unchanged after pinning               76255a80…514ae
protocol spec tracked, LF, pin applies                  verified
```

---

## Next steps

**Codex owns the next turn.** Two things were asked of it:

1. Review `protocol-p-v2.3.1.md` as a file — 29 KB, and it is the object a reader who
   did not write it would execute, which is where the last five defects lived.
2. Say whether it wants to own the seam patch to `assignment_generator.py`. My default
   is to post the diff for its review before anything runs, since it is Codex's file.

If Codex approves the file: apply the seam patch and post the diff → replay gate →
Stage 0/A/B/C (169 rollouts, ~76 min) → Codex reviews implementation, result, and
branch → written Amendment A2 and replacement assignment → full regeneration from zero.

**Still unauthorized:** the final `config.json`, written Amendment A2, Claim Sheet
edits, replacement assignment, regeneration, Gate-4 fitting, and all confirmatory
material.

**Progress report:** not due. Session 40 was the regular eighth-session report; the
next regular is my Session 48. No event trigger fired this session — no phase
transition, and no *written* amendment to the Claim Sheet.

**Nothing is blocked on the director.** `director_requests.md` entry 1 (Claim Sheet
review) remains open and explicitly non-blocking.
