# Progress Report - Codex, Session 128

**Written:** 2026-08-13 15:21 PDT
**Covers:** my Sessions 121-128 (previous regular report: Session 120)
**Phase:** 2 - Execution, with limited Phase-3 packet assembly
**Written for:** Randy

---

## The short version

The last report ended with the project's second learned-model run complete and its packet
documentation still under review. This eight-session stretch closed that documentation, published
one careful public heartbeat, and then moved to a different completion requirement: the hands-on
Slot-8 verification artifact promised in the Claim Sheet.

The verification artifact is not yet connected to a project result. The final configuration,
selected checkpoint, and validation-owned thresholds do not exist, so connecting today's
development record would make a polished picture look more authoritative than it is. The team
therefore designed and built the part that can be made honestly now: one scene-and-bundle contract,
one shared painter, a visibly fabricated fixture, an interactive menu, a deterministic 300-DPI
figure path, and a real-role command that refuses before reading anything.

The design is jointly approved. Claude then built the four-file implementation and explicitly
approved it. My Session-128 review found four defects in the user-facing and fail-closed behavior,
repaired them, and approved the new exact state. Claude's owner re-review is still required, so the
implementation is real and tested but the review loop is not closed.

One machine problem appeared outside this lane: Windows now blocks MuJoCo's compiled Python module
under an Application Control policy. That prevents the complete packet test suite and every
plant-dependent command from running. It is logged for you in `director_requests.md`. The current
verification work is unaffected because its two runtime modules deliberately import neither
MuJoCo nor PyTorch.

## The idea that matters: prove the display before giving it scientific authority

Slot 8 asks for an interactive side-by-side view: choose a body change, watch the conventional C1
and structural S systems replay the same task, read each fault call and confidence, and compare the
two tracking traces. That surface will eventually make the final result easier to inspect than a
table alone.

But a clear interface can create a false impression of finality. The current development record is
not a selected result, and the project has not frozen the configuration or the abstention and
unknown thresholds that a final display needs. A polished demo built directly from those records
would be more misleading than no demo.

The solution is a scaffold with an explicit authority boundary:

- The reachable fixture is visibly labeled **SYNTHETIC - NOT A RESULT** and **FABRICATED TRUTH**.
- The fixture deliberately contains a correct call, a wrong call, an abstention, high unknown
  scores, and a case where C1 and S are indistinguishable. It is not designed to flatter S.
- The interactive and scripted views share the same pure painter, so a report figure cannot drift
  from what the director saw in the menu.
- The future real-result path requires a separately reviewed connection record. Until that exists,
  the `roles` command returns `X_CONNECTION_UNAUTHORIZED` before opening a config, checkpoint,
  role index, or role payload.

