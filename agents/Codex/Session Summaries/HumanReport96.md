# Codex - Human Report, Session 96

**Date and time:** 2026-08-08 10:14 PDT

**Phase:** Phase 2 - Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Data generated: 0. Pilot /
validation / test reads: 0.** One corrected official plan artifact was regenerated in plan
mode. Plan mode wrote no run root and performed no fit.

**Progress-report session:** **yes** - this is Codex Session 96, so I also created
`agents/Codex/Progress Reports/Progress Report Session 96.md`, covering my Sessions 89-96.
No phase transition or Claim Sheet amendment occurred.

---

## Summary in one paragraph

Claude Session 96 explicitly approved the unchanged Route-A production executable and returned
a test-only state that pins the analyzer identity's portable text-hash domain and its malformed-
record refusal reason. I genuinely reviewed those additions, drove the production seam they
protect, ran all 214 focused tests normally and under `python -O`, and explicitly approved the
returned test blob unchanged. That closed the Route-A executable/test review on exact bytes
approved by both agents. I then ran the one permitted zero-fit `stage1-run-1` plan command,
independently reconstructed and authenticated the resulting document, and explicitly approved
the corrected plan at Git blob `c048b54b...` / SHA-256 `bdf674d5...`. Claude's independent
plan review is now open. The full packet suite passes 1,765 tests. No fit, checkpoint,
generation, rollout, later-role outcome read, threshold choice, config freeze or confirmatory
action occurred or is authorized.

## Startup and current-state reconciliation

I first checked `.agent-session.lock`; it was absent, so I created it before reading project
files. `CODEX_HOME` was unset in the shell, so I used the known Codex home path to read the
automation memory. I then followed `AgentPrompt.md`: read the complete Project Details,
Codex continuity, Codex-including chat summaries and active-chat state, and Claude's most recent
human report.

That reconciliation mattered because the automation memory ended at Codex Session 90, while
the repository had advanced through Codex Session 95 and Claude Session 96. The physical
Phase-2 tail and current continuity were consistent: Claude had approved production blob
`61d4fb97...` unchanged and returned only `test_capacity_sweep.py` blob `8e97f6a9...`.

The worktree was clean at startup and `HEAD == origin/main` at Claude Session-96 commit
`2e68e7c`.

## Review of Claude's returned tests

Claude added two test functions, one parametrized across six malformed inputs, for seven new
test cases total:

1. **CRLF checkout portability.** The test materializes `analyze_dev_fit.py` with Windows CRLF
   line endings, confirms the raw bytes differ, and requires the analyzer guard to accept the
   same canonical text identity. This pins the intended use of `code_identity()` rather than a
   raw file digest.
2. **Malformed recorded identity reasons.** Six inputs (`None`, empty text, non-digest text,
   an integer, upper-case correct hex and a short digest) must fail specifically because the
   approved analysis artifact carries no valid analyzer identity. A value comparison alone
   would reject them for the wrong reason and leave the shape guard deletable in silence.

I checked the additions against the actual guard, `dev_fit_contract.code_identity()`,
`protocol_p.canonical_text_sha256()`, the repository's `.gitattributes`, and the current Git
attribute state for `analyze_dev_fit.py`. The test file imports `hashlib`; the CRLF conversion
is active in the current LF tree; `text` and `eol` are genuinely unspecified for the analyzer;
and `core.autocrlf` is true. No production file changed in Claude's commit.

The exact returned state is:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw SHA-256    d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 8e97f6a94a3c5ac12e6ac85376913c9104424725
  canonical/raw SHA-256    61f700fb4b6c51df495cdfca1c0fa0b5aacb3d9021c0c04e3cee2a72746b99e0
  physical state           86,984 B / 2,121 lines / LF / no BOM / 214 tests
```

I explicitly approved both exact blobs in the active Phase-2 chat. Claude had already approved
them, so the Route-A executable/test loop is closed.

## Corrected zero-fit plan regeneration

Only after recording that approval did I run the corrected command once from
`Reproducibility Packet/scripts/`:

```text
..\..\venv\Scripts\python.exe -B -m utils.capacity_sweep --mode plan \
  --run-label stage1-run-1 --output-dir ..\results\capacity_sweep
```

The program reported:

```text
X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-1, 0 fits run
```

The resulting exact artifact is:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  physical state           13,786 B / one canonical-JSON line / no final newline
```

The semantic diff from the superseded plan has exactly one field change:
`code_identity.capacity_sweep.py` moved from the old executable digest to the jointly approved
`d91db2ef...` digest. The ten read-only anchors, forty new curve arms, two C9 compatibility
arms, bound inputs, namespaces, training protocol and budget are unchanged.

## Independent plan audit

I did not approve the producer's output from its console message alone. I:

- rebuilt `plan_document(run_label="stage1-run-1")` in memory and required exact equality with
  the stored JSON;
- passed the exact artifact and SHA-256 through `require_authorized_plan()`;
- reconstructed the complete 40-arm set as widths 16/24/40/48 x suites C1/S x seeds 0-4 and
  required uniqueness;
- reconstructed the ten 32-channel read-only anchors;
- verified the C9 identities are exactly C1 seed 0 and S seed 4;
- required the exact budget of 42 fits, 42 checkpoints, zero generation, zero non-dev reads and
  zero rollouts;
