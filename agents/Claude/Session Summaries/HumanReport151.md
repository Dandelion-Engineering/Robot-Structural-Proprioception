# Human Report — Claude Session 151

**Current date and time:** 2026-08-17 16:18 PDT (taken from the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session did two things: it discharged Codex's Session-150 cross-review finding against
my row-19 test seam, and it built read-order **row 20** — the bundle assembly — while
measuring, rather than guessing, the boundary that stops row 20's accept path from being
reachable in this packet today.

Nothing was reviewed, no Review Card exists for Step 4b-ii-b, and no chat was opened. That
remains deliberate: a card names a candidate, and the candidate is not finished.

### What Codex found, and why it was right

Codex's Session-150 review found **no defect in `resolve_provenance`**. It found something
more subtle and, in this project's terms, worse: the **test seam feeding row 19 built a
state the read order refuses two rows earlier**, while the tests' own comments asserted the
opposite. The row-19 verdicts were correct — the production path establishes those
equalities before row 19 is ever reached — but the evidence for invariant W6 was being taken
over an object that could not exist on the production path. Evidence taken over an
impossible state is not evidence.

I drove it at source before accepting it, and it came out slightly wider than reported. A
probe built the harness in a scratch tree, authenticated it, applied the exact Session-150
helper, and re-checked the joins rows 4 through 6 establish. Against the unedited
connection **all eleven hold**; after the helper **three hold and eight are broken**. Codex
reported eight equalities with one surviving — the same fault, partitioned slightly
differently.

### The repair, and the half of it that matters most

`_reprovenanced` now moves **every** copy the earlier rows bind: the record's own config
echo, both audit `config_hash` echoes, the established result's split and config identity at
their declared field paths, both audit documents, and every manifest row's `config_hash` and
split. It then requires the result to satisfy a join set written down **once**, so the
helper's post-condition and the tests asserting it cannot drift apart. The post-condition
**raises rather than asserts**, because this file's suite is deliberately re-run under
`PYTHONOPTIMIZE=1` and `assert` disappears there — a post-condition that vanishes under
optimisation is absent exactly when nobody is watching.

The half that matters most is the **negative control**: the Session-150 partial edit is
reconstructed as an input and required to be caught, naming all eight broken joins. Without
it, the new post-condition would be a guard no input can make decisive — the defect shape
this project calls lesson 242 — sitting on the seam that carries invariant W6's only
evidence. That is the last place it should be allowed to happen twice.

### Row 20 is built, and its accept path is measured as unreachable

`resolve_bundle` assembles the menu the two surfaces draw. It requires the record's menu,
the resolved series and the derived geometry to be one sequence in one order; requires the
assembled menu to equal the **established result's** declared case list (row 6 compared that
list against the record's menu — this compares it against the *assembly*, a different
object); calls `validate_bundle`, the gate both surfaces run first; and requires each
scene's arm identities to be the record's own.

Then it stops, and the stop is measured rather than argued. `validate_bundle` requires a
menu carrying at least one **structure**, one **actuator** and one **sensor** case. The
contract fixture writes two C1/S pairs — a `dev` pair labelled `healthy` and a `val` pair
labelled `structure` — and row 6 refuses a run whose split is not the record's, so the `val`
pair cannot enter a `dev` record's menu at all. **No menu this packet can currently build
passes the surface gate.** Driven end to end on the coherent fixture:

```text
validate_scene:  ACCEPTED
validate_bundle: REFUSED X_BUNDLE_INCOMPLETE -- a bundle must contain at least one
                 structure/actuator/sensor case; missing ['structure','actuator','sensor']
```

So row 20 ships with its three ordering refusals driven, the surface gate's refusal driven
end to end, and **the per-case assembly driven on its own** — `_scene_for` is reachable
because `validate_scene` is a different gate, and a test drives its whole field-by-field
mapping through it. What has **no test yet** is the accept path and the two identity
refusals, which sit behind a gate no input available today can pass. That is written into
the test file where the missing tests would be, in the form lesson 261 gave row 13, rather
than left to be rediscovered.

**This is not an argument for relaxing the gate.** A menu that cannot show a reader a
structure, an actuator and a sensor change side by side cannot support the comparison the
whole verification artifact exists to let a reader make. The repair is a fixture — a
three-case coherent harness — and it is the next session's first work.

## Challenges, and how they were handled

**The temptation to widen the scope.** The obvious move after measuring the boundary was to
build the three-case harness immediately and finish row 20's accept path in the same
session. I did not, and the reason is this session's own subject matter: the finding I was
discharging was caused by a fixture that *looked* coherent and was not. A three-case harness
needs three `dev` pairs whose `labels` **and** `estimator_outputs` payloads carry their
source classes coherently, a rewritten manifest, both audits rebuilt from a recomputed
census, and a three-case record — built in a hurry at the end of a session, that is exactly
the object Codex just caught me shipping. It is written up as the next build's first step,
with the reason the shortcut is forbidden.

**The temptation to relax the gate instead.** Deleting or weakening the
structure/actuator/sensor requirement would have made row 20's accept path green today. It
would also have deleted the requirement rather than met it. Recorded as lesson 271.

**The closed-half surface change.** Row 20 needs the record digest the chain authenticated,
and `AuthenticatedConnection` did not carry it. Taking it from a caller at assembly time
would let a caller supply a provenance identity (invariant V7 forbids exactly that);
re-measuring the file at assembly time would describe the file as it is *then*, not the
bytes rows 1 and 2 authenticated. So the field was added. This is the **second** closed-half
signature change 4b-ii-b carries, beside `authenticate_sources`' third parameter, and the
Review Card must name both.

