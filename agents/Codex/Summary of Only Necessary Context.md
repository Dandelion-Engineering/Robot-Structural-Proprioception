# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 128 on 2026-08-13.

## Resume here

- Branch: `main`.
- The first Slot-8 verification-artifact design is closed and jointly approved at Git blob `0753d4edc983dff3d2770bdb52ddc59d515fabbe` / raw and canonical SHA-256 `98e20ae1f37db3dcb034c0d21f2e1fa16667331702fa95725a0b7c739b060fc9`.
- Claude Session 128 built the bounded Step-2 scene/bundle, synthetic fixture, shared renderer, interactive surface, fail-closed real-role stub and V1–V19 tests.
- Codex Session 128 reviewed that exact build, accepted Claude's three flagged design decisions, repaired four additional contract gaps (CP–CS), and explicitly approved the exact reviewer state. Claude's explicit same-state owner re-review is still missing, so Step 2 is not closed and Step 3 is not authorized.
- The public root `README.md` remains unchanged at the jointly approved interpreted rung-2 heartbeat blob `f00ea0d9...`. The internal Slot-8 working-surface review does not yet warrant another public entry.
- The local Windows environment still cannot import MuJoCo because an Application Control policy blocks `_functions`; the focused Slot-8 suite and all non-MuJoCo packet tests are reproducible here.

## Exact Slot-8 Step-2 reviewer state

Codex approves these exact four files:

1. `Reproducibility Packet/scripts/utils/verification_scene.py`
   - Git blob / no-filter hash: `c12745abc1fff3f09a6077543cf9dc5cfcc49b3a`
   - raw/canonical SHA-256: `d811e0875b7dabeef053ca01ff908f66e3fc3f3472727e4d385478a228251597`
   - 63,651 bytes, 1,639 LF, zero CR, final LF present.
2. `Reproducibility Packet/scripts/render_verification_scene.py`
   - Git blob / no-filter hash: `0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5`
   - raw/canonical SHA-256: `fd8644d5dbd864ba335ae8e5585d9f65ae2a4f7f256aa997b6780ee29889ce0d`
   - 30,100 bytes, 785 LF, zero CR, final LF present.
3. `Reproducibility Packet/tests/test_verification_scene.py`
   - Git blob / no-filter hash: `cf61e5aad09bc5dceab15519e7888fb97fe70b27`
   - raw/canonical SHA-256: `b4747571120c6415f9344dd1da5c425932fadc1ca2ca14112236bcd9587a529f`
   - 43,252 bytes, 1,111 LF, zero CR, final LF present.
4. `Reproducibility Packet/tests/test_render_verification_scene.py`
   - Git blob / no-filter hash: `ba7d135afe62789af06ca114c1f4e904fd09d894`
   - raw/canonical SHA-256: `08fdeeb64c1d755c077244841f0799e6e5c8099de346baa77c6b8f3b76e4d835`
   - 33,822 bytes, 859 LF, zero CR, final LF present.

Do not treat downstream use, silence, or a later edit as approval. Claude must explicitly approve these same four states, or return a new exact state for review.

## CP–CS reviewer repairs

- **CP — visible case identity:** the interactive radio menu now displays the required human-readable `body_change.label`, maps labels back to case IDs, and rejects duplicate visible labels with `X_BUNDLE_INCOMPLETE`.
- **CQ — surface completeness:** both `render_bundle(...)` and `InteractiveVerificationSurface(...)` now call the shared bundle validator before writing or displaying, so an incomplete bundle cannot bypass the builder's fail-closed path.
- **CR — shared playback clock:** animation advances through `slider.set_val(...)`, keeping the visible slider, shared frame and repainted panels synchronized.
- **CS — project-relative output contract:** both CLI surfaces reject absolute, drive-qualified, rooted and parent-traversing output paths under both POSIX and Windows path grammars.

The accepted Claude-flagged rulings remain:

- Leave the synthetic geometry helper as implemented; any future real-role adapter design must assign each deformation code truthfully rather than inheriting a misleading synthetic mapping.
- A malformed `EstimatorOutput` remains `X_DECISION_UNSUPPORTED`, not `X_ROLE_UNAVAILABLE`.
- Fixture mode writes the static artifact and then opens the required interactive menu; no extra interactive flag is added.

## Verification reproduced in Session 128

- Focused Slot-8 tests: `158 passed` under normal Python.
- Focused Slot-8 tests: `158 passed` under `python -O` (one expected pytest assertion-rewrite warning).
- Full packet fallback: `1 failed, 1343 passed, 28 errors`; all 29 non-passes terminate at the same blocked MuJoCo import, including the one body-test failure.
- `py_compile` passed for both production modules and both test modules.
- `git diff --check` passed before closeout.
- Independent interaction probes passed, including visible label selection and slider synchronization.
- The scripted 300-DPI PNG and interactive wrapper were visually inspected and readable. Scratch images remain outside the repository under the automation visualization workspace.
- No real-role connection, later-role read, scientific fit, rollout, fixture figure set, or runbook execution occurred.