- checked every checkpoint destination is relative rather than a drive-qualified or absolute
  path;
- confirmed the capacity result directory contains only the plan;
- confirmed `results/capacity_sweep/stage1-run-1/` does not exist; and
- confirmed `config/config.json` remains absent.

I explicitly approved plan blob `c048b54b...` in a second Phase-2 chat turn and handed it to
Claude for independent exact-state review. Step 3 remains open until Claude approves or blocks
these bytes. Even joint plan approval cannot imply Step 4: execution remains blocked without a
separate joint authorization naming the approved plan digest.

## Verification

```text
focused Route-A suite                    214 passed in 4.28 s
focused suite under python -O            214 passed in 3.78 s
full packet suite                      1,765 passed in 136.93 s
plan reconstruction                       passed
exact-plan authorization gate              passed
arm/path/budget audit                       passed
compileall                                 clean
git diff --check                           clean

fits                                        0
checkpoint writes                           0
generation                                  0
rollouts                                    0
pilot / validation / test reads             0 / 0 / 0
capacity result/equivalence artifacts       0 / 0
capacity run root                           absent
config/config.json                          absent
lifetime Protocol-P rollouts               278 unchanged
```

The packet tests read the two approved development documents through fixtures. They did not
open a delivered observation payload or approved checkpoint and did not read any pilot,
validation or test outcome.

## Transcript hard gates

I used the stored append-only hard-gate procedure for both Phase-2 writes.

First append, explicit returned-test approval:

```text
pre-write bytes       1,654,286
pre-write lines       26,544
pre-write SHA-256     57e4c67e70d22b494d5aef5f4cdfd5bef043bbbfced18878b64d5b319a37b87d
post-write bytes      1,655,901
post-write lines      26,576
prefix retained       exact
header                unique at line 26,546, after boundary
```

Second append, corrected-plan approval and handoff:

```text
pre-write bytes       1,655,901
pre-write lines       26,576
pre-write SHA-256     4acf2f621ce0c94f7aa8e0ada814f7e2d0eb556c9db9256fa85e44ddd181f177
final bytes           1,658,183
final lines           26,622
final SHA-256         b10869d3368df9c1fd6369287a35a82e669abfd879a0b03cf9ecffb9d1cfb6d4
prefix retained       exact
header                unique at line 26,578, after boundary
Git diff              +78 / -0 across both appends
physically last       Codex
```

No Transcript Order Monitoring note was required.

## Director and public communication

Because Session 96 is an every-eighth-session cadence point, I created
`agents/Codex/Progress Reports/Progress Report Session 96.md`. It explains the design and
authorization repairs in non-specialist language, states that the corrected plan exists, and
keeps the no-result/no-fit boundary explicit. The Slot-8 verification artifact has no new state,
so the report does not manufacture an update for it.

I appended one lean public README milestone: the corrected plan exists at
`bdf674d5...1c0a5`, Codex has independently approved it, Claude's review is open, and no fit or
later action is authorized. The Phase-2 banner and 2026-08-08 last-updated date were already
current.

## Decisions and reasoning

1. **Approve the returned test state unchanged.** Both additions protect real contract
   properties, add no production path, and leave the plan identity untouched.
2. **Close the review in chat before re-planning.** The review-cycle rule makes approval a
   recorded exact-state act; plan mode followed only after that loop was closed.
3. **Run plan mode once, not repeatedly for convenience.** One deterministic official plan was
   the authorized action. Independent review used in-memory reconstruction rather than writing
   a second plan.
4. **Approve the plan but do not authorize it for execution.** Plan correctness and permission
   to spend 42 fits are deliberately separate gates.
5. **Add a public milestone.** The previous public entry ended with a superseded plan awaiting
   regeneration; the corrected official plan is a decision-relevant forward state.
6. **Leave `.gitignore` unchanged.** The active lock, virtual environments, Python caches and
   generated artifact classes are already covered. Only the intended tracked plan changed.

## Files created or updated

Created:

- `agents/Codex/Progress Reports/Progress Report Session 96.md` - regular director update.
- `agents/Codex/Session Summaries/HumanReport96.md` - this report.

Updated:

- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` - corrected zero-fit
  official plan.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` - append-only returned-test approval and plan approval/handoff.
- `README.md` - one lean corrected-plan milestone.
- `agents/Codex/README.md` - current navigation and Session-96 entries.
- `agents/Codex/Summary of Only Necessary Context.md` - completely rewritten resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py`.
- `Reproducibility Packet/tests/test_capacity_sweep.py`.
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`.
- `director_requests.md` - no new director-only blocker.
- root and packet `.gitignore` files - current rules cover all observed generated/local files.

## Next steps

1. Claude independently reviews plan blob `c048b54b...` and explicitly approves or blocks it.
2. If Claude approves unchanged, record Step-3 closure without inferring Step 4.
3. Any Step-4 execution authorization must be a separate joint act naming plan SHA-256
   `bdf674d5...1c0a5`.
4. Only after that authorization may the two compatibility fits and forty curve fits run.
5. The later C7 read-only analyzer remains unbuilt and unauthorized.
6. My next regular progress report is Session 104 unless a phase transition or approved
   Claim-Sheet amendment triggers one sooner.

-- Codex
