# Codex — Human Report, Session 117

**Date and time:** 2026-08-11 05:37 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. The next regular Codex progress report is Session 120 unless a
phase transition or approved Claim-Sheet amendment fires one sooner.

---

## Summary

This session reviewed Claude's Session-117 public-log edit and execution-authorization half,
performed an independent zero-fit preflight, supplied Codex's matching half on the exact approved
plan, executed the one authorized rung-2 run, and exact-state-audited the raw terminal artifacts.

The invocation completed successfully at terminal `X_RUNG2_OK` after 1,274.6 wall-clock seconds:
both rung-1 equivalence fits reproduced their approved checkpoints and loss histories exactly,
all ten rung-2 development arms completed, ten approved anchors were read, and zero rollout,
generation or non-development-read resources were spent.

The two Step-5 authorization halves are spent. There is no retry authority. The next allowed
technical act is Claude's Step-6 build of the new read-only rung-2 analyzer and focused tests on
synthetic/in-memory fixtures. Production analyzer invocation, the exact derived-state review,
section 5.4 interpretation, later-role reads, capacity/threshold selection and final configuration
remain separate and unauthorized.

## Public README review

Claude replaced one imprecise sentence in Codex's plan heartbeat. The old sentence said
independent review “reproduced all 107” checks, which mislabeled Codex's independently constructed
instrument as a replay and made one audit's count sound exhaustive. Claude's replacement correctly
states that the author and reviewer wrote separate 132-check and 107-check audits, that neither
borrowed code from the plan producer, that the program's authorization gate was driven directly,
and that Claude calibrated its instrument with 23 deliberate plan mutations.

I genuinely re-reviewed and explicitly approved that exact wording at Git blob
`485d83ce4c76a708899485fa8eb830c6892f156d` / cleaned SHA-256
`efee887595f830c27810d4935ba6555990649c580012611761ebb06b45004586`.

During closeout I then caught a separate stale banner field: the running log already carried
2026-08-11 entries while `Last updated` still said 2026-08-10. Per the Live-Run README playbook I
changed only that banner date to 2026-08-11 and explicitly approved the new exact state:

```text
README.md
  Git blob          abeac76cad401de682942424c9a9398237d5bdf5
  cleaned SHA-256   488c2531bfd81028c5513d3e6c281ba93808fcb1020aaa385b7196af33a14731
  cleaned form      145,938 B / 208 LF / 0 CR
  delta vs 485d83ce +1 / -1, banner date only
  Codex approval    explicit
  Claude review     open
```

No new running-log entry was added. Raw execution completion is real, but the approved analyzer
and joint derived read do not yet exist; the public log should not turn an unreviewed terminal
into a result sentence.

## Independent pre-authorization work

Before issuing Codex's half I ran the focused executable suite in both interpreter modes:

```text
normal mode        142 passed in 3.75 s
python -O          142 passed in 4.05 s
```

I then drove a separate **36-check zero-fit preflight** against the exact command and current
repository state. It established:

- the command resolved to the explicitly named packet base, plan and data root;
- `require_permitted_base` and `require_authorized_plan` accepted the exact
  `b51b0009...1040` plan;
- the live design, producer identities, protocol and budget still matched that plan;
- the fresh `rung2-run-1/` root was absent and its parent contained only `plans/`;
- ten rung-2 arms, two equivalence arms, ten anchors, 219,018 parameters and `MAX_FITS = 12`
  remained exact;
- the approved ledger and analysis identities still matched;
- all ten distinct approved checkpoint files existed at their planned digests and both
  equivalence targets resolved to their exact anchor;
- the approved loader returned only the 152 C1 plus 152 S development examples, with current
  assignment and manifest identities equal to the plan; and
- Python 3.12.10, NumPy 2.5.1 and PyTorch 2.11.0+cu128 matched Claude's half.

The probe called no fitting function, wrote no packet file and left the run root absent. I also
accepted Claude's zero-fit static closure of the fitting-loop equivalence's second link: the
normalized loop bodies, evaluated objects and constructor outputs were identical. The first link
remained Codex's Session-100 real-data measurement under unchanged producer/data/checkpoint
identities, with the production R6 gate still positioned to fail after the two small re-fits and
before any rung-2 fit if it did not reproduce.

## Exact execution

After the two explicit halves existed at the physical transcript tail, I invoked exactly once
from `Reproducibility Packet/scripts/`:

```text
..\..\venv\Scripts\python.exe -B -m utils.rung2_escalation ^
  --mode execute ^
  --base-dir ..\results\rung2_escalation ^
  --approved-plan ..\results\rung2_escalation\plans\rung2-run-1\rung2_escalation_plan.json ^
  --approved-plan-sha256 b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040 ^
  --data-root ..\..\data\gate3-base-dev-pilot-val-c1-s
```

The process exited `0` and printed ten completed rung-2 arms followed by:

```text
X_RUNG2_OK: 10 rung-2 arms fitted, 2 equivalence checks passed,
            10 approved anchors read, 0 rollouts spent
```

There was no second invocation, retry, alternative base, analyzer, C7 invocation, rollout,
generation run or reserved-role read.

## Raw terminal artifacts

The new namespace contains exactly two JSON artifacts and twelve Git-ignored checkpoints:

```text
Reproducibility Packet/results/rung2_escalation/rung2-run-1/
  rung2_escalation_result.json
    Git blob             0eb78d0f55a76b2467d6292a571216ad3eb395d7
    raw SHA-256          9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
    bytes / EOL          33,038 B / 0 LF / 0 CR / canonical JSON

  _equivalence/rung2_escalation_equivalence.json
    Git blob             351f47f4ea3da22be494cb917b90773d2cf2f36b
    raw SHA-256          ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
    bytes / EOL          6,261 B / 0 LF / 0 CR / canonical JSON

  checkpoints           2 equivalence + 10 rung 2 / all ignored by `*.pt`
  total namespace       exactly 14 files
```

