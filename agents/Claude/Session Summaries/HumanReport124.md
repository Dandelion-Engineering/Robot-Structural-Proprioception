# Human Report — Claude Session 124

**Current date and time:** 2026-08-12 05:24 PDT

## Summary

This session was one thing: the owner re-review of the Slot-8 verification-artifact design after
Codex reviewed it, found nine defects in my draft, repaired all nine, and handed it back.

I kept every one of Codex's nine repairs. I did not keep them because they read well — I kept them
because I went and measured the contract each one names, and each one was right. Then I found two
defects of my own in the reviewer state, repaired both, and returned the document with my explicit
approval. The design loop is now open on Codex for a second round.

Zero fits, checkpoints, rollouts, generation runs, plan invocations, analyzer invocations, and zero
pilot, validation or test reads. No real data was opened at all.

## What the session was for

The project has no open scientific lane. Every measurement lane is spent or shut, and the config
freeze is deliberately blocked. What is open is the one named completion requirement that has never
had an object: **Claim Sheet Slot 8, the director's verification artifact** — the hands-on thing
Randy is supposed to be able to open and use to check the result without reading the Technical
Report.

Codex ruled in its Session 122 that Slot 8 goes first, bounded to a *contract plus synthetic
scaffold* — explicitly not a demo that dresses up the current development record as a result. I
wrote that design in Session 123. Codex reviewed it in its Session 123 and blocked it. This session
is my half of the loop closing.

## What was accomplished

### 1. The handoff was authenticated before it was read

Codex declared its reviewer state as Git blob `0fabe5474…`, raw == canonical `1a7f6227…`,
38,299 bytes / 562 LF / 0 CR. The file on disk reproduced all of it, plus no BOM, a final newline,
and non-ASCII confined to en and em dashes. So the bytes I re-reviewed are the bytes Codex
approved. This is routine here, and it is routine because getting it wrong is how two agents end up
approving different documents while believing they agree.

### 2. All nine of Codex's findings were checked against objects outside the document

The temptation in an owner re-review is to read the reviewer's prose and decide whether it sounds
correct. That is not a check — it is the document checking itself, which is the failure mode
standing lesson S56 exists to name. Every one of Codex's findings asserts a fact about a contract
that physically exists in the packet, so I opened the contract.

- **BR.** The machine schema's `estimator_outputs` role has exactly nine fields, and
  `EstimatorOutput` carries the same nine. My table listed eight — `location_out` was missing.
  Simply wrong, and kept as repaired.
- **BS.** `task_reference` and `true_task_output` are fields of the privileged `plant` role;
  `controller_logs` has neither. And the live metric signature is
  `j_5s(t_s, task_reference, true_task_output, onset_time_s, *, window_s=5.0)` — my draft dropped
  `window_s`. **This is the one I am most glad Codex caught.** The whole point of the design is
  that the panel the director reads and the number the report publishes are the same quantity. A
  dropped window argument would have let them integrate over different intervals, and that
  divergence is invisible in a picture.
- **BT.** `plant` carries `q_true`, `deform_coords` and `true_task_output` — the fields that make a
  read-only planar body outline derivable without re-running the simulator. Slot 8 promises the
  director watches two robot copies; endpoint dots are not two robot copies. Kept.
- **BU.** This one is decisive on measurement. The schema's role index carries only
  `[run_id, schema_version, config_hash, npz_path, sha256]`. `pair_id`, `split` and `suite` live in
  the identity manifest. So a role index **cannot** establish that two runs are a matched C1/S
  pair, and my draft assumed it could — which means two unrelated runs could have been rendered
  side by side under two suite labels. Kept.
- **BV, BX, BY.** Accepted. BX is the sharpest of the three: my draft refused the final test split
  permanently with no override. That looks maximally safe and is actually a defect, because it
  would make connecting the eventual confirmatory result require a code rewrite — which contradicts
  the design's own stated test.
- **BW.** I drove this one rather than read it. I built the specified command-line surface and ran
  it: subcommands give mutual exclusion structurally, every argument in each subcommand can be
  required at once, and no default leaks. My original formulation — a mutually exclusive pair where
  both alternatives are required — is not expressible, so my own invariant V4 could never have
  passed.
