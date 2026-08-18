# Human Report — Claude Session 152

**Current date and time:** 2026-08-17 18:40 PDT (taken from the shell immediately before creating this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session discharged **both** of Codex's Session-151 cross-review findings, neither
contested, both re-driven at source by me before either was accepted — and one of them came
out **wider than reported**. It then built the **three-case coherent menu** the Session-151
boundary called for, which made read-order **row 20's accept path and its two identity
refusals reachable for the first time**, and drove them.

It is also a **regular progress-report session** (my session 152 = 19 × 8), so
`agents/Claude/Progress Reports/Progress Report Session 152.md` was written, covering my
Sessions 145–152.

Slot-8 sub-step 4b-ii-b is now **built through row 20 with row 20 complete**. Row 21 is the
one remaining read-order row and is **unblocked for the first time**. Nothing of 4b-ii-b is
reviewed, and there is still **no Review Card and no subject chat for it** — deliberately, for
the eighth consecutive session, because a card names a candidate and the candidate is not
stable yet.

**Zero scientific resource was spent.** No MuJoCo model was built, no rollout stepped, no fit
run, no figure rendered, and no role index, role payload, checkpoint, estimator output,
controller log, production config or pilot/val/test result was opened.

## Startup and context ingestion

- `.agent-turn` named Claude, `.agent-session.lock` was absent, so I created the lock and
  re-read `.agent-turn`, which still named Claude.
- Read `AgentPrompt.md` and all of `Project Details/Project Details.md`.
- Read my `Summary of Only Necessary Context.md` in full, and build-plan Appendix E.
- Reviewed the chat inventory. The only active chat is
  `chats/Claude-Codex-Human/Transcript Order Monitoring`; its physical tail is my own Session-144
  entry and no fault has been reported since, so **no reply was owed and none was posted** — a
  clean check is not a posting reason.
- **Cross-review:** read Codex's `HumanReport151.md` in full, which is where both findings were
  raised, plus the code regions they name.
- Authenticated the starting state at commit `30773d7` (`Codex Session 151`), working tree clean.

## Codex's finding 1 — the row-19 test seam, re-driven at source and found wider

Codex reported that the Session-151 `_reprovenanced` helper still returns a state the earlier
read order would not have produced. I built a scratch probe outside the repository, materialised
the harness, authenticated it, applied the **exact Session-151 helper**, and measured every
relation the earlier rows establish.

```text
                                        unedited      after the S151 helper
the eleven declared joins               hold          hold
recomputed census == carried census     holds         BROKEN  {'val': 4} vs {'dev': 2,'val': 2}
each audit manifest_audit == census     holds         BROKEN  (x2)
record 20-field manifest_row echoes     2/2           0/2
role-index config_hash == config        8/8           0/8
config_hash == its document's digest    holds         BROKEN
row 4 authority/config POLICY           accepts       REFUSES -- "a FINAL record names a
                                                      'draft' configuration"
```

Every relation Codex named reproduces. **The last row is mine rather than Codex's**: the
Session-151 state does not merely lack identity copies, it is a state one of row 4's *policies*
refuses outright.

### The repair

- `_provenance_joins` now states **eighteen** joins rather than eleven, adding the census, the
  two audit census blocks, the record's manifest echoes (both the 20-field comparison and the
  split), the role-index config hashes, and the config document's own canonical derivation.
- The post-condition is renamed `_require_post_row12_state` because it now checks three
  separable things, and the old name described only the first: the identity joins, row 4's
  authority/config policy (by **calling** `require_authority_config_policy`), and row 3's
  authority/split policy (by **calling** `connection_record._require_authority_split_policy`,
  the function that owns the rule).
- **`_reprovenanced` no longer takes a `config_hash`.** It takes `config_status`, edits the
  config *document*'s `status`, and re-derives the identity with `expected_config_hash`. An
  identity a caller hands in is an identity no document produced — which is finding 2's defect,
  in the test seam.
- One row-19 test still needs the single state row 3 forbids (`FINAL` over the `dev` split),
  because that is the only way to reach row 19's split input. It declares
  `split_policy_violated=True`, and the post-condition **inverts** the check rather than
  skipping it: setting the flag on a state row 3 would accept **fails**.
- The post-condition **names what it does not claim**: it does not require the config document
  to be one `validate_config_document` would accept as frozen. That document is a complete
  frozen `config.json`, and invariant W7's whole content is that this packet does not contain
  one and is not to manufacture one.

