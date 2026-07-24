# Human Report — Claude Session 27

**Date/Time:** 2026-07-23 18:38 PDT
**Phase:** Phase 2 — Execution (config `UNFROZEN`; Schema v1.0 + Amendment A1 in force)
**Session role:** Genuine first review of Codex's Config-Freeze Readiness Review (loop closed at same-state approval), plus one unblocked Gate-4 precondition — verifying the CUDA PyTorch toolchain on the project GPU.

---

## Executive summary

Two things happened this session, one required and one forward-looking.

1. **I closed the open review loop Codex left me.** After my Session 26, Codex ran its Session 26 and produced a new owned artifact — `agents/Codex/Config Freeze Readiness Review.md` — with the owner decision `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`, a seven-gate inventory of what must exist before `config.json` can be frozen, and a "DRAFT-vs-FROZEN" sequencing correction. It handed that to me for genuine first review. I reviewed it against the Claim Sheet and the live repository — independently reproducing its ten-item repository audit, checking its seven gates against the contract's pre-confirmatory-freeze requirements, and evaluating the sequencing argument — found it accurate and its BLOCK decision correct, and **approved the exact state, closing the loop.** I contributed my position on the one shared decision it correctly leaves open (Gate 6, the confirmatory controller protocol) and two non-blocking forward notes.

2. **I verified the learned-model toolchain on the GPU.** The single biggest unknown in my lane was whether a free, stable PyTorch build actually runs on this machine's RTX 5060 Ti, which is a Blackwell (sm_120) card — very new silicon that older CUDA wheels don't target. I installed `torch==2.11.0+cu128` and confirmed with a real GPU computation (not just the availability flag) that it works: capability sm_120, kernels execute, autograd runs, and the GPU result matches a CPU recomputation exactly. Pinned it. Gate 4's biggest risk is now a verified non-issue.

Nothing was frozen; every trace remains `dev-*`; the Claim Sheet is unchanged.

## Where the project stands (for context)

The development-screening arc of Phase 2 has reached its natural end. Over the last several sessions the team characterized the diagnosis side (the structural-sensing suite S strongly out-attributes the conventional suite C1 — 0.995 vs 0.704 four-way macro-F1) and closed every channel through which that attribution advantage could have translated into a *control* advantage on this bounded joint-space task: detection, classification, severity accuracy, confidence, and — via Codex's Session-25 actuator recovery-action screen that I reviewed last session — the actuator action family (positive but below the source-specific safety bar). The evidence keeps landing on the pre-registered "improves diagnosis, not control" shape (one of the outcomes we wrote down in advance).

The open question therefore shifted from "screen more variants" to "are we ready to freeze the confirmatory configuration and run the pre-registered confirmatory experiment?" Codex's readiness review answers: **not yet** — and lays out exactly what's missing. This session ratifies that answer and de-risks one piece of it.

## What I did, in detail

### 1. Context and cross-review (workflow steps 1–3)

I re-read `AgentPrompt.md` and `Project Details/Project Details.md` in full, my own continuity summary, and every chat summary/active transcript that includes me. The important discovery from the live git state: **HEAD was `Codex Session 26`, committed *after* my Session 26** — so Codex had done a full session I had not yet seen. This is exactly the cross-review case the working method describes (read the most recent unreviewed collaborator report + the work it points to). Codex's `HumanReport26.md` pointed to the readiness review and two append-only turns in the Phase-2 chat (closing the actuator-action loop, then handing me the readiness review).

### 2. Genuine review of the Config-Freeze Readiness Review

The readiness review is a reasoning/planning artifact, not a numbers artifact, so "genuine review" meant verifying its factual claims against the repository and testing its logic against the Claim Sheet — not recomputing a table. Specifically:

- **I independently reproduced its repository-presence audit. All ten "absent" findings are correct.** There is no machine-readable `schema/schema.json` (only the prose `schema-v1.0.md`); no `config.json` anywhere in the packet; no identity manifest; the learned models `TemporalAttributionNet` and `RMALatentEncoder` exist only as specification comments in `scripts/utils/estimator.py` (lines 44 and 51), with no class bodies; there is no deployable-loader class, no split/leakage-audit function, no confirmatory CLI, and no evaluation-driver CLI; and no Slot-8 verification artifact exists yet. I also confirmed the toolchain half independently — **zero `torch` imports** across the packet and no `torch` in the environment — so the learned rungs are genuinely unbuilt, not merely disconnected.
- **I checked the seven gates against the Claim Sheet's requirements for what must be frozen before confirmatory data are generated.** They are a faithful and complete decomposition (machine schema/config authority; role-separated storage + leakage/split audits; the multi-setting + compound-OOD design; the matched temporal/RMA models + capacity ladder + ≥5 seeds; calibration/abstention/OOD/uncertainty authorization; the confirmatory controller protocol; and the evaluation driver + immutable test manifest). I did not find a missing gate.
- **I evaluated the DRAFT-vs-FROZEN sequencing correction and found it both sound and important.** The old shorthand — carried in *both* agents' continuity, including mine — was "learned heads are post-config-freeze." Read literally against the Claim Sheet's requirement to freeze model/hyperparameters/thresholds *before* confirmatory generation, that's circular: you can't freeze a model you haven't built and selected. Codex's fix resolves it cleanly: the learned heads are implemented and selected on development/validation roles under a versioned *draft* config; the final immutable `config.json` is written after that selection and before any untouched `test` payload exists. I'm correcting my own continuity to match.

