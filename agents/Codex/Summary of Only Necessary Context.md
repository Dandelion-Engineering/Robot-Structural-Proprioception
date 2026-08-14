# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 130 on 2026-08-13.

## Resume here

- Branch: `main`.
- Slot-8 Step 1 (verification-artifact design) is closed / both approved at blob
  `0753d4edc983dff3d2770bdb52ddc59d515fabbe` / raw and canonical SHA-256
  `98e20ae1f37db3dcb034c0d21f2e1fa16667331702fa95725a0b7c739b060fc9`.
- Slot-8 Step 2 (scene/bundle, synthetic fixture, shared renderer, fail-closed role stub and
  V1–V19 tests) is closed / both approved at exact blobs `c12745ab`, `0ae5b19d`, `cf61e5aa` and
  `1833a472`.
- Slot-8 Step 3 (tracked synthetic figure set, packet runbook Step 32 and narrow digest-EOL rule)
  is now **CLOSED / BOTH APPROVED** at the exact state listed below.
- Step 4 and every real-result lane remain separately blocked. No connection-record design,
  real-role adapter/read, scientific role, config, checkpoint, capacity, threshold, final
  configuration, fit, rollout, analyzer invocation or C1-versus-S result is authorized.

## Exact jointly approved Step-3 state

### Ten tracked synthetic fixture files

```text
Reproducibility Packet/results/verification_fixture/
  verification_bundle.json          blob bdd40173be42de7f6b092ab97f3fface55e51fb3
                                      SHA-256 3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70
                                      340,741 bytes
  verification_bundle.sha256        blob 50402682e5a12745f53e3f0f0c7cc6b1854e06b6
                                      SHA-256 1b0dbce047cd32ff22b1b7db6695010729a077da6c46dd921e5620e95b21270e
                                      65 bytes / one LF
  soften_link_2.json                 blob 65e99e41dfda606eb187b0b5a271497a33b33fbf
  soften_link_2.png                  blob 436ff1793d33e72bee3892ef360e06f92f3cbfb7
  weaken_actuator_1.json             blob ac331d739ed880dfe0a947fee1735eaeccdc10ff
  weaken_actuator_1.png              blob 6b49e39a1d7f0d0e8d6d00f22b15cb3826587125
  bias_encoder_1.json                blob 5815bb2fae459dc9f70eb162c1daa4914a1e6636
  bias_encoder_1.png                 blob 607447ac029fb0bc437684e968cc4062ba470f56
  indistinguishable_softening.json   blob 84b87394a4ce9d737d2e3b109bf71347218c178d
  indistinguishable_softening.png    blob e36829c4af17074ff0162dcc02d96a390e773ff6
```

Every JSON is strict and canonical. Every standalone scene equals the corresponding bundled
scene. The four PNGs are 3,600 × 2,550 at `pHYs = (11811, 11811, 1)`, have the synthetic
provenance and no-result boundary drawn into the image, and are deterministic under the pinned
environment at fixture seed 7.

### Supporting exact states

- `Reproducibility Packet/README.md` — blob `4bc07f184ae826f53000238824f46347054b517a`
- `Reproducibility Packet/.gitattributes` — blob `70ec4e7b85ac6984c5c09003562fe9f7b09c2287`
- `Reproducibility Packet/.gitignore` — blob `ad29de35848ea786c9b6a790072860662d2ee5dd`
- root `.gitattributes` — blob `5a7720bc9bbeb74083c32548c71785676894a6ef`
- public root `README.md` — blob `3ab96e38bcf17dfb32c7342e26a07d9e0f889b83`

The narrow `results/verification_fixture/*.sha256 text eol=lf` rule is jointly accepted. It
protects a one-line reader-compared digest whose fresh Windows checkout otherwise changes from 65
to 66 bytes. Do not generalize this rule to the already approved Python source files or to JSONs
and PNGs that do not move.

## What independently closed Step 3

Codex Session 130 re-ran Step 32 exactly under `MPLBACKEND=Agg` into the ignored reproduction
directory. The generated directory contained exactly ten files and every file was byte-identical
to the tracked reference set.

Independent checks also established:

- strict/canonical JSON and exact bundle-to-scene equality;
- bundle SHA-256 `3bf51e94...5459d70` unchanged from the reviewed Step-2 fixture;
- live `j_5s` values of 0.324/0.111, 0.139/0.366 and two exact ties;
- the confidently wrong call, two abstaining arms, high-unknown case, decision change and
  indistinguishable pair all reproduce from the scene records;
- all four figures carry the visible synthetic/no-result boundary and 300-DPI encoding;
- fresh `git checkout-index` copies of the digest, bundle JSON and sampled PNG equal the working
  bytes exactly;
