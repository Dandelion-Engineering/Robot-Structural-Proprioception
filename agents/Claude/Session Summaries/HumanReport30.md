# Human Report — Claude Session 30

**Current date and time:** 2026-07-24 12:52 PDT
**Phase:** Phase 2 — Execution
**Session role:** Cross-review of Codex's Session-29 Gate-3 assignment (the experiment's pre-registration)
**Final config state:** **UNFROZEN** (no `config.json`; every trace `dev-*`)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

---

## Summary

This was a review session, and the single most consequential review in the project so far. Codex ran its Session 29 *after* my Session 29 — Standing Lesson 5 again: the startup snapshot showed `Codex Session 28` as `HEAD`, and the live `git log` showed `069e91e Codex Session 29`. In that session Codex closed the Gate-2 role-write loop on my S29 approval and then built **the Gate-3 assignment**: the complete pre-registration of the confirmatory experiment — every fault setting, every trajectory, every background condition, and the deterministic assignment of all of it to `dev` / `pilot` / `val` / `test`. Codex handed me the exact state and asked for `APPROVE_GATE3_ASSIGNMENT_V0_1` or `BLOCK_GATE3_ASSIGNMENT_V0_1` with file/line findings.

This is the checkpoint my own last two sessions flagged twice as needing one recorded **joint** approval before any headline model is fit. It is the moment the experiment's design becomes unfalsifiable-after-the-fact, so it is the moment to be hardest on it.

**Outcome: I blocked it — `BLOCK_GATE3_ASSIGNMENT_V0_1` — on one finding, with a tested remedy and three non-blocking notes. I made no edits to any review-target file.** The blocking finding is that the assignment's deterministic rotation of background conditions leaks fault identity into the observations, and leaks it **only to the structural-sensing suite** — which would have inflated the project's own headline number in the direction of its own hypothesis.

## What the artifact under review is

Codex's Session-29 commit `069e91e` added, in `Reproducibility Packet/`:

- `config/proposed-gate3-assignment-v0.1.json` — the self-hashed pre-registration (821 lines);
- `scripts/utils/gate3_assignment.py` — strict loader, canonical hashing, grid expansion, deterministic reservation expansion, semantic validator (899 lines);
- `scripts/validate_gate3_assignment.py` — read-only CLI;
- `tests/test_gate3_assignment.py` — 15 adversarial tests;
- plus a Step 2B section and boundary update in the packet `README.md`, and a `utils/__init__.py` entry.

It reserves **656** whole scenario/fault realizations (dev 76, pilot 76, val 168, test 336), declares five model-training seeds, keeps both generation permissions `false`, and materializes zero test payloads.

## What I did — a genuine review, not a rubber stamp

**Reproduced Codex's exact state and every number it reported.** Both file SHA-256 values in Codex's 10:29 replacement handoff match byte-for-byte (`gate3_assignment.py` = `8d095fea…c1880`, `test_gate3_assignment.py` = `00ea52fc…3569b`). Focused suite **15 passed**; full packet **373 passed in 9.11 s**; the read-only validator emits assignment hash `dev-5939ff5f…0cedb` bound to draft-config hash `dev-0211f2e7…6180`, reservations 76/76/168/336 = 656, projection 13,120, both permissions `false`, `test_reservations_materialized: 0`.

**Read the whole assignment and the whole validator, line by line**, and checked the properties that matter for a pre-registration rather than the ones that are easy to check: whole-trajectory and whole-fault-setting split ownership; no known fault tuple reused across any pair of splits (verified against the actual severity grids); suite never an input to split assignment; the common-random-number field set; the ≥5-seed floor; the compound/OOD label convention and its `ood_flag` metric-routing rule; the lifecycle interlocks and the self-hash binding.

**Independently verified Codex's one declared limitation instead of taking it on trust.** Codex restricted structural faults to zero-based location `1` and called that "the executable" location. I checked the plant: `scripts/utils/cable_plant.py:124-125` hard-rejects any structural location outside `{-1, 1}`, and softening is a whole-model swap driven by a single `structural_ei_remaining` parameter. So it is a genuine plant constraint, not an unforced narrowing, and the assignment declares it honestly.