### Two negative controls now, not one

The Session-150 partial edit remains the first control and breaks **11 of 18** joins. The
**Session-151 partial edit is the second, added this session**, and breaks **7 of 18**. Both are
additionally required to fail row 4's policy. This is lesson 272: a new post-condition whose
only witness is the *previous* generation's defect has never been shown to see the current one.

## Codex's finding 2 — row 20 accepted a caller-supplied provenance state

Driven at source on the coherent fixture, whose authenticated authority is `DEVELOPMENT_ONLY`
and whose `resolve_provenance` returns `DEVELOPMENT_ONLY`:

```text
forged FINAL              -> validate_scene ACCEPTED
forged SYNTHETIC_FIXTURE  -> validate_scene ACCEPTED
```

`validate_scene` **accepting** the forgery is what makes this blocking rather than cosmetic:
nothing after the assembly can see the disagreement, because by then the label is the only
statement of the fact. The one-case harness did refuse both — on the unrelated incomplete-menu
rule, which would have disappeared the moment the three-case menu landed.

**The repair:** `resolve_bundle` now requires `provenance.state == connection.record.authority`
**before the first scene is built**, refusing with `X_PROVENANCE_UNRESOLVED`. It is not a second
copy of row 19's rule — row 19 requires its own *computed result* to equal the authority; this
row requires the value it was *handed* to be that authority, and the two separate exactly when a
caller substitutes. `SYNTHETIC_FIXTURE` is refused as a consequence rather than as a special
case: `utils.connection_record` admits only the two public authorities, so no authenticated
record can make the equality hold (invariant V7).

After the repair, both forged states refuse with `X_PROVENANCE_UNRESOLVED` and an observer test
proves **no scene is built at all** on the forged path.

## The three-case coherent menu

`_three_case_menu` installs three additional `dev` pairs over the harness tree —
`menu-structure`, `menu-actuator`, `menu-sensor` — each carrying the **same coherent plant
record** row 18 needs, its own `labels` payload naming one required source class, and an
`estimator_outputs` payload whose `p_class` names that same class. It rewrites `manifest.csv`,
recomputes the census, rewrites both audits, appends to six role indexes, rewrites the
established-result artifact, declares the three cases in the record, and **restores every byte
on exit**.

Three things worth carrying:

1. **`observations` is not written at all.** `ROLE_NAMES` is `controller_logs`,
   `estimator_outputs`, `labels`, `plant` — no connection record names an observation payload.
   Reading that one line removed most of the estimated build (lesson 275).
2. **`controller_logs` is copied byte for byte** from the pair the contract fixture already
   wrote; nothing in it is per-case and rows 15–17 already accept it.
3. **The restoration is a tested property.** The installer touches ~20 files in a
   *session-scoped* tree, and a leak would not fail where it happens — it would quietly change
   what every later test measures. Both trees are digested path by path before and after and
   required to be equal, with the connection record excluded by name and its own restoration
   asserted separately (lesson 277).

**It is a fixture, not a rule change.** A menu that cannot show a reader a structure, an
actuator and a sensor change side by side cannot support the comparison the artifact exists for.

## What row 20 now has that it did not

- the **accept path** — one scene per declared case, in the record's order, every scene carrying
  the row-19 state and the record digest rows 1 and 2 authenticated, whole bundle passing
  `validate_bundle`;
- the **run-id and pair-id identity refusals**, driven by patching `_arm_identity`;
- the **ordered** established-result comparison, which one case could not separate from an
  unordered one and three cases can;
- both **forged-provenance refusals**, plus the no-scene-built observer.

## Verification

Run only with the project interpreter, from the repository root:

```text
.\venv\Scripts\python.exe -m pytest "Reproducibility Packet/tests/test_connection_adapter.py"
  "Reproducibility Packet/tests/test_authenticated_storage.py" -q
  -> 277 passed in 8.62 s          (was 265)

.\venv\Scripts\python.exe -O -m pytest <the same two files> -q
  -> 277 passed, 1 expected PytestConfigWarning, in 9.01 s

.\venv\Scripts\python.exe -m pytest "Reproducibility Packet/tests" -q
  -> 2,935 passed, 0 failed, in 178.15 s
```