## Decisions I made

1. **Accepted Codex's finding without contest**, after driving it at source myself. Third
   consecutive session in which Codex was right and I did not contest it.
2. **The join set is stated once and raised on, not asserted.** One statement of the
   precondition, shared by the helper and the tests; explicit `raise` so it survives `-O`.
3. **A negative control ships with the post-condition.** The Session-150 partial edit,
   reconstructed and required to be caught.
4. **Row 20 ships built but not fully exercised, with the gap written beside the code.** The
   alternatives were to hold the code back or to reach green by weakening a rule; the first
   loses work that is correct and driven as far as it can be, the second is dishonest.
5. **No card, no chat, no handoff.** Seventh consecutive session holding that line.

## Verification

- `test_connection_adapter.py`: **245 passed** (was 235).
- Focused pair (`test_connection_adapter.py` + `test_authenticated_storage.py`): **265
  passed** (was 255), and **265 again under `PYTHONOPTIMIZE=1`**.
- Packet-wide: **2,923 passed / 0 failed / 152.03 s**. The arithmetic closes exactly:
  2,913 + 10 = 2,923, and the ten are four seam tests and six on row 20.
- `py_compile` clean on both edited files; `git diff --check` clean; `git status --porcelain`
  shows exactly the two edited packet files.
- Both edited files: pure **ASCII**, **LF**, **0 CR**, no BOM, final newline — checked on the
  final bytes, per lesson 269.
- `git diff --numstat`: `217 0` on the module, `464 9` on the test file.

Working-tree identities of the two edited files (they enter the object store at this
session's commit; the Review Card, when it is written, will resolve them with
`git cat-file -t` before it governs):

```text
Reproducibility Packet/scripts/utils/connection_adapter.py
  blob 474b02c6fc884f79559b54b2fc9cd04ffb1d84bc
  raw  f4ce02c31bfd08f2817d32a2d433ad59f415d5343b223fcc406b407a94f02315
  155,277 B / 3,311 LF / 0 CR
Reproducibility Packet/tests/test_connection_adapter.py
  blob bf9e2738770573e154ed9975315920f7577e2170
  raw  519d3b75da8fe1af985b2ba94bae913aea65f3c9b16a6f2bbbf1db1417d1ef86
  206,424 B / 4,995 LF / 0 CR
```

## Scientific and authorization boundary

**This session spent zero scientific resource.** Counters unchanged: **278 rollouts, 67
fits, 67 checkpoints, zero pilot/validation/test reads.** It built no MuJoCo model, stepped
no rollout, ran no fit, selected no capacity or threshold, rendered no figure and made no
C1-versus-S statement. It opened no role index, role payload, checkpoint, estimator output,
controller log, production config or pilot/val/test result. The two off-limits identity
files (`storage_contract.py`, `role_contract.py`) were not edited. Every tree it built was
a temporary directory.

Disclosed reads, all tracked development text, none opening a payload:
`connection_adapter.py`, `connection_record.py`, `verification_scene.py`,
`render_verification_scene.py`, `build_data_contract_fixture.py`, `storage_contract.py`
(dataclass fields only), and design sections 4.1, 4.2, 4.3, 4.4, 4.7, 4.8 and 5.

Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed at both approvals at
their recorded bytes. Step 4b-ii-b remains mine, incomplete and wholly unapproved.

## The Live-Run README heartbeat

Checked, and the answer is **no**. No artifact finished, no phase closed, no result was
produced — a partial internal build plus one pre-handoff evidence correction is not a public
milestone. The root `README.md` is untouched at the jointly approved blob `7342bc8c`.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — `record_sha256` on
  `AuthenticatedConnection`; `resolve_bundle`, `_scene_for`, `_arm_identity` (row 20).
- `Reproducibility Packet/tests/test_connection_adapter.py` — the repaired row-19 seam with
  its join set, post-condition and negative control; six row-20 tests; the reachability
  boundary written where the missing tests would be.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — **Appendix E** appended (the measured
  finding, the repair, row 20, the boundary, the three disclosures the card must carry).
- `agents/Claude/Permanent Instruments.md` — lessons **270** and **271**.
- `agents/Claude/Session Summaries/HumanReport151.md` — this report.
- `agents/Claude/README.md` — Session 151 added.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 152.

No Review Card, chat transcript, protocol document, schema, configuration, scientific result
or root README was changed.

## Next steps

1. **The three-case coherent harness**, and with it row 20's accept path and its two
   identity refusals. Three `dev` pairs whose `labels` and `estimator_outputs` payloads carry
   `structure`, `actuator` and `sensor` coherently; manifest and both audits rebuilt from the
   recomputed census; a three-case record; every byte restored on exit. It belongs in the test
   file, **not** in `build_data_contract_fixture.py`, whose two-pair census closed tests pin.
2. **Row 21** — the exclusive create and the declared write set.
3. The audit-hook observer (W3/B4), then B2, B5 and the remaining B3 rows, then the `roles`
   CLI wiring and the additive `build_role_bundle` change.
4. The two-pass mutation sweep on the finished pair.
5. **Then** the Review Card and the subject chat, carrying three disclosures: the
   `schema.json` EOL-pin dependency, `authenticate_sources`' third parameter, and
   `AuthenticatedConnection.record_sha256`.
