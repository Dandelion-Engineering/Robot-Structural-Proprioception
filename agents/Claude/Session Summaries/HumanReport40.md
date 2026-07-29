# Human Report — Claude Session 40

**Current date and time:** 2026-07-29 12:50 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner response to Codex's Session-39 block. Verify all nine
required corrections at source, adopt them, build and verify the override seam
the protocol needed, and post Protocol P v2.3 as one clean replacement. Regular
progress report due (my Session 40).

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent — by decision, not by omission)

**Status posted:** `PROTOCOL_P_V2.3_POSTED_FOR_EXACT_STATE_REVIEW`

**Rollouts spent:** one, on the already-delivered healthy development row
`scenario_dev_t01_f000_r00`, through the patched path. No Protocol-P identity was
generated and no Protocol-P statistic was computed.

---

## Summary

### What was accomplished

Codex's Session 39 blocked `AMENDMENT_A2_PROPOSAL_V6` / Protocol P v2.2 with nine
required changes. This session did four things:

1. **Checked every one of the nine at source before accepting it.** All nine hold.
   None was wrong. Two are worse than Codex's text stated, and I said so in the
   turn rather than accepting the gentler version.
2. **Built the override seam** that v2.2 had described but that did not exist, and
   verified it three ways — reach, fail-loud, and transparency — including a
   byte-for-byte reproduction of the delivered row through the patched path.
3. **Posted Protocol P v2.3** as one clean replacement (`+662 / −0`, header at
   transcript line 7,108), addressing all nine requirements explicitly and
   section by section.
4. **Wrote the regular Session-40 progress report** covering my Sessions 33–40.

### The two pins that were worse than stated

**The `_dataset0` suffix was not a mislabel; it inverted a safety claim.**
`assignment_generator.py:521` appends `_dataset0` to `base_pair_id`
unconditionally, and that string is what both the driving `OnlineSensorSession`
and `SensorModel.observe` receive — so it is the realized RNG identity. Codex
correctly reported that my advertised suffix-free identity was not what the named
construction produces. What Codex's text did not say, and what I found on
checking, is the consequence: v2.2 claimed a leaked screen row would fail the
manifest audit **because it lacked** the suffix. Under the construction named in
the same paragraph, the row would have **carried** the suffix, so the guard I
advertised would have passed the leak straight through. That is the third
instance of Standing Lesson 20 in this project — describing a guard by what I
wanted it to check rather than what it checks.

**The ramp override is not merely un-plumbed; it is unreachable.** Codex reported
no injection seam for four parameters. Checking each, I found peak and severity
*are* reachable without touching Codex's file (by building a modified in-memory
assignment document), which I rejected on provenance grounds. But the ramp is
reachable by **no route at all**: `_physical_config:338` computes
`duration / 2.0` from `cycles` and `frequency_hz`, so every possible input
yields exactly fraction 0.5. Ramp fraction 0.125 — the value every pre-dataset
screen used — cannot be produced by any document. That makes a code change
unavoidable rather than merely convenient, which is the argument for the typed
seam being the cheapest correct option and not just the tidiest.

### The seam — built, not promised

Prototyped in scratchpad against the committed module. The packet was not
touched. A frozen `ScreenOverrides` dataclass (`probe_peak_force_n`,
`probe_ramp_fraction_of_duration`, `physical_faults`, `realized_pair_id`,
`provenance_hash`), a `screen_pair_id()` helper that makes base-vs-realized
identity explicit, keyword-only `overrides=None` on `_physical_config` and
`_generate_reservation`, and a rule that an active override **must** carry a
provenance hash which then replaces the stamped `config_hash` — so an altered run
cannot carry the base config hash into a persisted record.

Verification, in increasing cost order:

```text
B  REACH (0 rollouts)
   overrides=None peak / ramp        == assignment value / duration/2   0.05 / 0.625
   peak override                     -> CableModelConfig                0.15
   ramp fraction 0.125               -> CableModelConfig                0.15625
   ramp fraction 0.5                 == delivered hard-code             0.625
   ramp 0.0 / 0.5000001 / 0.6 / -0.1 / nan          all rejected
   active overrides without provenance hash          rejected
   structural FaultSpec severity     -> plant._physical_config          0.75
   faulted plant builds a second softened model; healthy builds none
   identity override                 -> basepair_protocolp_stageAB_c4 exactly

C  LEAK GUARD (0 rollouts) — the guard fed the exact state, not described
   suffix-free row      -> "dataset pair_id lacks the dataset0 suffix"
   suffixed, unapproved -> "manifest reservation set differs from selection"

A  TRANSPARENCY (1 rollout, 26.4 s) — overrides=None on the delivered row
   privileged array fields byte-identical         20 / 20
   S observation arrays byte-identical            30 / 30
   realized pair_id unchanged by the patch
```

