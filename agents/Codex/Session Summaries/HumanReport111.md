# Codex — Human Report, Session 111

**Date and time:** 2026-08-10 17:25 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a
phase transition or an approved written Claim Sheet amendment triggers one sooner.

---

## Summary

Claude returned the zero-resource Slot-9 rung-2 design requested in Codex Session 110:
`Reproducibility Packet/protocol/rung2-escalation-v0.1.md`. I authenticated the exact handoff,
read it against the Claim Sheet, limitation 127, the approved trainer/capacity-sweep seams, and
the review-cycle playbook, and completed a design-only reviewer pass.

The central direction is sound. The next capacity-ladder object is one named
recurrent-plus-attention estimator, not another width-only sweep of rung 1. Its authority comes
from Slot 9 and the carried capacity limitation, not from a trend in the unreadable Stage-1 curve.
The design keeps C1 and S exactly capacity-matched, uses the five existing anchor seeds for
commensurability rather than claiming precision, preserves all Stage-1 evidence, and separates
module build, executable review, plan, execution, analyzer, later-role reads, capacity selection,
thresholds and confirmatory work.

The returned bytes were not yet executable as a contract. I found seven blocking design-state
defects, repaired the still-unapproved v0.1 draft directly, re-opened the resulting state, and
explicitly approved the new exact blob:

```text
Claude-returned blob       b7449993ceeb657fb37feff36bff4cb827ceed0a
Codex-approved blob        1f65ab5f32715d8ec405bb362fbf5af302550b13
raw/canonical SHA-256      5ebca381c218afdbab17118c28b86891cf7b746d3ca2a36d318901cd463fa329
size / physical lines      52,541 B / 797 LF
CR / BOM / final newline   0 / none / yes
Git attributes             text, eol=lf
```

Because the reviewer changed the bytes, the review loop is still open. Claude must genuinely
re-open blob `1f65ab5f...` and explicitly approve it or return a new state. No rung-2 module build
is authorized until that exact-state owner re-review closes.

---

## What was reviewed and changed

### 1. Corrected the source of authority

The returned design treated both Slot 9 and Slot 14 as licenses for the action. Slot 9 directly
licenses the capacity-ladder climb. Slot 14 requires the final Technical Report to contain the
matched ablation and within-suite capacity sweep, but Stage 1 already supplies that sweep. A
single rung-2 configuration is not a second within-suite sweep. The document now keeps Slot 14 as
a reporting obligation and Slot 9 as the action's authority.

### 2. Made the 219,018-parameter architecture exact

The returned design named a single-query multi-head attention pool but did not specify the
projection structure. Its quoted parameter count implicitly required custom Q/K/V projections
with no attention output projection; an implementer using `nn.MultiheadAttention` unchanged
would have produced 228,330 parameters and failed the design's own exact-count invariant.

The reviewer state now fixes:

- the exact bias-bearing, two-layer, unidirectional GRU arguments;
- three bias-bearing `H -> H` Q/K/V projections;
- scaled dot-product attention with softmax over time;
- no attention output projection and no attention dropout;
- one later `Linear(2H -> H)` fusion projection; and
- rung-1-style RNG isolation so same-seed C1/S constructors begin bit-identically without
  advancing the caller's RNG stream.

It also carries an independently checkable component ledger totaling 219,018 parameters.

### 3. Separated size-band admissibility from architecture identity

The returned grid called an 82,778-parameter recurrent-plus-attention candidate “still rung 1”
because it falls below 100,001 parameters. That is not true: it is an undersized rung-2-family
candidate. Parameter count cannot identify the architecture rung by itself, and a future rung-3
ensemble may overlap the proposed size band.

I accepted D2's `[100_001, 1_000_000]` interval as the enforced admissible band for the named
rung-2 family, but corrected every claim that count alone classifies the ladder.

### 4. Narrowed the objective-reduction claim

The returned gate named an arm `LEARNED` when its combined final loss was below its first loss.
The approved objective includes a severity Gaussian-NLL term whose log-scale can reduce the total
without classification improving. A total-loss reduction is therefore not a learning or
classification signal.

The gate is now named only for what it computes:

```text
per completed arm          OBJECTIVE_REDUCED
whole successful run       OPTIMIZATION_CHECK_PASSED
```

The document explicitly forbids promoting that numerical smoke check into a learning or
performance claim.

### 5. Replaced the overlapping interpretation table with an ordered partition

The original §5.4 let an equivalence failure also imply “not learnable” before any rung-2 arm had
run, and a successful run matched both a build row and a sign row despite a heading that promised
one sentence. The reviewer state evaluates four mutually exclusive status branches in order:

1. equivalence failure or unmakeable comparison;
2. incomplete ten-arm execution after equivalence passes;
3. completed execution with at least one failed objective-reduction check; or
4. successful optimization check.

Only the fourth branch opens exactly one of the three predeclared sign descriptions. The analyzer
must suppress paired-sign and rung-comparison fields on every other branch.

### 6. Repaired the impossible refusal-persistence promise

The design said every refusal persisted an artifact while importing
`require_permitted_base()`, whose defining safety property is that it writes nothing under
`results/dev_fit`, including no refusal sink. A missing required destination also has nowhere
authorized to write.

Those are now the two disclosed stdout-only boundaries. Once a permitted base exists, every
terminal path still persists its named artifact. The duplicated refusal writer's equivalence
test now uses one fixed valid UUID, requires identical JSON payloads, and isolates the path
difference to the sink-directory component.

### 7. Bound the new checkpoints to their own producer state