- the `roles` subcommand returns `X_CONNECTION_UNAUTHORIZED`, exit 3, and creates no directory
  before opening any scientific input;
- 159 focused tests pass normally, 159 pass under `python -O` with the expected warning, and the
  standard packet suite passes **2,267 / 2,267**.

Claude explicitly approved the complete Step-3 state in Session 130. Codex explicitly approved
the same exact state unchanged in its Session-130 physical-tail turn. Step 3 is closed.

## Public Live-Run README

Claude's 2026-08-13 public entry correctly records the reviewed working surface, synthetic-only
fixture, absent scientific inputs and still-open Step-3 review at the historical moment it was
written. Codex approves exact root README blob `3ab96e38...` unchanged.

The entry is 495 words / 12 sentences, longer than the Live-Run playbook's lean one-or-two-sentence
target. It is a committed append-only public record with no factual defect, so do not rewrite it
or append a correction merely about length. Return future heartbeats to the lean form.

No new public entry was added in Codex Session 130; the existing entry already owns the milestone.

## Frozen sequencing and boundaries

1. Step 1 design: closed / both approved.
2. Step 2 implementation/tests: closed / both approved.
3. Step 3 fixture figure set and packet runbook step: closed / both approved.
4. Connecting a real result: separately blocked. It requires its own connection-record design,
   exact-state review and joint authorization; none exists.

The tracked synthetic fixture reads no config, checkpoint, scientific role index, role payload,
manifest or split. It licenses no C1-versus-S scientific statement.

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

## Smart App Control and suite-count correction

Smart App Control remains on in enforcement mode by the director's decision. Before treating a
future native import failure as project code, run:

`powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"`

If a new native block occurs, append a new numbered `director_requests.md` entry with the
diagnostic output. Do not propose turning SAC off; Randy has decided it stays on for now.

The clean standard packet suite is **2,267 passed, 0 failed, 0 collection errors**. The degraded
Session-128/129 counts are environment artifacts and must not propagate as suite measurements.

## Transcript state

The authoritative active thread is
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`.

After Codex Session 130's review append it is:

- 2,230,893 bytes;
- 36,266 LF / 19,709 CR;
- SHA-256 `5d374e3a449e5e745723743d3b6c359a354e153baba641baa1c18670bf6b584c`.

Claude's 2,226,528-byte pre-review state remains the exact prefix at SHA-256
`aca93693d7e5eb6129a1b6263b07115a7d4f1270bf37b24dd05c201aa6d35c25`. The Codex Session-130
header occurs exactly once after that boundary, Codex is physically last, and Git shows a single
tail hunk at `+73/-0`. No append-order recurrence occurred.

Transcript Order Monitoring still ends with Claude's independent confirmation of the Session-129
recurrence. Codex added no monitoring note in Session 130 because the append was clean.

For every future active-chat append: authenticate the full current bytes, record the physical
boundary, programmatically verify the complete EOF block is unique, use that exact complete block
as the patch context, then assert the prior bytes remain the exact prefix, the header occurs once
after the boundary, the new author is physically last, and Git is additions-only. If any assertion
fails, preserve the misplaced copy, append a dated physical-tail correction, and disclose it in
Transcript Order Monitoring.

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
- Slot-8 Step 3: closed / both approved.
- Slot-8 Step 4: blocked.

## Next Codex session

Expected Codex Session 131:

1. Authenticate the newest Phase-2 transcript state against the Session-130 hash above.
2. Read Claude's acknowledgement of the exact Step-3 closure and any separate authorized handoff.
3. Do not infer Step-4 authorization from Step-3 closure, an acknowledgement, silence or downstream
   use. Step 4 remains blocked unless a distinct connection-record design/review/authorization
   state appears in the live transcript.
4. Preserve the development/pilot/validation/confirmatory/test/final boundaries and the 2,267
   clean suite-count correction.
5. Keep future public heartbeats lean; do not rewrite the committed 2026-08-13 entry.

## Workflow rules

- Follow `AgentPrompt.md` and obey `.agent-turn` / `.agent-session.lock` before reading project
  state.
- Read all Codex-including active chats and summaries before acting; live transcript and repository
  bytes outrank continuity prose.
- Require explicit same-state approval. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Keep development, pilot, validation, confirmatory, test and final claims separate.
- Before closeout, check the public README obligation, update `.gitignore` if needed, review the
  exact diff, stage only intentional paths, run diff hygiene, commit/push, then delete
  `.agent-session.lock` and only afterward change `.agent-turn` to `Claude`.
