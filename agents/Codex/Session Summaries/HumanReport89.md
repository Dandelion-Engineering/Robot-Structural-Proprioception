# Codex — Human Report, Session 89

**Date and time:** 2026-08-07 06:13 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits: 0. Checkpoint writes: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase
transition and no approved Claim-Sheet amendment occurred.

---

## Summary

This was the same-state reviewer re-review requested by Claude Session 89. I genuinely reopened
both returned artifacts rather than accepting their handoff:

- Claude's Session-88 director progress report is approved unchanged at Git blob
  `58276bb4e0fee178843c5453ae35b931921da666`, canonical SHA-256
  `1e359749c72fb54bb885fff4a7c51de6758cd80240be46ecb3db3ca4fc347691`.
  Claude had already explicitly approved those exact bytes, so that review loop is closed.
- The capacity-escalation design needed two narrow reviewer corrections. I edited it and
  explicitly approve the resulting Git blob `618d9ada1ab94133429f5b0412abd70d2b9a2400`,
  canonical SHA-256
  `efe655ecd452293d5b5bee3a6434399324cddebc21483d18699cd9af3dd30b04`.
  Because this is a new reviewer-edited state, Claude must genuinely owner-review it before
  v0.1 freezes.

The main defect was an authorization overclaim. Claude correctly recognized that a plan needs
a run-level identity once machine paths are removed, but `run_label` cannot make a plan digest
single-use. The same approved plan can still be executed into two fresh physical roots because
the local executable has no durable external consumption registry. I kept `run_label` because
it makes every conforming retry a distinct, auditable plan and logical namespace; I removed the
claim that the field itself carries or consumes authorization. The one-execution boundary
remains a joint governance act, as it was for the payload extension.

The second defect was smaller but executable-facing. Claude's table named the project-defined
helpers in the copied fit loop, but called itself the complete call surface and said everything
else would be imported. The real body also contains copied control flow and direct
PyTorch/NumPy calls. I narrowed the table to the complete project-defined dependency surface,
added the omitted `TemporalAttributionNet` entry, and stated that C9 measures the full copied
seam.

No capacity executable, plan, fit, checkpoint, threshold, Stage-2 action, later-role read,
generation, rollout or final config action occurred.

## What was accomplished

### 1. Reconciled stale automation memory with the live repository

The automation memory ended at Codex Session 83, while the repository was already clean and
synchronized at Claude Session 89 (`d2f27c3`). I used the current Git history, Codex continuity,
Claude's HumanReport89, and the physical transcript tail as authority. No Claude lock was
present.

### 2. Approved Claude's returned progress report unchanged

I reviewed the full report at the director-facing Accessible-Piece bar. Claude retained
Codex's causal narrowing, restored plain-language register, and corrected the now-settled route
choice and 42-fit count without changing the evidence boundary. The report remains explicit
that the sweep can map width sensitivity under one fixed training protocol but cannot prove
that an undersized network caused the adverse first-fit direction.

The exact returned state is:

```text
agents/Claude/Progress Reports/Progress Report Session 88.md
  Git blob          58276bb4e0fee178843c5453ae35b931921da666
  canonical SHA-256 1e359749c72fb54bb885fff4a7c51de6758cd80240be46ecb3db3ca4fc347691
  physical state    16,183 B / 275 LF in this working tree / no BOM
```

The file is not LF-pinned, so the canonical digest rather than a checkout-specific raw digest
is the portable document identity.

### 3. Accepted Claude's sourced-constant and private-helper repairs

The approved analysis artifact contains exactly:

```text
paired_macro_f1.claim_sheet_success_bar      0.05
paired_macro_f1.sample_sd_S_minus_C1         0.149635726834
```

The design now names the latter field explicitly, treats the displayed value as reader
convenience rather than executable literal, and requires a finite positive value. That repair
is correct.

`fit_one_arm` does call private `_stack`; importing it is safer than copying the project-defined
batching logic, and the existing C9 equivalence gate remains the correct empirical backstop.

### 4. Corrected the run-identity / authorization boundary

Claude's returned text said `run_label` made an execution authorization single-use. I tested
that assertion against the actual authorization shape rather than the document's internal
story:

```text
same plan bytes + same approved digest + fresh physical root A -> digest gate can pass
same plan bytes + same approved digest + fresh physical root B -> digest gate can also pass
```

The local dirty-output check sees only its own target root. A deterministic plan document has
no external global state and cannot certify that its digest has already been spent elsewhere.

The corrected contract keeps `run_label` for a narrower, real purpose:

- each conforming retry uses a new logical namespace;
- each conforming retry produces a different plan and digest;
- preserved run artifacts make separately authorized acts distinguishable; and
- repeated use of the same label/digest is visible as a protocol violation when the preserved
  artifacts are compared.

It does not claim mechanical replay prevention. A second execution still requires a second
joint authorization as a governance rule.

### 5. Corrected the copied-loop dependency description

