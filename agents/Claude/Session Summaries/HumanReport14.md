# Human Report 14 — Claude

**Current Date and Time:** 2026-07-20 19:14 PDT

**Agent:** Claude · **Session:** 14 · **Project phase:** Phase 2 — Execution

---

## Summary

This was a cross-review-plus-build session. It did two things: (1) it discharged the one open review obligation carried from Codex Session 13 — a genuine first review of Codex's new interpretable **linear residual / system-ID baseline** — and (2) it built the shared **end-to-end recovery-seam regression test** that both agents had agreed (in Session 13) was the next thing worth committing.

Nothing was frozen; no phase closed; no Claim-Sheet amendment was written. The work remains Phase-2 development scaffolding, exactly as the framework expects at this stage — the central C1-vs-S research question is still unanswered and deliberately gated behind the config freeze and the trained attribution head.

**Headline outcomes:**
- Codex's `LinearResidualAttributionEstimator` was reproduced independently (a 22-check standalone script, *not* a re-run of Codex's tests) and **approved at its handed-off state — the first-review loop is closed.** I found no defect that warranted an edit.
- A new shared regression, `tests/test_recovery_seam.py`, was built and handed to Codex for first review. It pins, end-to-end over multiple real-plant steps, the seam property that was previously verified only piecewise. Full Reproducibility Packet went **134 → 138 tests**, all passing.
- Two non-blocking forward points were raised (a per-suite calibration-fairness note for the eval; a benign re-bind observation). A tiny consistency nit I owed from Session 13 was deliberately **carried forward** rather than reopening a freshly-closed artifact.

## What was accomplished (in order)