**Decision: I approved the exact handed-off state.** I found no error to fix, so under the review-cycle playbook the correct close is an explicit same-state approval. To keep that from being a rubber stamp, my approval turn records the independent verification above, and it is explicit that the approval covers the audit, gate inventory, and sequencing — and does *not* pre-decide Gate 6, which the review correctly leaves open as a shared decision.

### 3. My input to the one shared decision (Gate 6)

Both recovery-action families (structural and actuator) are blocked on this task, but the Claim Sheet still requires a fair, pre-declared controller comparison. I named the governance distinction between the two honest paths, because they are not equivalent in process:

- **The in-contract default (no amendment):** build a fair protocol — no-action baseline, transparent attribution-driven recovery at reviewed floors, an RMA baseline, and an oracle ceiling — and actually *run* the pre-registered paired conventional-vs-structural control comparison. On this joint-space task it will very likely return no control gain (the structural fault produces no *joint* deficit — the damage moves to the end-effector, which the joint score never charges for), which is the pre-registered "diagnostic-only" landing already written into the contract. Running it and landing there needs no amendment and yields the clean, valuable negative.
- **Narrowing the confirmatory scope to information/detection-only** (not running a genuine control arm) changes what the experiment tests against the two-layer success bar, so *that* branch is a Claim-Sheet amendment — which means director sign-off and a progress report.

I recommended the default: pre-registration is exactly the tool for "we expect this to fail," so we should run the comparison rather than decline to. I flagged this as the one place I'd like us to converge explicitly before the manifest work hardens around it.

### 4. Two non-blocking forward notes

1. **One recorded joint approval on the draft manifest before any headline model is fit.** The freeze-ready checklist requires both agents to approve the *final* config, but the multi-setting grids and the trajectory/fault-setting → role assignment determine the validation data model selection runs on. That assignment should carry one explicit joint approval — lighter than the final freeze, but real — so a split decided unilaterally can't silently shape model selection.
2. **Gate 4's fallback, for the record** (now moot — see below): had no free CUDA build carried sm_120 kernels, the fallback was a cu-tagged nightly build or CPU training (the models are small enough for CPU to be slow-but-sufficient at ≥5 seeds).

### 5. Verifying the CUDA PyTorch toolchain on the RTX 5060 Ti (Gate-4 precondition)

This was the session's forward contribution. Verifying the GPU toolchain needs no config, manifest, or data, so it doesn't jump ahead of Codex's persistence-foundation work in the queue — it just converts an open risk into a known fact, and it is squarely in my lane (I own the learned rungs).

- Installed `torch==2.11.0+cu128` (CUDA runtime 12.8) into the project `venv` from the official CUDA-12.8 wheel index.
- Ran a real verification (`scratchpad/verify_torch_sm120.py`): `cuda.is_available()=True`; device capability **sm_120 (12, 0)**; the wheel's architecture list includes `sm_120`; a real GPU `matmul → relu → sum → backward` executes and finite-checks; and the GPU result matches a CPU recomputation at **0.000e+00** relative difference. (The last checks matter because the availability flag can read True while kernels fail to launch on an unsupported architecture — so I ran actual kernels, not just the flag.)
- Pinned `torch==2.11.0+cu128` in the root `requirements.txt`, behind an `--extra-index-url` line pointing at the cu128 wheel index so the pin stays installable by a future reader (per the pin-the-moment-you-install standard).
- Confirmed the install did not disturb the environment: numpy/scipy/scikit-learn/mujoco/pandas/control/matplotlib are all still at their pinned versions, and the shared `test_recovery_seam.py` remains green.

## Challenges and how they were handled

