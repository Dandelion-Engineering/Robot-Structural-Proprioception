# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 129 on 2026-08-13.

## Resume here

- Branch: `main`.
- Slot-8 verification-artifact Step 1 (design) is closed / both approved at blob
  `0753d4edc983dff3d2770bdb52ddc59d515fabbe` / raw and canonical SHA-256
  `98e20ae1f37db3dcb034c0d21f2e1fa16667331702fa95725a0b7c739b060fc9`.
- Slot-8 Step 2 (scene/bundle, synthetic fixture, shared renderer, fail-closed role stub and V1–V19
  tests) is now **CLOSED / BOTH APPROVED** at the exact four-file state below.
- Only Claude's bounded Step 3 is authorized: generate the synthetic fixture figure set into the
  Reproducibility Packet through the approved scripted path, add the corresponding runbook step,
  and return the exact state for review.
- Claude also owns the lean root Live-Run README heartbeat for the newly reviewed Slot-8 working
  surface. Codex left the root README unchanged in Session 129.
- Step 4 and every real-result lane remain separately blocked: no connection record, real-role
  adapter/read, scientific role, capacity, threshold, final configuration, fit, rollout or
  analyzer work is authorized.

## Exact jointly approved Step-2 state

Both Claude and Codex explicitly approve these exact four files:

1. `Reproducibility Packet/scripts/utils/verification_scene.py`
   - Git blob / no-filter hash: `c12745abc1fff3f09a6077543cf9dc5cfcc49b3a`
   - raw/canonical SHA-256: `d811e0875b7dabeef053ca01ff908f66e3fc3f3472727e4d385478a228251597`
   - 63,651 bytes / 1,639 LF / 0 CR.
2. `Reproducibility Packet/scripts/render_verification_scene.py`
   - Git blob / no-filter hash: `0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5`
   - raw/canonical SHA-256: `fd8644d5dbd864ba335ae8e5585d9f65ae2a4f7f256aa997b6780ee29889ce0d`
   - 30,100 bytes / 785 LF / 0 CR.
3. `Reproducibility Packet/tests/test_verification_scene.py`
   - Git blob / no-filter hash: `cf61e5aad09bc5dceab15519e7888fb97fe70b27`
   - raw/canonical SHA-256: `b4747571120c6415f9344dd1da5c425932fadc1ca2ca14112236bcd9587a529f`
   - 43,252 bytes / 1,111 LF / 0 CR.
4. `Reproducibility Packet/tests/test_render_verification_scene.py`
   - Git blob / no-filter hash: `1833a4724ed2a20429d202109165c4ba4ca21624`
   - raw/canonical SHA-256: `634214fb018c9550e5e7a00c22bd9d0a1f5d6374985d7f0d0c4a66fde2becbed`
   - 34,780 bytes / 878 LF / 0 CR.

All four are pure ASCII, no BOM, final LF, and filtered equal to `--no-filters`. No
`.gitattributes` rule pins `*.py`, so Git blob identities are the durable review identities and
raw SHA-256 values are working-tree measurements.

## What closed the final review round

Codex Session 128 repaired four contract gaps:

- CP: visible radio entries now use human-readable body-change labels, with duplicate labels
  refused before the mapping is built.
- CQ: both scripted and interactive surfaces validate the complete bundle before writing or
  displaying it.
- CR: animation advances through the slider observer, so the visible timeline and painted frame
  remain synchronized.
- CS: both CLI modes enforce project-relative output paths under Windows and POSIX grammars.

Claude Session 129 accepted all four repairs, then changed only the render-test file to add two
load-bearing checks:

- the public `select_label` callback's unknown-label refusal is pinned;
- every visible radio entry is driven, so asymmetric label-to-case swaps cannot survive.

Codex Session 129 re-opened the callback/mapping implementation, reviewed the exact diff, reproduced
the tests and approved `1833a472` unchanged. Both approvals now name the same four-file state.

## Verification and Smart App Control correction

The director authorized a separate Repair Agent to diagnose the MuJoCo import block. Its append in
`director_requests.md` establishes:

- Smart App Control remains on in enforcement mode by the director's decision.
- The transient block affected unsigned MuJoCo `_functions.cp312-win_amd64.pyd` and cleared without
  intervention after 397 Code Integrity events from 14:33 through 16:23 PDT.
- Before treating any future native import failure as code, run:

  `powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"`

- If a new native block occurs, append a new numbered `director_requests.md` entry with the
  diagnostic output. Do not absorb it quietly and do not propose turning SAC off; Randy has decided
  it stays on for now and will reassess after the next incident.
- A test count measured during a block is discarded as a suite measurement and re-run after the
  diagnostic reports healthy.

Codex Session 129 ran that diagnostic. It reported all eight native packages healthy and MuJoCo able
to build and step. Exact verification then passed:

- focused Slot-8 normal: 159 passed in 29.10 s;
- focused Slot-8 under `python -O`: 159 passed in 29.26 s, one expected warning;
- standard packet-wide suite: **2,267 passed in 163.71 s, 0 failed, 0 collection errors**.

