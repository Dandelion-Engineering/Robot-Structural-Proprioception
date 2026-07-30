# Human Report — Claude Session 45

**Current date and time:** 2026-07-29 19:34 PDT

**Phase:** Phase 2 — Execution

**Session role:** Implementer and operator of the Protocol P §7 replay gate

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config.json` remains absent

**Protocol-P execution state:** The replay gate ran and **passed**. No Stage 0, no Stage
A/B/C, no Protocol-P identity, no statistic, no screen artifact. The confirmatory test
split remains untouched at zero identities and zero payloads.

---

## Summary

### Where the session started

Codex's Session 44 closed the implementation review of the generator seam I built in my
Session 44, approving both files at their exact committed state and answering all three
questions I had handed it. It then authorized exactly one thing: **run the pinned one-row
replay gate**, post the evidence, and stop. Stage 0 and Stages A/B/C remain unauthorized
until that evidence is reviewed.

That is what this session did.

### What the replay gate is, in plain terms

Protocol P is a pre-registered screen that will spend 169 physics rollouts (about 76
minutes) deciding whether the gentle diagnostic probe the project actually delivers is
strong enough to make a structural stiffness-loss fault *measurable at all* above the
run-to-run noise of a healthy arm. That is a stop/go question for the whole structural
stratum of the confirmatory experiment.

Every one of those 169 rollouts is built by the same generator function that built the
development dataset back on 2026-07-24. Section 7 of the protocol therefore makes one
question a precondition on the entire screen:

> Does rebuilding a *single* delivered run from the committed inputs reproduce the
> retained artifact **exactly**?

If it does not, the instrument that would produce the screen's numbers is not the
instrument that produced the data everything else is anchored to, and no result from it
would be interpretable. Failure means Stage A does not start.

### What I built and ran

A new packet script, `scripts/protocol_p_replay_gate.py`, which implements the gate:

- **Invariant I1 — every pinned digest present and unchanged, each through its own hash
  domain.** Protocol P pins files of two disjoint kinds and applying the wrong hash helper
  to either one breaks it. Text files (the protocol itself, the approved assignment) are
  hashed after stripping a byte-order mark and folding Windows CRLF line endings to LF, so
  the digest survives a fresh clone on a different operating system. The two retained
  `.npz` binaries are hashed as **exact bytes with no transformation**, because a `.npz`
  is a ZIP archive whose payload contains CRLF byte pairs *as data* — folding them would
  corrupt the identity. The gate additionally recomputes each binary's wrong-domain digest
  as a **reported diagnostic**, reproducing the two values the protocol records, so the
  domain split is demonstrated live rather than asserted.
- **Invariant I2 — array equality on replay.** All 20 privileged plant fields and all 38
  observed payload entries must be equal in dtype, shape and value.
- **Identity binding.** The replayed reservation is compared field-by-field against the
  retained manifest row, so the run being replayed is *proved* to be the one that produced
  the pinned references rather than assumed from the naming convention.
- **Provenance scope.** The replay runs with no overrides and must therefore stamp the
  *base* configuration hash. This is a requirement, not a default: the stamped hash is a
  stored field of the observation, so stamping anything else would change the artifact's
  bytes and fail the comparison by construction.
- **Ephemerality.** The gate must write nothing. It inventories the data root, the packet
  tree and the repository's top-level files before and after the rollout and reports every
  difference, so a stray write from any layer of the stack is visible.

### The result

**REPLAY_GATE_PASS — one row, exact.**

```text
I1   protocol      54,621 B  5689dad7...bdf421f   (canonical text, raw == canonical)
     assignment    22,760 B  76255a80...3514ae    (canonical text, raw == canonical)
     plant ref  3,176,122 B  ed5b1f39...b65e45    (raw bytes; 18 CRLF pairs inside)
     obs ref      929,068 B  cdde17f6...bb4c83    (raw bytes;  1 CRLF pair inside)
I2   plant        20/20 fields equal
     observation  38/38 entries equal   (531 NaNs matched position for position)
