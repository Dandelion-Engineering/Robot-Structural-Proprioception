# Human Report — Claude Session 31

**Current date and time:** 2026-07-24 13:58 PDT (session work); report written 2026-07-24 14:05 PDT
**Phase:** Phase 2 — Execution
**Session role:** Reviewer — re-review of the corrected Gate-3 assignment I blocked last session
**Final config state:** **UNFROZEN** (`config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION` (unchanged)
**Session decision:** `APPROVE_GATE3_ASSIGNMENT_V0_1` — **Gate 3 is now CLOSED at joint same-state approval**

---

## Summary

### What this session was

Last session I blocked the experiment's complete pre-registration — the Gate-3 assignment — because the rule that hands background conditions out to runs leaked fault identity, and leaked it only to the suite the project exists to test. Codex accepted the diagnosis in its Session 30, implemented the remedy, strengthened it beyond what I asked for, and handed back a replacement state. This session was the re-review of that state, and the decision on whether the project's pre-registration can be locked.

**I approved it. Gate 3 is closed.** That is the single most consequential thing that happened: the experiment's blueprint is now fixed and both agents have explicitly approved the same bytes of it. Generation of development, pilot, and validation data is authorized. The one-shot confirmatory test set remains untouched and unmaterialized.

### How I reviewed it — the part that mattered

The lesson I wrote down last session was that the defect had been invisible to every internal-consistency check: Codex's 15 adversarial tests, its hashes, its counts, and its lifecycle interlocks were all correct. The flaw lived in what the correct rules *jointly implied*. I only found it by expanding all 656 planned runs and asking what actually occurs.

So I refused to review the fix by reading the new formula and agreeing that it looked right. I rebuilt the audit and re-ran it on the corrected state, plus new checks aimed at what the fix itself could break.

**The blocking defect is gone, and "gone" here is an exact number rather than a judgement:**

| measurement | blocked state (S30) | approved state (S31) |
|---|---|---|
| distinct context-cell distributions per split | 2 | **1** (all four splits) |
| mutual information, fault setting → context cell | > 0 | **0.0000000000 bits** (all four splits) |
| fault settings with `payload XOR environment` locked | 19/19, 19/19, 21/21, 21/21 | **0/19, 0/19, 0/21, 0/21** |
| runs in a cell `healthy` can never occupy | ~47.6% (160/336 at test) | **0.00%** (all four splits) |
| alignment bit separates severity, dev→test | yes, same polarity | **no** — every setting sees both values |
| context cells realized per fault setting | 4 / 4 / 4 / 4 | **4 / 4 / 8 / 8** |

Mutual information of exactly zero is the strong form: the background conditions carry no information about the fault anywhere in the design, rather than merely less. Coverage also improved as predicted — validation and test now realize the complete eight-cell factorial per fault instead of half of it.

**One check I had not run before, and which I now think belongs in every pre-registration review.** I re-derived the entire 656-row expansion straight from the JSON, with my own loop reading the table and the index rule out of the document's own `expansion_rule` prose — then diffed it row for row against the packet's `expand_reservations`. Identical, 656/656. This is the check that proves the *pre-registered description* and the *code that will generate the data* are the same object. That property was silently false in the blocked state: the prose claimed a decorrelating rotation and the arithmetic delivered the opposite. A pre-registration whose text and code disagree is not a pre-registration, and nothing in the test suite was positioned to notice.

**Everything else reproduced exactly.** All four declared SHA-256s matched byte-for-byte. I recomputed the canonical assignment hash with my own serializer rather than calling the packet's helper — exact match on `dev-70832daa…65de`. Focused suite 18 passed; full packet 376 passed in 9.11 s; the read-only validator reproduced every field. Reservations 76/76/168/336 = 656, projection 13,120, both generation permissions `false`, zero test reservations materialized, no `config.json`, no `data/`. Compound/OOD settings share the identical distribution as known settings, so the out-of-distribution rows are not separable by context either. 656 unique scenario IDs, 2,624 seed values with zero collisions, zero known fault tuples reused across any split pair.

**Codex's strengthening was better than what I proposed.** I asked for an invariant requiring every fault setting to see the same *set* of context cells. Codex implemented same *distribution* — same cells at the same frequencies — correctly observing that equal sets with unequal counts still leak. It also bound the balanced cell table inside the self-hashed assignment JSON instead of leaving it as a code convention, so the property is part of what the hash certifies rather than something a future edit could quietly drift from. Both changes are improvements on my proposal and I said so.

### The finding I did make — and why it is a note and not a block

The fix could not avoid introducing one association, and I measured it: **in development and pilot only, the payload is a deterministic function of which trajectory the arm runs** (mutual information 1.000 bit; 0.000 bits in validation and test, on all three axes).

Before raising it I checked whether it was avoidable, by brute-forcing every possible 4-cell design over the 2×2×2 condition space:

```text
designs satisfying BOTH pairwise balance AND no-trajectory-alias : 0
designs satisfying pairwise balance only                         : 2
designs satisfying no-trajectory-alias only                      : 6
```

The two properties are mutually exclusive at two repeats per trajectory, and the reason is clean: pairwise balance forces a constant-parity set (only two exist), while breaking the trajectory alias on all three axes forces each trajectory's pair of cells to be bitwise complements, which flips parity. So this is a forced trade-off, not an oversight — in Codex's implementation or in the table I proposed last session.

**And the other side of the trade is worse for this specific experiment.** The best no-alias alternative aliases payload with *environment* — and environment is the thermal axis, which reaches the observation stream only through the strain gauges, the channel only the structural suite has. That would correlate the confound the treatment arm reads most strongly with the channel that defines the treatment arm. Pairwise balance was the right side of the trade.

**Direction of harm decided the call.** Payload is far more legible in the structural suite than in the conventional one. A model trained where payload is predictable from the excitation pattern can absorb it by conditioning on trajectory instead of learning payload-invariant fault features; at validation and test that shortcut breaks, and it breaks harder for the arm with the more payload-sensitive channels. **It cannot inflate the paired S − C1 contrast; it can only depress it.** That is exactly the standard I applied when I blocked last session — the disqualifying property there was that the leak *favoured* the hypothesis — so applying the same standard consistently makes this one a recorded limitation.

What it does cost is null attribution: if the structural suite does not clear the bar, "training-split payload aliasing" becomes a live alternative explanation alongside genuine hypothesis failure, and the Claim Sheet requires separating hypothesis failure from method failure. Given that this project's evidence keeps landing on the diagnostic-only shape, the null is the outcome most likely to need defending. So I recorded the clean remedy with a recommendation rather than burying it: raising development and pilot repeats from 2 to 4 makes both properties hold simultaneously (each trajectory then gets its own parity coset, every axis varies within every trajectory, and each split becomes a complete factorial), at a cost of 656 → 808 reservations, about 23% more simulation. **I explicitly did not block on it and explicitly did not ask Codex to do it** — Codex owns generation cost, so it owns that call, and I approve either way.

**It also interacts with the interpretation rule Codex accepted last session.** Pilot shares development's aliasing; validation and test do not. So the pilot→validation step of the degradation ladder changes two things at once — the confound severity escalates *and* the aliasing disappears — and a contrast that decays there is not cleanly attributable to the confound rung alone. I flagged that I will state it explicitly when I implement the rule in the Gate-7 evaluation driver, rather than letting the ladder read as a clean single-variable escalation.

## Challenges and how they were handled

**The main challenge was deciding whether to block a second time.** I found a real, measurable, avoidable-in-principle design flaw in the corrected state. The instinct after a successful block is to block again. I worked the decision instead of following the instinct, and three things settled it: the flaw is mathematically forced at the planned budget (I proved that rather than assuming it); its direction is conservative, so it cannot manufacture the result we are testing for; and it lives in the training and method-gate splits, while the splits whose identities actually lock at approval — validation and test — measured completely clean on every axis. Blocking a sound artifact over a conservative-direction limitation would have been the review cycle looping rather than converging, which the playbook warns about explicitly at roughly this point (this was round-trip three on one artifact).

**The second challenge was resisting the symmetric error** — approving too easily because the fix addressed my finding. The guard against that was refusing to accept the new formula on inspection. The row-for-row re-derivation from the JSON and the zero-mutual-information measurement are what make the approval evidence-backed rather than deferential, and they are also what turned up the trajectory alias that a formula reading would have missed entirely.

**A small operational one:** my first invocation of the read-only validator used a flag name that does not exist (`--draft-config`); the script failed loudly with a usage message and I corrected it to `--config`. Worth recording only because that is the software standard working as intended — a script that fails loudly on wrong input rather than silently running against a default.

## Important decisions

1. **`APPROVE_GATE3_ASSIGNMENT_V0_1` on the exact replacement state**, closing Gate 3 at joint same-state approval. This is the project's pre-registration, and it is now locked.
2. **The trajectory-payload alias is a declared limitation, not a blocking condition** — decided on direction of bias (conservative), on locked-versus-amendable scope (training splits, not confirmatory), and on a proof that it is unavoidable at the planned budget.
3. **The 2 → 4 repeat remedy is offered as a non-blocking amendment Codex owns**, with my recommendation in favour, rather than imposed as a review condition.
4. **The pilot-versus-validation structural difference will be stated in the Gate-7 driver** when I implement the degradation-ladder interpretation rule, so the ladder is not reported as a single-variable escalation.
5. **No edits to any review-target file.** The tracked state is byte-identical to Codex's handoff, so the approval names exactly the state Codex approved.

## Reasoning paths explored

- **Could the alias favour the hypothesis by any route?** I worked through the evaluation side and satisfied myself it cannot: both arms are scored on the same validation/test rows in a paired design, so the confound structure at evaluation is identical for both, and the pairing is preserved. The only asymmetry is in training exposure, and that runs against the structural suite because it carries the more payload-sensitive channels.
- **Is a fix available that keeps both properties at the current budget?** Brute-forced; the answer is no, with a parity argument explaining why. This is the reasoning path I am most glad I ran, because I very nearly raised the alias as a defect Codex should have avoided, which would have been wrong.
- **Is the alternative design better?** No — it aliases payload with temperature, which is worse for this experiment specifically. Checking the alternative rather than assuming a fix exists is what turned the finding from an accusation into a trade-off.
- **Does closing Gate 3 trigger a progress report?** No. The triggers are every eighth session (mine is next at Session 32), a phase transition, or an approved Claim Sheet amendment. Gate 3 is infrastructure inside Phase 2 and the assignment is not the Claim Sheet, so no report is due. I checked rather than assumed.

## Insights gained

- **The check that should have existed all along is "does the pre-registered text generate the pre-registered data?"** Re-deriving the expansion from the document's own prose and diffing against the code is cheap, and it is the check that would have caught the original defect one session earlier. In the blocked state the prose said "decorrelating rotation" and the arithmetic said the opposite; nothing in a 15-test adversarial suite was positioned to notice, because every test verified the code against itself.
- **A reviewer needs a consistent standard for blocking, and direction of bias is the right one.** I blocked in Session 30 because the flaw favoured the hypothesis and would have been unfalsifiable after the fact. Applying the identical test here yields "note, not block". Using a different standard the second time — blocking because I *could* — would make the review process unpredictable, which is worse for the project than either individual call.
- **Check that a flaw is avoidable before you report it as one.** The brute-force search changed the finding from "you should have avoided this" to "this is a forced trade-off and you took the right side of it", which is both more accurate and more useful. That check cost about five minutes.
- **A conservative confound is not free.** It cannot manufacture a win, but it degrades the interpretability of a null — and on this project the null is the likely outcome. Recording it now, before any number exists, is what keeps it a pre-registered expectation rather than a post-hoc excuse.

## Files created

- `agents/Claude/Session Summaries/HumanReport31.md` — this report.

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session-31 approval turn, appended at the physical tail (`+93 / −0`, verified).
- `README.md` (root, Live-Run) — one running-log entry: the corrected blueprint was re-audited by measurement and jointly approved; the leak is exactly zero; one conservative-direction training-split limitation declared; generation authorized for development/pilot/validation only.
- `agents/Claude/README.md` — workspace index: Gate-3 state, the Session-31 review, monitoring result, packet test count 373 → 376, report range through `HumanReport31.md`.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten resume state.

## Files deliberately not changed

- **Every Gate-3 review target** — `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`, `scripts/utils/gate3_assignment.py`, `scripts/validate_gate3_assignment.py`, `tests/test_gate3_assignment.py`. As reviewer I made no edits, so my approval names exactly the state Codex approved.
- `Reproducibility Packet/config/draft-config-v0.1.json` — Codex embeds the approved assignment and recomputes the draft hash; that is its next turn, not mine.
- Final `Reproducibility Packet/config.json` — remains absent. Nothing this session moves the freeze.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` — the check was clean, and the duty is to flag recurrences. A clean-check note was already recorded in Session 23; adding one every session would bloat a director-facing thread.
- `director_requests.md` — nothing this session requires the director.
- `agents/Claude/references.md` — no external source was read this session. It remains without entries for Sessions 20–31, which are reproduction, construction, measurement, and review sessions.

## Cross-review performed

I read Codex's `agents/Codex/Session Summaries/HumanReport30.md` in full and its Session-30 turn in the active Phase-2 transcript, then verified its claims against the artifacts rather than the summary: all four SHA-256s, an independent canonical-hash recomputation, both test suites, the read-only validator, the packet README wording change, and the git-level diff of its commit. I re-audited the corrected design by direct measurement on the expanded reservations, and re-derived the expansion independently from the JSON to confirm the documented rule and the code agree. I also verified the lifecycle boundary held at the filesystem level — no `config.json`, no `data/` directory.

## Monitoring duty

Clean, and this is the **ninth consecutive clean append**. Codex's Session-30 turn was a verified `+90 / −0` pure tail addition (2765 → 2855 lines), diff hunk anchored at 2763, exactly one Session-30 header at line 2769, Codex physically last. Nothing inserted mid-file. No note added to the monitoring thread — the duty is to flag recurrences, and the thread already records that the rule works.

My own turn was appended with a rebuilt binary end-of-file writer enforcing four gates before it will leave the file in place: marker absent before the write, prior bytes an exact prefix afterwards, marker occurring exactly once and after the recorded boundary, and the new turn physically last, with automatic rollback on any failure. It recorded `+93 / −0`, confirmed at the git level.

## Where the project stands

**Gate 3 is CLOSED.** The seven-gate freeze path now reads: (1) schema and config authority ✓ → (2) role-separated storage foundation ✓ → (2) role write path ✓ → **(3) multi-setting design and manifest ✓ (this session)** → (2) live generator and role-completeness audit **[Codex, next]** → (4/5) matched learned models and calibration on validation **[mine]** → (6) controller protocol and sample size **[shared]** → joint immutable config freeze → one-shot confirmatory generation and evaluation (7) → Phase 3.

Still forbidden and unchanged: final `config.json`, materializing any test identity or payload, headline model fitting, and any claim that Gate 2 or the config freeze is complete.

## Next steps

1. **Codex** embeds the approved assignment into the draft config, recomputes the draft-config hash, and builds the real assignment-driven generator paths (distal payload, split-owned environment, contact-window scheduling, compound plant-plus-sensor faults), then runs the generated-data role and leakage audit with draft-state test refusal active. It also decides on the non-blocking 2 → 4 repeat amendment.
2. **Me, next session:** verify the live git state first (the startup snapshot has now lagged four sessions running); read Codex's newest report and the Phase-2 chat tail. If Codex has taken the 2 → 4 amendment, re-review that new state the same way — expand, measure, re-derive. If it has declined, record the limitation as settled pre-registration and carry it into the Gate-7 plan.
3. **My lane opens once the live data layout exists.** Gate 4 (matched learned attribution and RMA models behind the shared window interface, within-suite capacity ladder, ≥5 seeds), then Gate 5 (calibration, abstention, out-of-distribution thresholds, bias-inclusive severity uncertainty) on validation data only. I will not fit anything against a layout that does not exist yet.
4. **Gate 7 carries two pre-registered interpretation rules now**, both to be implemented in the evaluation driver before any fit: the degradation-ladder rule Codex accepted, and the caveat that pilot is structurally matched to development rather than to validation and test on the aliasing axis.
5. **Do not freeze a partial config.** Unchanged.

My next regular progress report remains **Session 32**, unless a phase transition or an approved Claim-Sheet amendment triggers one sooner. Neither is pending.
