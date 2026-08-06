# Codex — Human Report, Session 84

**Date and time:** 2026-08-06 10:38 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**
**Fits run this session:** **0.** This session audited Claude's completed ten-arm fit and ran inference-only analysis.
**Progress-report session:** no. The next regular Codex progress report is Session **88**.

---

## Short result

Claude's first ten learned-model development fits are valid inside their narrow authorized
boundary. I independently verified the tracked result ledger, all ten checkpoint hashes,
the exact dev-only data/assignment/code identities and the reported in-sample metrics.

The two main review decisions are:

1. **Finding W remains disclosed.** The dirty-output refusal can raise when its own refusal
   name is unwritable, but the path is outside the authorized fresh-directory invocation,
   destroys no prior bytes and is already part of the previously disclosed loud-exception
   class. Editing the exact fitted producer now would also break current-packet
   reproducibility of the provenance ledger it emitted.
2. **Finding X is accepted forward through a separate analysis artifact.** The historical
   fit ledger stays unchanged. A new read-only script verifies the fit state and persists
   the four post-fit loss terms plus in-sample accuracy, macro-F1 and five-seed pairing.
   It runs zero fits, zero generation and zero rollouts and reads no later role.

The new analysis supports the public claim that the implementation optimizes in sample,
but nothing stronger. C1/S mean in-sample accuracy is **0.870 / 0.817** and macro-F1 is
**0.682 / 0.650**, against a **0.632** majority-class baseline. The paired S-minus-C1
macro-F1 mean is **-0.0321** with sample SD **0.1496**. This is a seed-sensitivity warning,
not a held-out comparison or a capacity decision.

---

## Work completed

### 1. Reconstructed the live state rather than trusting the older automation handoff

The automation memory ended at Codex Session 78, while the live repository had advanced to
Claude Session 84. I read the controlling project details, Codex continuity, all Codex
chat summaries and the physical tail of the active Phase-2 transcript before acting.

The live state showed:

- both agents already approved the exact trainer/test state
  `caa00418b2f404575dca7cda167e6be76c99183a` /
  `cbc4064fddee8d2b548c95ddc32709dfbf0653e6`;
- Claude had run the ten authorized development-only arms once into a fresh output
  directory;
- the tracked fit ledger was new and the ten rebuildable checkpoints remained ignored;
- Claude asked Codex to rule on Finding W and Finding X; and
- no pilot, validation or test outcome, final config or confirmatory identity had been
  touched.

### 2. Independently audited the tracked fit ledger and checkpoints

I approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

The audit established:

- ten unique and complete `(suite, seed)` arms: C1/S × seeds 0–4;
- ten checkpoint files present and every raw SHA-256 equal to its arm record;
- 152 examples per arm, split evenly across the diagnostic and ordinary trajectories;
- exact manifest, config, assignment and three role-index digests;
- the same eight-file fit code identity in the top-level ledger and every arm;
- `X_FIT_OK`, ten fits in Claude's completed run and zero rollouts;
- no drive-letter path, backslash, repository name or user name in the ledger; and
- `config/config.json` still absent.

The exact dev class census is healthy 8, structure 16, actuator 32 and sensor 96. Both
suites have zero OOD rows, so this fit says nothing about OOD behavior.

The review-cycle rule remains literal: Claude created and described the ledger but did not
explicitly approve an exact digest in the handoff. My exact-state reviewer approval is now
recorded; Claude's owner approval of the same `f18c98b2...` / `d4cefb61...` state remains
open.

### 3. Ruled Finding W disclosed

Claude reproduced a real edge: if `dev_fit_output_refused.json` is itself an unwritable
file or directory, the stale-output refusal cannot overwrite that name and raises before
returning its named terminal code.

I did not edit the fitted trainer. The ruling rests on four facts:

- the authorized invocation requires a fresh directory, so this path is not on its graph;
- the edge destroys no prior result or checkpoint bytes;
- the failure is loud rather than permissive; and
- the current trainer bytes are part of each checkpoint's recorded provenance, so a
  post-run edit solely for this unreachable refusal would make the packet's current
  producer diverge from the tracked reference result.

The disclosure is conditional, not permanent permission. If a later authorization admits
reused or hostile output directories, or the trainer changes for another reason, Finding W
must close before that new state executes.

### 4. Built a reproducible, read-only fit analysis for Finding X

Created:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  cef8c35a553e93dd540edd8ffa1bca44dd145bc0
Reproducibility Packet/tests/test_dev_fit_analysis.py
  Git blob  9837499e708ff583837586507e4f3f858024c07c
Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  raw SHA-256  a5926ea1eb0b09314438aa7d7b74b4ecbcbd17b04a016d719743aa6e6cf4ee5f
  Git blob     d61edd330b29032367217ff9d61525713ffa61a6
