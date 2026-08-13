# Human Report - Codex Session 128

**Current date and time:** 2026-08-13 15:22 PDT

## Summary

This session completed the required AgentPrompt workflow through the technical review and closeout
preparation for Slot-8 verification-artifact Step 2.

Claude handed off four explicitly approved files: the verification scene/bundle and synthetic
fixture module, the shared painter/interactive/scripted renderer module, and their two test files.
I authenticated the four exact blobs and the preceding transcript state before reviewing. The
owner state passed all 144 focused tests, but direct code review, public-surface drives, and visual
inspection found four contract-level defects its tests missed. I repaired the implementation and
tests, explicitly approved the new exact four-blob state, and handed it back to Claude through the
append-only Phase-2 transcript.

The repaired state now:

- displays human-readable body-change labels in the director's radio-button menu rather than
  internal case IDs;
- requires those display labels to be unique;
- validates a complete V1 bundle at both rendering boundaries before creating output or a UI;
- advances the visible timeline slider together with the animated frame;
- enforces the frozen project-relative output-directory contract across Windows and POSIX path
  forms, including parent traversal; and
- carries twelve additional regression tests plus two Windows-rooted path cases, increasing the
  focused suite from 144 to 158 tests.

I explicitly approved the reviewer-edited blobs. Claude's genuine same-state owner re-review is
open, so Step 2 is **OPEN / CODEX APPROVED / OWNER RE-REVIEW REQUIRED**. Step 3 remains blocked: no
fixture figure set was checked into the packet, and no packet runbook step was added. The public
Live-Run README remains unchanged because the synthetic working surface has not reached joint
approval.

I independently reproduced the new machine blocker Claude reported: `import mujoco` fails because
Windows Application Control blocks `mujoco._functions`. The focused Slot-8 lane does not import
MuJoCo and remains healthy. The packet-wide fallback suite reports 1,343 passed, one failure, and
28 collection errors; the failure and all collection errors terminate at the same blocked MuJoCo
DLL import. The director request already logged by Claude is accurate and remains open.

This was also my regular eighth-session progress-report trigger. I wrote
`agents/Codex/Progress Reports/Progress Report Session 128.md`, covering Sessions 121-128 at the
director-facing readability bar.

No fit, checkpoint, rollout, generation, analyzer or C7 invocation occurred. I read no scientific
role, role index, config, checkpoint, pilot, validation or test outcome. I made no capacity, rung,
width, probability-threshold, abstention-threshold, final-configuration or scientific C1-versus-S
decision.

## Exact review state

Claude's original handoff identities reproduced exactly:

```text
verification_scene.py              blob 1c45ac0f...  raw SHA-256 81bf4dcf...
render_verification_scene.py       blob 4c5ce765...  raw SHA-256 f94d8290...
test_verification_scene.py         blob fcc250a0...  raw SHA-256 34c543ec...
test_render_verification_scene.py  blob 0c9f85db...  raw SHA-256 d547d390...
```

The reviewer-edited state I approve is:

```text
Reproducibility Packet/scripts/utils/verification_scene.py
  Git blob (filtered == --no-filters)  c12745abc1fff3f09a6077543cf9dc5cfcc49b3a
  raw == canonical SHA-256             d811e0875b7dabeef053ca01ff908f66e3fc3f3472727e4d385478a228251597
  bytes / LF / CR                      63,651 / 1,639 / 0

Reproducibility Packet/scripts/render_verification_scene.py
  Git blob (filtered == --no-filters)  0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5
  raw == canonical SHA-256             fd8644d5dbd864ba335ae8e5585d9f65ae2a4f7f256aa997b6780ee29889ce0d
  bytes / LF / CR                      30,100 / 785 / 0

Reproducibility Packet/tests/test_verification_scene.py
  Git blob (filtered == --no-filters)  cf61e5aad09bc5dceab15519e7888fb97fe70b27
  raw == canonical SHA-256             b4747571120c6415f9344dd1da5c425932fadc1ca2ca14112236bcd9587a529f
  bytes / LF / CR                      43,252 / 1,111 / 0

Reproducibility Packet/tests/test_render_verification_scene.py
  Git blob (filtered == --no-filters)  ba7d135afe62789af06ca114c1f4e904fd09d894
  raw == canonical SHA-256             08fdeeb64c1d755c077244841f0799e6e5c8099de346baa77c6b8f3b76e4d835
  bytes / LF / CR                      33,822 / 859 / 0
```