1. **Completed the full AgentPrompt startup workflow.** Re-read `AgentPrompt.md`, all of `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, and my workspace `README.md`. Ran the chat context-first batch protocol: read every `Summary.md` in the three concluded chats that involve me, then the complete active Phase-2 transcript before replying. Re-read the in-force `Claim Sheet.md` (the contract I review against) and the `Playbooks/review-cycle.md` playbook before doing the review.

2. **Reconciled the live git state against a stale startup snapshot.** The session-start snapshot showed HEAD at "Claude Session 11" with a dirty tree; the live repository was actually at `1260e92 Codex Session 13` with a **clean** working tree. My Session-13 continuity file had warned this snapshot is often stale, so I verified with `git log`/`git status` and worked against the real clean baseline. (This is a recurring, expected quirk, not a problem — the live tree and continuity files are authoritative.)

3. **Discovered Codex's Session-13 turn had landed** since my Session 13: the active chat had grown from 764 to 799 lines. In it, Codex accepted my two Session-13 approvals (both loops confirmed closed) and built a **new artifact in its lane** — the Claim-Sheet-required interpretable residual/linear-system-ID baseline — explicitly approving it and handing it to me for genuine first review. That was the open loop this session had to answer.

4. **Genuinely first-reviewed the linear residual baseline** (`utils/residual_baseline.py` + `tests/test_residual_baseline.py`). I read it against the Claim Sheet (Slot 5's "interpretable floor," the §D leakage boundary, the matched-ablation discipline) and the software/scientific standards, confirmed the base-class and output contracts it builds on, and then **reproduced the load-bearing properties independently** rather than trusting the tests. My 22-check script verified:
   - **The ARX + residual math is exactly what is claimed.** I reconstructed the normalized affine ARX fit (masked mean/scale → the `[1, x[t-1], mask[t-1], u[t], u_mask[t]]` regressor → per-target ridge normal equations with an unpenalized intercept) and the `[signed_mean, rms, valid_fraction]` residual vector from records I built separately; my coefficients and residual vector match the module's to `max|Δ| < 1e-9`. The fit's transition count equals `Σ(n_steps−1)`, proving one-step transitions never bridge record boundaries.
   - **The matched-ablation / leakage boundary is structural.** The conventional suite C1 predicts zero gauge scalars and the structural suite S predicts exactly four; the *only* difference between their predicted-state layouts is those four gauge channels (clean nesting — the whole point of the ablation). `tau_cmd` is treated only as the exogenous input, never a predicted state. A C1 record that unmasks a gauge is rejected; a wrong-suite record is rejected; and the run-identity/label fields are never consumed (I set them to garbage and the residual output was byte-identical).
   - **The re-fit lifecycle is atomic and self-invalidating.** A re-fit replaces the model and nulls the residual centroids and abstention threshold; a re-fit that raises leaves the old model fully intact; scoring refuses a re-fit reference until re-calibrated; and the tail-resolution guard fails loud below `ceil(min_tail/false_abstention_rate)` (100 at the 5% default).
   - **The safety boundary holds end-to-end.** The estimator always emits `location_out=-1`, `severity_uncertainty=inf`, and a valid §D output. Critically — the property Codex's own seam smoke does not exercise (it drives only a healthy rollout) — I fed a *confident* structural output and a *confident* actuator output, each with infinite uncertainty, through the real recovery controller, and both stay exactly nominal. So "this floor cannot trigger active recovery" holds through the shared controller gate's `np.isfinite(severity_uncertainty)` clause, not merely through the missing location.

   Full packet **134 passed** on my machine. I approved both files at Codex's handed-off state; **the first-review loop is closed.**

5. **Built the shared end-to-end recovery-seam regression** (`tests/test_recovery_seam.py`, new). This is the committed test I proposed in Session 13 and Codex green-lit in Session 13. It drives the real `CablePlant → OnlineSensorSession → EstimatorCommandPolicy → GainScheduledRecoveryController` loop over multiple steps through `run_online_rollout` and asserts four things:
   - a **localizing** actuator attribution stand-in sustains active inverse-gain compensation, restoring the delivered torque at the attributed joint to nominal across the whole rollout, with no saturation;
   - a **detection-only / unlocalized** stand-in on the same fault stays exactly nominal and leaves delivery degraded — isolating the controller's finite-uncertainty gate as the seam's attribution boundary;
   - the two arms **diverge** (attribution restores delivery; detection alone does not) — the "does attribution improve control" property in mechanism form;
   - a **structural** stand-in applies the sustained global command derate over the whole rollout.

   The stand-ins are fixed deployable outputs (not a trained head) and every assertion is on applied/delivered torque, so — per the agreement with Codex — it is explicitly labeled an **interface/mechanism** regression, *not* a tracking-recovery (`J_5s`) or safety result, which the frozen evaluation driver will own later. This pins the one seam property previously verified only piecewise (a single plant step, a single policy call), so that when the learned head, the RMA latent, and the oracle eventually drive this same socket, its control semantics are already fixed. Packet **134 → 138 tests**, all green; `compileall` clean.

6. **Posted the Session-14 review-cycle reply** in the active Phase-2 chat: the same-state approval of the residual baseline with my reproduction evidence, the hand-off of the new seam regression for Codex's first review, the two forward points, and the carried-forward nit. Appended against the unique physical tail and re-verified the append (my header appears exactly once and is physically last — standing monitoring duty satisfied).

7. **Completed the session closeout:** this report, a workspace-README update, a full rewrite of the continuity summary, a `.gitignore` review, and the commit/push.

## Important decisions and reasoning

- **Approve the residual baseline as-is rather than manufacture edits.** The review-cycle playbook is explicit that when the reviewer finds nothing to change, the correct move is to explicitly approve the state as-is — that closes the loop. My independent reproduction found the diagnosis and implementation both correct and the honesty boundaries intact, so I approved rather than inventing cosmetic changes.
- **Build the seam regression this session.** It was the highest-value, clearly-scoped, already-agreed piece of buildable work: it lives on my `EstimatorCommandPolicy` socket, both agents wanted it, and it closes the last seam property that was only verified in pieces. The genuinely blocked work (the learned attribution head and RMA latent) stays blocked — it needs a CUDA PyTorch build, a frozen config, and confirmatory data that do not exist yet, and standing up an untrained network now would violate the efficiency standard and produce a guess dressed as a result.
- **Do not reopen the just-closed estimator loop for a cosmetic nit.** In Session 13 I flagged a tiny consistency nit (one detector floors a standard deviation at `1e-12`, its sibling at `1e-3`) and explicitly deferred it to my next *substantive* estimator increment. It never bites a real calibration set. Reopening a freshly jointly-approved artifact for an aesthetic floor change is low value and mild churn, so I carried it forward again, on the record, to fold into the learned-head work.
- **Leave the Live-Run README untouched.** The heartbeat check found nothing log-worthy: closing a review loop on development scaffolding and adding a mechanism test are not finished public artifacts, phase closes, or frozen results, and the running log is lean by design. This matches how both agents handled the analogous Session-13 scaffolding sessions.

## Challenges and how they were handled

- **A stale startup git snapshot.** Resolved by verifying live state directly (`git log`/`git status`), as my continuity file instructed — the live clean tree at Codex Session 13 controlled the session.
- **My own reproduction script initially "failed" two atomicity checks.** On inspection this was a flaw in *my test*, not Codex's code: I had assumed that re-fitting an S-bound estimator with a C1 record would raise mid-fit, but `fit_dynamics` legitimately *re-binds* to whichever suite the new healthy records carry (invalidating all downstream state), so my "failed re-fit" had actually succeeded as a clean suite rebind. I corrected the test to trigger a genuine mid-fit failure (a too-few-transitions record) and confirmed true atomicity, and I noted the re-bind behavior as a benign observation in the chat. Worth recording because it is a good example of the reviewer's own instrument being wrong rather than the artifact — caught by reading the failure instead of trusting it.

## Files created

- `Reproducibility Packet/tests/test_recovery_seam.py` — the shared end-to-end recovery-seam regression (my socket; handed to Codex for first review).
- `agents/Claude/Session Summaries/HumanReport14.md` — this report.

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the Session-14 review-cycle turn.
- `agents/Claude/README.md` — workspace guide updated for Session 14.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten for the next session.

`agents/Claude/references.md` is unchanged: this was a review-and-mechanism-test session that introduced no new external source (the seam test uses the already-cited residual/system-ID and recovery rationale). The root `README.md` and `.gitignore` are unchanged after their required checks.

## Verification performed

- Independent reproduction script (my own records, not Codex's tests): **22/22 checks pass** — ARX/residual math bit-match, matched-ablation nesting, leakage guard, identity non-consumption, atomic re-fit lifecycle, tail guard, and the end-to-end safety boundary including a confident-structure/actuator output held nominal.
- New seam regression `tests/test_recovery_seam.py`: **4/4 pass**.
- Full Reproducibility Packet: **138 passed** (134 handed off + 4 new seam tests).
- `compileall -q` over packet scripts and tests: clean.
- Active-chat Session-14 header count: exactly 1; new Claude turn is physically last (line 840).

## Next steps / pending actions

1. **Codex to first-review `tests/test_recovery_seam.py`.** If Codex edits it, I must re-open and genuinely owner-re-review both the feedback and the edits before that loop can close.
2. **Codex's likely next lane work:** the evaluation-sized closed-loop controller comparison (separating exact actuator-delivery compensation from `J_5s` tracking recovery and privileged safety), and the real MuJoCo endpoint-contact extraction required before any optional-contact pilot. If Codex opens a new review loop, I review it next session.
3. **My deferred, still-blocked builds (do not start early):** the learned attribution head (`TemporalAttributionNet`) and the RMA-style latent — both need a CUDA PyTorch build (GPU-verified for this Blackwell GPU), a frozen config, and confirmatory data. The `null_std` consistency nit folds into that increment.
4. **Before confirmatory generation (shared):** settle the validation-sized healthy/known calibration roles (with per-suite probability calibration per my forward point), severity/onset grids, non-load-bearing sensor constants, contact-enabled cases, the split/leakage/storage audits, then freeze and hash the complete config.
5. **Do not freeze `config.json`** until the open items resolve; current role hashes remain `dev-`.

**Next regular Claude progress report: Session 16** (Phase-0-close, Phase-1-close, and Session-8 reports already exist and do not reset the per-agent counter; Session 14 closed no phase and wrote no amendment, so it triggers no report).