```

The analyzer:

- loads strict JSON and refuses duplicate keys/non-finite constants;
- validates the complete matched ten-arm ledger and all arm-level bindings;
- requires the fit result to name the current executable training state;
- loads only the exact authorized dev rows through the production loaders;
- verifies every checkpoint digest before strict state-dict loading;
- runs inference only on CPU under the shared deterministic-convolution context;
- computes fixed-four-class accuracy and macro-F1;
- persists class, location, severity and OOD loss terms separately;
- records both fit-code and analysis-code identities with bare labels only;
- records the class/OOD/trajectory census and simple empirical baselines; and
- states the no-generalization/no-selection/no-threshold authority in the artifact itself.

The artifact contains no local path. Regenerating it twice produced identical bytes.

### 5. Reproduced the reported metrics

```text
                              C1        S      empirical baseline
class cross-entropy         0.434     0.557          1.010
accuracy                    0.870     0.817          0.632
macro-F1                    0.682     0.650              -

paired S-C1 macro-F1 mean  -0.0321
paired five-seed sample SD   0.1496
```

The per-seed macro-F1 pairs reproduce Claude's scratch values at displayed precision. The
loss decomposition also reproduces Finding X: severity Gaussian NLL averages **-1.162**
for C1 and **-1.116** for S, which drives the post-fit total to **-0.190 / +0.016**. A
negative total is allowed by the loss definition and is not itself a learning signal.

The analysis separates two non-equivalent quantities:

- `training_final_epoch_mean_loss`: mean minibatch total during the last optimizer epoch;
- post-fit full-batch terms: recomputed after the last update over all 152 examples.

### 6. Updated the packet and public documentation

`Reproducibility Packet/README.md` now includes:

- Step 26: copy-paste plan and fit commands, fresh-output rule and exact result outputs;
- Step 27: the read-only analysis command, tracked artifact/hash and bounded metrics;
- a current boundary that no longer says the learned head is untrained or the trainer is
  absent; and
- explicit separation of in-sample development evidence from capacity, calibration,
  validation and confirmatory work.

The first draft invoked `scripts.utils.dev_fit_trainer`, which failed because the packet's
package expects `scripts` to be the `PYTHONPATH` root. I corrected the runbook to the tested
PowerShell form:

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.dev_fit_trainer ...
```

The exact plan command then returned `X_PLAN_OK`, ten arms, zero fits and zero rollouts.

The newest root `README.md` entry now states the architecture fact precisely: both suites
use the same 39,594-parameter network, while S supplies four additional nonzero gauge
channels without additional parameters. The preplanned capacity ladder is the test of
whether rung 1 is undersized; it is not an automatic explanation for the adverse
in-sample direction.

### 7. Appended the exact-state handoff safely

The active transcript append passed the hard gate:

```text
pre-write bytes       1,445,575
pre-write lines       22,897
pre-write SHA-256     5694c0c22377b9ff99fb9a0486779f15a43aa55ca3c26f7b72f23eae2cc01aa7
final bytes           1,451,674
final lines           23,022
new header line       22,901; unique and after the boundary
prefix check          byte-identical
diff                  +125 / -0
physical last author  Codex
replacement chars     0 in the append
```

The handoff explicitly approves the fit ledger and the five reviewer-created
analysis/document states, records the W/X rulings and leaves Claude's genuine owner review
open.

---

## Verification

```text
analysis tests                       10 passed
analysis tests under python -O       10 passed; expected pytest warning only
trainer + analysis focused           59 passed
focused under python -O              59 passed; expected pytest warning only
full packet suite                     1,526 passed in 126.52 s
compileall                            clean
git diff --check                      clean
documented plan command               X_PLAN_OK; 10 arms; 0 fits; 0 rollouts
analysis regeneration                 byte-identical twice
checkpoint digests                    10 / 10 matched
analysis path disclosure              none
config/config.json                    absent
```

No fit, checkpoint creation, data generation, plant simulation or physical rollout occurred
in this Codex session. The existing ignored checkpoints were read for verification only.

---

## Files created

- `Reproducibility Packet/scripts/analyze_dev_fit.py`
- `Reproducibility Packet/tests/test_dev_fit_analysis.py`
- `Reproducibility Packet/results/dev_fit/dev_fit_analysis.json`
- `agents/Codex/Session Summaries/HumanReport84.md`

## Files updated

- `README.md`
- `Reproducibility Packet/README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

---

## Decisions and next actions

1. Claude should genuinely review and explicitly approve or contest the exact fit ledger,
   analyzer, tests, analysis artifact and two README states named in the active transcript.
2. Finding W remains disclosed for the current historical producer; it blocks any future
   reused/hostile-output authorization unless closed first.
3. The analysis artifact, not a rewritten ledger or unauthorized rerun, carries Finding X
   forward.
4. The seed spread is a Gate-6 design warning only. It does not itself authorize more
   seeds, a capacity choice or a confirmatory design change.
5. No next capacity fit may run until a separately reviewed executable state and explicit
   authority exist.
6. Pilot, validation and test outcome reads; threshold work; final `config.json`; new
   generation; and all confirmatory activity remain blocked.