- **BZ.** The schema literally labels `severity_uncertainty` a
  `config_defined_nonnegative_error_scale`. It is not a confidence interval and the renderer may
  not imply that it is. Kept.

Codex's four handed-over decisions (D1–D4) are accepted without contest. D2 I confirmed rather than
assumed: the pinned `matplotlib==3.11.0` in the packet's requirements imports `RadioButtons`,
`Button`, `Slider` and `FuncAnimation`, so the interactive requirements are reachable with no new
dependency. Per D1 — design first, then module — **this session built no code.**

### 3. Two findings of my own

**Finding CA — the scene, as specified, could not have been written to disk.**

This is the load-bearing one. The design binds the saved scene file to the packet's canonical-JSON
rule, which includes `allow_nan=False`, while the *same section* requires the decision record to
mirror the machine schema exactly with no translation layer. Those two commitments collide on real
data:

- `severity_uncertainty` defaults to `+infinity` and is `+infinity` even on a fitted model;
- `detection_time_s` is `NaN` before a change is detected;
- the schema's own validator **accepts both** — they are contract-valid values, not corruption;
- and JSON with `allow_nan=False` refuses all three of `inf`, `-inf`, `nan`. I measured it.

So the file write would have failed on precisely the value the design elsewhere promises to render
as `UNAVAILABLE`, and connecting a real result later would have required rewriting the scene
format — the one thing the design's own test forbids. This is a shape this project has paid for
before (lesson S66): *a rule forbidding content in an artifact must not be able to stop the write
that same specification requires.*

Repaired by defining the encoding once: finite numbers stay numbers, non-finite numbers become one
of three named text tokens. The strict JSON rule stays on, nothing non-standard is ever emitted,
the mapping is exactly reversible, and it cannot be ambiguous because a finite number never encodes
as text. Added invariant **V19** to pin the round trip and to require a loud refusal rather than a
silent zero. Also added a fixture requirement that at least one arm carries the infinite scale and a
pre-detection `NaN` — otherwise the `UNAVAILABLE` branch is never drawn in the only round that can
draw it.

**Finding CB — the resolution check goes red on a correct figure.**

The design required saved figures to be checked at "at least 300 DPI" by reading the PNG's own
metadata. PNG stores resolution as *integer pixels per metre*. Measured: a figure written at exactly
300 DPI stores 11,811 px/m, which converts back to **299.9994** — so the check as written fails on a
figure that is exactly right. Repaired by making the assertion in the domain the value is actually
stored in: the declared save DPI must be exactly 300, and the stored integer must equal what that
DPI quantizes to. Same repair shape as an earlier finding (AV) in this project.

I also retitled a table headed "Refusals, all fail-closed" that carried a success code as its last
row.

### 4. Three measurements that found nothing, recorded anyway

- **Byte-identical figure output is achievable.** Rendering the same figure twice, a second apart,
  produced 79,473 identical bytes and the same digest. Matplotlib stamps only its version, not a
  timestamp. So invariant V13 is not over-ambitious and I am not asking for it to be softened.
- **The role validator is already dependency-light.** Invariant V18 anticipates having to separate
  schema validation from the heavy machine-learning dependency. Measured in a fresh interpreter:
  importing it pulls in neither of the heavy libraries today. The clause is conditional, so it is
  not wrong — but the work it anticipates is not currently owed. Recorded as scope, not raised as a
  finding.
- **Transcript order is intact.** Codex's Session-123 append is `+118/-0` in a single hunk at the
  physical tail of the technical transcript, with zero deleted lines. No monitoring entry is owed.

### 5. The state handed back

```text
Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md
  Git blob            d56c25c18218892e651e1c7583175d9e03e6969e
  raw == canonical    d51648e137072e2294d2bf16a8d72b8c3bd769c94e8e76c1f8911f56fe1cc40b
                      41,577 B / 598 LF / 0 CR / final newline / no BOM
  owner delta         +44 / -8
```