## Frozen Slot-8 design and sequencing

The jointly approved design still controls all implementation decisions. It permits only:

- the shared typed scene/bundle model and validation,
- deterministic synthetic fixture construction,
- one shared painter used by static and interactive surfaces,
- the fail-closed real-role loader stub,
- V1–V19 contract tests.

Sequence:

1. Step 1 design: closed at both approvals on `0753d4ed...`.
2. Step 2 implementation/tests: Codex reviewer state approved by Codex; Claude owner re-review open.
3. Any real-role adapter or connection: separate design/review/authorization only after Step 2 closes.
4. Fixture figure set, runbook integration and later gate work: separately blocked.

## Closed prior state that still controls

- Stage 1 is complete as scoped. The paired curve has no readable shape at five points and five seeds; no trend statement, capacity choice or threshold selection is licensed.
- Literal Slot-9 rung 2 is complete as scoped. The one fit invocation and one analyzer invocation are spent. Both agents approve analysis blob `a2fa857b...` / raw SHA-256 `604d7272...`, and frozen section 5.4 is jointly applied at the exact `OPTIMIZATION_CHECK_PASSED` + `MIXED` sentence pair.
- All ten rung-2 arms have zero healthy and structure F1. That persisted-value observation must accompany the weak objective/sign description without causal attribution.
- The packet-runbook review is closed at README blob `f5e677c8...`; the public interpreted heartbeat is closed at root README blob `f00ea0d9...`.
- The Stage-1 precision note is closed and licenses no additional work.
- Checkpoint `67` remains a bounded development artifact. No confirmatory, validation, generalization, threshold, final-configuration or engineering-usability claim follows.

## Transcript state and append rule

The authoritative active thread is `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

After the Session-128 Codex append it is:

- 2,199,774 bytes,
- 35,754 LF,
- 19,709 CR,
- SHA-256 `98ab2f375a7295d026e815538086e2118bab12af2a396a7c3c26e4054486355d`.

The newest turn is Codex's `Session 128 Step-2 review`, which records CP–CS, the exact four approved reviewer blobs and the owner re-review ask.

All active chats are append-only. Before appending, read the physical UTF-8 byte tail and record byte/line state. Construct the new file as the exact previously authenticated byte prefix plus one LF-only payload. Then assert prefix equality, unique header after the pre-write boundary, physical-last authorship and the new whole-file hash. If any assertion fails, append a dated repair and disclose it in Transcript Order Monitoring.

## Current gate map

- Claim Sheet and accessible companion: jointly approved.
- Schema v1.0 + A1 and Amendment A2: in force.
- Gate 1: closed.
- Gate 2: generic/base-role paths approved.
- Gate 3: closed.
- Gate 4: blocked; estimator/controller real-role connection is not authorized.
- Gates 5–7: blocked.
- Final `config.json`: does not exist.
- Capacity/threshold selection: not authorized.
- Slot-8 Step 1: closed.
- Slot-8 Step 2: exact reviewer state awaiting Claude approval.
- Slot-8 Step 3 and later: blocked.

## Next session

Expected Codex Session 129:

1. Authenticate the newest Phase-2 transcript suffix against the Session-128 post-state above.
2. Read Claude's response to the exact four-file handback.
3. If Claude explicitly approves all four unchanged reviewer blobs, acknowledge and close Step 2. If Claude edits any file, review and verify the new exact state before approval.
4. Do not authorize or implement Step 3 merely because Step 2 closes. First agree the next bounded design/review lane and preserve every separate authority gate.
5. Keep the public root README unchanged unless a separately reviewed director-facing update is justified.

## Workflow rules

- Follow `AgentPrompt.md` on every project turn and obey `.agent-turn` / `.agent-session.lock` before reading project state.
- Read all Codex-including active chats and summaries before acting; use the live transcript and repository state over stale handoff prose.
- Preserve Claude ownership of the Slot-8 implementation while Codex is reviewer unless the transcript explicitly reassigns ownership.
- Require explicit same-state approval. Reviewer edits, downstream use and silence are not approval.
- Never spend a fit, analyzer, rollout, real-role read or execution authority unless the exact required halves and prerequisites are present.
- Keep development, pilot, extraction, validation, confirmatory and final claims separate.
- Use explicit path-scoped commits, verify the remote push, then release the session lock and pass `.agent-turn` to Claude in that order.
