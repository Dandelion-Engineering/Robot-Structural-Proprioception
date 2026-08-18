# Human Report — Claude Session 153

**Current date and time:** 2026-08-17 20:31 PDT (read from the shell at the moment this report was created)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

Two things happened this session, and they are the two Codex's Session-152 review asked
for plus the one my own build plan sequenced next.

1. **Both of Codex's Session-152 cross-review findings are discharged.** Neither is
   contested. I re-drove both at source against my own Session-152 bytes before
   accepting either, and both turned out to have a sharper form than the report gave
   them. Codex has now been right five reviews running on this build.
2. **Read-order row 21 is built**, which means all twenty-one rows of the connection
   adapter's fail-closed read order now exist. Row 21 is the only row that writes
   anything: it creates the publication directory exclusively and publishes the
   declared file set.

Everything in sub-step 4b-ii-b remains **wholly unreviewed**, and there is still no
Review Card and no subject chat for it. That is deliberate and has now held for nine
consecutive sessions: a card names a candidate, and the candidate is not stable yet.

The session spent **zero scientific resource**. No MuJoCo model was built, no rollout
stepped, no fit run, no figure rendered from real data, and no `pilot`, `val` or `test`
payload was read. The counters stand unchanged at 278 rollouts, 67 fits, 67 checkpoints.

## What Codex found, and what I measured

### Finding 1 — the seam ran row 4's *policy* and never row 4's *validator*

The adapter's row 4 validates the configuration document through the packet's own
`validate_config_document`. My Session-152 test seam — the helper that builds a
"post-row-12" connection state so row 19's provenance rules can be driven — ran row 4's
*policy* check and skipped that validation. Codex measured that the `frozen`
configuration the seam produced would have been refused.

Re-driven here, the refusal is not one clause but five:

| frozen clause | required | what the Session-152 seam produced |
|---|---|---|
| source file name | `config.json` | `config/draft-config-v0.1.json` |
| `decision` | `APPROVE_CONFIG_FREEZE` | the draft's blocking decision |
| `confirmatory_payloads_allowed` | `True` | `False` |
| `open_gates` | empty | five gates retained |
| freeze-required paths resolved | 8 of 8 | **0 of 8** |

**The part worth recording is why I had declined the check.** Session 152 wrote a
careful paragraph saying the post-condition deliberately does not run the validator,
because invariant W7 forbids this packet manufacturing a frozen `config.json`. Measured
this session: `validate_config_document` reads the source path **only for its name** and
never opens it, so a validator-accepted frozen state needs no file at all — and this
same test file has carried a complete validator-accepted frozen fixture document since
acceptance test B8. W7 is a rule about what the packet *contains*. It was never a reason
to skip a check that opens nothing.

**The repair.** The post-condition now calls row 4's own validator at the
authority-appropriate setting, the seam builds its frozen lifecycle out of the existing
fixture document under a `config.json` source path, and the join list gains a nineteenth
entry binding that path to the record's own declaration. The probe confirms neither the
live packet nor the test harness's temporary packet gains a `config.json` file.

**What is still not claimed is now exactly one field**, named and pinned by a test: the
record's echo of the config file's *byte* digest. The seam writes no file, so there is
no byte rendering row 4 would have hashed, and inventing one would put an identity into
the state that no read produced — which is the exact defect shape the previous review
found twice.

### Finding 2 — the menu fixture did not restore the record it rewrote

The three-case fixture installs a temporary menu over the test harness, rewrites the
connection record to declare it, and on exit restores every file that record names — but
not the record itself. Codex measured the leak. Re-driven here, it is worse than stale:

```text
post-exit authenticate_connection -> X_IDENTITY_MISMATCH on established_result.sha256
```

The record left behind **does not authenticate at all**, because it still declares the
digests of the temporary artifacts that the same cleanup had just put back. My digests
and Codex's agree exactly. The same hole was in this file's other two installers.

**The repair.** All three installers now save and restore the record in their own
cleanup. The restoration test compares the whole tree with **no exclusion and no manual
repair** — the exclusion was the reason no test could see this — and a new test drives
the property over all three installers by re-running the read order after each one exits.

### The third negative control

My own standing rule says a widened check must be shown to catch the *current*
generation's defect. Applying it to this widening, the two existing controls turn out not
to be evidence about it at all:

| control | broken identity joins | row 4 policy | row 4 validator |
|---|---|---|---|
| Session-150 partial | 11 of 19 | refuses | refuses |
| Session-151 partial | 7 of 19 | refuses | refuses |
| **Session-152 document** | **0 of 19** | **accepts** | **refuses** |

Both older controls would have been caught by the *old* post-condition. The third one was
built so that the new call is the only thing left that can refuse it.

## Row 21 — the last row of the read order

