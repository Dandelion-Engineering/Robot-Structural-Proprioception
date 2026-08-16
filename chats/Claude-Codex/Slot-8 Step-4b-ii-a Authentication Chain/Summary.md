# Summary — Slot-8 Step-4b-ii-a Authentication Chain

**Date Range:** 2026-08-15 (Claude Session 141) – 2026-08-16 (Claude Session 144)
**Participants:** Claude (owner), Codex (reviewer)
**Governing card:** `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`
**Terminal outcome:** **Approved with Follow-ups** — both agents approved the same exact bytes.
**Final transcript:** 56,232 B / 855 LF / 0 CR, sha256
`4a0ec1fb75fbefe1f149d627aa3274aea38f3703022a218560ff8ff8de589544`.

---

## What this chat was

The review of the **first half of Slot-8 sub-step 4b-ii**: read-order rows 4 through 12 of
the approved Step-4a connection-record design — the *authentication chain*, the part that
establishes that the file at a named place is the file the record named. Coherence, geometry
and output (rows 13–21) were deliberately left to a second half, **4b-ii-b**, which was not
started and which receives its own Review Card and its own chat.

Codex ruled on the split before reviewing any content and accepted it. That ruling is the
precedent worth carrying: when a design names one build step that is really a program, the
*review* is what splits, not the design — and the design's sub-step does not close until both
halves close.

## The approved state

| artifact | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `6ec198464a6b418c9e280addbbd16b5eb8c67d46` | `2f3cb4050a7c1d291ac3d75ce414ea2c2bf51d038cb6e23974f3e7054fadfe97` | 97,541 / 2,115 / 0 |
| `Reproducibility Packet/scripts/utils/authenticated_storage.py` | `f1d09ca0e4fe91f862b5736210ebb47e40d838ef` | `7da660b1b840ee813360d1e0a9c9757c0fe68c6b0368814877cf3582530c3f62` | 14,338 / 336 / 0 |
| `Reproducibility Packet/tests/test_connection_adapter.py` | `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9` | `1c6860ba13878ec6f693cb943b6e432a55fab22d741ab9602552b2eaf249ff07` | 118,956 / 2,959 / 0 |
| `Reproducibility Packet/tests/test_authenticated_storage.py` | `28323ff7e0fbfb78e204b1c647efaad9efa1670e` | `f89bb783af5891041723ce958a9c70179d60ee96821f2aa5d0a62ed39fd95d97` | 23,163 / 547 / 0 |

**Superseded — never review or build from:** `dafa73b5` / `9cadb11d` (Round 1),
`01653d9c` / `c5d4e023` (Round 2), `c24cb0cf` / `00b25820` / `07c48cc8` / `213367e8`
(the Round-3 owner handoff).

## The three rounds, in one paragraph each

**Round 1 (Claude S141 build → Codex S142 review).** Codex recorded six findings in one
numbered ledger. All six were accepted without contest and integrated: the record's own
location was unbound and missing from W3's expected set; `frozen=True` is shallow, so an
authenticated record could be edited into a different allowlist without touching a hashed
byte; the finite-number gate was not total; the path rule refused traversal but not
non-portable spellings; `case_id` reached the shared renderer as a filename; and the composed
output namespace was neither length-bounded nor one-to-one.

**Round 2 (Claude S142 response → Codex S142 review).** Five findings closed. **Finding 1
stayed open**, and Codex demonstrated why: `RolePayloadLoader.load` hashes a path and then
*reopens* it, so a payload replaced between the two opens is accepted and its values
returned. The authenticated bytes were not the interpreted bytes.

**Round 3 (Claude S143 response → Codex S143 review → Claude S144 re-review).** The repair
had to reach two files inside a recorded code identity. Claude built Codex's accepted scope
expansion into `storage_contract.py` and `role_contract.py`, **measured that it takes the
packet-wide suite to 52 failed / 25 errors and makes two read-only analyzers refuse three
completed, unrepeatable runs**, and reverted it whole. The repair instead lives in a **new**
module, `scripts/utils/authenticated_storage.py`, which no recorded identity contains. Codex
then made two mechanical reviewer corrections and approved; Claude re-reviewed the same bytes
and approved, closing the card.

## The load-bearing facts a later session must not undo

- **`storage_contract.py` and `role_contract.py` are two of the eight files in
  `dev_fit_trainer.training_code_identity`.** Editing either breaks three completed lanes.
  This is decision D4's rule reaching two more of the same eight files. **Do not edit either.**
  A later round that needs them changed is an amendment against three approved artifacts and
  needs its own card.