**Then I probed the design for shortcuts** — the class of defect a passing test suite cannot catch, because the tests check that the rules were followed, not what the rules imply.

### The blocking finding

Every split owns exactly two payloads, two temperature profiles, and two contact profiles, so all three rotations in `expand_reservations` are taken mod 2. At that catalog size, the two coefficients that were meant to decorrelate them are dead arithmetic: `2 * fault_index` at `gate3_assignment.py:650` is always even, as is `2 * trajectory_index` at line 656. What survives is

```text
payload XOR environment = fault_index % 2   —   constant within every fault setting
```

I expanded the tracked assignment and measured it rather than trusting the algebra: **payload is a perfect deterministic function of environment in 80 of 80 fault settings**, in all four splits, and only 4 of the 8 payload×environment×contact cells are realized per setting.

Two consequences, both of which transfer from `dev` into `test` because the known settings occupy identical enumeration indices in every split:

1. **`healthy` — one of the four scored classes — is a priori impossible on ~47.6% of runs** (dev 36/76, pilot 36/76, val 80/168, test 160/336), because it is a single setting at index 0 and therefore only ever occurs in two of the four cells.
2. **Within structure and actuator, the alignment bit perfectly identifies which of the two severity levels is present, with the same polarity in dev and test.** A model that learns "bit 1 means more severe" on development data carries it straight into the confirmatory set — contaminating the severity rung that feeds the recovery controller.

The reason this is blocking rather than a note is that the leak is **not symmetric between the arms being compared**. Temperature enters the observation stream in exactly one place — the thermal apparent-strain term at `sensor_model.py:423-424`, 10 µε/°C, applied to `gauge_obs` — and `gauge_obs` is S-exclusive (`schema_types.py:108-111`). C0 and C1 have no temperature channel at all. So S can read both bits and compute the alignment; C1 structurally cannot. The pre-registered bar is a paired **S − C1** macro-F1 improvement of ≥0.05 absolute, and this design would have handed S a free fault-identity cue on roughly half the runs — inflating the estimand in the direction of the hypothesis, in a way no outside reader could later separate from a real effect.

### The remedy I proposed (and tested before proposing it)

Drop `fault_index` from all three rotations and index a fixed balanced context-cell table by `k = trajectory_index * realizations + replicate`. I prototyped it against the tracked assignment: every fault setting then sees an **identical** context-cell set, so the association goes to exactly zero rather than merely down — and coverage *improves*, from 4 of 8 cells per setting to the full 8 in both `val` and `test`. I also asked that the property become an enforced validator invariant (the current validator checks that every profile is *used*, at lines 862-867, but not how profiles combine), so it is defended by the suite rather than by arithmetic that happens to work out.

## Challenges and how they were overcome

The finding was not visible from reading. The formulas look decorrelated — they contain distinct coefficients on distinct indices — and all 15 of Codex's adversarial tests pass. It only appears when you notice the catalogs have exactly two members and carry the mod-2 arithmetic through. I found it by refusing to review the rotation as text and instead expanding all 656 reservations and asking directly: *for each fault setting, which context cells actually occur?* That is Standing Lesson 2 (audit from the artifact, not the summary) applied to a design rather than to a result.

I also deliberately checked the finding's severity in both directions before blocking, because a reviewer who inflates findings is as costly as one who misses them. I confirmed contact is *not* aliased (only payload/environment are), that structure/actuator/sensor each span both alignment values so only the single-setting `healthy` class is fully compromised at class level, and that the severity leak is real by printing the per-setting mapping for dev and test side by side.

## Important decisions and reasoning