Row 21 creates `<output-dir>/<record_label>/` exclusively and writes exactly the declared
set: one bundle document, its digest file, and one scene document plus one 300-DPI figure
per case. Nothing else, and no subdirectory.

**The figure writer is passed in rather than imported**, and that is forced rather than
chosen: the renderer is the entry point that calls *into* the adapter, so importing it
would close a cycle, and it is the only module on this surface that imports matplotlib
while the adapter opens nothing and draws nothing.

**An injected collaborator is a seam, and that is the exact fault this review has found
twice.** So nothing the writer reports is taken on trust. The file set is compared to the
record's own menu by set equality in both directions; the published documents must be
byte-identical to the canonical renderings of the objects this chain assembled; the bundle
digest is re-measured from the bytes on disk rather than read from the writer's report;
the digest file must name the document beside it; and **each figure's own embedded
resolution chunk must state the DPI the report claims** — a report of a DPI is not a DPI.
Thirteen refusal tests drive one comparison each.

A second run at the same record label refuses **before the writer is reached at all**
(driven with a counting writer that is never called), and the first publication is
required to be byte-identical afterwards.

The cheap stub those thirteen tests use is itself bound to the real renderer: one test
drives both over the same bundle and requires them to agree on the file set, the report's
identity fields, the published bytes and each figure's declared resolution.

## Verification

Run only with the project interpreter, from the repository root.

```text
test_connection_adapter.py                      279 tests  (was 257)
focused pair (adapter + authenticated storage)  299 passed in 15.59 s   (was 277)
the same pair under `python -O`                 299 passed in 14.76 s
packet-wide suite                             2,957 passed / 0 failed / 190.80 s
```

The arithmetic closes exactly: 2,935 + 22 = 2,957, where the 22 are four tests on the
seam and the installers and eighteen on row 21. The packet-wide suite was run twice —
once before the line-ending repair described below and once after it, on the final bytes
— and returned 2,957 both times, which is what says that repair moved nothing but bytes.

`py_compile` clean, `git diff --check` clean, `git status --porcelain` shows only the two
intended files plus this session's own documents. Both candidate files are pure ASCII, LF,
0 CR, no BOM, final newline — **checked on the final bytes**, which is what caught the one
operational fault below. `git diff --numstat` reads `343 1` on the module and `842 37` on
the test file.

**One operational fault of my own, and the instrument that caught it.** Scripted edits made
with Python's `Path.write_text` silently converted both candidate files to CRLF, because
that call translates newlines to the platform's on Windows. `git diff` showed nothing,
because Git normalises line endings on read here — **the diff is structurally blind to this
class**. A byte count of the working tree is what saw it. Both files were converted back and
every suite re-run.

## Scientific and authorization boundary

- No MuJoCo model built, no rollout stepped, no fit or checkpoint created, no figure
  rendered from real data. Counters unchanged: **278 rollouts, 67 fits, 67 checkpoints,
  zero pilot/validation/test reads.**
- No role index, role payload, checkpoint, estimator output, controller log, production
  configuration or pilot/val/test result was opened. Every tree the tests bind is under
  `tmp_path`; the two probes ran in temporary directories outside the repository.
- The two files that carry the training-code identity of three approved artifacts were not
  edited.
- Slot-8 steps 1, 2, 3, 4a, 4b-i and 4b-ii-a remain closed at both approvals and at their
  recorded bytes. Sub-step 4b-ii-b remains mine, incomplete and unapproved.
- Steps 4c–4f, production connection records, real-role reads, capacity or threshold
  selection, the final configuration freeze and every C1-versus-S statement remain blocked.

## Live-Run README heartbeat

Checked and answered **no**. Completing an internal read-order row in an unreviewed build is
not an artifact closure, a phase transition or a scientific result, and the public log is
lean by design. The root README stands unchanged at its jointly approved bytes.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — row 21 (`write_bundle`,
  `WrittenBundle`, the PNG resolution reader) and its constants.
- `Reproducibility Packet/tests/test_connection_adapter.py` — the seam repair, the third
  negative control, the installer restoration repair and eighteen row-21 tests.
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — Appendix G, appended.
- `agents/Claude/Permanent Instruments.md` — lessons 278–282 and one forward correction
  inside lesson 277.
- `agents/Claude/Session Summaries/HumanReport153.md` — this report.
- `agents/Claude/README.md` — index and gate map refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 154.

No Review Card, chat transcript, protocol document, Claim Sheet, configuration, result
artifact or public README byte was changed.

## Next steps

1. The audit-hook observer that proves the adapter opens exactly the declared file set.
2. Acceptance tests B2 and B5, and the remaining B3 refusal rows.
3. The `roles` CLI wiring and the additive change to the public bundle entry point.
4. The two-pass mutation sweep on the finished pair.
5. Only then the Review Card, the subject chat and the handoff to Codex for a formal
   Round 1.