- **`utils.authenticated_storage` is the bytes-domain door.** It reuses every rule from its
  owner — `audit_identity_manifest`, `_validate_role_index_rows`, `validate_role_payload`,
  `_expected_root` and `RolePayloadLoader` itself as the base class — and restates only the
  reading mechanics, held shut by equality tests against the closed path-based functions.
  **Do not "de-duplicate" it back into the closed files.**
  `test_the_closed_utilities_keep_the_identity_three_approved_artifacts_record` exists so a
  later session finds this out here rather than downstream.
- **`authenticated_bytes` is the only way a file enters the module:** one open, digest over
  the bytes that read returned, compare, return those bytes. `require_still_authentic` — the
  bracket idiom — is deleted.
- **Codex's two Round-3 corrections stand.** `authenticate_config` compares the config's
  declared raw `schema_sha256` against the raw digest of the schema bytes the adapter
  authenticated, *before* calling `validate_config_document`; and `npz_archive_from_bytes`
  refuses a valid `.npy` stream as a `StorageContractError` rather than leaking a `TypeError`.
- **Checkpoints stay path-digested and that is deliberate.** Nothing in this lane interprets
  a checkpoint, so there is no second reading for a first to have to match.
- **`schema.json` is read exactly twice and the count is pinned at two, not excused.**
  `config_contract.validate_config_document` takes the schema as a document but re-derives its
  raw digest from `schema_path`. Closing that needs a `schema_sha256` parameter on a fourth
  closed contract, outside this card's scope. Codex's guard narrows what the second read can
  do; it does not remove it.

## The tracked follow-up, carried into the 4b-ii-b card

**The adapter's raw-domain schema comparison silently depends on the
`schema/schema.json text eol=lf` pin.** Both `.gitattributes` files already call that pin
load-bearing for `config_contract`'s raw comparison; the new guard makes it load-bearing for a
second consumer, and nothing in the candidate says so. Measured with `git checkout-index`:
`schema.json` materialises on a fresh Windows checkout at 15,212 B / 670 LF / 0 CR, raw digest
identical to the tracked blob, so raw and canonical are the same number and the dependency is
invisible from inside the packet. The follow-up is one sentence of documentation in 4b-ii-b,
not a repair.

## Evidence at closure

Focused suite **185 passed**; focused suite under `PYTHONOPTIMIZE=1` **185 passed**;
packet-wide suite **2,793 passed** (Codex 154.90 s, Claude 151.61 s); `py_compile`,
`git diff --check` and `git status --porcelain` all clean; fresh-interpreter import leaves
`torch` and `mujoco` absent.

Two independent two-pass mutation controls were run, both entirely outside the repository:
Claude's 28-mutant sweep on the Round-3 build (25/25 real caught) and Claude's 8-real +
3-control sweep on Codex's reviewer delta (6/8 caught, the two survivors proved **equivalent
mutants** under the `schema.json` EOL pin by direct measurement of all three digest values).

## Scientific resource

**Zero across all four sessions.** Counters unchanged throughout: **278 rollouts, 67 fits,
67 checkpoints, zero pilot/validation/test reads.** No production connection record, real role
index, real role payload, checkpoint, estimator output, controller log, production config or
pilot/validation/test result was opened; no MuJoCo model built, no rollout stepped, no fit run,
no figure rendered.

## What this closure authorizes, and what it does not

It authorizes **Step 4b-ii-b** to begin, under a new Review Card and a new subject chat.
It authorizes **nothing else**. `build_role_bundle` still refuses unconditionally with
`X_CONNECTION_UNAUTHORIZED`, and that remains correct until the whole of sub-step 4b closes —
4b-ii-a changed no public surface. Steps 4c, 4d, 4e and 4f, and every scientific gate behind
them, remain shut. A closed review loop authorizes the next step only, and never a run.

## One process note

Codex's Round-3 chat append mis-anchored on a repeated `— Claude` / `---` delimiter and landed
before the physical EOF. Codex's own in-turn prefix check caught it, it left the misplaced
entry in place and appended a dated correction at the physical tail, and Claude confirmed the
whole account independently against primary Git objects: the delta is `106 0` — **purely
additive** — and deleting exactly the two inserted line ranges reproduces the predecessor byte
for byte. Recorded in `chats/Claude-Codex-Human/Transcript Order Monitoring/`.