The returned document pinned the design digest and checked the eight historical trainer
identities but did not explicitly require each new checkpoint to carry the complete new producer
identity. The reviewer state adds that gate. Plan mode binds, execute mode verifies, and every arm
plus the run artifact persists a sorted code-identity map containing:

- the eight unchanged historical trainer entries;
- `capacity_sweep.py` and `analyze_dev_fit.py`, whose scoring/persistence paths are imported;
- `attribution_net_rung2.py`; and
- `rung2_escalation.py`.

The design digest proves which protocol authorized the executable; it no longer stands in for
the code identity that produced a checkpoint. The equivalence gate also now compares both state
dictionaries and per-epoch loss histories against the approved Session-84 records.

---

## Decisions on Claude's four questions

1. **D1 — accepted.** Import `_CausalDilatedBlock` and `_PerStepChannelNorm` inside the same
   package and test that rung 2 defines no local causal-block copy. This is safer than a second
   causality implementation.
2. **D2 — accepted with corrected semantics.** Keep `[100_001, 1_000_000]` as the enforced
   admissible band for the named recurrent-plus-attention family. Do not treat parameter count as
   the architecture classifier for the whole ladder.
3. **D3 — accepted.** Use seeds `{0,1,2,3,4}` because those are the five available anchor pairs.
   This is commensurability, not precision. Any larger seed extension needs a separate
   justification based on measured rung-2 dispersion.
4. **D4 — accepted.** Do not edit `attribution_net.py`, `dev_fit_trainer.py`, or
   `capacity_sweep.py`. Their recorded identities are more important than correcting the stale
   ladder flag, narrow type annotations, or refusal-sink API. Those remain disclosed and tested.

I also accepted Claude's proposal to split permanent internal instruments out of its roughly
400-KB continuity file. The current gate map, current exact-state handoff, and next-read routing
must remain in `Summary of Only Necessary Context.md`; the permanent audit/gate instruments may
move to one tracked Claude-owned reference file read on demand. This is an internal workspace
organization change, not a Claim Sheet amendment or packet artifact.

---

## Verification

No project-data or executable test was needed for a document-only review. I performed the checks
that bear directly on the edited contract:

```text
returned Git blob / raw digest / LF attributes          reproduced exactly
seven architecture-grid parameter counts                independently reproduced
selected custom-Q/K/V parameter count                   219,018
unchanged nn.MultiheadAttention counterfactual          228,330
ordered outcome partition                               exhaustive / one branch
git diff --check                                        clean
config/config.json                                      absent
development rows / .npz / checkpoints opened           0 / 0 / 0
fits / checkpoint writes / generation / rollouts        0 / 0 / 0 / 0
pilot / validation / test reads                         0
```

The parameter-count reproduction used only arithmetic in the project virtual environment and no
project data. It matched all seven rows of Claude's construction grid exactly.

The Phase-2 transcript append passed the physical-EOF hard gate:

```text
pre-write transcript       1,904,898 bytes / 30,750 LF
pre-write SHA-256          3a7f5974387e34e7d667c357be63c5b04e1cebb6af5d2d6adb68dd829162639f
Codex header               unique at physical line 30,752
old prefix                 byte-identical
transcript diff            +109 / -0, one tail hunk
last agent                 Codex
post-write transcript      1,911,511 bytes / 30,859 LF
post-write SHA-256         26de87a7260c6e3975a6e06d3da7f61e6402d79c621c711e69139ef59acd0803
```

No Transcript Order Monitoring entry was required. The public Live-Run README was checked and
left unchanged: a reviewer-edited design with owner re-review still open is not a finished
artifact, phase transition, outward-facing result, or new scientific finding.

---

## Files created or updated

- `Reproducibility Packet/protocol/rung2-escalation-v0.1.md` — reviewer-edited design, explicitly
  approved by Codex at blob `1f65ab5f...`; Claude owner re-review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact findings, D1-D4 rulings, approval, boundary and continuity-split response.
- `agents/Codex/Session Summaries/HumanReport111.md` — this report.
- `agents/Codex/README.md` — updated navigation and current rung-2 review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 112.

Deliberately unchanged: every executable/test, every Stage-1 plan/result/artifact/checkpoint, the
Claim Sheet, both `.gitattributes` files, both `.gitignore` files, `director_requests.md`, the
public Live-Run README, and `Reproducibility Packet/config/config.json` (still absent).

---

## Resource and evidence boundary

This session performed no fit against any development row, opened no observation payload or
checkpoint, wrote no checkpoint, generated no data, spent no rollout, ran no C7 action, ran no
plan mode, read no pilot/validation/test outcome, selected no capacity, set no threshold, and
materialized no final configuration.

Stage 1 remains complete as scoped and still licenses exactly its no-readable-shape sentence.
The reviewer-approved rung-2 design is not jointly approved until Claude approves the same exact
blob. Even after closure it authorizes only writing the architecture module and its tests; every
later act remains separately gated.

---

## Next steps

1. Claude re-opens exact blob `1f65ab5f32715d8ec405bb362fbf5af302550b13` and either explicitly
   approves it or returns a new design state.
2. Only after same-state closure may Claude write
   `Reproducibility Packet/scripts/utils/attribution_net_rung2.py` and its tests.
3. The executable, plan mode, twelve-fit execution, analyzer, exact artifact review, §5.4 read,
   validation capacity selection, all thresholds and confirmatory work remain separate gates.
4. Claude may perform the approved internal continuity split while preserving the active gate map
   and precise next-read routing in its ordinary summary.
5. Codex Session 112 is a regular progress-report session in addition to its normal work.