All four have a final LF, no BOM, ASCII-only content, zero CR bytes, and equal filtered and
no-filter Git blobs. I deliberately did not add end-of-line attributes: no packet runtime hashes
these Python files, Git blobs are the durable review identities, and raw working-tree digests are
already labeled as local measurements that can materialize differently under
`core.autocrlf=true`.

## Findings and repairs

### CP - the interactive menu exposed implementation IDs to the director

The approved design's A1 requirement says the director selects a named body change without typing,
and property 8 says unique case labels are bundle data. The owner implementation instead used the
mapping keys as `RadioButtons` labels:

```text
soften_link_2
weaken_actuator_1
bias_encoder_1
indistinguishable_softening
```

The bundle already carried the intended labels:

```text
Soften link 2 by 30%
Weaken actuator 1
Bias encoder 1
Soften link 1 by 10% (the two suites are indistinguishable)
```

I added one label-to-case mapping in the interactive surface, changed the radio callback to use the
human-readable label, and required exact label uniqueness in `validate_bundle`. The regression
test now drives `RadioButtons.set_active(...)` and proves the visible choice selects the expected
case. A second test proves duplicate labels refuse with `X_BUNDLE_INCOMPLETE`.

### CQ - an incomplete bundle could reach both surfaces

The builders called `validate_bundle`, but `render_bundle` and `InteractiveVerificationSurface`
did not. Because the dataclasses and constructors are public, a caller could assemble a partial
menu and send it directly to either surface. That violated V1's complete-menu-or-nothing guarantee
at the boundary where publication occurs.

Both surfaces now validate the bundle before creating an output directory or UI. A regression
test removes the sensor case, requires both surfaces to refuse with `X_BUNDLE_INCOMPLETE`, and
confirms the scripted path leaves no partial directory behind.

### CR - animation and the visible timeline diverged

`advance_frame` changed `surface.frame` and repainted directly, but never updated the `Slider`.
The body and call panels moved while the control continued to display the previous frame. This was
not a scientific-timebase error; it was a user-visible state mismatch.

Playback now advances through `slider.set_val(...)`. The slider's callback owns the frame update
and repaint, so the displayed frame, control thumb, and painter cannot take separate routes. The
test asserts both values wrap from the final frame to zero together.

### CS - the output path contract was only documentation

Both CLI subcommands accepted absolute destinations and `..` traversal even though section 4.2
requires a project-relative `--output-dir`. I added one parser used by both subcommands. It rejects:

- POSIX absolute paths;
- Windows drive-qualified paths;
- Windows rooted paths without a drive;
- Windows or POSIX parent traversal.

The tests cover fixture and role subcommands across all forms. Valid packet-relative output remains
unchanged. The role path still refuses with `X_CONNECTION_UNAUTHORIZED` before reading any named
input when its CLI is otherwise valid.

## Decisions on Claude's flagged questions

1. **Distal-point mismatch exit code:** I chose option (a). The current design has no truthful
   exit code for a geometry mismatch and Step 2 has no real adapter. The fixture generator calls
   the public helper for every arm and its passing and failing sides are tested. The separate
   Step-4 connection-record/adapter design must assign the code before real geometry is reachable.
2. **Malformed `EstimatorOutput`:** I accept `X_DECISION_UNSUPPORTED`. A schema-D-invalid decision
   cannot be causally selected or rendered by the call panel. This is the narrowest current code
   and fails safely.
3. **Fixture CLI shape:** accepted. Since V4 fixes the two fixture arguments exactly, one fixture
   invocation writes the deterministic scripted set and opens the menu. No new `--interactive`
   flag is needed.

## Verification performed

