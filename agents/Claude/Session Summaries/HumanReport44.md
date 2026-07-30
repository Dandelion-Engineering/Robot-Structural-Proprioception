# Human Report — Claude Session 44

**Current date and time:** 2026-07-29 18:41 PDT

**Phase:** Phase 2 — Execution

**Session role:** Implementer. Codex approved Protocol P v2.3.3 at my exact digest and
authorized one thing: apply the specified seam to the generator and post the applied diff
plus focused tests for a separate implementation review. That is what this session did.

**Final config state:** **UNFROZEN** (`config.json` remains absent)

**Protocol-P execution spent:** zero. No replay, no stage, no identity generated, no
statistic computed, no artifact written. `results/protocol_p/` does not exist. The
confirmatory test split remains at zero identities and zero payloads.

**Decision posted:**

```text
APPROVE_SEAM_IMPLEMENTATION_CURRENT_STATE
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

---

## Summary

### What was accomplished

**1. The Protocol-P specification review loop closed.** Codex's Session 43 approved
`protocol-p-v2.3.3.md` at exactly the digest I approved in my Session 43 —
`5689dad7…8bdf421f`, 54,621 bytes, pure LF. I re-derived that digest myself before
touching anything rather than trusting the transcript, and also re-derived the I13b test's
raw digest and git blob hash. All four matched Codex's independently reported values. After
seven review rounds, both agents now approve the same byte-state of the screen's
pre-registration. Codex also accepted the I13b sequencing deviation I disclosed last
session and approved the test in place, so nothing needed reverting.

**2. Applied the §3 seam patch** to `Reproducibility Packet/scripts/utils/assignment_generator.py`
(+141 / −5). This is the code change the screen requires and cannot work around. Three
additions, all keyword-only, all defaulting to existing behaviour:

- **`ScreenOverrides`** — a frozen dataclass carrying the five things a screen may deviate
  from the approved assignment document. Every field defaults to `None`, so a
  default-constructed instance is inert. `is_active()` tests `value is not None` rather
  than truthiness, because an empty fault tuple means "explicitly healthy" and is *falsy* —
  a truthiness test would silently fall through to the reservation's own fault list.
- **`screen_pair_id`** — returns the override's realized identity when supplied, else the
  approved `…_dataset0` identity. The dataset suffix is applied only on the unoverridden
  branch, so the protocol's "screen identities carry no dataset suffix" invariant holds by
  construction rather than by a later assertion.
- **`_screen_stamped_hash`** — validates that an overriding rollout carries a nonempty
  `dev-` prefixed provenance hash whose remainder is one lowercase SHA-256 digest and which
  differs from the base configuration hash. It reuses the packet's own `re_full_sha256`
  rather than writing a second hex predicate, so "this passes the storage layer's
  validator" is true by *sharing the implementation* instead of by agreeing with it.

Plus the two function changes: `_physical_config` gained probe peak and ramp-fraction
overrides (peak must be finite and positive; fraction finite in `(0, 0.5]`, matching the
mechanics envelope), and `_generate_reservation` now computes the stamped hash first and
passes it — not the base hash — to the closed-loop sensor session and to every observation.

**3. Wrote 37 focused tests** in a new permanent packet file,
`tests/test_assignment_generator_screen_overrides.py`. Full packet suite: **442 passed in
11.28 s** (405 pre-existing, unchanged, plus the 37 new).

**4. Proved the tests actually catch defects** — and found that one of them did not. Detail
below; this is the session's real content.

### Challenges and how they were overcome

**The important one: my own test suite had a hole, and only defect injection found it.**

A green suite over a correct patch proves nothing about whether the tests would notice the
patch being *wrong*. So I injected ten plausible slips into the applied seam one at a time,
ran the focused file against each, and restored from a pristine byte copy between cases
(restoration asserted byte-identical each time, and again at the end).

The first pass left one defect **completely uncaught**: if `_generate_reservation` never
forwards the overrides to `_physical_config`, zero tests fail.

That is the expensive one to miss. Identity, provenance, fault list, and every guard would
all still be correct, and every one of the screen's 169 planned runs would have quietly
simulated the *delivered* probe — the wrong ramp shape at the wrong amplitude — while the
results recorded the candidate we believed we ran. The screen's entire job is to choose
among probe candidates; it would have selected one it never applied.

Why the tests missed it: I had tested `_physical_config`'s override handling directly, and
those tests *pass the overrides in themselves*. A missing wire between the two functions is
invisible to them. This is the same failure shape the project has now hit repeatedly — a
check on a necessary condition silently licensing the sufficient one.

The fix captures the mechanics configuration at the point where the plant is actually
constructed. I chose that over observing the probe in the strain readings because the probe
begins 2.0 s into a run, so a behavioural check would cost a ~1000-step simulation per
condition, and the property in question is a wiring property — physical fidelity does not
enter it. Second pass: **all ten defects caught, none uncaught**, restoration byte-identical,
post-restore suite green.

**A reachability problem, structurally identical to one from two sessions ago.** The
specification requires the stamped hash to reach *both* the closed-loop sensor session and
every observation. The observation half is straightforward to assert, because the hash is a
stored field of the observation record. The session half is not reachable at all: the
session's hash flows only into an object that `_generate_reservation` discards before
returning. This is the same architectural situation that forced the plant's softening-boundary
check into its own standalone test last session. Rather than leave the requirement untested
or quietly narrow the specification to its assertable half, I captured it where the session
is constructed. Defect injection confirms that test discriminates.

**A guessed identifier.** My first run failed on one test because I had invented a plausible
sensor-fault setting id from memory instead of reading it. Queried the assignment document
for the real one. Small, but it is the same class of mistake as citing from memory, and the
correct habit is to read rather than recall.

### Important decisions I made

1. **I added one raise the specification does not name, and flagged it as a deviation.**
   The specification defines what to stamp when an override is active and what to stamp
   otherwise, but never names the state "inert override that nonetheless carries a
   provenance hash." The literal reading silently stamps the base hash and discards the
   provenance. I made it raise, because the specification already establishes exactly this
   principle one paragraph earlier for probe overrides — an override that cannot take effect
   must fail loudly rather than be discarded — and because the silent version is the worse
   failure: the caller believes the artifact carries a screen identity while it carries the
   approved one. It cannot affect the screen either way, since every screen rollout sets an
   active field. **I flagged it at the top of my handoff, gave the reasoning, and told Codex
   I will drop it on request.** Applying a principle the spec states to a case it did not
   enumerate is one step past "implement §3," and that step is the reviewer's to authorize.

2. **I deleted a test rather than ship it.** I had written a check for the specification's
   "the screen persists no dataset artifact" condition that asserted a temporary directory
   was empty after a rollout. It passed — vacuously. The function writes nothing by
   construction, so the assertion would hold even if it wrote to a hard-coded path
   elsewhere. A green test that proves nothing is worse than no test, because it reads as
   coverage. My position is that this condition belongs with the screen driver script, which
   does not exist yet; I asked Codex to confirm.

3. **The new tests go in the permanent packet suite, not a screen-scoped location.** I
   applied Codex's own reasoning for the plant test: these are generator-contract guards,
   and any future consumer of the override mechanism needs them after the screen is over.

4. **I did not touch `.gitattributes`.** Both new/changed files are pure LF now but are
   unpinned, so a fresh clone on Windows renders them with different line endings and their
   raw fingerprints will not reproduce there. I reported the fact, reported the
   line-ending-stable git blob hashes alongside the raw ones, and left the decision to
   Codex — the protocol byte-pins exactly two text files by design, neither is source, and
   `.gitattributes` is shared root configuration.

5. **I added a second short append naming a scope boundary.** Codex's stated review
   checklist lists a runtime construction check that is *not* part of the seam — it lives in
   the screen driver, which is unauthorized and unbuilt. Rather than let its absence read as
   an omission and cost a full review round, I named the boundary explicitly and invited
   correction.

6. **Live-Run README: ran the heartbeat, added nothing.** Codex had already published the
   joint-approval milestone earlier the same day, and this session's output is a single
   artifact in *open* review. Announcing my own unreviewed work inverts the reviewer's
   order — the same call I made in Session 43, and the same one Codex made for its Session 42.

7. **No progress report.** My next regular one is Session 48. No phase transition closed and
   no written Claim Sheet amendment was approved this session (approving a protocol revision
   is neither).

### Reasoning paths explored

I considered testing the probe-override wiring behaviourally — run long enough to see the
probe move the strain readings — and rejected it on cost and on aim: it would have bought a
physics observation to answer a wiring question, at roughly 9 seconds per run against
sub-second for the direct check.

I considered whether the inactive-with-provenance case might be better left as the
specification literally reads, on the grounds that deviating from an approved spec is
exactly what the project's review discipline exists to prevent. What decided it was that the
specification's own probe branch states the general principle; I am extending a stated rule
to an unenumerated case, not inventing one. That is still the reviewer's call, which is why
it leads the handoff instead of hiding in the diff.

### Insights gained

- **Unit-testing the two ends of a wire cannot test the wire.** When a test supplies the
  input that a caller is supposed to supply, it proves the callee behaves — and says nothing
  about whether the caller ever calls it that way. The seam's most consequential guard was
  the one no unit test could see.
- **Defect injection is cheap and it is not optional.** Ten mutations, a few minutes, and it
  turned a suite I would have handed off with confidence into one that had a hole in the
  single most result-moving wire in the patch.
- **When a property is unreachable from where you want to assert it, that is information
  about the architecture, not an excuse.** Twice now in three sessions, the answer has been
  to assert it where it *is* reachable rather than to drop the requirement.
- **Deleting a vacuous test is a positive contribution.** It removes a false signal.

### Files created or updated during this session

- `Reproducibility Packet/scripts/utils/assignment_generator.py` — **the seam patch**,
  +141 / −5. raw sha256 `07fbbe563b5a904eba2d57f58e436e84975d2891ea7ebf4cac9f24253ce5b06b`,
  git blob `1c565888edd6e538cbb281894ab6c4cdc418bb6b`, 36,326 bytes, UTF-8, no BOM, pure LF.
- `Reproducibility Packet/tests/test_assignment_generator_screen_overrides.py` — **new**,
  37 tests. raw sha256 `69f1df3145e58a68ceccd698e198afa030391e00adc3b8be518335a2924f0635`,
  git blob `2ec96c9f995fa9e9efad0000af1d3364a4994db4`, 23,116 bytes, pure LF.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — two appends, **+235 / −0** total, now 9,207 lines. My main turn's
  header is at line 8,976 and the scope note's at 9,176; both passed all four EOF gates.
- `agents/Claude/Session Summaries/HumanReport44.md` — this report.
- `agents/Claude/README.md` — workspace map updated for the new co-owned test file.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

**Not changed:** `protocol-p-v2.3.3.md`, the I13b test, the schema, the draft config, the
assignment document, `config.json` (still absent), any result, any dataset payload, label or
role index, `director_requests.md`, `.gitignore`, `.gitattributes`, the root `README.md`, or
the monitoring chat.

### Transcript-order monitoring

Codex's Session-43 append was verified clean at the git level: +91 / −0, header appearing
exactly once at line 8,885, and the 8,881-line pre-write prefix intact. **No recurrence —
clean-append streak nine to ten.** My standing duty is to flag recurrences, so a clean
session adds no entry to the monitoring thread; I verify at the git level regardless of what
either agent reports.

### Cross-review performed

I read Codex's Session-43 chat turn in full, its complete `HumanReport43.md`, its running-log
addition to the public README, the approved `protocol-p-v2.3.3.md` end to end, and the
generator, storage-contract, sensor-model and rollout sources the patch touches. I
independently re-derived every digest Codex reported rather than accepting them, and I
verified its claim about the plant activation path against the source before relying on it.
Codex's report is accurate on every point I could check. One thing I did not accept at face
value was its review checklist, which lists a check that belongs outside the seam — hence
the scope note.

### Next steps

1. **Codex owns the next turn.** It reviews the exact implementation bytes above and either
   approves the same state or edits and hands back. Three questions are open for it: keep or
   drop the inactive-with-provenance raise; where the screen's persistence-boundary test
   should live; and whether to pin the two files' line endings.
2. **Nothing executes until that loop closes on an explicitly approved state.** No replay,
   no identity, no statistic, no Stage 0/A/B/C.
3. After implementation approval: the one-row replay gate, then Stage 0, then Stages A/B/C
   (169 rollouts, roughly 76 minutes).
4. Then Codex reviews the results and the terminal branch, followed by the written
   Amendment A2 and a replacement assignment requiring both agents' approval, then full
   dataset regeneration from zero.
5. The 472 existing payloads remain readable development data and remain slated for
   supersession. They are not to be built on.
6. `config.json` stays absent and the test split stays at zero until the joint freeze.
