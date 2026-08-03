# Claude Human Report — Session 64

**Date and time:** 2026-08-03 00:19 PDT

**Phase:** 2 — Execution

**Decision:** I explicitly approve the four-file Step-2 partial state at
`b7b2430a` / `c23e61d3` (Codex's two files, byte-unchanged) and
`2f7c33b2` / `ad6b32fe` (Codex's `protocol_p_results.py` and its tests, plus my
additive `LogicalRow` fix and three tests). **Codex owns the next turn.** Zero physical
rollouts were spent; the project's lifetime total remains **151**. Step 2 is still
incomplete — the payload-boundary executable is unbuilt — so no plan mode, no replay, no
extension rollout, no Amendment A2, and no config materialization is authorized.

---

## What I found when I arrived

Codex's Session 63 did two things. It approved the payload-boundary extension v0.2 at my
`538ae06b…` state, which **closes the document review loop** — both agents have now
explicitly approved the same exact bytes — and it then used the Step-2 authority that
closure grants to build two of the extension's three prerequisites: the additive
`ScreenOverrides.distal_payload_mass_kg` field on the generator seam, and the additive
`PhysicalKey.distal_payload_mass_kg` field on the results layer. It approved that
four-file state and handed it to me for genuine first review.

So this session's work was the review, plus the regular progress report, which was due at
my Session 64 and covers Sessions 57–64.

## What I did

### 1. Verified both of Codex's changes with my own instrument

I deliberately did not re-run Codex's six mutations (Lesson 53: when you re-verify
someone else's verification, change the instrument). I wrote my own sweep harness with my
own case list and ran it over Codex's two files **and** my own edit together.

```text
10 cases | 10 caught | 0 survivors | both passes agree | baseline green in every copy
harness  fresh isolated packet copy per case, __pycache__ cleared before each run,
         PYTHONDONTWRITEBYTECODE=1 in the subprocess env, no -x, whole sweep run twice
```

Codex's seven cases — the key field, the factory normalisation, the report line,
`is_active()`, the override-to-config connection, the finite/nonnegative guard, and the
conversion guard — were each killed, twice, with identical failing-test sets. I also read
both changes against the property each is supposed to have rather than against the diff:
zero is a mass and not an absent override; the validation happens before any plant is
compiled; `is_active()` covering the field is what forces a mass-only override to carry a
base-distinct `dev-` provenance stamp; and every committed `ScreenOverrides(` construction
is keyword-form, so inserting the new field before `provenance_hash` binds nothing wrongly.

### 2. Found one defect, and measured it rather than arguing it

**`PhysicalKey` gained the payload field and `LogicalRow` did not — and
`LogicalRow.physical` is the only thing in the results layer that *produces* a
`PhysicalKey`.** Every consumer reaches a key through that property: the distinct-body
census (`protocol_p_results.py:647`, `:945`), the collision detector (`:671`), the
reuse-body equality (`:724`), the provenance read (`:743`), the measurement read (`:854`),
and the driver's own ledger write (`run_protocol_p_screen.py:867`).

I built the extension's exact §5/§6 shape — eight common-random-number identities at
`sensor_seed = 160000 + 1000k + 2`, ten ladder rungs at `k=0`, seven masses — and measured
it at zero rollout cost:

```text
extension rollouts built as logical rows : 126
distinct keys via LogicalRow.physical    : 18       <- §3.2 requires 126
the row-derived key's mass field         : None, at every one of them
physical_key() called with a mass        : 0.025 vs 0.200 distinct = True
the 0.025 kg and 0.200 kg ladder rows    : same key = True
ResultsLedger.record, second body        : ProtocolPError, refused as an already-recorded
                                           body whose key carries distal_payload_mass_kg=None
```

**Two scope statements I attached to it, both against the finding's own interest.** First,
it fails **loudly**, not silently: §3.2 warns that a colliding key "would let the 0.025 kg
rollout be silently reused as the 0.200 kg row," and that is not what this code does —
`ResultsLedger.record` refuses a duplicate key, `ledger.has()` has no call site in
`scripts/` at all, and reuse is decided by the declared `reused_from` rather than by a
ledger probe. Under the §8 stage order the refusal lands about nine rollouts in. Second,
**Codex's build satisfies §3.2's bullet list exactly as written** — the dataclass field,
the `float()` normalisation, and `physical_key_report` are all there. What is missing is
the property §3.2 gives as the *reason* for the field ("it resolves which logical rows
cite an already-measured rollout"), which is a statement about row-mediated paths that no
row-mediated path can see. The justification and the implementation are about different
objects.

### 3. Fixed it additively, and pinned the inertness

```text
LogicalRow.distal_payload_mass_kg: float | None = None
  - additive, defaults None, which is the mass every Protocol-P row already has
  - threaded into .physical
  - deliberately NOT threaded into .key
```

Inertness is pinned rather than asserted: a new test walks the full 180-row inventory and
requires every row's mass to be `None`, the distinct-body count to be
`EXPECTED_PHYSICAL_ROLLOUTS == 168`, and **every row's key to equal the key built by
calling `physical_key()` without the mass argument at all** — the clause that goes red if
the default ever stops being `None`.

`key` is untouched on purpose and the docstring records why, so nobody later "finishes"
the job: §11.2 nests the extension's rows under `per_mass[]` and identifies them by
`fault_physical_key` / `healthy_physical_key`, so the extension needs the mass in the
*physical* key and never in the logical one; and adding an element to `key` would move
`stage_a_origin_row_key` and the reported `reused_from` tuples, which is not an inert
change. I said explicitly in the chat that if Codex expects the executable to identify
rows by `key` across masses, it should say so and I will do that properly rather than as
a rider on this loop.

### 4. Named two more closed doors for whoever writes the executable

Neither is a defect and neither blocks the loop, but both are the same shape as the
finding above — the extension cannot inherit a results-layer entry point just because the
object it needs lives in that module.

1. **`ResultsLedger.record` requires `stage_of_origin in SCREEN_STAGES`, and
   `SCREEN_STAGES` is `("A", "B", "C")`.** The extension's stages are X0P/X0E/XR/XA/XM-C/
   XL/XM-B/XZ, so it cannot record into this ledger without a third change to an approved
   artifact or mislabelling its stages as Protocol P's — and mislabelling is exactly what
   `stage_of_origin` exists to prevent. My read: the extension should carry its own ledger
   and reuse only `physical_key`, `physical_key_report` and `PhysicalKey`, which are
   precisely the three things Codex's build made mass-aware. That deserves an explicit
   sentence in the executable's design, not a default.
2. **`require_inventory_shape` hard-codes Protocol P's 180/168/12 census** through
   `expected_counts`, so the extension's 126/532 census needs its own shape function.
   Worth saying out loud because §3.2's "the census the results layer prints is therefore
   checkable against this document" reads as though the existing census function would do
   the checking, and it will not.

### 5. One non-blocking observation I did not act on

The two mass-validation raise sites in `_physical_config` emit the same sentence, and one
of them fires for a value that is not a number at all, where "finite and nonnegative"
misdescribes what went wrong. Both guards are independently killable in my sweep (at 1 and
3 failing tests), so this is **not** the carried requirement (ee) failure mode where a
shared sentence hides a dead guard — it is a message-quality point only. I left it
untouched deliberately so Codex can close this loop with a plain approval if it agrees.

### 6. The regular progress report

Session 64 is my eighth session since the last one, so I wrote
`agents/Claude/Progress Reports/Progress Report Session 64.md`, covering Sessions 57–64 at
the Accessible-Piece bar. Its spine: the screen **ran**, and then its result turned out to
be conditional on payload mass — measured at the two lightest weights of eight — and the
four sessions since have gone into designing the follow-up carefully rather than writing
the result up as though the dependency were not there. It names what is not working
(six unmeasured masses, an unidentified mechanism, a development split with no detectable
structural setting) as plainly as what is.

### 7. Live-Run README heartbeat

The check fired this session and the answer was yes: the document loop **closed**, which
is the milestone my Session 63 note said the log should wait for. One entry appended at
the end of the running log (`+3/−1`, including the banner date moving to 2026-08-03),
covering the agreed plan, the 19,448-state licensing enumeration, the start of
construction, and the gap where the payload column existed but nothing could fill it.

## Challenges, and how they were handled

- **Judging whether the `LogicalRow` gap was Codex's defect or the document's.** It is
  arguably the document's: §3.2's bullet list is fully satisfied. I resolved it by asking
  what §3.2 exists to deliver rather than what it lists, measuring the delivered property
  (126 → 18), and fixing it additively rather than sending the state back — which keeps the
  loop to one round instead of two.
- **Resisting the overstatement.** The finding is much more dramatic if I say a key
  collision would silently misattribute a measurement. I checked whether any code path
  actually does that, found `ledger.has()` has no callers and `record` refuses duplicates,
  and stated the finding at the strength the evidence supports.
- **Deciding what *not* to change.** Threading the mass into `LogicalRow.key` looks like
  the completion of the same fix and is not: it moves `stage_a_origin_row_key` and the
  reported `reused_from` tuples. I left it, documented why in the class docstring, and
  handed the decision to Codex.

## Insights worth carrying

- **An additive field is only additive where something can produce it.** The field was
  added to the key, the factory and the report — every place a key is *consumed* or
  *rendered* — and not to the one place a key is *built from a row*. The completeness
  check that would have caught it is not "is the field everywhere the type appears" but
  "name every producer of this object, and check each one passes the new input."
- **The sharpest question for a review of a partial build is what the piece was *for*,
  not what its spec listed.** The spec bullets were all satisfied and the property they
  were written to secure was not.
- **The recurrence pattern is now three deep.** Lesson 88 (a control that varies the thing
  it controls for), Lesson 89 (fixing the science broke a key silently), and now this: the
  fix for the key that could not distinguish bodies produced a key that no row could fill.
  Each time, the defect lived one layer below the layer that was being fixed.

## Files created or updated

- `Reproducibility Packet/scripts/utils/protocol_p_results.py` — additive `LogicalRow`
  field, threaded into `.physical`, docstrings recording why `.key` is untouched.
  Blob `2f7c33b274bfe7ee16ecdf0dc7227ca6bd159f9c` (`+24/−1`).
- `Reproducibility Packet/tests/test_protocol_p_results.py` — three tests: the row carries
  its mass into its key; two rows differing only in mass are two bodies the ledger
  accepts; the 180-row Protocol-P inventory keys exactly as it did before the field
  existed. Blob `ad6b32fef834cb55225b6cea1ac7831f090391de` (`+62/−0`).
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-64 review turn (`+184/−0`, header unique, physically last).
- `agents/Claude/Progress Reports/Progress Report Session 64.md` — new, regular cadence,
  covers Sessions 57–64.
- `README.md` (root, Live-Run) — one running-log entry, banner date to 2026-08-03
  (`+3/−1`).
- `agents/Claude/Session Summaries/HumanReport64.md` — this file.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.

**Not modified:** Codex's `assignment_generator.py` and
`test_assignment_generator_screen_overrides.py` are byte-unchanged at its handoff blobs;
I verified that after every sweep pass.

## Verification

```text
focused suites   124 passed  (121 -> 124)
full packet      1,136 passed in 115.35 s  (1,133 -> 1,136)
mutation sweep   10 cases, 10 caught, 0 survivors, two passes agreeing
physical rollouts spent this session   0    (project lifetime total 151)
plan mode run    no     config/config.json   absent     test split   untouched
```

Neither published analyzer imports `protocol_p_results`, so no artifact byte-identity
re-verification is owed for this change — checked, not assumed.

## Next steps

1. **Codex reviews `2f7c33b2` / `ad6b32fe`.** If it approves, the seam loop closes and the
   only remaining Step-2 target is the executable.
2. **Build the payload-boundary executable** (§§4–12), review it, and sweep it. It needs an
   explicit decision on the two closed doors above — its own ledger and its own census
   shape — before it is written, not after.
3. Then, and only as a separately authorized step, plan mode; then, as a further separate
   authorization, the run.
4. Nothing is blocked on the director. `director_requests.md` entry 1 (Claim Sheet review)
   remains open and non-blocking.

— Claude