- **Blocked rather than approving with a condition.** The review cycle admits exactly two answers, and a defect that biases the headline estimand toward the hypothesis cannot be carried as a forward note. Test identities lock at approval; this is the last cheap moment to fix it.
- **Proposed a remedy but did not apply it.** `gate3_assignment.py` is Codex's file and Codex is the owner of this artifact. A reviewer who edits the artifact forces the owner into a re-review of a state the reviewer authored, which is the loop the review-cycle playbook exists to avoid. Codex implements, owns, and re-hands off.
- **Bundled every finding into one turn** rather than dripping them across round-trips — one blocking finding, three non-blocking notes (`split_group_id` is unique per reservation so its manifest-audit guarantee is vacuous; the OOD arm rests on only two compound settings per split; test severities sit partly outside the fit hull, which matters for the severity regression head and not for classification).
- **Offered to pre-register one interpretation rule in my own lane.** Every confound axis escalates monotonically dev → pilot → val → test, and test is the most extreme rung on all three at once. That is a good design, but it means a null at test has two causes — the hypothesis failing, or nothing generalising that far — and the Claim Sheet requires separating hypothesis failure from method failure. I proposed recording now, before any fit exists, that the paired contrast is reported at every rung and a test null counts as hypothesis failure only if the contrast is present at the earlier rungs. Better settled before we are looking at a number.

## Insights gained

- **A passing adversarial test suite certifies that the rules were followed, not that the rules are right.** All 15 tests, the hashes, the interlocks, and the counts were correct; the defect was in what the correct rules jointly implied. Reviewing a pre-registration means simulating the design's consequences, not verifying its internal consistency.
- **Dead arithmetic hides in small catalogs.** `2 * fault_index` reads as decorrelation and is identically zero mod 2. Any formula whose behaviour depends on a catalog size should either assert that size or be replaced by an explicit table.
- **The dangerous confound is the one that favours you.** A leak that hurt the hypothesis would have shown up as a disappointing result and been investigated. This one would have shown up as a *win*, which is precisely the condition under which nobody looks harder.

## Files created

- `agents/Claude/Session Summaries/HumanReport30.md` (this file)

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my `BLOCK_GATE3_ASSIGNMENT_V0_1` review turn, appended at the verified physical tail (**+96 / −0**, four gates asserted, turn physically last)
- `README.md` (Live-Run) — banner date to 2026-07-24 and one running-log entry recording the blocked pre-registration in plain language
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout

## Files deliberately not changed

- Every Gate-3 review-target file — a reviewer does not edit the artifact under review; the tracked state is byte-identical to Codex's handoff
- `Reproducibility Packet/config/draft-config-v0.1.json` and `config.json` (absent) — the freeze stays blocked
- `agents/Claude/references.md` — no external sources were read this session
- `.gitignore` — no new artifact class; my probes live in the session scratchpad and are not committed

## Review state at closeout

- **OPEN:** the Gate-3 assignment loop, blocked at my Session-30 review. Codex owns the next turn: address the rotation finding, re-hash the assignment, and re-hand off the replacement state for my exact-state decision.
- **CLOSED and not to be reopened:** Gate-1 / Gate-2 foundation (my S28), Gate-2 role-write path (my S29), Config-Freeze Readiness Review (S27), actuator-action (S26), class-probability (S25).
- **Monitoring duty: clean.** Codex's three Session-29 appends were a verified `+61 / −0` pure tail addition (2608 → 2669), Codex physically last. Eighth consecutive clean append; nothing added to the monitoring thread.

## Next steps / pending for future sessions

1. **Codex Session 30** revises the context rotation, ideally adds the "identical context-cell set across all fault settings" validator invariant, recomputes the assignment hash, and re-hands off.
2. **My Session 31** re-reviews that replacement state on the same standard — expand the reservations and measure the association directly, not read the formulas — and, if it holds, records the one joint pre-registration approval that unblocks Gate 3.
3. Only then does my own lane open: Gate 4 (`TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface) and Gate 5 (calibration/abstention/OOD/uncertainty on validation only). **No model, no data, ahead of the approved assignment.**
4. `config.json` stays absent. No partial freeze.
5. My next regular progress report is Session 32 — unless a phase transition or an approved Claim-Sheet amendment triggers one sooner.
