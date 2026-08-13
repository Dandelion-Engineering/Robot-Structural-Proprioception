# Human Report — Claude Session 128

**Current date and time:** 2026-08-13 14:46 PDT

## Summary

Codex closed Slot-8 design **Step 1** in its Session 127 — both agents now approve the same bytes,
blob `0753d4ed`, and Codex's turn authorized exactly one thing: my Step-2 build. This session did
that build. Four new files, 144 new tests, one chat handoff, one progress report (this is my
regular Session-128 cadence report), and one director-only blocker logged.

The build is `Reproducibility Packet/scripts/utils/verification_scene.py` (the scene/bundle value
contract, its canonical-JSON codec and the labeled synthetic fixture),
`Reproducibility Packet/scripts/render_verification_scene.py` (the one shared painter, both
wrappers, the two-subcommand CLI and the fail-closed role stub), and the two test files carrying
invariants V1 through V19. Every scene the code can currently produce is `SYNTHETIC_FIXTURE` and
carries a **SYNTHETIC — NOT A RESULT** banner drawn into the figure; the real-role path refuses
with `X_CONNECTION_UNAUTHORIZED` before opening anything.

I also hit an environment blocker that is not the project's doing: **`import mujoco` now fails on
this machine because a Windows Application Control policy blocks the DLL.** That takes 29 of the
packet's tests out and makes the packet's full-suite count unmeasurable this session. It is logged
as entry 2 in `director_requests.md`, and the Slot-8 lane is unaffected because it imports neither
MuJoCo nor PyTorch by design.

**Spend: zero of everything.** No fit, checkpoint, rollout, generation run, analyzer or C7
invocation; no pilot, validation or test read; no role payload, role index, checkpoint or config
opened by any module or any test; no capacity, rung, width or threshold chosen; no figure written
into the packet. Checkpoint count not re-read — nothing this round depends on it; it stands at 67.

## What was accomplished

### 1. The handoff was authenticated before anything was built

The transcript on disk is 2,179,798 bytes at SHA-256
`3dd3424a7cafc4e1cd4fa99a199e039105126b025788a2134e5a592ef9e05be3` — exactly the post-write digest
Codex published in its Session-127 turn. So Codex was physically last, the approval I built against
is the one on disk, and **no Transcript Order Monitoring entry was owed**; I appended none. The
design at `0753d4ed` reproduced its declared identity and I did not touch it.

### 2. `verification_scene.py` — the contract, the codec and the fixture

```text
Git blob (filtered == --no-filters)  1c45ac0fe214521250a5dc18fa44650da1375c23
raw == canonical SHA-256             81bf4dcffc82454fed91a58da07879c4f703a2b04b67add0fb0a43a76cb5bc7d
bytes / LF / CR                      63,428 / 1,633 / 0
```

The load-bearing decision in it is **where each fact lives**, which is finding CN's lesson applied
in four places rather than one:

- **Decisions are `utils.estimator.EstimatorOutput` values.** Not a scene-local mirror of the nine
  schema-D fields — the live struct itself, and per-decision validity is established by calling
  that class's own `validate()`. There is no translation layer because there is no second type,
  which is design property 1 satisfied structurally rather than by discipline.
- **The analysis-window check is a call.** `_validate_tracking_window` calls `utils.metrics.j_5s`
  and re-raises whatever it raises as `X_WINDOW_UNSUPPORTED`.
- **Class order is `utils.metrics.SOURCE_CLASS_ORDER`**, imported.
- **Canonical JSON is `utils.protocol_p.canonical_json`**, with `allow_nan=False` still on and the
  three-string non-finite wire encoding doing the work CA specified.

Two clock facts are deliberately **not** bound, and both were checked against live source:

- `controller_t_s` is carried, validated finite and strictly increasing, and **never compared to
  `playback_t_s`** (finding CI's repair). The fixture deliberately carries the one-control-interval
  offset the live loop actually produces.
- **`onset_index` is carried verbatim and never used to index `playback_t_s`.** I went looking for a
  second instance of CI's shape and this is where it would have been:
  `assignment_generator._step_index` makes the label's onset `onset_s / dt` while `cable_plant`
  stamps `t_s` **after** advancing, so `plant.t_s[onset_index]` is one control interval later than
  `onset_time_s` in real data. Binding them would have re-created CI on a second axis. Only
  `onset_time_s` is used, and only by the live metric.

The fixture emits four named cases — `soften_link_2`, `weaken_actuator_1`, `bias_encoder_1`,
`indistinguishable_softening` — covering structure/actuator/sensor and jointly covering every
branch section 4.4 requires: confident correct, confident wrong, an abstention, a high
`unknown_score`, an indistinguishable pair, `+inf` severity scale with a pre-detection `NaN`, and a
decision state that changes. Grid: 141 samples at 20 Hz on the plant's own `(k+1)·dt` stamping
convention, onset exactly on sample 19 at 1.000 s, window close exactly on sample 119 at 6.000 s,
grid running on to 7.05 s so the derived scripted frame is **interior** rather than terminal.

### 3. `render_verification_scene.py` — one painter, two wrappers, two subcommands

```text
Git blob (filtered == --no-filters)  4c5ce765034a889d165d1fad82c354323cccfaa1
raw == canonical SHA-256             f94d82903cbccd62dc96f1e375054261d5999d7a8292d341594073882798f4c0
bytes / LF / CR                      28,449 / 746 / 0
```

`draw_scene(scene, *, frame) -> Figure` is pure and pyplot-free: it opens nothing, writes nothing
and holds no state. The scripted wrapper writes only its declared PNG / scene-JSON / bundle-JSON /
digest set. **The interactive wrapper paints nothing itself** — every update calls the same
painter, renders that figure to an RGBA buffer and displays it, so the animated view and the
published still cannot diverge. That is the converse of standing lesson S56 made structural.

### 4. The tests — 144, one named for each invariant

```text
tests/test_verification_scene.py         blob fcc250a0  42,477 B / 1,089 LF
tests/test_render_verification_scene.py  blob 0c9f85db  31,636 B /   795 LF
```

A mechanical sweep over the finished bytes confirms **every one of V1–V19 has at least one test
named for it, with none missing and none invented above 19.** Two of them are the ones I most want
to survive:

- **V15's delegation test** monkeypatches `j_5s` to raise a sentinel string no design document has
  ever contained and requires construction to refuse carrying that sentinel — plus an AST test
  asserting `_validate_tracking_window` contains a `j_5s` call. Replace the call with a checklist
  and both go red for a stated reason.
- **V6's accept side** requires a controller payload on the one-interval-offset grid to be
  **accepted**, and a second test requires an equal grid to be accepted too, so neither convention
  gets frozen in. Deleting either is how CI comes back.

The six `X_WINDOW_UNSUPPORTED` refusal shapes are asserted individually, and a companion test
**measures** that the last two (non-positive `window_s`; a window spanning fewer than two control
samples) pass every other named check — so the reason the enumeration was replaced by a call is in
the suite rather than only in the design's prose.

### 5. Measurements

```text
fixture bundle build            0.004 s
one scene painted               0.032 s
full scripted figure set        1.747 s   (4 PNG at 300 DPI + 4 scene JSON + bundle + digest)
canonical bundle document       340,741 B
canonical bundle SHA-256        3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70
one 300-DPI PNG                 440,690 - 459,160 B
pHYs payload on every PNG       (11811, 11811, 1)
```

Section 7 of the design asked for exactly those three timings. The scripted set is byte-identical
across two renders into different destinations, verified with `filecmp.cmp(shallow=False)` over
every written file.

**V11's byte half is a real check rather than a rasterization I cannot read**: `savefig` writes the
banner and the fixture disclaimer into PNG `tEXt` metadata alongside the figure-level artist that
draws them, so the test finds the exact strings in the file's bytes. And the pHYs payload is
`(11811, 11811, 1)` exactly — the test asserts that, and separately asserts that
`11811 × 0.0254 < 300.0`, which is the check that would have gone red on a correct figure had CB
not been found.

### 6. The environment blocker

`import mujoco` fails at the interpreter level:

> `ImportError: DLL load failed while importing _functions: An Application Control policy has
> blocked this file.`

28 packet test modules import it transitively and fail at collection; a 29th test fails inside the
same import. Measured with `--continue-on-collection-errors`: **1,328 passed, 1 failed, 28
collection errors**, every one of the 29 traced to that single import. **I did not quote a smaller
number as if it were the suite** — the full-suite count is unmeasurable while this holds, and
saying so is the honest report. Logged as `director_requests.md` entry 2 with the fallback named.

My two files alone: **144 passed in 21.20 s**, and **144 passed in 25.79 s under `python -O`**.

## Challenges and how they were overcome

### The Bash heredoc silently ate backslashes, three times

Three of my in-place edits went through a `python - <<'PY'` heredoc, and the shell collapsed
backslash sequences despite the quoted delimiter. The damage: one replacement pattern silently
failed to match (I noticed because the figure still had the old two-line title), one wrote
`..\venv` into `director_requests.md` as a vertical-tab character, and one turned a test's
`re.compile(r"\bci\b")` into `re.compile(r"ci")` — which then matched "confidence" and made the
test fail loudly. All three were caught, and the third was caught **because it failed**, not
because I read it.

The rule I am carrying forward: **never use a Bash heredoc for content containing backslashes.**
Use the Write/Edit tools, or build the string from `chr(92)` with no literal backslash in the
command. I re-swept all four finished files for control bytes and non-ASCII afterwards and they are
clean.

### A timestamp I wrote before I finished writing

The chat turn's header reads `14:47 PDT`; the append actually completed at about `14:41 PDT`. I set
the header while drafting and did not re-check the clock before writing. **I did not edit the chat
to fix it** — that file is append-only and a five-minute slip is not worth a correcting turn — so it
is recorded here instead. The ordering relative to Codex's 13:07 turn is unaffected. The rule:
read the clock immediately before writing the header, not while drafting the body.

### The design's exit-code table has no code for one check it states

Section 4.1's field table says the final centerline point must agree with `true_task_output`, and
property 6 / V16 assign that check to the future adapter with a declared tolerance — but the 4.3
table names **no exit code** for a geometry mismatch, and all twelve existing codes would have been
a lie if I had raised one. I did not invent a thirteenth. It ships as a public
`require_distal_point_matches_task_output(arm, *, tolerance=...)` with the tolerance declared once
at module level, called by the fixture generator on every arm it builds, with both its accept and
refuse sides tested — and the question is flagged to Codex to rule on rather than settled in a
build round.

### Layout that was legible only after looking at it

The first rendered figure had the FABRICATED TRUTH line overlapping the body-panel title, an
equal-aspect body plot stretched across a 13-inch axis, and two-line panel titles overflowing
horizontally. None of that is visible from the code. I rendered to the scratchpad and **looked at
the images**, three times, before the layout was right. Worth recording because the invariant tests
would all have passed on the unreadable version.

## Important decisions

1. **`EstimatorOutput` is the decision type, not a mirror of it.** The strongest available reading
   of design property 1 and of standing lesson 199.
2. **The fixture deliberately does not flatter `S`.** Case 1 gives `S` the smaller post-onset
   deviation, case 2 gives `C1` the smaller one, case 3 gives both the same, case 4 is exactly
   identical — and a test asserts at least one case is smaller for each suite. A synthetic menu
   whose every panel favoured the structural suite is precisely the misreading this design exists
   to prevent, and the banner alone did not seem sufficient.
3. **Fixture mode writes the scripted set and then opens the menu.** Section 4.2 pins fixture
   mode's argument set to exactly `--fixture-seed` and `--output-dir`, and V4 pins that set by
   equality, so an `--interactive` flag would have failed V4 as written. Both surfaces therefore
   run from one subcommand with no new flag. Flagged to Codex as a reading rather than asserted as
   the only one.
4. **A decision failing the live schema-D contract refuses with `X_DECISION_UNSUPPORTED`.** That is
   a reading of the 4.3 row rather than a literal item in it; the alternative — not validating
   decisions at construction — lets a malformed decision reach a renderer. Flagged.
5. **The public Live-Run README was not touched.** I ran the heartbeat check and agree with Codex's
   Session-127 call: the lean public milestone is the **reviewed** working surface, and step 2's
   review loop is open.
6. **The MuJoCo block was reported, not worked around.** No `--ignore` list quoted as a suite
   count, no smaller number presented as the whole.

## Reasoning paths explored

I considered making the distal-point check a construction-time refusal under `X_PAIR_MISMATCH` or
`X_TIMEBASE_MISMATCH`. Both would have been false labels for a geometry mismatch, and inventing a
fourteenth code is a design change I have no authority to make in a build round. Flagging it costs
one round-trip and keeps the exit table honest.

I considered checking `playback_t_s` for uniformity, monotonicity and finiteness at construction
under `X_TIMEBASE_MISMATCH`. **That would have broken V15**, which requires a non-uniform grid to
surface as `X_WINDOW_UNSUPPORTED` — my check would have pre-empted the delegation for exactly the
shape the delegation exists to cover. Construction therefore checks only the grid's *rank*, and
every property of the grid itself is delegated. This is the same shape as CN one level down, and I
only saw it because I read V15's six shapes before writing the validator rather than after.

I considered embedding the interactive controls into the painter's own figure via subfigures. That
would have required extending the pinned `draw_scene(scene, *, frame)` signature with a `figure=`
keyword. Rendering the painter's output to a buffer and displaying it keeps the signature exactly
as approved, and makes the "one source" property structural instead of conventional.

I considered whether the JSON decoder is a way to smuggle a `FINAL`-labelled scene into a renderer,
since it reconstructs provenance from a document rather than computing it. It is not reachable:
**no CLI argument reads a bundle or scene document.** Fixture mode builds from a seed and role mode
refuses. The codec exists for round-trip auditing, and the module docstring and a test both say so.

## Insights gained

**The question that found three defects across two sessions is the same question.** "When this
object names a fact some other object already owns, does it point at that object or copy it?" In
Session 127 it found CN. In this session it found the `onset_index` trap before it was written, and
it found the uniformity-check trap that would have broken V15. A copy takes on an obligation to
stay current that nothing in this project enforces — and the enforcement mechanism, when you can
build one, is a test that makes the copy impossible rather than a comment asking for it.

**A test that asserts a call happened is weaker than a test that assumes the call and watches it
fail.** The AST test proving `_validate_tracking_window` contains `j_5s` can be satisfied by a
function that calls it and ignores the result. The monkeypatch test — replace the function with one
that raises a sentence no design document contains, then require that sentence to appear in the
refusal — cannot. Both are in the suite; only the second is load-bearing.

**Looking at the picture is a measurement.** Nineteen invariants and 144 tests passed on a figure
whose truth line overlapped its title and whose body panel was a sliver. The tests check what the
artifact must never do; none of them checks whether a human can read it, and for a *director's*
verification artifact that is the property the whole thing exists for.

## Files created or updated

- `Reproducibility Packet/scripts/utils/verification_scene.py` — **new**, blob `1c45ac0f`
- `Reproducibility Packet/scripts/render_verification_scene.py` — **new**, blob `4c5ce765`
- `Reproducibility Packet/tests/test_verification_scene.py` — **new**, blob `fcc250a0`
- `Reproducibility Packet/tests/test_render_verification_scene.py` — **new**, blob `0c9f85db`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Step-2 handoff with the four exact identities, the measurements, the two flagged
  design questions and my explicit approval (`+205/-0`, 0 CR added, prefix asserted byte-identical)
- `director_requests.md` — appended entry 2, the MuJoCo Application Control block (`+41/-0`)
- `agents/Claude/Progress Reports/Progress Report Session 128.md` — **new**, the regular
  Session-128 cadence report covering S121–S128
- `agents/Claude/Session Summaries/HumanReport128.md` — this report
- `agents/Claude/README.md` — the Slot-8 bullet pruned to purpose under the file's own maintenance
  rule (9,364 chars → 5,767 across two bullets) and a new bullet for the four Step-2 files
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 129

Read but not modified: `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md`,
`schema/schema.json`, `utils/metrics.py`, `utils/estimator.py`, `utils/role_contract.py`,
`utils/assignment_generator.py`, `utils/cable_plant.py`, `utils/protocol_p.py`, and Codex's
`HumanReport127.md` (the cross-review read — nothing to correct, no loop opened).

The root Live-Run README and the Transcript Order Monitoring chat were deliberately unchanged.

## Next steps

1. **Codex reviews the four Step-2 blobs** against the frozen design, the Reproducibility Packet
   playbook and the Review Cycle playbook. If it edits or blocks, **the owner re-review is mine and
   comes first.**
2. **Codex should rule on the two flagged questions**: the missing exit code for a distal-point
   geometry mismatch, and the `X_DECISION_UNSUPPORTED` mapping for a decision that fails the live
   schema-D contract.
3. **Step 3 stays blocked** until this loop closes: no fixture figure set into the packet, no
   runbook step.
4. **Step 4 — connecting a real result — is a separate design, review and joint authorization**,
   and it also needs the three inputs section 1.1 lists as absent.
5. **The MuJoCo block is Randy's**, logged as entry 2. Nothing in the current lane waits on it, but
   the next thing that needs a rollout does.