The `ramp fraction 0.5` line is the seam's own regression test: the single
fraction the current code can express is reproduced exactly, so the seam is a
strict extension rather than a reimplementation.

### Corrections adopted without argument

- **Finding J's ratio.** I had argued the unmatched-identity confound cancels
  between numerator and denominator because both use the same two rows. It does
  not: the two norms reduce **different time samples**, so the divergence enters
  each with its own 0.8 Hz content, and a norm is not additive in the two terms
  anyway. "Cancels" and "clean" are withdrawn. The 2.37–3.64× is now labelled
  as the ratio of the **total unmatched-row** difference between two windows,
  not a fault-effect multiplier. The probe-start origin is retained on purely
  prospective grounds (config-derived, contains the whole declared burst, fixed
  before any response is seen).
- **`Q95_c^gauge`.** My claim that it distinguishes "no mechanical signature"
  from "closed-loop divergence dominates" was the stronger error — it is Codex's
  own argument for why M2 was a decomposition and not a bound, which I had
  already accepted and then spent anyway. Narrowed to a conditional healthy-null
  diagnostic with no mechanism attribution and no authority.
- **Replay-gate localization.** "Look above the generator, not inside it" is
  removed. One zero-override healthy row cannot validate an override path that
  did not exist when the gate ran.
- **`assert` under `-O`.** Adopted globally; twelve named decision-bearing
  invariants now use explicit `raise ProtocolPError`. `assert` survives only in
  `tests/`.

### Independent verification of Codex's own numbers

Per Standing Lesson 2, I re-derived rather than trusted:

- Both retained reference hashes match Codex's exactly
  (`ed5b1f39…b65e45` plant, `cdde17f6…86bb4c83` observation).
- The approved assignment file SHA-256 is
  `76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae`, and the
  full `approved_assignment_hash` is
  `dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1` — both
  now pinned into the provenance recipe rather than carried truncated.
- **One number reconciled before it could look like a contradiction.** Codex
  reported 38/38 S payload arrays; I report 30/30. Same record, two flattenings:
  the npz carries 38 keys = 30 per-channel arrays (5 dicts × 6 channels) + 8
  metadata entries (`schema_version`, `suite`, `run_id`, `pair_id`,
  `config_hash`, `split`, `channel_names`, `suite_available_mask`). v2.3 pins the
  38-key form, because it is the persisted object and it contains `pair_id` and
  `config_hash` — which is exactly why the provenance requirement matters.

## Challenges and how they were overcome

### A requirement that appeared to conflict with a standing prohibition

Codex required v2.3 to "define an executable, typed screen-override seam" while
keeping "Protocol P implementation or execution" unauthorized. Taken literally,
those pull against each other: a seam is code, and code is implementation.

Resolved by splitting the object from its authorization. The seam is **specified**
in the pre-registration as an exact patch (signatures, validation, and the lines
that change), and **verified executable** in scratchpad — not applied to the
packet, not run on any Protocol-P identity, and not used to compute any
Protocol-P statistic. That respects the block while making the word "executable"
mean something checked rather than asserted. It is also Standing Lesson 14's
corollary applied deliberately for the fifth time: making a specification
executable is itself the defect-finding technique. It found one more defect
this session (below).

### A defect the prototype found that no amount of reading would have

Writing the seam surfaced something neither agent had raised: when
`physical_faults` is overridden, `_fault_components` still returns the *source
reservation's* label, so a screen run built on a healthy reservation would
describe itself as healthy while its plant carries a structural fault. Protocol P
never persists a screen record and never reads a screen label, so I did not patch
it — but I named it in the turn and handed the scope decision to Codex rather
than leaving a mislabeled-record footgun for whoever first persists an overridden
run. My judgement is that it belongs to that future consumer, not to Protocol P;
Codex owns the file and may disagree.

### Two probe errors of my own, both caught by the probe rather than by review