`test_connection_adapter.py` alone collects **257** (was 245). The arithmetic closes:
2,923 + 12 = 2,935. `py_compile` and `git diff --check` are clean; `git status --porcelain`
named exactly the two packet files plus my own workspace documents.

`git diff --numstat`: `49 13` on `connection_adapter.py`, `1066 92` on
`test_connection_adapter.py`. Both files measured on their **final bytes**: pure ASCII, LF,
0 CR, no BOM, final newline.

**Candidate identities at the end of this session:**

- `Reproducibility Packet/scripts/utils/connection_adapter.py`
  - blob `a1236ed937e5deeca8b6aa86cd43f16269ef6139`
  - raw `007b870ee57143a9d1af9a890b54240cd3387ad5053ad5c08445b18630eeeac0`
  - 157,693 B / 3,347 LF / 0 CR
- `Reproducibility Packet/tests/test_connection_adapter.py`
  - blob `6f6a2b135080764e5eb40bcc89159ca3e8eaadb7`
  - raw `db00779e818fe0e6fc08cbbcb50ec237f237da7b40d3fc9fb79796d500dd6fcd`
  - 247,241 B / 5,969 LF / 0 CR

The Session-151 states `474b02c6` / `bf9e2738` are **superseded**; do not review or build from
them.

**No mutation sweep ran, and that is on plan.** The build plan sequences the two-pass sweep on
the *finished* pair, and the pair is not finished. Its staged-tree set (`scripts`, `tests`,
`schema`, `config` and `results`) is unchanged.

## Scientific and authorization boundary

- Counters unchanged: **278 rollouts, 67 fits, 67 checkpoints, zero pilot/validation/test
  reads.** The checkpoint count was not re-read — no fit ran.
- No MuJoCo model built, no rollout stepped, no fit run, no figure rendered.
- Disclosed reads, all tracked development text, none opening a payload:
  `connection_adapter.py`, `connection_record.py`, `role_contract.py`, `storage_contract.py`,
  `config_contract.py`, `verification_scene.py`, `build_data_contract_fixture.py`, and
  `schema/schema.json`'s `labels` role declaration.
- Every tree the tests bind is under `tmp_path`; the probe ran in a temporary directory outside
  the repository and was deleted.
- The two off-limits identity files (`storage_contract.py`, `role_contract.py`) were **read and
  not edited**.
- Slot-8 Steps 1–3, 4a, 4b-i and 4b-ii-a remain closed at both approvals at their recorded
  bytes. Steps 4c–4f, production connection records, real-role reads, the capacity and threshold
  choices, the final configuration and every C1-versus-S statement remain blocked.

## Live-Run README heartbeat

Checked; the answer is **no** and the file is unchanged at the jointly approved blob
`7342bc8c`. No artifact finished, no phase closed, and no scientific result was produced — a
partial internal build inside an unreviewed sub-step is none of the three triggers.

## Files created or updated

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — row 20's provenance bind and its
  documentation (`49 13`).
- `Reproducibility Packet/tests/test_connection_adapter.py` — the repaired seam, the eighteen
  joins, the renamed post-condition, the second negative control, the three-case menu installer
  and eleven new tests (`1066 92`).
- `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` — **Appendix F**, appended (`170 0`).
- `agents/Claude/Permanent Instruments.md` — lessons **272–277**, appended (`59 0`).
- `agents/Claude/Progress Reports/Progress Report Session 152.md` — new, the regular S145–S152
  report.
- `agents/Claude/Session Summaries/HumanReport152.md` — this report.
- `agents/Claude/README.md` — indexed Session 152.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 153.

No chat transcript, Review Card, protocol document, schema, configuration, result artifact,
Claim Sheet or public README byte was changed.

## Next steps

1. **Row 21** — writing the finished bundle. Unblocked for the first time; its accept path needs
   a bundle the surface gate accepts and there is now one.
2. The audit-hook observer (W3/B4), then B2, B5 and the remaining B3 rows.
3. The `roles` CLI wiring and the additive `build_role_bundle` docstring change.
4. The two-pass mutation sweep on the finished pair — budgeted before the handoff, not after.
5. Then, and only then, the Review Card and the subject chat, carrying **three disclosures**:
   the `schema.json` EOL-pin dependency, `authenticate_sources`' third parameter, and
   `AuthenticatedConnection.record_sha256`. Session 152 added no fourth.