The degraded 1,328/1,343/1,344 counts in the dated Session-128/129 records are honest measurements
of a blocked environment and are not suite counts. Do not propagate them into continuity, the
Technical Report or public artifacts. State the clean 2,267 count when a count is needed and cite
the `director_requests.md` correction.

## Frozen sequencing and boundaries

The jointly approved Slot-8 design still controls:

1. Step 1 design: closed / both approved.
2. Step 2 implementation/tests: closed / both approved at the four blobs above.
3. Step 3 fixture figure set and packet runbook step: now authorized, Claude-owned, exact-state
   review required before it closes.
4. Connecting a real result: separate connection-record design, exact-state review and joint
   authorization only after Step 3; currently blocked.

Step 3 may only run the scripted synthetic fixture path. It must not read config, checkpoints,
scientific role indices or recorded result payloads, and it does not license any C1-versus-S claim.

## Closed prior state that still controls

- Stage 1 is complete as scoped. Its five-point/five-seed curve has no readable shape; no trend,
  capacity or threshold statement is licensed.
- Literal Slot-9 rung 2 is complete as scoped. The one fit invocation and one analyzer invocation
  are spent. Both agents approve analysis blob `a2fa857b...` / raw SHA-256 `604d7272...`; frozen
  section 5.4 is jointly applied at `OPTIMIZATION_CHECK_PASSED` + `MIXED`.
- All ten rung-2 arms have zero healthy and structure F1. This persisted-value observation must
  accompany the weak objective/sign description without causal attribution.
- Packet runbook Steps 30–31 are closed at README blob `f5e677c8...`; the interpreted public
  rung-2 heartbeat is closed at root README blob `f00ea0d9...`.
- Checkpoint 67 remains a bounded development artifact. No validation, confirmatory,
  generalization, threshold, final-configuration or engineering-usability claim follows.
- Claim Sheet Amendment A2 remains in force and all development/pilot/validation/confirmatory
  boundaries remain intact.

## Transcript state and recurrence record

The authoritative active thread is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

After Session 129 it is:

- 2,217,342 bytes;
- 36,047 LF / 19,709 CR;
- SHA-256 `50af23e951b1afaefe932cef7cb0939edabf968b078dfb654af9319c62c181a5`.

Codex's first 17:31 approval copy was misplaced at line 23,894 because the patch used repeated
`-- Claude` separator context. Assertions caught it before closeout. The misplaced copy is preserved;
the dated physical-tail correction at line 36,003 is operative and restates the exact approval,
Step-3 authorization, environment correction and later blocks. Git shows two disclosed
addition-only hunks, `+118/-0`.

Transcript Order Monitoring contains the required disclosure as a single `+32/-0` tail hunk. It is
42,714 bytes / 746 LF / 161 CR at SHA-256
`0f73837371e86fcd8a146de4285aa5f3913db61d2af6e3413629d1f05f6bc721`.

For every future active-chat append: authenticate the full current bytes, write only from a
programmatically verified unique complete EOF block, then assert the exact prior bytes remain the
prefix, the header occurs once after the boundary, the new author is physically last, and Git is
additions-only. If any assertion fails, preserve the misplaced copy, append a dated physical-tail
correction, and report it in Transcript Order Monitoring.

## Current gate map

- Claim Sheet and Accessible Claim Sheet: jointly approved; A2 in force.
- Schema v1.0 + A1 and A2 boundaries: in force.
- Gates 1 and 3: closed.
- Gate 2: generic/base-role paths approved.
- Gate 4 and Gates 5–7: blocked.
- Final `config/config.json`: does not exist.
- Capacity/threshold selection: not authorized.
- Slot-8 Step 1: closed / both approved.
- Slot-8 Step 2: closed / both approved.
- Slot-8 Step 3: authorized, Claude-owned, not yet reviewed.
- Slot-8 Step 4: blocked.

## Next Codex session

Expected Codex Session 130:

1. Authenticate the newest Phase-2 transcript state against the Session-129 hash above.
2. Read Claude's Step-2 closure acknowledgement, Live-Run README heartbeat and Step-3 handoff.
3. Review the generated synthetic figure/scene/bundle/digest set and packet runbook edit against
   the frozen design and Reproducibility Packet playbook. Verify determinism, completeness,
   300-DPI `pHYs`, canonical JSON, provenance banners, packet-relative paths and absence of real
   scientific input reads.
4. Require exact-state approval before closing Step 3. If any file changes, hand the new exact state
   back to Claude; do not infer approval from generation or downstream use.
5. Keep Step 4 and every real-role/scientific-result lane blocked.

## Workflow rules

- Follow `AgentPrompt.md` and obey `.agent-turn` / `.agent-session.lock` before reading project
  state.
- Read all Codex-including active chats and summaries before acting; live transcript and repository
  bytes outrank stale continuity prose.
- Preserve Claude ownership of Step 3 and Codex's reviewer lane.
- Require explicit same-state approval. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Keep development, pilot, validation, confirmatory, test and final claims separate.
- Before closeout, check the lean public README obligation, update `.gitignore` if needed, review
  the exact diff, stage only intentional paths, run diff hygiene, commit/push, then delete
  `.agent-session.lock` and only afterward change `.agent-turn` to `Claude`.
