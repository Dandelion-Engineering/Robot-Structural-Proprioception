# Human Report — Claude Session 154

**Current date and time:** 2026-08-17 22:26 PDT (taken from the shell at the moment this report was created)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution) · **Lane:** Slot-8, sub-step 4b-ii-b

---

## Summary

Codex reviewed my Session-153 work and returned two findings. I drove both at source before
changing a line, both reproduced exactly — my digests match the ones Codex published, to the
character — and I contested neither. Codex has now been right six sessions in a row on this
build.

**Both findings are the same fault as each other, and it is a fault this review has found
before in a different place: a value that reaches a checked object from *beside* it rather than
from inside it.** Session 153 built read-order row 21 and checked its injected figure-writer
exhaustively, on exactly that reasoning — and did not notice that the *bundle* it publishes
arrives through the same kind of seam.

1. **Row 21 published a bundle assembled under a different connection.** I built two genuinely
   authenticated connections over one temporary tree — same authority, same three-case menu,
   different record labels and therefore different record digests — resolved the whole chain
   under the first, and handed the result to row 21 together with the second. It published. The
   directory was named for connection B while every scene inside it, including the bundle
   document a reader is told to verify, identified connection A. The destination check had the
   same hole one layer down: it compared only the folder's *name* against the record label, so a
   correct name under an entirely wrong parent was accepted and populated.
2. **The PNG resolution check was not fail-closed.** A figure whose resolution chunk had a
   corrupted checksum was *accepted* as 300-DPI evidence; a figure whose header declared nine
   bytes over a one-byte body escaped the adapter's refusal surface as a raw `IndexError`. Those
   two outcomes look opposite and are one defect: a parser that indexes into bytes it has not
   proved are there, and believes a chunk it has not proved is intact.

Both are repaired, and the repairs are structural rather than patches to the two reported
inputs. I also built the next item on the plan, **the audit-hook observer (invariant W3,
acceptance test B4)**, which measures — from outside the module, at the interpreter — that one
adapter call opens exactly the files the connection record names and nothing else.

Evidence: `test_connection_adapter.py` **309** tests (was 279), the focused pair **329** and 329
again under optimised Python, packet-wide **2,987 passed / 0 failed / 185.03 s**. The arithmetic
closes exactly: 2,957 + 30 = 2,987.

**Zero scientific resource was spent.** Counters unchanged: 278 rollouts, 67 fits, 67
checkpoints, zero pilot/validation/test reads.

---

## What I did, in order

### 1. Startup and the cross-review duty

Read `.agent-turn` (named Claude), created `.agent-session.lock`, re-read `.agent-turn`, then
`AgentPrompt.md` and all of `Project Details/Project Details.md`. Read my continuity file, the
build plan's Appendix G, every chat summary I am a participant in and the one active transcript
(`Transcript Order Monitoring`). **No reply was owed there** — the last entry is my own Session-144
confirmation and Codex reported no ordering fault this cycle. A clean check is not a reason to post.

For cross-review I read Codex's `HumanReport153.md` in full, which is where its two findings live.
Codex's session was a general recent-work review rather than a formal Review Card round, because I
have not declared a stable candidate — that is the correct state and both agents are holding it.

### 2. Both findings driven at source before any repair

I do not repair a reported defect I have not reproduced myself. Both probes ran in a temporary
directory **outside the repository**, against a fresh harness.

**Finding 1 reproduced, with Codex's own numbers:**

```text
connection A label   adapter-fixture
connection A sha256  56a6d1b19548defcb5bcf1698166b809352de03418f2e1282db2f233d36d64b4
connection B label   adapter-fixture-b
connection B sha256  af93cceab0196ec4d8cf6d7a2fa0a10660ffa83dd6af46451c878ea00d645647
bundle A scene names adapter-fixture
RESULT               published under .../adapter-fixture-b/, accepted
```

and the destination half: substituting `<harness-root>/wrong-parent/adapter-fixture` — correct
basename, wrong place — was also accepted and populated.

**Finding 2 reproduced:**

```text
corrupted pHYs CRC          accepted, returned (11811, 11811) pixels per metre
pHYs header 9 / 1-byte body IndexError("index out of range"), no refusal code
```

### 3. The repairs

**One owner for the provenance block.** I extracted `_provenance_for(connection, case, state)`,
which row 20 now calls to *assemble* and row 21 calls to build its *comparand*. Row 21 compares
by walking `dataclasses.fields(Provenance)` rather than a hand-written list of fields. **That is
the part worth keeping: a field added to that dataclass later is bound at row 21 without anyone
remembering to bind it.** A hand-listed set cannot have that property.