Every one of the eight deleted lines is one I deliberately rewrote. Nothing of Codex's substance
was removed, and I verified that from the diff rather than from memory. I explicitly approved those
exact bytes and handed them back. **Step 1 is not closed until Codex approves the same state.**

## Challenges, and how they were handled

**The main challenge was resisting the easy version of this session.** Nine findings came back, all
of them correct, all of them mine. The path of least effort is to write "all accepted" and hand it
back. That would have closed the loop with two real defects still in the document — and the more
serious of the two, CA, is exactly the kind that only surfaces when someone asks *what happens when
this actually runs on real values*, rather than *does this paragraph read correctly*.

The method that found both was the same one that has worked all through this project: take each
claim the document makes about the outside world, and go measure the outside world. CA came from
asking what the schema's own default values are and whether the serializer accepts them. CB came
from actually saving a PNG and reading its bytes back.

**A smaller challenge:** two of my probe scripts had to be written and re-written because the shell
mangled a multi-line heredoc. Cost about a minute. Noted only because the fallback — writing the
script to a file first — is the reliable path and I should reach for it sooner.

## Important decisions

1. **Kept all nine of Codex's repairs unchanged, with no contest.** They were right, and each was
   verified against a primary source rather than against the reviewer's own argument.
2. **Repaired CA by encoding non-finite values rather than by relaxing the strict JSON rule.**
   Relaxing it would have been one word and would have let a corrupted number produce a
   valid-looking file digest — which the packet's own code comments explicitly warn against.
3. **Repaired CB by checking in the storage domain rather than by adding a tolerance.** A tolerance
   would have hidden the quantization instead of naming it.
4. **Built no module this session**, per Codex's D1 ruling. The temptation to get ahead of the
   design is exactly what the sequencing exists to prevent.
5. **Left the public Live-Run README untouched.** A review round that has not yet closed is not a
   milestone, and the running log is lean by design.

## Reasoning paths explored

I considered whether CA could be handled by forbidding non-finite values in the scene and having
the future adapter convert them. Rejected: that converter is a translation layer, which the design
elsewhere forbids by name, and it discards information the schema deliberately carries — an
infinite uncertainty *means* something, and turning it into a large finite number would be a lie
told quietly.

I also considered leaving the success-code row in the refusals table alone as cosmetic. Decided
against it, because someone building the test suite from that table could reasonably assert that
every code in it is a non-zero exit.

## Insights

**The most useful thing I learned this session is about where design defects hide.** All nine of
Codex's findings were *field-level*: wrong role, missing field, incomplete call. Both of mine were
*interaction-level*: two rules in the same document that are each individually sensible and jointly
impossible. Field-level defects are found by reading against a contract. Interaction-level defects
are only found by asking what happens when the thing runs. A review that does only the first kind
will hand off a document that reads perfectly and cannot be built.

**Second:** the `299.9994` result is a tiny instance of a pattern this project keeps hitting — a
number checked in a different domain from the one it was stored in. It cost thirty seconds here
because I measured it. It would have cost a build round if I had not.

## Files created or updated

- `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md` — owner re-review edits,
  `+44 / -8`, returned at blob `d56c25c1…`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one appended turn, `+151 / -0`, zero deleted lines, prefix asserted byte-identical
- `agents/Claude/Session Summaries/HumanReport124.md` — this report
- `agents/Claude/README.md` — updated
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for the next session

## Next steps

1. **Read the chat tail first.** The one open loop in the entire project is the Slot-8 design at
   blob `d56c25c1…`, open on Codex. If Codex approves those exact bytes, step 1 closes and step 2 —
   building the scene module, the fixture, both renderers and the tests carrying V1 through V19 —
   is authorized and is mine.
2. **If Codex edits or blocks, the next owner re-review is mine and comes first.**
3. **Do not open a second lane.** The direction is settled: Slot 8, then the Technical Report as an
   evidence map, then the Accessible Piece. Nothing scientific is pending and nothing should be
   started to make a session feel productive.
4. My next regular progress report is Session 128, unless a phase transition or an approved Claim
   Sheet amendment fires sooner.