```text
owner-state exact identities                       reproduced
transcript digest chain                            reproduced
owner focused tests                                144 passed
reviewer focused tests                             158 passed
reviewer focused tests under python -O             158 passed; expected pytest warning only
packet-wide --continue-on-collection-errors        1,343 passed, 1 failed, 28 collection errors
fresh `import mujoco`                              blocked by Windows Application Control
independent menu/slider/path interaction probe      passed
manual inspection of 300-DPI scripted PNG          passed
manual inspection of interactive wrapper figure    passed
Python bytecode compilation                         passed
git diff --check before closeout                    passed
```

The packet-wide single failure is
`test_dev_fit_contract.py::test_the_authority_string_equals_the_extension_scripts_own_constant`;
it fails only when importing the extension script reaches MuJoCo. The 28 collection errors reach
the same DLL boundary. Neither reaches either edited Slot-8 runtime module.

The first interactive CLI probe opened the expected GUI and therefore remained active until the
window was closed. I terminated the exact process tree I had spawned after capturing the temporary
review figures; no unrelated Python process was touched and no generated figure was added to the
project.

## Transcript integrity

The Phase-2 transcript append used the complete existing file as the asserted byte prefix rather
than a text patch over its mixed line endings:

```text
prior bytes / LF / CR   2,192,838 / 35,642 / 19,709
prior SHA-256           8611d45f0afecb310e0dc113687911af057b63b48f8619f0e37a7221fdd128e4
EOF anchor count        1
session delta           +113 / -0, physical tail
post bytes / LF / CR    2,199,774 / 35,754 / 19,709
post SHA-256            98ab2f375a7295d026e815538086e2118bab12af2a396a7c3c26e4054486355d
new header count        1 after the recorded line boundary
last agent header       Codex Session 128 Step-2 review
```

The first 2,192,838 bytes were re-read and reproduced the prior digest after the write; the exact
new payload was the physical suffix. No Transcript Order Monitoring entry was needed because no
order or byte-prefix failure occurred.

## Challenges and how they were overcome

### Passing tests encoded one wrong behavior

The original menu test asserted that radio labels equaled the bundle's internal keys, so the test
made the defect look required. I resolved this against A1 and property 8 rather than preserving the
test as authority. The rewritten test drives the human-readable control and the data model now
enforces the uniqueness that makes the mapping unambiguous.

### A GUI command correctly blocked the shell

Running fixture mode outside the test suite selected an interactive Matplotlib backend, created the
window, and waited in `plt.show()`. This was expected behavior, not a hang in the renderer. I used
the already-written temporary figures for visual review, then positively identified and stopped
only the exact two-process launcher/interpreter tree spawned by that command. Later visual probes
used the non-interactive Agg backend.

### The full suite could not produce its normal count

I did not bypass or disable Windows Application Control and did not exclude MuJoCo modules and call
the remainder a full pass. I reproduced the base import failure, ran the approved fallback with
collection errors continuing, and reported its exact pass/fail/error shape. The current lane is
still directly verified because its two modules and tests are dependency-light by design.

### Mixed transcript line endings made ordinary patching unsafe

The transcript contains both CRLF and LF. Prior project evidence shows that a line patch can look
additions-only in Git while rewriting physical bytes. I used the full prior byte sequence as the
literal prefix, generated the timestamp at write time, appended an LF-only payload, and asserted
prefix digest, suffix identity, header uniqueness, boundary position, last-agent predicate, and
additions-only Git diff before continuing.

## Important decisions

1. **Do not approve the owner blobs merely because 144 tests passed.** The actual director-facing
   control and bypass routes exposed four missed requirements.
2. **Repair tests with the code.** Each finding now has a fail-before/pass-after regression test.
3. **Keep Step 2 open.** Reviewer edits mean Claude must genuinely re-open the exact four blobs.
4. **Do not add an end-of-line pin without a runtime integrity need.** Git blob identities are
   sufficient for this review object.
5. **Do not promote the synthetic scaffold publicly yet.** The root README milestone remains
   same-state approval of the working surface, not a unilateral implementation.
6. **Keep the machine security block with the director.** Agents should not weaken a Windows
   execution-control policy to recover MuJoCo.

## Reasoning paths explored

I considered approving the menu's case IDs as acceptable stable names because every case was
present. That failed the user-level A1 requirement: the director was promised body-change choices,
and the bundle already had explicit display labels. Showing the IDs also left property 8's label
uniqueness unused. The correct repair was to map labels to IDs, not to rename IDs or duplicate
scene state.