The first run of the verification script failed on the structural-fault check
because I read `_fault_config`, an attribute that does not exist. The real path is
`CablePlant._physical_config`, replaced via `dataclasses.replace` at
`cable_plant.py:99-103`, with the softened MuJoCo model built separately at
`:118-121`. Fixing it produced a *better* check than I had written: the evidence
that the override reaches the physics is that the faulted plant builds a second
softened model and the healthy plant builds none — a structural fact, not a field
read.

The same read taught me something I had half-wrong in my own notes. The healthy
plant's `structural_ei_remaining` reads 0.50, which looks alarming next to a
fault severity of 0.75. It is inert: the healthy model is built with
`softened=False` and never consumes the field. Only the fault path sets it, and
the fault's severity *is* the remaining-EI fraction. The dataclass default is
dead in the healthy branch. Worth knowing before I quote either number.

## Important decisions

1. **Adopt all nine requirements rather than negotiate any of them.** Every one
   survived a source check. Arguing a correct pin costs a round-trip and buys
   nothing; this is the fourth block on this protocol and the convergence cost is
   already the thing I am watching.
2. **Choose the suffix-free screen construction** over accepting the generator's
   `_dataset0` suffix (Codex's requirement 3 offered both). Reason: it makes the
   leak guard real rather than rhetorical. Tested both tripwires — the suffix
   assertion at `assignment_generator.py:241-242` and the approved-set comparison
   at `:244` — and observed both raise on the exact state.
3. **Require a provenance hash whenever any override is active**, and stamp it in
   place of the base config hash. A screen run therefore cannot masquerade as a
   base-config run in a persisted record. `dev-` prefix retained so screen
   artifacts stay ineligible for confirmatory analysis.
4. **Keep the packet untouched.** The patch changes code Codex owns; it goes in
   as a reviewable diff after approval, not as a fait accompli inside a protocol
   proposal.
5. **Build the screen reservation by copying the delivered dev reservation for
   the target context cell and replacing exactly two fields** (`sensor_seed`,
   `base_pair_id`), with every other field asserted equal to its source. The
   ladder fault enters only through the override, so the assignment catalog is
   never mutated.
6. **Do not soften the odds.** Case B and Case C remain roughly comparable, and
   one of S38's reasons for leaning toward Case B — Finding J's ratio — is now
   unavailable. That is a downward revision on top of last session's downward
   revision, and it is stated as such in the progress report and the public log.

## Reasoning paths explored

- **Whether any of the four overrides could avoid touching Codex's file.** Peak
  and severity can, via a mutated in-memory assignment document; rejected because
  it is precisely the provenance failure requirement 4 targets. Ramp cannot, by
  any route. Identity cannot. So the code change was forced, and the typed seam
  became the cheapest correct option rather than a preference.
- **Whether to accept the `_dataset0` suffix instead of overriding it.** Accepting
  is less code. Rejected because the leak guard would then rest on the
  approved-set comparison alone, and the suffix assertion — a cheap, independent
  tripwire — would be permanently unavailable to the screen. Two guards for one
  extra field is a good trade.
- **Whether Finding J's ratio could be salvaged with a matched-window argument.**
  It cannot. Any version of the claim requires the nuisance term to be equal
  across two different time reductions of the same rows, and nothing supplies
  that. I looked for a weaker true version and found only the descriptive one
  Codex named, so I adopted that.
- **Whether the label-stamp gap belongs in Protocol P.** Decided no — Protocol P
  neither persists nor reads a screen label — but decided that "not mine" is not
  a reason to leave it unsaid.
- **Whether a third same-day public log entry is justified.** The playbook warns
  against a session-by-session journal. Judged yes on one ground: Codex's
  correction entry leaves the public record showing a blocked protocol with the
  corrections unresolved, and a reader stopping there sees an open dispute. One
  lean entry closes that loop and carries the guard error, which is exactly what
  the log exists for.

## Insights gained

1. **STANDING LESSON 25 (new) — a guard's claimed scope must be tested against
   the construction that will actually run, not against the construction you had
   in mind.** v2.2's leak guard was not merely mislabeled; it was inverted,
   because the identity it was written for and the identity the named function
   produces differ by one suffix. A guard is a claim about a *specific* input
   distribution, and naming a construction changes that distribution. Third
   instance of the guard family (rank guard S39, necessary-vs-sufficient S38),
   and the first where the flaw was in the interaction between two things I had
   both written correctly in isolation.
2. **A private function is an authority, not an interface.** Naming
   `_generate_reservation` fixed Finding K's construction gap and simultaneously
   created a new one, because the function transforms identity and hides
   candidate-defining parameters below its signature. "Use the real code" is
   necessary but not sufficient; the protocol also has to name what the real code
   does to its inputs.
3. **The cheapest regression test for an extension is the one behaviour the old
   code could already express.** Ramp fraction 0.5 is the only fraction the
   current generator can produce, so asserting the seam reproduces it exactly is
   a complete proof that the seam is a superset. I would not have thought to look
   for that test if the hard-coded value had been anything less convenient.
4. **A dataclass default can be dead in one branch and load-bearing in another,
   and reading it without the branch is how you misquote it.** `structural_ei_remaining
   = 0.50` on a healthy plant means nothing at all.
5. **Convergence cost is itself a signal worth reporting.** Four blocks on one
   protocol is either a rigorous review loop or an author who keeps
   mis-specifying. I believe the former — every block found a defect that would
   have contaminated a measurement, and finding them before spending 76 minutes
   of simulation is the cheapest possible timing — but I wrote the
   counter-argument into the progress report rather than only the flattering
   reading, and committed to escalating to the director rather than looping a
   fifth time if round five does not converge.

## Verification

```text
seam prototype                       all checks PASS (see the table above)
one-row transparency replay          20/20 privileged, 30/30 S arrays, 26.4 s
retained reference hashes            both match Codex's, independently computed
assignment file SHA-256              76255a80…514ae, recomputed this session
transcript append hard gates         4 / 4 passed
  pre-write lines                    7,107
  pre-write SHA-256                  FA21BD45773E62B0CE00162A959BB77C04AB3DDD09374F4DFE350F42C2BEF754
  post-write lines                   7,769
  Session-40 header                  line 7,108, occurring exactly once, after the boundary
  transcript diff                    +662 / -0
Codex's S39 append (monitoring duty) 6,853 -> 7,107, +254 / -0, header at 6,855
                                     after the boundary — CLEAN. Streak: six.
                                     No monitoring note filed (duty is recurrences).
live git state at session start       Codex Session 39 (554a54a) had landed after
                                     my snapshot — Standing Lesson 5 holds for the
                                     thirteenth consecutive session.
```

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended Protocol P v2.3 and the point-by-point response (`+662 / −0`).
- `agents/Claude/Progress Reports/Progress Report Session 40.md`
  — **new.** Regular per-agent progress report covering Sessions 33–40.
- `README.md`
  — one running-log entry (append-only; no prior entry rewritten).
- `agents/Claude/Session Summaries/HumanReport40.md`
  — this report.
- `agents/Claude/README.md`
  — navigation and current-state refresh.
- `agents/Claude/Summary of Only Necessary Context.md`
  — completely rewritten for Session 41.

**No Reproducibility Packet source, config, schema, result, or test file was
changed.** The seam prototype lives in the session scratchpad
(`probe_s40_seam.py`, `append_turn.py`, `turn_s40.md`) and is deliberately not
committed: it is a change to code Codex owns and goes in as a reviewable diff
only after approval. `references.md` gained no entry — no external source was
read this session.

## Next steps

**Codex owns the next turn:** exact-state review of Protocol P v2.3.

If v2.3 is approved, my order is:

1. Apply the §2 patch to `assignment_generator.py` and post the diff for review
   **before** anything runs — it is Codex's file.
2. Run the stop-or-go replay gate (1 rollout). If the pinned reference hashes do
   not match, or byte equality fails, nothing else runs.
3. Stage 0 (0 rollouts) → Stage A (108) → Stage B (32) → Stage C (28).
   169 rollouts, ~76 min at the 26.4 s/rollout measured this session. Background
   job; poll the results JSON, not the log.
4. Codex reviews the implementation, the result, and the branch before any
   written amendment.

Two open items I am carrying, neither blocking:

- **The label-stamp scope question** handed to Codex at the end of §2.
- **The convergence commitment:** if round five does not close, escalate to the
  director instead of looping.

**Nothing is blocked on the director.** `director_requests.md` entry 1 (Claim
Sheet review) remains open and explicitly non-blocking.
