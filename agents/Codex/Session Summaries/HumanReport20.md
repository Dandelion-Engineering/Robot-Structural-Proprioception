# Human Report 20 — Codex

**Session date and time:** 2026-07-22 15:56 PDT (checked at the shell immediately before creating this report)
**Phase:** Phase 2 — Execution
**Session type:** Owner re-review close plus a new role-separated control-headroom screen

---

## Summary

This session first closed Claude's edited review of the Session-19 structural-recovery-action screen. I genuinely re-opened the decision code, new baseline-integrity tests, generated report, and packet runbook, independently exercised all ten broken-baseline counterfactuals, and explicitly approved Claude's exact handed-back state. The structural-action review loop is now closed at same-state approval. The accepted interpretation is narrower and stronger than the original recorded margin: the four-seed source-specificity sign is unresolved, while the robust block rests on the global-versus-localized contrast and the near-zero structural tracking deficit.

I then built the prerequisite both agents identified: a role-separated, no-recovery screen that asks whether any admissible fault setting creates enough tracking deficit for the Claim Sheet's 10% control bar to be reachable at all. The screen varied only structural remaining stiffness and actuator remaining gain while holding the approved bounded task/contact/controller condition fixed. It used three tuning seeds to select the mildest physical setting clearing a predeclared 12% per-seed deficit gate (10% contract bar plus a 2-point development margin), followed by four disjoint assessment seeds.

The result is split:

- **Actuator headroom advances.** A 0.50 remaining actuator gain is the mildest setting to pass, with a 13.20% mean and 13.12% minimum deficit on disjoint assessment seeds.
- **Structural headroom blocks.** No remaining-EI setting from 0.75 down to 0.05 reaches the gate. The disjoint mean deficit moves from +0.11% at 0.75 remaining EI to −5.00% at 0.05; on this bounded task, severe softening eventually improves tracking rather than harming it.
- **The fixed sensor control is live.** A 0.05 rad observation-side encoder bias on a physically healthy plant produces a 15.69% mean / 15.61% minimum disjoint deficit. It was deliberately not selected because sensor severity was fixed rather than swept, but it establishes that sensor-fault recovery design remains a real control problem.

The recorded decision is:

`ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

This is development headroom evidence only. It is not attribution, recovery-action efficacy, validation-sized evidence, or a frozen fault grid. `config.json` remains explicitly unfrozen.

---

## Startup and context ingestion

I followed `AgentPrompt.md` in its required order:

1. Read all of `Project Details/Project Details.md`.
2. Read Codex's prior `Summary of Only Necessary Context.md`.
3. Read every relevant concluded-chat `Summary.md`.
4. Read the complete active Phase-2 transcript through its 1,490-line physical EOF.
5. Read the in-force `Claim Sheet.md`, Claude's latest continuity and `HumanReport20.md`, and `Playbooks/review-cycle.md`.
6. Inspected git status and HEAD (`b8ea8da`, `Claude Session 20`) before trusting continuity.
7. Read `Playbooks/reproducibility-packet.md` and `Playbooks/live-run-readme.md` before creating packet artifacts and updating public status.

The repo began clean on `main`, aligned with `origin/main`.

---

## Review-cycle close: Claude's Session-20 edits

Claude had edited the Session-19 structural-action state rather than approving it same-state. The primary correction added `_baseline_comparison_sound()` to `screen_structural_recovery_action.py`: every percentage and the source-specificity margin is measured against `no_action_1p00`, so those baseline arms must be complete, evaluated exactly once, action-free, A1-clean, and unsaturated just like the acting arms.

I re-reviewed both the diagnosis and implementation:

- all ten baseline counterfactuals (five failure modes × structural/healthy source) block the appropriate assessment gate and the overall decision;
- the committed valid rows preserve the original `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY` decision key-for-key;
- focused structural-action plus recovery-control tests were 37 passed;
- the generated report reproduced byte-for-byte at SHA-256 `06cb38cddcaf2371e2ba60afa186f8a605b31d211a01f6ce0d89567935096732`; and
- compile and diff checks were clean.

I explicitly approved Claude's exact handed-back state. That loop is closed.

I also accepted the report boundary: the `−0.263` percentage-point healthy/structural margin is smaller than its own four-seed spreads and has no computed uncertainty, so its sign is not established. The robust block is that the localized 2× action recovers 6.16% while the global 2× action recovers 20.37%, showing most of the apparent benefit comes through the command at the non-localized joint, and the underlying structural no-action deficit is only approximately +0.05%.

---

## New fault tracking-deficit screen

### Purpose and controlled variable

The screen exists to measure control headroom before designing another intervention. It holds these prior-approved development choices fixed:

- six-second onset-plus-five-second audit;
- bounded smooth task profile;
- z = 0.200 m endpoint plane;
- observed-joint PD controller;
- 0.05 N, 0.8 Hz one-cycle probe;
- W=768 / stride=16 scheduled held-decision lifecycle; and
- C1 observation path with the existing realistic sensor model.

Every estimator output is held healthy, so no recovery action is ever authorized. Only fault severity changes.

### Predeclared grid and roles

Physical grids:

- structural remaining EI: `{0.75, 0.50, 0.25, 0.10, 0.05}`;
- actuator remaining gain: `{0.85, 0.70, 0.50, 0.25, 0.10}`.

Fixed control:

- encoder bias: `0.05 rad`, injected only into `OnlineSensorSession`; the physical plant remains healthy.

Roles:

- tuning sensor seeds: 16000–16002;
- assessment sensor seeds: 16100–16103.

Advancement requires, on every seed:

- no-action tracking deficit at least 12%;
- one held healthy classifier evaluation;
- zero recovery-command changes, including before the decision;
- exact paired pre-fault hash against the healthy denominator;
- zero A1 safety incidents; and
- zero saturation.

The mildest passing tuning severity is selected separately for structure and actuator. Only the tuning-selected setting may advance on disjoint assessment.

### Baseline correction caught before handoff

My first implementation gated every fault row but did not explicitly gate the healthy denominator rows. The raw-row audit exposed this before handoff. I added `_healthy_baseline_gates()` so a baseline that acts, evaluates twice, moves early, saturates, or raises an A1 flag blocks every comparison that depends on it. Five parameterized baseline regressions now pin this invariant. This is the same bug class Claude found in the prior artifact, applied forward rather than repeated into a decision.

### Results

| Source | Remaining fraction | Disjoint mean deficit | Disjoint minimum | Gate |
|---|---:|---:|---:|---|
| Structure | 0.75 | +0.11% | +0.09% | BLOCK |
| Structure | 0.50 | +0.08% | +0.06% | BLOCK |
| Structure | 0.25 | −0.89% | −0.97% | BLOCK |
| Structure | 0.10 | −2.23% | −2.28% | BLOCK |
| Structure | 0.05 | −5.00% | −5.06% | BLOCK |
| Actuator | 0.85 | +2.69% | +2.64% | BLOCK |
| Actuator | 0.70 | +6.28% | +6.24% | BLOCK |
| Actuator | 0.50 | +13.20% | +13.12% | PASS / selected |
| Actuator | 0.25 | +23.16% | +23.03% | PASS |
| Actuator | 0.10 | +65.73% | +65.40% | PASS |

The structural result answers the immediate sequencing question: nominal-controller retuning is not the prerequisite for another structural action screen on this task. There is no structural tracking deficit to recover anywhere in the screened range. The next action review should use the advancing actuator 0.50 condition and the existing inverse-gain mechanism, with source specificity present during candidate selection and an uncertainty-bearing disjoint assessment.

The sensor-control deficit is also above the headroom gate, but sensor severity was not a swept/selected family. It stays a fixed readout and establishes a later design obligation rather than an advancing setting.

---

## Challenges and how they were handled

### Transcript append recurrence

My first owner-approval turn was mistakenly inserted at transcript line 1,331 because an apparently specific patch anchor matched an earlier occurrence. The physical-tail verifier caught it immediately: Codex was not physically last and the new header did not occur after the pre-write 1,490-line boundary.

I preserved the misplaced content, appended a dated transcript-order correction at the verified physical tail using the complete unique EOF block, and rechecked it. The correction header occurs exactly once after the 1,504-line repair boundary at line 1,508, and Codex is physically last. The later deficit-screen handoff used that full unique tail as its anchor and passed: pre-write 1,516 lines, header exactly once at line 1,520, Codex physically last at line 1,562.

No prior transcript content was deleted, moved, truncated, or rewritten.

### Avoiding another unsound denominator

The new screen initially repeated the prior artifact's structural shape: the fault arm was gated more strongly than the denominator it was measured against. Because this was caught before handoff, no recorded decision or artifact needed correction. The healthy-baseline guard was added, the result regenerated, and all five outputs remained byte-identical.

### Keeping the result scoped

The actuator and sensor deficits could be mistaken for recovery results. They are not. The artifact deliberately authorizes no recovery and uses fixed development settings. Its only claim is that sufficient control headroom exists for a later action screen to be meaningful.

---

## Files created or updated

### Created

- `Reproducibility Packet/scripts/screen_fault_tracking_deficit.py`
- `Reproducibility Packet/tests/test_fault_tracking_deficit.py`
- `Reproducibility Packet/results/fault_tracking_deficit_screen/summary.json`
- `Reproducibility Packet/results/fault_tracking_deficit_screen/candidate_summary.csv`
- `Reproducibility Packet/results/fault_tracking_deficit_screen/tuning_rows.csv`
- `Reproducibility Packet/results/fault_tracking_deficit_screen/assessment_rows.csv`
- `Reproducibility Packet/results/fault_tracking_deficit_screen/fault_tracking_deficit_report.md`
- `agents/Codex/Session Summaries/HumanReport20.md` (this report)

### Updated

- `Reproducibility Packet/README.md` — added Step 14, renumbered later steps, and updated the current boundary.
- `README.md` — appended one lean development-direction milestone; prior public log entries were not rewritten.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — preserved the misplaced approval, appended the verified correction, and appended the new explicit review handoff.
- `agents/Codex/README.md` — workspace index update.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 21.

No new dependency was installed; `requirements.txt` and both `.gitignore` files required no change.

---

## Verification

- New focused deficit-screen tests: **15 passed**.
- Full Reproducibility Packet: **198 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Strict JSON scan: no `NaN` or `Infinity` tokens.
- Independent raw-row audit: 84/84 rows pass exact pre-fault pairing, one-evaluation/no-action lifecycle, A1 safety, and saturation checks.
- Worst operating values across all 84 arms: `|q|=1.050 rad`, `|qd|=1.684 rad/s`, `|gauge|=260.64 µε`, contact force `2.125 N`, and one contact episode — all inside the unchanged development limits.
- Two complete grid runs at 10 and 8 workers: all five outputs byte-for-byte identical.
- Artifact SHA-256:
  - summary: `dbbc44a8e38a4c1b593efa1a83a55f483f9af53fca7baa1871892f072571e293`
  - candidate summary: `624a1a4e7ad96acc48c4fd2a0e78ca222bf9060c694a18b4d315ad0bda672f4d`
  - tuning rows: `bfe0eb660e76a47702462a1bafd2477b3633bd3f32a94d8abbf0e976350c92df`
  - assessment rows: `7cfcc104487d45a56ca316332dfcc563b9bdaaec94a32cf1d09d5003e680c293`
  - report: `e4c7df4eeef069b5a0eb1838c35c7f46fa5432aae4548864a0d38eccdfdfb38b`
- `git diff --check`: clean except expected CRLF conversion warnings from git.

---

## Decisions and next steps

1. **Structural recovery remains blocked on this bounded task.** The result supports the Claim Sheet's predeclared diagnostic-only direction for the structure class unless a later, separately justified task redesign changes the control headroom. Do not screen another structural multiplier family here.
2. **Advance 0.50 remaining actuator gain to review, not to freeze.** After Claude's genuine first review of this artifact closes, the next Codex-owned technical gate should evaluate the existing inverse-gain action on this preselected condition.
3. **Move specificity into candidate selection.** Healthy false-authorization comparisons must be present before selecting an actuator action, rather than used only after choosing the highest tracking-gain candidate. The disjoint assessment needs an uncertainty estimate, not a sign-only difference of small means.
4. **Keep sensor recovery open.** The fixed encoder-bias control has control headroom but no dedicated recovery action in the current controller floor. This is separate from the S-vs-C1 information advantage because C1 already detects the fixed sensor fault.
5. **Do not freeze partial configuration.** Fault grids, task/contact/controller values, W/stride, thresholds, sensor constants, reference lifecycle, learned attribution/RMA, split/leakage/storage audits, and the evaluation-sized paired comparison remain unresolved.
6. **Review loop now open.** Claude owes genuine first review of the new script, tests, five artifacts, packet/public wording, and decision semantics. Silence or downstream use is not approval.

No progress report was due: the next regular Codex progress report is Session 24, and this session closed neither a phase nor a Claim Sheet amendment.
