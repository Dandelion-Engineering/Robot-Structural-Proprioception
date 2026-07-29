# Human Report — Codex Session 38

**Current date and time:** 2026-07-28 21:29 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state review of Claude's Amendment A2 proposal v5 and
unrun Protocol P v2.1

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)

**Governing decision:**
`BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

**Session decision:**
`BLOCK_AMENDMENT_A2_PROPOSAL_V5_PENDING_EXECUTABLE_COMMAND_SHAPE_GUARD_TERMINAL_CLASSIFIER_AND_UNMATCHED_SCOPE_PINS`

---

## Summary

### Startup and exact state

I followed the repository's `AgentPrompt.md` workflow before acting:

- read `Project Details/Project Details.md`;
- restored the Codex continuity state from Session 37;
- read every Codex-inclusive concluded-chat summary;
- read the complete transcript-order monitoring thread;
- ingested the active Phase-2 technical state through Claude Session 38;
- read Claude's `HumanReport38.md` and current continuity file;
- read `Playbooks/review-cycle.md`;
- checked the live Claim Sheet, approved Gate-3 assignment, draft config,
  split-specific severity roles, generator, RNG keying, sensor model, stored
  observation shapes, synchronous reduction, and plant step convention;
- checked live git state and confirmed `HEAD == origin/main == 73449a9`
  (`Claude Session 38`) before editing; and
- confirmed the monitoring thread needed no reply.

Claude Session 38 posted `AMENDMENT_A2_PROPOSAL_V5`, containing a clean
Protocol P v2.1 replacement. It correctly applied all five corrections from
Codex Session 37, adopted the role-coverage rule, and disclosed a new,
directionally favorable correction: the proposed harmonic window had been
anchored to fault onset even though the delivered diagnostic probe begins one
second later.

No Protocol-P implementation or rollout was performed.

## Finding J: independently reproduced and approved

### Source-level timing

The generator computes:

```text
duration = cycles / frequency_hz
diagnostic_tip_load_start_s = onset + start_offset_s
diagnostic_tip_load_ramp_s = duration / 2
```

For the development diagnostic trajectory:

```text
fault onset:         1.0 s / step 500
probe start offset:  1.0 s
probe start:         2.0 s / step 1000
probe duration:      1.25 s / 625 control steps
```

The plant applies the probe while advancing step 1000. Because stored states
are post-integration, the first probe-affected record row is step 1000 at
`t_s=2.002`. The correct record window is therefore `[1000,1768)`, containing
625 probe-affected rows and 143 post-probe rows. The previous `[500,1268)`
window captured only 268 of those 625 probe rows.

This also confirmed that the existing control-step convention, although easy
to misread from stored measurement times, does not create a one-step error in
the corrected origin.

### Independent development-only measurement

Using the repository venv, the delivered development plant rows, and the
packet's actual `harmonic_coefficients` implementation, I reproduced:

```text
remaining EI  cell   D @ step 500   D @ step 1000   ratio
0.75          r00       0.0649          0.1584       2.44
0.75          r01       0.0598          0.1593       2.67
0.75          r02       0.0368          0.0872       2.37
0.75          r03       0.0266          0.0968       3.64
0.50          r00       0.1868          0.4787       2.56
0.50          r01       0.1847          0.4755       2.58
0.50          r02       0.0841          0.2755       3.28
0.50          r03       0.0778          0.2798       3.60
```

The small differences from Claude's printed ratios are rounding only.

I also reproduced the probe-free ordinary-trajectory control at its own
development fault onset, step 400:

```text
healthy ||b||:  0.4771  0.4850  0.4993  0.5075
D at EI 0.75:   0.0129  0.0155  0.0200  0.0246
D at EI 0.50:   0.0257  0.0256  0.0488  0.0531
```

The correction therefore has the reported substantive effect: it raises the
privileged structural difference by roughly 2.4–3.6 times while leaving the
sensor-only null instrument unchanged. It also confirms the probe-free
negative control at its honest scope.

### Prospective origins

Reading only the assignment text, not non-development outcomes, I verified:

```text
split   w0     w1     run steps   in bounds
dev     1000   1768   3000        yes
pilot   1150   1918   3050        yes
val     1025   1793   3075        yes
test    1175   1943   3125        yes
```

All origins are exactly on the control grid and every window fits.

### Decision

I explicitly approved:

1. anchoring the instrument to the config-derived probe start;
2. rejecting a response-selected peak-aligned window; and
3. carrying the same rule into the written amendment and any later hash-bound
   replacement assignment.

The correction propagates forward. It does not reopen pre-dataset screens,
where probe start and fault onset coincide by construction.

## Decisions on Claude's three explicit questions

### Corrected window origin: approved

The operative window is approved.

The nonoperative empirical-peak disclosure contains a small numerical error.
On the same development r00 healthy privileged trace, scanning every
admissible start gives:

```text
start 1208: ||b|| = 2.092897106   (maximum)
start 1216: ||b|| = 2.088070233
start 1000: ||b|| = 1.880585474
```

The rejected alternative is still approximately 11.29% larger than the
probe-start value, so the disclosure's direction and magnitude are right. The
location/value must be corrected to `1208 / 2.0929`, or reduced to the
approximately 11% statement, in the next clean text.

### Zero-cost unmatched secondary: accepted with narrower scope

I approved retaining the seven unmatched distances as a zero-rollout
descriptive sensitivity. They show what happens when the one Stage-B fault
vector is compared with seven different healthy identities.

I rejected the claim that they "bound" one-shot unmatched performance. The
seven values share the same fault-side realization, are dependent, and contain
no fault-side replication. They cannot estimate or bound a general one-shot
unmatched distribution.

The next protocol must pin:

```text
conditional descriptive sensitivity
seven dependent distances sharing one fixed fault-side identity
no quantile, gate, pass/fail route, or inferential bound
```

The matched statistic remains the only mechanics verdict. `TESTABLE` remains a
necessary, not sufficient, condition for learnability.

### Role-coverage counts: approved

I approved reporting the known-class structural testable count `0/1/2`
separately for development, pilot, validation, and test.

The existing zero-count consequences stay intact. Count 1 is reported as a
thin, single-severity role but does not create a new terminal branch. OOD
components at 0.45 and 0.55 never enter known-class coverage.

## Why Protocol P v2.1 remains blocked

### The Stage-0 command uses the wrong shell syntax

The clean protocol's multiline command uses `^`, which is a `cmd.exe`
continuation character. The project's operational shell is PowerShell, where
the caret is a literal argument.

I verified harmlessly:

```text
.\venv\Scripts\python.exe -c "import sys; print(sys.argv)" ^
-> ['-c', '^']
```

The posted command would therefore give argparse stray `^` arguments. The next
text must provide one PowerShell-executable line, PowerShell backtick
continuations, or a PowerShell argument array. The approved packet working
directory and packet-relative output convention remain unchanged.

### The measurement-time shape guard is not exact

The proposed reduction says:

```python
t_g = tm if tm.ndim == 1 else tm[:, 0]  # fail loud on any other rank
```

That silently accepts any `[T,M]` array and discards columns `1..M-1`. Current
stored `ObservedRecord` objects produce `[T]`; delivered development S records
have shape `(3000,)`.

The cleanest rule is to require `[T]`. If legacy `[T,1]` support is
intentionally retained, the code must explicitly accept only rank 2 with
`shape[1] == 1`, reject everything else, and assert the time length matches
`gauge_obs` and `gauge_valid`. The harmonic helper already checks final
one-dimensional alignment, finite/strictly increasing time, and sufficient
valid samples.

### The terminal contradiction classifier is overbroad

The delivered data measured only the specific candidate:

```text
peak = 0.05 N
ramp_fraction_of_duration = 0.5
```

at healthy, EI 0.75, and EI 0.50. It did not show that every other candidate
must pass healthy or EI 0.75.

The v2.1 terminal rule:

```text
failed at healthy or remEI 0.75 -> implementation-integrity failure
```

can misclassify a mixed branch. The known 0.05/0.5 candidate could pass its
previously measured healthy/0.75 conditions but fail newly visited EI 0.35,
while every other candidate fails some healthy/0.75 gate. All candidates would
be inadmissible without contradicting any prior measurement.

The next text must scope the contradiction to the previously measured
candidate:

```text
0.05 N / ramp 0.5 fails healthy or EI 0.75
  -> contradiction with its delivered-row pass; implementation-integrity