The controls use Matplotlib's GUI-neutral
[radio-button, slider, and button widgets](https://matplotlib.org/stable/api/widgets_api.html), so
the packet adds no new web framework or dependency. That is a small but important affordability
choice: the verification path should be easier to run than the research pipeline, not harder.

## What happened in Sessions 121-128

### 1. The rung-2 documentation and public heartbeat closed

Session 121 re-opened the packet runbook after Claude's correction round and independently checked
the per-class counts, five paired signs, two equivalence controls, checkpoint boundary, and runtime
record. Both agents then approved the same packet README bytes.

Sessions 122-123 did the same for the public Live-Run README. The final wording says the central
scientific question remains unanswered while acknowledging that several development protocols and
narrower build questions are settled. It does not say that "nothing is frozen," and it does not
mistake an internal run for a research conclusion.

### 2. The verification-artifact design took five rounds to close

Claude drafted a packet-local scene contract. Across Sessions 123-127, the two agents found and
repaired several classes of defect before code existed:

- missing task-output and geometry fields;
- caller-supplied authority that could have mislabeled development data;
- incomplete authentication of paired C1/S inputs;
- a serializer that could not carry the estimator's valid infinity and not-a-number defaults;
- a shared painter with no frame argument, so it could not animate;
- separate arm clocks that could have shown different physical times at one frame;
- a call panel with no causal rule, which could have displayed a final diagnosis before it existed;
- a controller timestamp equality the live loop does not promise; and
- a duplicated checklist for the tracking metric that already had one live source of truth.

The jointly approved design now makes one scene-level playback grid authoritative, selects the
latest decision available at each frame, delegates tracking-window validity to the live metric,
and keeps all scientific inputs outside the renderer.

### 3. Claude built the four-file Step-2 object

The build comprises:

- `scripts/utils/verification_scene.py` - values, validation, strict JSON, and fixture generation;
- `scripts/render_verification_scene.py` - shared painter, interactive surface, scripted figures,
  CLI, and fail-closed role stub; and
- two test files carrying the design's V1-V19 invariants.

Claude's state passed 144 focused tests in normal and optimized Python modes. The generated scene
was readable at 300 DPI, carried the warning and provenance inside the image, and persisted the
exact PNG resolution metadata the design requires.

### 4. Codex repaired four defects in the implementation

The tests all passed, but direct interaction probes found behavior the tests had encoded
incorrectly or not encoded at all:

1. The radio menu displayed internal IDs such as `soften_link_2` instead of the human-readable
   body-change names the director is supposed to choose.
2. The surface functions trusted that every caller had already validated the bundle, so an
   incomplete menu could be rendered if the normal builder was bypassed.
3. Animation advanced the picture while leaving the visible timeline slider on the old frame.
4. Both CLI modes accepted absolute and parent-traversing output paths despite the frozen
   packet-relative contract.

The corrected state shows descriptive labels, requires those labels to be unique, validates the
whole bundle before either surface opens, advances through the slider itself, and rejects Windows
or POSIX output paths that can escape the packet. The focused suite is now **158 tests**, passing
in normal and optimized modes. I explicitly approved the repaired four blobs; Claude must now
re-open and approve those exact bytes or return another state.

## What was unexpected

- A test can prove that every case appears in the radio menu while still proving the wrong thing:
  the original test required the internal IDs. Looking at the control as a director would exposed
  the mismatch immediately.
- The animation's scientific frame and picture stayed synchronized, but the slider did not. This
  is a presentation-state bug, not a numerical bug, and it only appears when the control is driven.
- V1's "complete menu or nothing" guarantee lived in the builders but not in the surfaces. Public
  value types make builder bypasses possible, so the boundary that publishes or displays data has
  to reassert the invariant.
- A path can be lexically relative and still escape through `..`, and Windows has rooted and
  drive-qualified forms that a POSIX-only check will miss.

## What is working

- The exact-state review cycle continues to find defects even when all owner tests pass.
- The scientific and presentation layers are separated. Rendering reads no role and makes no
  model, capacity, threshold, or configuration choice.
- The synthetic fixture is conspicuously non-scientific and contains failure cases, not a staged
  demonstration of S winning.
- One painter drives the interactive and scripted views.
- The four edited files pass 158 focused tests in both Python modes and compile cleanly.
- The root public README remains lean. It has not advertised a surface whose review is still open.

## What is not working or remains open

- Claude's same-state owner re-review is required before Step 2 closes.
- No fixture figures are checked into the packet and no runbook step is authorized until that
  review closes.
- Connecting a real result is a later design, review, and joint authorization. The final config,
  selected checkpoints, and validation-owned thresholds are still absent.
- Capacity, probability threshold, abstention threshold, and final configuration remain undecided.
- Pilot, validation, and test outcomes remain unread for those decisions.
- The packet still has 67 ignored checkpoint files without a final clean-machine distribution or
  recovery ruling.
- `import mujoco` is blocked by Windows Application Control. Microsoft describes
  [Smart App Control](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/overview)
  as an execution-control feature that can block unknown or unsigned binaries. The project has not
  diagnosed which exact policy component made this decision; it has only reproduced the block at
  the MuJoCo DLL boundary. Resolving the machine policy is a director/admin action, not an agent
  workaround.
- `director_requests.md` entry 1, the non-blocking Claim Sheet review, also remains open.

The packet-wide fallback suite currently reports **1,343 passed, 1 failed, and 28 collection
errors**. The failure and all collection errors terminate at the same blocked MuJoCo import. That
is not being reported as a clean full-suite pass.

## Verification artifact

There is now a real, inspectable synthetic verification surface. It shows two bodies, causal fault
calls, confidence and unknown state, tracking traces, onset and analysis windows, provenance, and
the synthetic warnings. It can write deterministic 300-DPI figures and expose the same four cases
through an interactive menu.

What it verifies today is only the mechanism: the scene contract can carry the promised information
and both surfaces can display it consistently. It verifies nothing about whether structural sensing
helps the robot. That remains behind the final scientific connection and confirmatory protocol.

## What happens next

1. Claude genuinely re-reviews the four reviewer-edited Step-2 blobs and either approves them
   exactly or returns a new state.
2. Only after same-state approval may Step 3 generate the fixture figure set into the packet and
   add its runbook step.
3. The real-result adapter remains a separately designed and authorized Step 4. It must assign a
   truthful refusal code to distal geometry mismatch and authenticate every config, checkpoint,
   pair, role index, and payload it reads.
4. Any future plant-dependent work waits for the MuJoCo application-control issue to be resolved.

The important state is simple: the verification mechanism exists and has survived one substantive
review, but it is still a synthetic scaffold and still one owner approval short of closure.

-- Codex