AST inspection of `dev_fit_trainer.fit_one_arm` confirmed that the body directly invokes
project helpers plus PyTorch/NumPy operations, object methods, and Python built-ins. The design
now says exactly what is imported and what is copied:

- imported project-defined dependencies: `TemporalAttributionNet`,
  `require_predeclared_seed`, `deterministic_conv_precision`, `arm_loss`, `_stack`, and
  `DevFitDataError`;
- copied expressions/control: seed setup, Adam construction, row permutation, finite checks,
  epoch/batch loops, optimizer operations, loss-history aggregation, and final finite-weight
  check.

C9 continues to compare the entire duplicate fit seam, not merely the helpers in the table.

### 6. Independently reproduced the design's current source bindings

Using only the project virtual environment and disabling bytecode writes:

```text
channels      parameters   receptive field
16               10,586             1,023
24               22,786             1,023
32               39,594             1,023
40               61,010             1,023
48               87,034             1,023
```

All five constructors accepted `enforce_rung1_band=True`. The current trainer identity has
eight entries and matches every one of the ten ledger arms exactly. The two planned C9 source
states, C1 seed 0 and S seed 4, each carry a 20-epoch loss history and their approved checkpoint
files are present.

### 7. Verified the packet and transcript

The complete packet test suite passed:

```text
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='scripts'
..\venv\Scripts\python.exe -B -m pytest tests -q

1,551 passed in 114.44 s
```

The Phase-2 transcript append used Claude's exact physical EOF block and passed the hard gate:

```text
pre-write bytes          1,537,662
pre-write lines          24,502
pre-write SHA-256        61b44375ad19b6378e4337d11e80484219d427287cb9b93e57113f0d51916067
final bytes              1,542,930
final lines              24,595
Codex header line        24,504; exactly once and after the boundary
old prefix               byte-identical under the pre-write SHA-256
Git diff                 +93 / -0
physical tail            Codex, followed by the separator
```

No append-order recurrence occurred, so the Transcript Order Monitoring chat was correctly
left unchanged.

## Challenges and how they were handled

- **The saved automation handoff was six Codex sessions behind.** I treated it as historical
  context and let live Git/transcript state control the work.
- **Claude's authorization diagnosis contained both a real problem and an overclaimed repair.**
  I separated identity/auditability from replay prevention rather than either removing the
  useful field or accepting a false one-time guarantee.
- **The call-site table mixed two scopes.** Direct AST/source inspection separated
  project-defined dependencies from copied library/control expressions.
- **Windows line endings make raw Markdown digests unstable for unpinned files.** I used the
  project's canonical-text digest for the progress report and verified the LF-pinned protocol
  file's raw and canonical digests are identical.

## Important decisions and reasoning

1. **Approve the progress report unchanged.** Its causal boundary, register, current route and
   fit count are all accurate.
2. **Keep `run_label`, narrow its claim.** It is valuable run identity and audit structure;
   it is not a local one-time authorization mechanism.
3. **Do not add an external registry in this design.** That would be a materially new stateful
   authorization subsystem. The existing project treats execution permission as a joint
   governance act, so the honest design is to name the enforcement boundary.
4. **Import private `_stack` and disclose it.** Preserving one batching definition is safer
   than avoiding a private import by copying science-affecting plumbing.
5. **Leave the public Live-Run README unchanged.** An open design review is not a finished
   artifact, phase close, result or pivot. Its blob remains `a544f9d2...`.

## Current exact states

```text
capacity design
  Git blob                 618d9ada1ab94133429f5b0412abd70d2b9a2400
  canonical/raw SHA-256    efe655ecd452293d5b5bee3a6434399324cddebc21483d18699cd9af3dd30b04
  physical state           57,324 B / 900 lines / LF / no BOM
  reviewer delta           +71 / -44; git diff --check clean
  approval                 Codex approves; Claude fresh owner re-review open

Claude progress report
  Git blob                 58276bb4e0fee178843c5453ae35b931921da666
  canonical SHA-256        1e359749c72fb54bb885fff4a7c51de6758cd80240be46ecb3db3ca4fc347691
  approval                 Claude and Codex approve; loop closed
```

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport89.md`

Updated:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Deliberately unchanged:

- `agents/Claude/Progress Reports/Progress Report Session 88.md`
- `README.md`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
- every executable, test, result JSON, checkpoint and config artifact

The existing `.gitignore` and packet `.gitignore` already cover locks, virtual environments,
caches, secrets, logs, local datasets and rebuildable model payloads; no ignore change was
needed.

## Next steps

1. Claude genuinely reopens and explicitly approves or contests capacity-design blob
   `618d9ada...`.
2. If Claude approves it unchanged, v0.1 freezes and the Route-A capacity executable plus tests
   may be written. That executable receives a separate exact-state review.
3. Only after executable same-state approval may a zero-fit plan be produced and reviewed.
4. Only a later separate joint authorization may run the two C9 equivalence fits and forty
   curve fits.
5. Pilot, validation, test, thresholds, Stage 2, final `config/config.json`, generation,
   confirmatory reads and all rollouts remain blocked.

— Codex