that candidate passes those conditions but fails EI 0.35
  -> newly observed physical safety/method limit

other candidates' failures
  -> logged normally; no prior-pass contradiction by themselves
```

If multiple facts apply, record all of them. The known candidate controls
whether prior evidence was contradicted.

### The unmatched secondary's "bound" wording is decision-bearing

The arithmetic is accepted, but its inferential scope must be corrected before
implementation. Otherwise later reporting could treat seven dependent,
fixed-fault distances as an empirical bound they do not provide.

## Proposal content retained

Everything else in Protocol P v2.1 remains substantively approved for the next
exact text:

- all five v4 corrections;
- safe terminal handling for failed probes and unsafe ladder values;
- Cases A/B/C only after ten safe valid M2 verdicts;
- vector-8 across four gauges;
- the development diagnostic trajectory and four balanced cells;
- Stage-A selection without `T1`;
- direct measurement of all ten ladder values;
- the per-cell Stage-C rule;
- eight healthy replicates per cell;
- `np.quantile(..., method="higher")`;
- the corrected complete-tuple CRN explanation and identity assertions;
- Stage-C numeric tripwire as diagnostic only;
- signal, validity mask, and measurement time in the observed reduction;
- packet-directory output convention;
- measured/first-order thermal-insensitivity wording;
- the inclusive torque gate and 108-rollout Stage-A worst case;
- role-owned severity allocation without outcome-informed rebalancing;
- known-class role coverage and separate OOD roles;
- ordinary structural rows retained in the primary estimand without a
  predeclared direction;
- exact test contact `[1.8,3.3]`;
- the unchanged success bar; and
- arithmetic total of 168 rollouts in the nonterminal worst case.

## Authorization boundary

Still unauthorized:

```text
Protocol P implementation or execution
written Amendment A2
Claim Sheet or Accessible Claim Sheet edits
replacement Gate-3 assignment
amended regeneration
Gate-4 model fitting
final config.json
pilot/validation/test outcome reads
confirmatory identity or payload materialization
```

I asked Claude for one clean Protocol P v2.2 replacement carrying the four
blocking pins and corrected/reduced peak disclosure. Codex owns the next review
after that text arrives.

## Verification and evidence boundary

All Python used the repository venv.

Read-only execution performed:

- direct NumPy loading of existing development plant rows;
- the packet's existing `harmonic_coefficients`;
- exact source/config arithmetic;
- a harmless PowerShell argument-passing check; and
- a read-only every-start scan of the development r00 privileged trace.

The full scoped packet regression suite also passed:

```text
399 passed in 9.62s
```

No project rollout was run. No new identity, payload, result, config, or script
was created.

I opened only development payload values. A broad filename listing while
locating the three role roots printed non-development filenames, but no
pilot/validation/test payload content or outcome was opened. Confirmatory
identity/payload counts remain zero.

Repository state before edits:

```text
HEAD:         73449a9 (Claude Session 38)
origin/main:  73449a9
worktree:     clean
config.json:  absent
```

## Transcript handling

The Phase-2 reply used the UTF-8 physical-tail hard gate.

Before writing:

```text
physical lines:       6,169
bytes:                563,382
SHA-256:              2F9900273CE7CCE6B0D47FBBD911D5CE1D573D2C53272950FEFB861685520BC4
Session-38 header:    absent
EOF-anchor matches:   1
physical last author: Claude
```

After writing:

```text
physical lines:        6,425
bytes:                 572,523
new header line:       6,171
new header count:      1
header after boundary: yes
old-prefix SHA-256:    exact match through the former final newline
technical diff:        +256 / -0
physical last author:  Codex
```

No prior transcript byte changed. No transcript-order recurrence occurred, so
the monitoring thread was left unchanged.

## Public live-run status

Claude Session 38 already added a lean public entry for Finding J. This session
performed internal exact-state review and found proposal-text defects; it did
not produce a new scientific result, finish an artifact, or close a phase.
The root Live-Run README therefore requires no additional entry.

## Files created

- `agents/Codex/Session Summaries/HumanReport38.md` — this report.

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only v5 review, independent reproduction, partial decisions, and
  exact replacement requirements.
- `agents/Codex/README.md` — workspace index through Session 38.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately unchanged

- `README.md`, because Claude already recorded Finding J and this review block
  is not a second public milestone;
- `Claim Sheet.md` and `Accessible Claim Sheet.md`, because Amendment A2 is not
  approved;
- every Reproducibility Packet script, result, assignment, and config;
- the ignored pre-amendment dataset;
- the transcript-order monitoring thread;
- both source ledgers; and
- `Reproducibility Packet/config.json`, which remains absent.

## `.gitignore` review

The current root rules still cover the ignored multi-gigabyte dataset, virtual
environment, scratch work, caches, logs, model artifacts, local secrets,
LaTeX intermediates, OS files, and IDE files. This session adds only tracked
Markdown records and creates no untracked generated artifact. `.gitignore`
requires no change.

## Challenges and reasoning

### Distinguishing a large correct finding from a fully executable protocol

Finding J is important, directionally favorable, and independently correct.
That made it especially important not to let agreement with the scientific
correction substitute for same-state approval of the whole text. The
PowerShell command, shape guard, terminal classifier, and unmatched scope are
small individually, but all sit on paths intended to become automated and
decision-bearing.

### Resolving the apparent timing off-by-one

The stored record's first row is at `t_s=0.002`, so the nominal 2.0-second probe
start appears at stored time row 999. Reading only time values suggests the
window should start at 999. Reading the causal loop and plant advance order
shows why 1000 is correct: row 999 is the post-integration result of the
interval ending at 2.0 seconds; step 1000 is advanced with the diagnostic load
active and is the first affected row. The review therefore kept the proposed
index rather than introducing a new off-by-one error.

### Testing the terminal rule with a mixed counterexample

The new safety/method distinction was sensible but its subject had been lost
in the clean protocol. Constructing a branch where the known candidate fails
only at the new severity and other candidates fail earlier showed that a
global "failed at healthy/0.75" test could falsely declare an implementation
contradiction. Scoping the classifier to the only candidate with prior
same-configuration evidence fixes it without changing the terminal action.

### Separating a sensitivity from an empirical bound

The unmatched calculation is useful and free, but seven comparisons sharing
one fault vector do not constitute seven independent one-shot trials. Keeping
the numbers while removing inferential language preserves the honest
diagnostic value.

## Insights gained

1. A pre-registration can be scientifically sound but operationally
   non-executable because its shell syntax belongs to a different shell.
2. Shape coercion is an analyst choice unless every accepted shape and
   transformation is explicit; a comment saying "fail loud" does not make a
   permissive `else` branch strict.
3. A terminal branch classifier must name the exact object whose prior evidence
   it claims to contradict.
4. Reusing one side of a comparison gives a conditional sensitivity, not a
   population bound.
5. Post-integration storage conventions require reading the execution order,
   not inferring causal boundaries from timestamp equality alone.
6. A directionally favorable correction deserves independent reproduction and
   stricter same-state review, not expedited approval.

## Next steps

1. Claude posts one clean Protocol P v2.2 replacement that:
   - uses a PowerShell-executable Stage-0 command;
   - pins an exact measurement-time shape/length guard;
   - scopes the `NO_ADMISSIBLE_PROBE` contradiction classifier to the
     previously measured 0.05 N / ramp-0.5 candidate;
   - describes the unmatched values as a dependent fixed-fault descriptive
     sensitivity with no inferential bound; and
   - corrects or removes the rejected peak-location number.
2. Codex reviews that exact text and explicitly approves or blocks it.
3. Only after proposal approval may Claude implement Protocol P.
4. Codex reviews the exact implementation before execution.
5. After an approved development-only run, Codex reviews the exact output and
   branch.
6. Only then may the synchronized written Amendment A2, Accessible Claim Sheet
   update, packet/exclusion record, and replacement assignment be written.
7. Both agents must explicitly approve those exact states before any
   regeneration.
8. Keep final `config.json` absent and test identities/payloads at zero until
   all remaining gates close.

No regular Codex progress report is due until Session 40 unless a playbook
event trigger occurs first.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 original generator/base roles: exact-state review closed
Gate-2 generator hardening: exact-state review closed
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved at the pre-A2 assignment
Gate 4: BLOCKED on executable Protocol P v2.2 / corrected Amendment A2
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Confirmatory identities/payloads materialized: 0 / 0
```
