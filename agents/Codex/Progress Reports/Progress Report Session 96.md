# Progress Report — Codex, Session 96

**Date:** 2026-08-08
**Covers:** my Sessions 89–96 (previous regular report: Session 88)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with a proposed development-only width sweep whose design was still in
review. Eight Codex sessions later, the design is frozen, the program and its tests are jointly
approved, and a corrected zero-fit plan now names the exact work that could be done.

Nothing has been fitted during this stretch. No new model, checkpoint, simulation, generated
data, or result exists. The plan is a promise made before spending: ten existing models remain
read-only, forty new width arms would be fitted, and two compatibility arms would first prove
that the new fitting route can reproduce the old route exactly. The maximum is 42 fits and 42
new scratch checkpoints, with no physical simulation and no reserved-data read.

Codex has independently rebuilt and approved the corrected plan. Claude's independent review
of those exact bytes is now open. Even if that review closes unchanged, the fits remain blocked
until both agents issue a separate execution authorization naming the approved plan's exact
fingerprint.

## Why a small measurement needed this much review

The scientific question sounds simple: if the network is made wider, does the training-set
behavior of either sensor suite change? The difficult part was making sure the stored answer
could not silently describe a different experiment from the one both agents approved.

The review cycle found four kinds of boundary problem before any fit ran:

1. **A plan label was being asked to do more than it can.** A name such as
   `stage1-run-1` gives the run a stable identity, but it cannot by itself make permission
   single-use. The design now states that limit honestly and binds a conforming run to an
   atomically created `<base>/<run_label>/` directory.
2. **A failure record could look complete while losing evidence.** Early executable states
   could omit downstream unattempted arms, accept one required arm twice, lose partial
   compatibility state, or write a refusal whose file name and internal attempt identity did
   not agree. Those paths now preserve a complete, checkable terminal record.
3. **A guard and writer could spell the same destination independently.** Each piece looked
   correct in isolation, but a future edit could make them disagree. The reviewed program now
   derives each protected destination once and shares that definition.
4. **The first plan missed one imported program in its authorization chain.** The omitted
   module loads every training example and computes the reported accuracy and macro-F1. Claude
   proved that its scoring rule could change while the plan stayed byte-identical. The repair
   compares that module's current fingerprint with the fingerprint already recorded in the
   approved analysis artifact before writing a plan and again before authorizing execution.

The last finding is why the first plan was superseded. It was an accurate description of the
approved sweep at the time, but the stronger authorization check changed the program's own
identity. Keeping the old plan would have meant approving one program and running another.

## What now exists

The frozen development-only design permits five widths while holding the temporal receptive
field and optimization settings fixed:

```text
channels             16      24      32      40      48
parameters        10,586  22,786  39,594  61,010  87,034
new curve fits        10      10       0      10      10
```

The 32-channel row is the ten already-approved development models and is read-only. The forty
other rows are the proposed new curve. Before any of them may run, two 32-channel compatibility
fits—C1 seed 0 and S seed 4—must reproduce the approved checkpoints and every recorded training
loss bit-for-bit. Failure stops the run before the curve starts.

The corrected plan is:

```text
file        Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
Git blob    c048b54b8081271d76a6adacf8526d201c446c17
SHA-256     bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
authority   development only; no capacity selection or sensor-suite conclusion
status      Codex approved; Claude independent exact-state review open
```

I compared it with a fresh in-memory reconstruction, drove the program's own authorization
gate, checked every arm and destination, and compared it with the superseded plan. The only
semantic change is the capacity-sweep program fingerprint; the inputs, arms, paths, protocol,
and budget are unchanged.

## What is working

- The design, executable, and tests now carry two-agent exact-state approval.
- The corrected plan is deterministic, machine-path-free, and accepted by the current
  executable's pre-spend authorization gate.
- The plan names every read-only anchor, every new arm, both compatibility fits, the two
  approved development documents, all training-code identities, and the fixed budget.
- A new portability test proves that the analyzer identity remains valid when the same text is
  checked out with Windows CRLF line endings; a raw-byte implementation would fail that test.
- The full packet suite passes **1,765 tests**, including 214 focused capacity-sweep checks in
  normal mode and under Python optimization.
- This eight-session stretch spent **zero fits, zero checkpoint writes, zero generation, zero
  rollouts, and zero pilot/validation/test reads**. The lifetime Protocol-P-related simulation
  total remains 278.

## What is not working yet

- The corrected plan has only Codex's approval. Claude still owes an independent read of the
  exact plan bytes, so the planning gate is open.
- No capacity curve has run. There is therefore no evidence yet about whether width explains
  any part of the unstable first-fit behavior.
- The later capacity-analysis program is not yet built. It must report the two suites' absolute
  curves and their paired difference without manufacturing a causal explanation.
- No model size, probability threshold, detection threshold, abstention rule, or uncertainty
  threshold has been selected.
- The final `config.json`, confirmatory identities, confirmatory data, and headline result
  remain blocked behind their later gates.
- Your Claim Sheet review in `director_requests.md` remains open and non-blocking. Nothing in
  this stretch requires a new decision from you.

## What happens next

Claude's next exact task is to open plan blob `c048b54b...`, reconstruct its commitments, and
approve or block those bytes. If Claude edits it, Codex must review the new state; approval is
not inferred from an edit or handoff.

If both agents approve the same plan, Step 3 closes. Step 4 is still separate: both agents must
explicitly authorize one execution and name the approved SHA-256. Only then may the two
compatibility fits and forty curve fits run. A later read-only analyzer will summarize that
development evidence without reading pilot, validation, or test outcomes.

The Slot-8 director verification artifact has no new state in this eight-session stretch, so
this report does not manufacture an update for it.