identity          all 20 manifest fields equal
ephemerality      3,119 files watched; 0 added, 0 modified, 0 removed
rollout cost      26.37 s
```

The gate ran twice on identical inputs (before and after a fix described below) and
produced 58/58 equality both times, at 25.58 s and 26.37 s.

### The finding worth keeping: this is also a regression test on last session's patch

Section 7 asks whether the construction path still reproduces the delivered artifact. It
does. But the two reference files were generated on **2026-07-24** — five days and one
patch before this run. They predate the Session-44 seam entirely.

So the replay is also an empirical regression test on that patch. Codex verified the
unchanged branch by tracing it against the parent source and concluded that the default
ramp, fault derivation, base hash, dataset pair identity, online session, post-hoc
observation path and return tuple all retained their prior values. The replay now says the
same thing **by measurement, at bit level, through the whole stack**: the seam changed
nothing on the ordinary path, including every floating-point value across 3,000 simulation
steps and all 531 NaN positions in the observed payload.

That distinction matters. A source review can establish that a branch is not taken. Only
an end-to-end bit comparison can establish that nothing downstream of it moved.

Two smaller measured properties fell out of the run:

- The delivered dataset was generated observing suites C1 and S together in one call;
  §4's pinned construction path observes **S alone**. It reproduced exactly, which means
  the sensor model carries no state across suites — the random-number keying really is
  `(sensor_seed, pair_id, channel, stream)` and nothing else.
- Zero contact steps on a reservation assigned a contact profile, consistent with the
  earlier finding that 0 of 76 development runs actually touched. Expected, recorded so
  the number is not read as a surprise.

### A defect I introduced and removed, because the shape of it is instructive

My first version of the ephemerality check printed exactly this:

```text
added 0 · modified 0 · removed 0
```

That is true, and it is **indistinguishable from a check that watched nothing**. A reader
cannot tell "watched 3,119 files, none changed" from "the watch list resolved to empty."
This is a cousin of the vacuous test I deleted last session, but worse in one respect: it
is not a test that cannot go red, it is a *report* that cannot be told apart from a
vacuous one, so the reader has no way to even ask the question.

Fixed two ways: the report now prints its denominator, and the inventory function *raises*
below a floor of 100 files rather than certifying a no-write claim from a snapshot that
could not carry it. Both states are tested. It cost one extra 26-second run, because the
evidence I hand a reviewer should come from the bytes that are committed, not from an
earlier version I had since changed.

### Verifying the gate before trusting it

A gate's dangerous failure is not a false alarm — it is a **vacuous pass**. Before running
it I put its comparison layer through the defect-injection technique that found the wiring
hole in last session's patch: **21 cases against the real retained payloads — 19 injected
defects plus 2 controls. All 21 behaved as required.** The cases that matter:

| Injected defect | Caught |
|---|---|
| one value moved by one unit in the last place (plant and observed) | yes |
| one NaN replaced by 0.0 | yes |
| one number replaced by NaN | yes |
| dtype narrowed float64 → float32 | yes |
| array truncated by one row | yes |
| stamped config hash swapped for a screen hash | yes |
| key missing / key added / wrong entry count | yes |
| wrong binary file substituted into a pinned slot | yes |
| unapproved protocol version bump (filename drift) | yes |
| identity field or field-set drift | yes |

The NaN pair is load-bearing. The observed gauge channel carries **real** NaNs from sensor
dropout and latency — 531 of them — so the comparison *must* treat matched NaN positions
as equal or it would fail a perfectly correct replay. Making it NaN-tolerant is precisely
how it could have become NaN-blind, so both directions are tested explicitly.

### Making that verification permanent

The injection sweep lives in a scratch file that will not survive the session, and it
depends on data that is not in the repository. So I wrote the portable form of it as a
permanent packet test, `tests/test_protocol_p_replay_gate.py` — **30 tests, 0.24 s**, no
dependence on the git-ignored references. Beyond re-covering the comparison layer on
synthetic payloads it does three things worth naming:

1. It binds two pre-registered counts to their *definitions* rather than to literals: the
   20 privileged fields against the record's own field list, and the 38 observation entries
   against `5 × (number of registry channels) + 8`. If the schema ever gains a field, the
   gate fails loudly instead of silently comparing 20 of 21.
2. It checks the committed protocol and assignment files against their approved digests,
   which makes *"the pre-registration has not drifted"* a permanent automated check rather
   than something we re-verify by hand each session.
3. It covers the binary/text domain split by its **property** — that folding CRLF changes
   a digest — on a synthetic file, so the check is portable to a clean machine that has
   none of the retained data.

Full packet suite after the additions: **472 passed in 11.21 s** (was 442).

### Packet runbook maintenance

Three packet scripts had no entry in the packet README, which is the runbook a stranger is
supposed to be able to follow. I added steps for my two — the replay gate, and my
Session-34 structural separability screen, which had been missing since it was written.
The replay-gate entry states honestly that an outside reader **cannot** run it, because
the two pinned references are local artifacts of the dataset generation step and are not
distributed, and points at the portable test file instead. The third missing script is
Codex's; I flagged it in the chat rather than editing another agent's entry.

## Challenges and how they were overcome

**Ordering inside the digest checker surfaced through a failing test, not a review.** My
first version of the protocol-filename-drift test failed with the *wrong* error: the
absence guard fires before the filename guard, so my placeholder paths tripped absence
first. The fix was to give the test real files in the binary slots so the guard under test
is the one that fires. Small, but it is the difference between a test that proves a guard
works and a test that passes for an unrelated reason.

**Deciding what the gate should not do.** The obvious extra is a packet test that runs the
whole gate end-to-end and skips when the dataset is absent. I decided against it: it would
skip on every clean checkout, and a test that is green-by-skipping everywhere except one
machine reads as coverage while providing none — the same failure I deleted a vacuous test
for last session. The split I shipped instead is: the script *is* the executable gate, and
its comparison layer is permanently tested without the data. I handed that decision to
Codex rather than burying it.

**Knowing where to stop.** Building the Stage driver next was tempting and is not blocked
by anything technical. I did not, for two reasons: Codex set the sequence and the replay
review is what closes next, and handing a reviewer two review surfaces at once muddies a
loop that is currently one clean object. Codex's enumerated driver requirements are carried
forward verbatim in my continuity file.

## Important decisions I made

1. **The replay gate is a committed packet script, not a scratch measurement.** It is the
   executable form of a pre-registered stop/go gate; it belongs in the packet where it can
   be reviewed and re-run, not in a temporary file whose result exists only as a paste.
2. **The gate writes nothing, deliberately, and proves it.** Protocol P and the reviewer
   both require the replay to be ephemeral. Rather than assert that, the script measures
   it against 3,119 real files and refuses to make the claim from an undersized snapshot.
3. **Import production's own serialization rather than re-implementing it.** The plant
   comparison uses the generator's own payload function, so the comparison *shares* the
   implementation instead of agreeing with a second copy of it. This is the same reasoning
   that made last session's seam reuse the packet's existing hash predicate. Because that
   function is private to another agent's file, I handed the coupling decision to Codex.
4. **No entry in the public Live-Run README this session.** The project's public log has
   consistently published milestones *at reviewer approval*, not at completion, and the
   replay result is explicitly pending Codex's review. Publishing ahead of the reviewer
   would invert that order for the first time. The entry belongs on the log one turn from
   now — and whoever writes it should also correct the current entry's forward-looking
   statement that "no replay has run yet," which this session made false.

## Reasoning paths explored

- **Whether to compare the regenerated observation by writing it to a temporary file and
  hashing the bytes.** Rejected: a `.npz` is a ZIP container, so byte identity of a
  *regenerated* archive is not a property of the data and would produce spurious failures.
  The protocol already says this — the input is guarded by exact binary identity, the
  output by array equality — and the script says so in its docstring.
- **Whether to require dtype equality at all.** Kept, and reported separately from value
  equality, so that a dtype-only difference would be visible as exactly that rather than
  as a generic mismatch. A narrowed dtype can compare equal by value and is still a
  different artifact.
- **How strong a claim the ephemerality check can support.** Weak on its own — the script
  has no write path, so it cannot fail on its own account. It is not vacuous, though,
  because the layers *underneath* it can write: MuJoCo demonstrably writes a log file at
  the repository root under some conditions. The check is scoped and reported as what it
  is.

## Insights gained

1. **A green report must disclose its denominator.** "Nothing changed" and "nothing was
   watched" produce identical output unless the count is printed. The remedy is two-part:
   print the denominator, and refuse to make the claim when the denominator is too small
   to support it.
2. **A replay gate written for one purpose can settle a different question for free.**
   Because the retained references predate the seam, the same run that certifies the
   construction path also certifies that last session's patch perturbed nothing. Worth
   asking of any reproduction check: *what else does this comparison happen to hold fixed?*
3. **NaN tolerance and NaN blindness are one line apart.** Any comparison that must accept
   real missing data needs both directions tested — a NaN that became a number, and a
   number that became a NaN — or the tolerance silently becomes a hole.

## Files created or updated

- `Reproducibility Packet/scripts/protocol_p_replay_gate.py` — **new.** The executable
  §7 gate. 30,760 B, pure LF, git blob `947d39d0…`.
- `Reproducibility Packet/tests/test_protocol_p_replay_gate.py` — **new.** 30 permanent
  tests. 14,283 B, pure LF, git blob `887e4e78…`.
- `Reproducibility Packet/README.md` — added Step 22 (structural separability screen) and
  Step 23 (the replay gate, with its honest data-availability boundary).
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — appended my Session-45 turn (+230 / −0, header once at line 9,340,
  physical tail, all four append gates green).
- `agents/Claude/Session Summaries/HumanReport45.md` — this report.
- `agents/Claude/README.md` — workspace map updated.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 46.

Not changed, deliberately: the root `README.md` (see decision 4), `.gitattributes` (per
Codex's Session-44 answer — Protocol P hashes neither source file), and
`agents/Claude/references.md` (no external sources were read this session).

## Next steps

1. **Codex reviews the replay evidence and the two new files**, and either approves the
   same state or edits and hands back. Two questions are open for it: whether to keep the
   private cross-module import or promote that function, and whether it wants a
   skip-if-absent integration test despite my argument against one.
2. **Stage 0 and Stages A/B/C stay unauthorized** until that review closes.
3. **Then the Stage driver**, against the requirements Codex enumerated: build the full
   override bundle from an explicit condition, enforce the identity and construction
   invariants before each rollout, key results from the explicit condition rather than the
   stale returned label, and persist nothing outside a results-only output root — with the
   persistence test surrounding a real output path so a wrong write can actually fail it.
4. **The public log entry** recording that the replay ran and reproduced exactly, once
   approved.
5. Unchanged downstream: the written A2 amendment and full dataset regeneration, then the
   Gate-4 learned models and calibration, the remaining dataset roles, the controller
   protocol, the joint configuration freeze, and only then the one-shot confirmatory
   generation and evaluation.

My next regular progress report remains **Session 48**, unless a phase transition or an
approved written Claim Sheet amendment triggers one sooner. Neither fired this session.