## Independent result audit

I wrote and ran a separate read-only audit over the two JSON documents and twelve checkpoints.
It passed **261/261 checks**. The audit established:

- exact terminal, run-label, plan, design, producer, protocol, authority and budget identities;
- exact `12/12` total, `2/2` equivalence and `10/10` rung-2 fit/checkpoint counters;
- zero rollout, generation and non-development-read counters in both artifacts;
- exact ten approved read-only anchor records and current ledger/analysis identities;
- the exact 304-of-944 development-only census and its assignment/manifest identities;
- identical equivalence records across the run and equivalence artifacts;
- `PASS`, bit-identical weights and bit-identical 20-epoch histories for both equivalence arms;
- both refit checkpoint files matching their exact approved anchor digests;
- the exact ten planned `(suite, seed)` rung-2 records, each at 219,018 parameters, receptive
  field 31, 152 examples and 20 finite epoch values;
- all ten rung-2 checkpoint digests, distinctness, state-key sets, tensor shapes, dtypes,
  serialized parameter counts and finite tensor values;
- exact canonical one-line JSON serialization and key sets, with no absolute filesystem path;
  and
- acceptance by the production completion validator.

All ten raw `objective_reduced` fields are `true` and each is internally consistent with its own
finite first/final 20-epoch history. This is only a primitive integrity statement. I did **not**
derive `OPTIMIZATION_CHECK_PASSED`, compute paired signs or rung differences, run an analyzer,
apply section 5.4, make a learning/classification claim, select capacity or choose a threshold.

## Append-order recurrence and repair

My first 05:08 transcript patch failed the standing hard gate. I had verified a longer unique
EOF anchor but applied a patch whose actual context was only the repeated `— Claude` signature
and separator. The 100-line turn landed at line 19,811, not the physical tail.

The immediate assertions caught the wrong prefix, pre-boundary header and still-last Claude
header before any project run began. I preserved the misplaced copy, then appended a 52-line
dated correction from a newly verified complete EOF block. That correction retained the entire
2,010,849-byte intermediate state exactly under SHA-256
`5667e933f62119e67e599c1b990d7889667ae5dd819a6404900aac55ea28fa09`, restated every
decision-bearing part of the authorization, and became the physically last header before the
run.

I also reported the recurrence in the director-visible monitoring thread. Its 30,362-byte prior
state was retained exactly under SHA-256
`0535df0e515d1d651b033b8059046114a07e161ee9899e24fda67ab526d498a0`; the new
Session-117 monitoring header is unique after that boundary and physically last. The monitoring
diff is additions-only at `+33/-0`.

After the repair, the result handoff and README banner correction each used the complete
pre-verified EOF block and passed exact byte-prefix, unique-header, post-boundary, physical-tail
and additions-only checks. The final technical transcript state before closeout is:

```text
bytes / LF / CR     2,020,093 / 32,776 / 19,456
SHA-256             615b9df58ab868cc3425c057d096db9ca68d497122c1931ff3a946f940e4a1b9
working-tree delta  +277 / -0, two disclosed hunks
last agent header   Codex Session-117 README banner correction
```

## General recent-work correction

`git diff --check HEAD^ HEAD` exposed one trailing-space line in Claude's rewritten continuity
file. I removed only that trailing space. It did not affect any technical state or gate.

## Files created or updated

- `Reproducibility Packet/results/rung2_escalation/rung2-run-1/rung2_escalation_result.json`
  — new tracked raw run-level terminal artifact.
- `Reproducibility Packet/results/rung2_escalation/rung2-run-1/_equivalence/rung2_escalation_equivalence.json`
  — new tracked exact equivalence record.
- Twelve `.pt` files under the same run root — created by the authorized invocation and ignored
  by the packet/root `*.pt` rules.
- `README.md` — accepted Claude's plan-entry edit and corrected the stale last-updated banner;
  current blob `abeac76c...`, Claude review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — preserved the misplaced authorization, appended the dated correction, recorded the exact
  result audit and handed over the banner correction.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — recorded the caught append-order recurrence and verified repair.
- `agents/Claude/Summary of Only Necessary Context.md` — removed one trailing space found by the
  general recent-work diff check.
- `agents/Codex/Session Summaries/HumanReport117.md` — this report.
- `agents/Codex/README.md` — updated the workspace index and active gate state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 118.

The frozen design, architecture module/tests, executable/tests, plan and approved earlier
development records were not modified.

## Resource accounting

```text
fits attempted / completed     12 / 12
checkpoints written            12
rollouts                        0
generation runs                0
non-development reads          0
production analyzer calls      0
C7 invocations                 0
```

The real development split was read during preflight and execution. Pilot, validation and test
outcomes remain unread for capacity, threshold, final-configuration and confirmatory decisions.

## Current gate and next steps

1. Step 5 is **spent / one invocation complete** at terminal `X_RUNG2_OK`.
2. The raw result/equivalence state passed Codex's 261-check integrity audit; Claude has not yet
   reviewed a derived artifact because none exists.
3. Step 6 is open only for Claude to build `scripts/analyze_rung2_escalation.py` and its focused
   tests. Production invocation on the real result remains unauthorized until that code/test
   state completes explicit same-state review.
4. Step 7 exact derived-state review and joint section-5.4 application remain blocked.
5. Claude should review current README blob `abeac76c...`; a further edit returns a new state.
6. No retry, capacity/threshold choice, later-role read, generation, rollout or final
   configuration is authorized.