I considered validating only the fixture bundle and leaving surface functions as trusted internal
APIs. The types and functions are public packet APIs, and V1 is a publication/display guarantee.
Revalidating at the two consuming boundaries is inexpensive and prevents partial output before it
exists.

I considered updating `surface.frame` and then separately setting `slider.val`. That would still
create two update routes and risk duplicate repaint behavior. Routing animation through
`Slider.set_val` makes the widget callback the one owner of timeline movement.

I considered checking only `Path.is_absolute()` for output directories. That is insufficient for
a packet intended to work across platforms: a Windows drive-relative path and a rooted path without
a drive have different semantics, and `..` can escape while remaining lexically relative. Checking
both `PureWindowsPath` and `PurePosixPath` plus parent segments makes the declared contract portable.

I considered assigning the distal-geometry mismatch to `X_PAIR_MISMATCH`. The current exit table
does not say that code owns per-arm derived-geometry inconsistency, and there is no real adapter in
Step 2. Deferring the assignment to the adapter design keeps the table truthful without weakening
the tested fixture path.

## Insights gained

**User-facing semantics need user-facing tests.** Counting radio entries and checking their keys
does not establish that the director sees the promised choices. The useful test drove the actual
widget and read the visible labels.

**A complete-object invariant belongs at the consumption boundary too.** Builders are not security
or publication boundaries when values can be constructed directly. Rendering should fail closed on
the object it receives.

**One clock in the data does not guarantee one timeline in the interface.** The scene's scientific
frame was correct while the visible slider was stale. Synchronization has to include the controls a
human uses to understand the state.

**Portability includes path grammar.** A path rule written for one operating system is not a packet
contract. The parser now measures both grammars even when tests run on only one host.

## Files created or updated

- `Reproducibility Packet/scripts/utils/verification_scene.py` - added unique menu-label
  validation.
- `Reproducibility Packet/scripts/render_verification_scene.py` - added project-relative path
  parsing, surface-boundary bundle validation, human-readable radio labels, label-to-ID selection,
  and slider-synchronized playback.
- `Reproducibility Packet/tests/test_verification_scene.py` - added duplicate-label refusal.
- `Reproducibility Packet/tests/test_render_verification_scene.py` - added path-form, incomplete
  surface, visible-label callback, and synchronized-slider coverage; updated valid CLI tests to use
  project-relative outputs.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - appended the authenticated review, repairs, exact identities, explicit approval and remaining
  owner gate.
- `agents/Codex/Progress Reports/Progress Report Session 128.md` - regular cadence report covering
  Sessions 121-128.
- `agents/Codex/Session Summaries/HumanReport128.md` - this report.
- `agents/Codex/README.md` - updated the workspace map for the new report and current co-owned
  Slot-8 implementation state.
- `agents/Codex/Summary of Only Necessary Context.md` - completely rewritten for Session 129.

Read but not modified: `AgentPrompt.md`, all of `Project Details/`, `Claim Sheet.md`, the Slot-8
design, Review Cycle and Reproducibility Packet playbooks, every Codex-including chat summary and
active transcript, Claude's HumanReport128, the packet schema and live metric/estimator sources,
the root Live-Run README, and the Transcript Order Monitoring chat.

The scratch figures used for visual inspection live outside the project under the Codex
visualization directory and are not repository artifacts.

## Next steps

1. Claude re-opens and genuinely reviews exact blobs `c12745ab`, `0ae5b19d`, `cf61e5aa` and
   `ba7d135a`, then explicitly approves them or returns a new exact state.
2. Until that happens, Step 2 remains open and Step 3 remains blocked.
3. After Step-2 closure, the next authorized work is the fixture figure set and packet runbook
   integration, followed by their own review.
4. The real-result connection record and adapter remain a separate Step-4 design/review/joint
   authorization. That design must assign the distal-geometry refusal code.
5. Randy/admin resolves the MuJoCo Windows Application Control block before any plant-dependent
   work or clean full-suite count is required.
6. Capacity, thresholds, final configuration and every confirmatory lane remain behind their
   existing gates.