Before it creates anything, row 21 now requires the bundle's menu to be the record's menu in the
record's order, its declared version to be this module's, its own provenance state to be the
authenticated authority, and every field of every scene's provenance block to be what this
connection produces.

**One derivation for the destination.** `_authority_output_root` re-derives
`<packet-root>/<authority parent>/<record label>/` from authenticated values only, proves it
resolves inside the packet root, and requires the bound value to equal it. **I deleted the old
basename check rather than keeping it beside the new one** — a guard whose removal changes no
outcome is indistinguishable from its own absence. The two directions the equality separates on
are covered by two *tests* instead: a moved basename and a moved parent.

**A total PNG walk.** Every chunk is bounded before it is read and checked before it is believed
(CRC-32 over the chunk's own bytes); the sequence must end at `IEND` with nothing after it; and
exactly one resolution chunk is permitted, because two disagreeing chunks would make the declared
DPI a function of which one a reader's decoder happened to keep.

**A third hole the finding exposed, which nobody had reported.** The publishing loop indexed the
bundle's scenes with case ids taken from the record, so a bundle whose menu was not the record's
produced a raw `KeyError` instead of a named refusal — the same class of unproved index as the
PNG defect. The new menu check closes it and a test drives it.

### 4. The audit-hook observer (W3 / B4)

`sys.addaudithook` sees the interpreter's own `open` event, so a file opened through `numpy`,
through `csv`, through one of the closed utilities or through a bare builtin all arrive
identically. The instrument the previous review built patches `Path.read_bytes`, which can only
see opens that go through that one door.

Measured, with nothing filtered on either side:

```text
one authenticated connection over the three-case menu
  48 open events over 47 distinct paths
  observed - expected = {}      expected - observed = {}
  exactly one path is opened twice: schema/schema.json, count 2
```

The second read of the schema was already known and count-pinned by the previous review; it is
now pinned at the interpreter rather than at one patched function, so a future second read taken
through any other route fails instead of joining an allowance.

**The observer's own anchor comes first.** A hook that recorded nothing would satisfy set
equality against an empty set and containment in either direction, so the first test drives a
builtin `open` *and* an `os.open` on a file no allowlist names and requires both to be recorded.
A fourth test uses the same instrument on row 21: every path the row **or its injected writer**
opens is a child of the tree row 3 bound.

**The instrument's cost, stated as a measurement.** A process-wide audit hook cannot be removed
once installed. The packet-wide suite ran **180.46 s without it and 185.03 s with it** (Session
153's figure was 190.80 s), so the cost is inside run-to-run variation — but it is written down
rather than assumed.

---

## Challenges, and how they were handled

- **Repairing a defect I had not yet reproduced would have been the fast path.** Both of Codex's
  probes were described precisely enough to fix from the description. I rebuilt both anyway,
  because a repair aimed at a described defect is aimed at the description. In this case the
  re-drive paid twice: it produced digests that match Codex's exactly (so the two accounts are of
  one object), and it surfaced the third hole — the raw `KeyError` on a foreign menu — which
  neither of us had reported.
- **The reported truncation input does not land where its name suggests.** Codex's one-byte
  `pHYs` body is refused because the *file ends inside a chunk header*, not because a `pHYs` body
  was short: the parser never gets far enough to know which chunk it was about to read. I kept
  that exact input in the table beside a bare truncation case and said so in the docstring, so
  the test pins the reported defect rather than a neighbour of it.
- **The strict parser had to be shown not to break real figures.** A parser made stricter is only
  correct if it still accepts what the packet actually produces. Two things establish that: the
  accept-path test drives the real matplotlib writer end to end, and a new test walks all ten
  tracked Step-3 fixture figures and requires each to pass the full CRC-checked walk and declare
  the derived resolution.
- **Scripted edits again.** Every edit this session was applied by a script that reads and writes
  **bytes**, never `write_text`, which is the Session-153 fault (lesson 282). Both files were
  re-measured on their final bytes: pure ASCII, LF, 0 CR, no BOM, final newline.

---

## Decisions I made

1. **No new exit code.** The read-order table names only the success code for row 21, so the new
   refusals reuse the codes the rows above already use: `X_IDENTITY_MISMATCH` for a presented
   identity that disagrees with an authenticated one, `X_PROVENANCE_UNRESOLVED` for the
   destination and the bundle state, `X_BUNDLE_INCOMPLETE` for the menu and the version. Design
   section 4.5's table stays closed.
2. **The provenance comparison walks the dataclass rather than a list**, and a coverage test
   requires the substitution table in the tests to name every field — so the *tests* fail when the
   dataclass grows, while the *code* does not need to change.
3. **The weak destination guard was deleted, not kept.** See above.
4. **No Review Card and no subject chat were opened**, for the tenth consecutive session. A card
   names a candidate, and the candidate is not stable until the remaining scope is built.
5. **The public README was not touched.** Discharging review findings and building an internal
   observer in an unreviewed build is not an artifact closure, a phase transition or a result. The
   root README stays at the jointly approved blob `7342bc8c`.

---

## Files created or updated

| file | what changed |
|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `_provenance_for` extracted; `_authority_output_root` added; row 21 binds menu, version, state and every provenance field; the PNG walk made total and CRC-checked. `git diff --numstat` `239 42`. Blob `3baa0178`, raw `438b3059cb6de99069dfe4f9828f9ef1cd00b9fd22a4412ab3e0b03851ef99fa`, 182,777 B / 3,886 LF / 0 CR |
| `Reproducibility Packet/tests/test_connection_adapter.py` | 30 net new tests: the two-connection refusal, the wrong-parent destination, nine provenance fields plus a coverage test, the foreign menu, the version, the bundle state, eight malformed PNGs, two more writer-disagreement rows, the tracked-figure acceptance check, and the four audit-hook observer tests. `git diff --numstat` `561 1`. Blob `fd841d52`, raw `ba08534123f3adeea0df31f38449c9c8714adfb26488f64196136690d5f75ca5`, 307,187 B / 7,334 LF / 0 CR |
| `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` | **Appendix H** appended (`169 0`, purely additive) — the two findings, their measurements, the repairs, the observer and what is left |
| `agents/Claude/Permanent Instruments.md` | standing lessons **283–286** appended (`49 0`) |
| `agents/Claude/Session Summaries/HumanReport154.md` | this report |
| `agents/Claude/README.md` | Session 154 indexed |
| `agents/Claude/Summary of Only Necessary Context.md` | completely rewritten for Session 155 |

No protocol document, Claim Sheet, configuration, result artifact, Review Card, chat transcript or
public README byte was changed.

---

## Scientific and authorization boundary

- **Counters unchanged: 278 rollouts, 67 fits, 67 checkpoints, zero pilot/validation/test reads.**
  No MuJoCo model was built, no rollout stepped, no fit run, no checkpoint written and no figure
  rendered from real data.
- No production connection record, real role index, real role payload, checkpoint, estimator
  output, controller log or production configuration was opened. Every tree the tests bind is
  under `tmp_path`; both probe files ran outside the repository and were not committed.
- **Disclosed reads**, all tracked development text or tracked fixture output, none opening a
  payload behind it: `connection_adapter.py`, `connection_record.py`, `verification_scene.py`,
  their test files, and the ten tracked Step-3 fixture PNGs under `results/verification_fixture/`,
  read for their chunk structure only.
- **The two off-limits identity files** (`storage_contract.py`, `role_contract.py`) were neither
  read nor edited.
- Slot-8 steps 1, 2, 3, 4a, 4b-i and 4b-ii-a remain closed at both approvals. **4b-ii-b remains
  wholly unreviewed and owner-held.** `build_role_bundle` still refuses unconditionally, which is
  correct until the whole of 4b closes. Steps 4c–4f, the configuration freeze, every capacity and
  threshold choice and every C1-versus-S statement remain blocked.

---

## Next steps

1. **B2 and B5** — the synthetic end-to-end across both fixtures, and the determinism check
   (invariant V13): the coherent fixture rendered twice must give byte-identical scenes and
   figures.
2. **The remaining B3 rows** — one case per row of the read order, rows 13–21.
3. **The `roles` CLI wiring and the additive `build_role_bundle` change**, which should also fix
   that function's live docstring gloss of `--config`.
4. **The two-pass mutation sweep** on the finished pair, budgeted *before* the handoff, with the
   staged tree carrying `scripts`, `tests`, `schema`, `config` and `results`.
5. **Then** the Review Card and the subject chat, then the handoff to Codex for Round 1. The card
   carries three disclosures: the `schema.json` end-of-line pin dependency, the
   `authenticate_sources` signature change and the `AuthenticatedConnection.record_sha256`
   addition. Session 154 added no fourth.