- **A stale-continuity trap, avoided by checking git first.** My own continuity summary was written at the end of *my* Session 26 and predated Codex's Session 26. Had I trusted it, I'd have missed an entire unreviewed session and the open loop waiting for me. Reading the live git log at the start (rather than assuming the startup snapshot was current) surfaced `Codex Session 26` as HEAD and set the whole session's agenda correctly. Standing lesson reinforced: verify the live repository state before trusting any continuity document.
- **Reviewing a reasoning artifact without a table to recompute.** Unlike last session's actuator screen (where I re-ran the physics and diffed byte-for-byte), the readiness review has no numbers to reproduce. The genuine-review move here was different: reproduce its *factual* claims (the repository audit) and test its *logic* against the contract (the seven gates, the sequencing argument). That's what makes a same-state approval of a planning document honest rather than deferential.
- **The bleeding-edge-GPU risk.** sm_120 (Blackwell) is new enough that "PyTorch supports CUDA" doesn't imply "PyTorch runs on this card." I treated the install as a hypothesis to test, not a given, and verified with a real kernel launch. It passed, which removes the single largest uncertainty from the learned-model work.

## Decisions I made

- Approved Codex's readiness review at its exact committed state (loop closed); recorded independent verification so the approval is earned.
- Took the position that Gate 6 should default to *running* the pre-registered control comparison (in-contract, no amendment), reserving the scope-narrowing branch — which would need an amendment — for the case where a fair control arm genuinely can't be run.
- Did the PyTorch/sm_120 verification now, as the one unblocked and sequence-independent piece of Gate 4, rather than deferring it until the rest of the model work is queued.
- Left the public Live-Run README untouched this session (heartbeat check below).

## Live-Run README heartbeat check

Checked. My session ratified an internal readiness plan (a BLOCK — no freeze) and verified the model toolchain; neither is a finished public artifact, a phase close, or a research result. Codex — the author of the readiness review — made the same judgment for its Session 26 and did not log it publicly. The running log is lean by design, so for consistency I left the banner (Phase 2 / In Progress, 2026-07-23) and running log unchanged. The natural next public-log entry is the actual config freeze or the first confirmatory result. (Low-priority thought carried to continuity: the pivot from development-screening to confirmatory-pipeline build might merit one lean public entry once the first foundation component actually lands — worth raising with Codex then, not unilaterally now.)

## Files created

- `agents/Claude/Session Summaries/HumanReport27.md` (this report)

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my same-state approval + Gate-6 position + forward notes + toolchain result (`+36 / −0`, pure tail append, verified at the git level).
- `requirements.txt` — pinned `torch==2.11.0+cu128` behind the cu128 `--extra-index-url`.
- `agents/Claude/README.md` — refreshed current-state references to Session 27.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 28.

## Files deliberately not changed

- `agents/Codex/Config Freeze Readiness Review.md` — I approved it same-state; no edits, so Codex's owned artifact is untouched.
- `config.json` — remains absent by design; the freeze is blocked.
- Root `README.md` (Live-Run) — heartbeat checked, intentionally unchanged (see above).
- `agents/Claude/references.md` — no external sources were read this session (review + toolchain work), so no new entries, consistent with recent construction/review sessions.
- `.gitignore` — already covers `venv/` (where the 2.7 GB torch install lives) and model files (`*.pt`, `*.pth`, `*.ckpt`, `*.onnx`); no change needed.

## Monitoring duty (standing)

Clean check — no recurrence. Codex's Session-26 append to the Phase-2 transcript was a pure `+32 / −0` tail addition with Codex physically last (verified at the git level via `git show --numstat`). That's the fifth consecutive clean append since the sharpened anchor rule; per the duty (flag recurrences, keep the director thread lean) I added no note to `Transcript Order Monitoring`. My own append this session used the binary-EOF-append script with hard gates and verified `+36 / −0` afterward.

## Next steps (for Session 28)

1. **Read Codex's latest first** (its next `HumanReport` + Phase-2 chat tail). Codex's stated next increment is Gate 1 + the Codex/shared portion of Gate 2 — the machine `schema.json`, a draft/frozen config contract with canonical hashing, and the role-manifest/loader/audit foundation. If it has landed that, review it.
2. **Converge with Codex on Gate 6** (run the pre-registered control comparison vs. narrow-scope-plus-amendment) before the manifest hardens.
3. **My lane, once the persistence foundation + Gate-3 draft manifest exist:** build the matched `TemporalAttributionNet` + `RMALatentEncoder` behind the shared `[W,D]` interface (the toolchain is now verified ready), then per-suite calibration/abstention/OOD/uncertainty selected on validation only.
4. **Do not freeze a partial config**, and do not build model/data ahead of the jointly-approved draft manifest (pre-registration integrity).
